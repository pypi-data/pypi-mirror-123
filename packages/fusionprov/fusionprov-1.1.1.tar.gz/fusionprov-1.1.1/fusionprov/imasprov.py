import argparse
import json
import os

import imas
from prov.dot import prov_to_dot
from prov.model import ProvDocument

from fusionprov import utilities


class ImasProv:
    """
    This is the class for finding the provenance information for a given
    IDS, which can then be used to produce a provenance document that adheres
    to the W3C-PROV standard.

    Attributes:
        data_ids (imas.ids): The IDS containing the data that this class will
        produce a provenance document for, e.g. 'equilibrium', 'magnetics',
        'thomson_scattering'.

        dataset_desc (imas.ids.dataset_description): The dataset_description
        IDS that corresponds to the data_ids. It is the user's responsibility to
        ensure that the two are from the same pulse file.

        dataset_fair (imas.ids.dataset_fair): The dataset_fair IDS that
        corresponds to the data_ids. It is the user's responsibility to ensure
        that the two are from the same pulse file.
    """

    def __init__(self, data_ids, dataset_desc=None, dataset_fair=None):
        self.data_ids = data_ids
        self.dataset_desc = dataset_desc
        self.dataset_fair = dataset_fair
        self.prov_doc = ProvDocument()

    def imas_uri(self):
        """
        Returns the IMAS data dictionary documentation url based on the version
        used to put the IDS. If the version is not found in the IDS, it will be
        taken from the dataset_descritpion or dataset_fair IDS. Failing that, it
        will return the url for the data_dictionary version 3.31.0
        """
        default_version = "3.31.0"
        if self.data_ids.ids_properties.version_put.data_dictionary:
            version = self.data_ids.ids_properties.version_put.data_dictionary
        elif self.dataset_desc:
            try:
                version = self.dataset_desc.ids_properties.version_put.data_dictionary
            except:
                pass
            else:
                print("Data dictionary version found in dataset_description IDS")
        elif self.dataset_fair:
            try:
                version = self.dataset_fair.ids_properties.version_put.data_dictionary
            except:
                pass
            else:
                print("Data dictionary version found in dataset_fair IDS")
        else:
            version = default_version
        uri = f"https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-{version}/html_documentation.html"
        return uri

    def extract_source(self):
        """
        Converts the contents of ids_properties.source field to dict if it 
        contains json. Otherwise, fills the dict using the _no_source() method.
        """
        try:
            self.data_source = json.loads(self.data_ids.ids_properties.source)
            self.data_source["source"] = self.data_ids.ids_properties.source
        except ValueError:
            print(
                "ids_properties.source not filled according to "
                "recommended template. Provenance information will be "
                "incomplete."
            )
            self.data_source = self._no_source()

        self.prov_doc.add_namespace("IMAS", self.imas_uri())
        self.prov_doc.add_namespace(
            self.data_source["database"], self.data_source["database_uri"]
        )

    def _no_source(self):
        """
        Fills data_source dict with "UNKNOWN" if the ids_properties.source field
        is not filled according to the template.
        """
        empty_source = {
            "database": "UNKNOWN",
            "database_uri": "UNKNOWN",
            "shot": "UNKNOWN",
            "run": "UNKNOWN",
            "data_uri": "UNKNOWN",
            "input_signals": "UNKNOWN",
            "source": f"SOURCE: {self.data_ids.ids_properties.source}"
        }
        return empty_source

    def create_code_agent(self):
        if self.data_ids.code.name and self.data_ids.code.repository:
            self.prov_doc.add_namespace(
                f"{self.data_ids.code.name}", f"{self.data_ids.code.repository}"
            )
        else:
            return None

        code_agent = self.prov_doc.agent(
            f"{self.data_source['database']}:{self.data_ids.code.name}",
            {
                "prov:type": "prov:SoftwareAgent",
                f"{self.data_ids.code.name}:commit": self.data_ids.code.commit,
                f"{self.data_ids.code.name}:version": self.data_ids.code.version,
                f"{self.data_ids.code.name}:repository": self.data_ids.code.repository,
                f"{self.data_ids.code.name}:parameters": self.data_ids.code.parameters,
            },
        )
        return code_agent

    def serialize_provenance(self, graph=False):
        """
        Serialize provenance document to both xml and json formats. Optionally 
        also graphically as png.
        """
        directories = ("prov-xml", "prov-json", "prov-graph")
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Generate document file in both .json and .xml
        json_file = utilities.slugify(f"{self.data_ids.__name__}_prov") + ".json"
        xml_file = utilities.slugify(f"{self.data_ids.__name__}_prov") + ".xml"
        json_path = os.path.join("prov-json", json_file)
        xml_path = os.path.join("prov-xml", xml_file)
        self.prov_doc.serialize(json_path)
        self.prov_doc.serialize(xml_path, format="xml")

        if graph:
            # Generate graphical representation
            dot = prov_to_dot(self.prov_doc)
            graph_file = utilities.slugify(f"{self.data_ids.__name__}_prov") + ".png"
            graph_path = os.path.join("prov-graph", graph_file)
            dot.write_png(graph_path)

    def prov_from_data_ids(self, graph=False):
        """
        This method will provice basic provenance for an IDS that may be
        supplied on its own without a dataset_description or dataset_fair IDS.
        """
        print(f"Generating a provenance document for {self.data_ids.__name__} ids.")

        self.extract_source()

        ids_entity = self.prov_doc.entity(f"IMAS: {self.data_ids.__name__.title()} IDS")
        data_entity = self.prov_doc.entity(
            f"{self.data_source['database']}:"
            f"shot {self.data_source['shot']}, "
            f"run {self.data_source['run']}, "
            f"{self.data_ids.__name__} data, "
            f"{self.data_source['source']}"
        )
        self.prov_doc.wasDerivedFrom(ids_entity, data_entity)

        ids_provider_agent = self.prov_doc.agent(
            f"{self.data_source['database']}:{self.data_ids.ids_properties.provider}"
        )
        code_agent = self.create_code_agent()
        self.prov_doc.wasAttributedTo(ids_entity, ids_provider_agent)

        if code_agent:
            self.prov_doc.wasAttributedTo(data_entity, code_agent)

        try:
            data_put_activity = self.prov_doc.activity(
                "IMAS:put", startTime=self.data_ids.ids_properties.creation_date,
            )
        except ValueError:
            data_put_activity = self.prov_doc.activity("IMAS:put")

        data_dict_entity = self.prov_doc.entity(
            f"IMAS:data dictionary version {self.data_ids.ids_properties.version_put.data_dictionary}"
        )
        access_layer_entity = self.prov_doc.entity(
            f"IMAS:access layer {self.data_ids.ids_properties.version_put.access_layer}"
        )
        access_layer_lang_entity = self.prov_doc.entity(
            f"IMAS:access layer language {self.data_ids.ids_properties.version_put.access_layer_language}"
        )
        self.prov_doc.used(data_put_activity, data_dict_entity)
        self.prov_doc.used(data_put_activity, access_layer_entity)
        self.prov_doc.used(data_put_activity, access_layer_lang_entity)
        self.prov_doc.wasGeneratedBy(ids_entity, data_put_activity)
        self.prov_doc.wasAssociatedWith(data_put_activity, ids_provider_agent)

        self.serialize_provenance(graph=graph)


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve and document the provenance of an Interface Data "
        "Structure (IDS)."
    )
    parser.add_argument("database", help="IMAS database")
    parser.add_argument("shot", help="Shot number", type=int)
    parser.add_argument("run", help="Run number", type=int)
    parser.add_argument("ids", help="IDS name")
    parser.add_argument(
        "--graph",
        "-g",
        help="In addition to text formats, write prov in graph form as .png. "
        "Default: false",
        action="store_true",
    )
    parser.add_argument(
        "--remote",
        "-r",
        help="Request data from remote database. By default the data will be read from the local IMAS database.",
        action="store_true"
    )
    args = parser.parse_args()

    if args.remote:
        pulse = imas.ids(args.shot, args.run)
        pulse.open_public(args.database)
    else:
        user = os.environ["USER"]
        imas_version = os.environ["IMAS_VERSION"]
        pulse = imas.ids(args.shot, args.run)
        pulse.open_env(user, args.database, imas_version)

    ids = getattr(pulse, args.ids)
    ids.get()
    print("Getting IDS...")
    ids_prov = ImasProv(ids)
    ids_prov.prov_from_data_ids(graph=args.graph)
