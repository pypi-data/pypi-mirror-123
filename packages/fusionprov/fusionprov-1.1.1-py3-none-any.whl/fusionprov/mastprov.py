import argparse
import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from collections.abc import Mapping
from itertools import zip_longest
from typing import Any, Dict

import pyuda
try:
    from mast.mast_client import ListType
except ModuleNotFoundError as error:
    logging.info(f"{error}. If not on the Freia cluster, provenance reports can be produced for uda signals only.")
    FREIA = False
else:
    FREIA = True
from prov.dot import prov_to_dot
from prov.model import ProvDocument

from fusionprov import utilities


class MastProvFactory:
    subclasses = {}

    @classmethod
    def register_subclass(cls, data_type):
        def decorator(subclass):
            cls.subclasses[data_type] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, data_type, params):

        if data_type not in cls.subclasses:
            raise ValueError(f"Input {data_type} is not a valid data type.")

        return cls.subclasses[data_type](params)


class MastProv(ABC):
    def __init__(self, params):
        self.prov_doc = ProvDocument()
        self.client = pyuda.Client()
        self.client.set_property("get_meta", True)
        self.data = params["data"]
        self.shot = params["shot"]
        self.run = params["run"]
        self.graph = params["graph"]
        self.log_file = None

    machine = "MAST"
    namespace_uri = "https://users.mastu.ukaea.uk"
    data_location = "$MAST_DATA"

    def get_input_files(self, log_file=None):
        """
        Finds the raw or analysed datafiles that were used to produce the
        analysed data.
        """
        if not log_file:
            log_file = self.log_file
        matches = re.findall(
            r"(?<=/)[r|x][a-z][a-z][0-9]*?\.nc|(?<=/)[r|x][a-z][a-z][0-9]*?\.[0-9][0-9]|(?<=/)a[a-z][a-z][0-9]*?\.[0-9][0-9]|(?<=/)a[a-z][a-z][0-9]*?\.nc",
            log_file,
        )
        datafiles = set(matches)
        input_files = []
        for datafile in datafiles:
            if datafile[0] in ["a", "e"]:
                log = self.get_log(file_code=datafile[:3])
                input_files.append({datafile: self.get_input_files(log_file=log)})
            else:
                input_files.append(datafile)
        return input_files

    def data_ro(self):
        return "MAST INBOX"

    def get_session_leader(self):
        """
        TODO: Provide link to session information so authorised users can find
        who the session leader was.
        """
        return "SESSION LEADER"

    def get_scheduler_trigger(self):
        """
        TODO: Find a way to show why a pass was performed for run numbers
        greater than 0.
        """
        if self.run == 0:
            return "Automatic post-shot analysis run"
        else:
            return "TBD"

    def get_analysis_code_author(self):
        """
        Provides the resonsible officer for the analysis code or contact
        details for MAST Ops team.
        """
        return "MAST INBOX"

    @abstractmethod
    def build_prov(self):
        pass

    @abstractmethod
    def validate():
        pass

    def write_signal_prov(
        self,
        signal,
        signal_data_entity,
        scheduler_run_activity,
        record_shot_activity,
        scheduler_pass_trigger_agent,
        signals_done=None,
    ):
        if signals_done is None:
            signals_done = []

        if signal not in signals_done:
            if type(signal) is str:
                input_data_entity = self.prov_doc.entity(f"{MastProv.machine}:{signal}")
                self.prov_doc.wasDerivedFrom(signal_data_entity, input_data_entity)
                signal_ro_agent = self.prov_doc.agent(
                    f"{MastProv.machine}:{self.data_ro()}"
                )
                self.prov_doc.used(scheduler_run_activity, input_data_entity)
                if signal[0] in ["x", "r"]:
                    self.prov_doc.wasGeneratedBy(
                        input_data_entity, record_shot_activity
                    )
                self.prov_doc.wasAttributedTo(input_data_entity, signal_ro_agent)

            elif type(signal) is dict:
                for k, v in signal.items():
                    file_code = k[:3]
                    scheduler_run = self.get_scheduler_run(
                        file_code=file_code, log_file=self.get_log(file_code=file_code)
                    )
                    scheduler_run_activity = self.prov_doc.activity(
                        f"{MastProv.machine}:{scheduler_run[0]}",
                        startTime=scheduler_run[1],
                        endTime=scheduler_run[2],
                    )
                    self.prov_doc.wasAssociatedWith(
                        scheduler_run_activity, scheduler_pass_trigger_agent
                    )
                    analysis_code = self.get_analysis_code(file_code=file_code)
                    analysis_code_entity = self.prov_doc.entity(
                        f"{MastProv.machine}:{analysis_code}"
                    )
                    analysis_code_author = self.get_analysis_code_author()
                    analysis_code_author_agent = self.prov_doc.agent(
                        f"{MastProv.machine}:{analysis_code_author}"
                    )
                    self.prov_doc.used(scheduler_run_activity, analysis_code_entity)
                    self.prov_doc.wasAttributedTo(
                        analysis_code_entity, analysis_code_author_agent
                    )
                    self.write_signal_prov(
                        k,
                        signal_data_entity,
                        scheduler_run_activity,
                        record_shot_activity,
                        scheduler_pass_trigger_agent,
                        signals_done=signals_done,
                    )
                    signal_data_entity = self.prov_doc.entity(f"{MastProv.machine}:{k}")
                    for signal in v:
                        self.write_signal_prov(
                            signal,
                            signal_data_entity,
                            scheduler_run_activity,
                            record_shot_activity,
                            scheduler_pass_trigger_agent,
                            signals_done=signals_done,
                        )
            signals_done.append(signal)

    def write_prov(self):
        self.build_prov()

        directories = ("prov-xml", "prov-json", "prov-graph")
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

        file_name = f"{self.data}_{self.shot}_{self.run}_prov"

        json_file = utilities.slugify(file_name) + ".json"
        xml_file = utilities.slugify(file_name) + ".xml"
        json_path = os.path.join("prov-json", json_file)
        xml_path = os.path.join("prov-xml", xml_file)
        self.prov_doc.serialize(json_path)
        self.prov_doc.serialize(xml_path, format="xml")

        if self.graph:
            dot = prov_to_dot(self.prov_doc)
            graph_file = utilities.slugify(file_name) + ".png"
            graph_path = os.path.join("prov-graph", graph_file)
            dot.write_png(graph_path)


@MastProvFactory.register_subclass("data_file")
class MastFileProv(MastProv):
    def __init__(self, params):
        super().__init__(params)
        if self.run is None:
            self.run = self.get_latest_run()
        if FREIA:
            self.file = self.file_name()
        else:
            self.file = params["data"]
        self.log_file = self.get_log()

    @staticmethod
    def validate(params) -> bool:
        client = pyuda.Client()
        if params["data"].lower()[0] in ["a", "e"]:
            return any(
                params["data"].lower() in signal.source_alias
                for signal in client.list_signals()
            )
        else:
            return False

    def get_latest_run(self):
        signal_list = self.client.list(
            ListType.SIGNALS, shot=self.shot, alias=self.data
        )
        highest_pass_number = max([signal.pass_ for signal in signal_list])
        return highest_pass_number

    def file_name(self):
        """
        Returns the name of the datafile based on MAST convention.
        """
        file_sources = self.client.list(ListType.SOURCES, shot=self.shot)
        files = [source.filename for source in file_sources]
        file_name = next(file for file in files if self.data in file)
        if file_name:
            return file_name
        else:
            raise FileNotFoundError

    def get_scheduler_run(self, file_code=None, log_file=None):
        """
        Searches the log file for the line that contains the scheduler
        launch script and the execution start/end times.
        """
        if not file_code:
            file_code = self.data
        if not log_file:
            log_file = self.log_file
        matches = re.findall(f"run_{file_code}.*?:[0-9][0-9]:[0-9][0-9]", log_file)
        start_call = matches[0].split()
        end_call = matches[-1].split()
        scheduler_script = start_call[0]
        start_time = f"{start_call[-2]} {start_call[-1]}"
        end_time = f"{end_call[-2]} {end_call[-1]}"
        scheduler_run = (scheduler_script, start_time, end_time)
        return scheduler_run

    def get_log(self, file_code=None):
        """
        Retrieves the log file for the signal as a string.
        """
        if not file_code:
            file_code = self.data
        filename = f"{file_code}_0{self.shot}.log"
        path = f"/net/raidsrvr/data/MAST_Data/{self.shot}/Pass{self.run}/{filename}"

        if FREIA:
            log = self.client.get_text(path)
        else:
            signal = f'TESTPLUGIN::nathan(filename="{path}")'
            log = self.client.get(signal, '', raw=True).str

        return log

    def get_analysis_code(self, file_code=None):
        """
        Retrieves the analysis codes used to produce the data.
        """
        if not file_code:
            file_code = self.data
        filename = f"info_{file_code}_0{self.shot}_{self.run}.dat"
        location = f"{MastProv.data_location}/{self.shot}/Pass{self.run}/"
        return location + filename

    def build_prov(self):
        """
        Collates the provenance information for the given data file into a
        W3C-PROV document.
        """
        print(f"Generating a provenance document for {self.file} file...")

        self.prov_doc.add_namespace(MastProv.machine, MastProv.namespace_uri)

        file_entity = self.prov_doc.entity(f"{MastProv.machine}:{self.file}")

        data_ro_agent = self.prov_doc.agent(f"{MastProv.machine}:{self.data_ro()}")
        self.prov_doc.wasAttributedTo(file_entity, data_ro_agent)
        scheduler_run = self.get_scheduler_run()
        scheduler_run_activity = self.prov_doc.activity(
            f"{MastProv.machine}:{scheduler_run[0]} run={self.run}",
            startTime=scheduler_run[1],
            endTime=scheduler_run[2],
        )
        scheduler_pass_trigger = self.get_scheduler_trigger()
        scheduler_pass_trigger_agent = self.prov_doc.agent(
            f"{MastProv.machine}:{scheduler_pass_trigger}"
        )
        if FREIA:
            shot_date, shot_time = self.client.get_shot_date_time(shot=self.shot)
            start_time = f"{shot_date} {shot_time}"
        else:
            start_time = None

        record_shot_activity = self.prov_doc.activity(
            f"{MastProv.machine}: Record shot {self.shot}",
            startTime=start_time,
        )
        session_leader = self.get_session_leader()
        session_leader_agent = self.prov_doc.agent(
            f"{MastProv.machine}:{session_leader}"
        )

        input_files = self.get_input_files()
        signals_done = []
        for signal in input_files:
            self.write_signal_prov(
                signal,
                file_entity,
                scheduler_run_activity,
                record_shot_activity,
                scheduler_pass_trigger_agent,
                signals_done=signals_done,
            )
            signals_done.append(signal)

        self.prov_doc.wasAssociatedWith(record_shot_activity, session_leader_agent)
        self.prov_doc.wasGeneratedBy(file_entity, scheduler_run_activity)
        analysis_code = self.get_analysis_code()
        analysis_code_entity = self.prov_doc.entity(
            f"{MastProv.machine}:{analysis_code}"
        )

        analysis_code_author = self.get_analysis_code_author()
        analysis_code_author_agent = self.prov_doc.agent(
            f"{MastProv.machine}:{analysis_code_author}"
        )

        self.prov_doc.used(scheduler_run_activity, analysis_code_entity)
        self.prov_doc.wasAssociatedWith(
            scheduler_run_activity, scheduler_pass_trigger_agent
        )
        self.prov_doc.wasAttributedTo(analysis_code_entity, analysis_code_author_agent)


@MastProvFactory.register_subclass("uda_signal")
class MastSignalProv(MastProv):
    def __init__(self, params):
        super().__init__(params)
        if self.run == None:
            self.signal = self.client.get(self.data, self.shot)
            self.run = int(self.signal.meta["pass"])
        else:
            self.signal = self.client.get(self.data, self.shot, self.run)
        try:
            self.signal_name = self.signal.meta["signal_name"].decode("utf-8")
        except:
            self.signal_name = self.signal.meta["signal_name"]
        self.file_prov = MastFileProv(
            {
                "data": self.signal.meta["filename"][:3].decode("utf-8"),
                "shot": self.shot,
                "run": self.run,
                "graph": self.graph,
            }
        )

    @staticmethod
    def validate(params) -> bool:
        client = pyuda.Client()
        signal = params["data"]
        if signal.lower() in set(
            [signal.source_alias for signal in client.list_signals(shot=params["shot"])]
        ):
            return False
        elif signal.lower() in set(
            [signal.generic_name.lower() for signal in client.list_signals(shot=params["shot"])]
        ):
            return True
        elif signal.lower() in set(
            [signal.signal_name.lower() for signal in client.list_signals(shot=params["shot"])]
        ):
            return True
        else:
            return False

    def build_prov(self):
        """
        Collates the provenance information for the given signal into a
        W3C-PROV compliant json, xml and optionally a graphical output.
        """
        print(
            f"Generating a provenance document for {self.signal_name} data from shot {self.shot}, pass {self.run}..."
        )
        self.file_prov.build_prov()
        self.prov_doc = self.file_prov.prov_doc
        signal = f"{MastProv.machine}:{self.shot}_{self.run}_{self.signal_name}"
        signal_entity = self.prov_doc.entity(signal)
        self.prov_doc.wasDerivedFrom(
            signal_entity, f"{MastProv.machine}:{self.file_prov.file}"
        )


@MastProvFactory.register_subclass("image_file")
class MastImageProv:
    def __init__(self, params):
        pass

    @staticmethod
    def validate(params) -> bool:
        client = pyuda.Client()
        try:
            client.get_images(params["data"], params["shot"])
        except pyuda.cpyuda.ServerException:
            return False
        return True

    def write_prov(self):
        print("Provenance for image data is in development.")


def parse_params(*args, **kwargs) -> Dict:
    """
    Collates the user-provided parameters into a dictionary of the type that the classes are expecting.

    Returns
    -------
    Dict
        A dictionary with keys: data, shot, run and graph.
    """
    params = {"data": None, "shot": None, "run": None, "graph": False}
    if args:
        if len(args) == 1 and isinstance(args[0], Mapping):
            for key, _ in params.items():
                if key in args[0]:
                    params[key] = args[0][key]
        else:
            args_dict = dict(zip_longest(params, args))
            params.update(args_dict)

    for key, _ in params.items():
        if key in kwargs:
            params[key] = kwargs[key]

    return params


def guess_data_type(params: Dict[str, Any]) -> str:
    """Runs each classes validator on the params in turn until a valid class is identified."""
    if not FREIA:
        return "uda_signal"
    for data_type in MastProvFactory.subclasses:
        if MastProvFactory.subclasses[data_type].validate(params):
            return data_type
    else:
        print(f"Invalid data type {params['data']}")
        sys.exit(1)  # TODO: Define and raise custom exception


def write_provenance(*args, **kwargs) -> None:
    params = parse_params(*args, **kwargs)
    data_type = guess_data_type(params)
    prov_data = MastProvFactory.create(data_type, params)
    prov_data.write_prov()


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve and document the provenance of MAST and MAST-U " "data."
    )
    parser.add_argument("shot", help="Shot number", type=int)
    parser.add_argument(
        "run",
        nargs="?",
        default=None,
        help="Run number. Will default to the latest run.",
        type=int,
    )
    parser.add_argument("data", help="Data or signal to document provenance for.")
    parser.add_argument(
        "--graph",
        "-g",
        help="In addition to text formats, write provenance in graph form as .png. "
        "Default: false",
        action="store_true",
    )
    args = parser.parse_args()

    params = {
        "data": args.data,
        "shot": args.shot,
        "run": args.run,
        "graph": args.graph,
    }

    write_provenance(params)
