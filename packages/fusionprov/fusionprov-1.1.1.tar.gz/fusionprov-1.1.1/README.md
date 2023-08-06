# fusionprov
## A python package for retrieving and documenting the provenance of fusion data.

<br/>

INTRODUCTION
----------------
----------------
The FAIR4Fusion projects seeks to make data produced by the nuclear fusion community FAIR compliant. Part of this is to ensure that the provenance of fusion data is readily available such that users can be confident in the quality of the data.

This package provides a way to retrieve provenance information for a given data-set from the institute that produced/owns the data and generate provenance documents that adhere to the W3C-PROV standard.

<br/>

### mastprov
------------
This module provides the `write_provenance()` function that will collate the provenance information for the signal or analsed data file into a W3C-PROV compliant provenance document in json and xml formats. Optionally, it will also output a graphical representation of the provenance as a png.

EXAMPLE:
```
import fusionprov

fusionprov.write_provenance("ip", 30420, graph=True)
```
<br/>

The `mastprov` module can also be run from the command line:

```> mastprov 30420 ip --graph```

<br/>

Both examples will generate directories in the current working directory for json, xml and png, storing the PROV documents in the relevant location.

<br/>

MAST/MAST-U DATA FILES

Provenance documents can also be generated from the level of the data file itself within your Python script or from the command line:

EXAMPLE:
```
import fusionprov

fusionprov.write_provenance("efm", 30420, graph=True)
```
or

```> mastprov 30420 efm -g```

<br/>

### imasprov
------------
This module provides the ImasProv class. The class should be instantiated with an IDS (Interface Data Structure) containing the dataset, and optionally the accompanying dataset_descritption/dataset_fair IDSs.

Currently, the prov_from_data_ids() method will generate the provenance document from information in the 'ids_properties' and 'code' trees in the IDS.

From the command line, the module will read in IDS data from your local imasdb, e.g.:

```> imasprov WEST 56900 3 equilibrium --graph```

Building provenance structures from remote datasets is currently limited to WEST data. The `--remote` or `-r` flag will try to retrieve data from the WEST UDA server provided your environment is correctly configured, e.g.:

```> imasprov WEST 54178 0 magnetics --graph --remote```

Again, the module will generate directories in the current working directory for json, xml and png, storing the PROV documents in the relevant location.

<br/>

REQUIREMENTS
------------
------------

NOTE: The '--graph' option enables graphical output for provenance dosuments, but requires that the graphviz package be installed. You will need to install graphviz using your package manager of choice, e.g.:

`brew install graphviz`

Additionally, the mastprov module requires a local UDA installation and the imasprov module requires an IMAS installation (which may include UDA depending on your environment).

<br/>

INSTALLATION
------------
------------
This tool currently runs as a standalone package, available on PyPi, but may be adapted into a UDA plugin in the future. Provided that other dependencies are present, simply run:

`pip install fusionprov`

<br/>

DEVELOPERS
----------
----------
For those wishing to define further data types and generate provenance documents for them, a Factory Design Pattern is implemented in the `mastprov` module. Write a class for your data type, including a (static) `validate` method and a `write_prov` method. The class should expect parameters as a dictionary with keys, `"data"`, `"shot"`, `"run"` and `"graph"`.

Finally, decorate your class with `@MastProvFactory.register_subclass("<data_type>")` replacing `<data_type>` with a label that is not yet in use by the other classes.

EXAMPLE:
```
@MastProvFactory.register_subclass("my_data_type")
class MyMastDataType:
    def __init__(self, params):
    """Initialisation"""

    @staticmethod
    def validate(params) -> bool:
    """Validation logic goes here. It should return True if params["data"] is a valid label for your data type.""" 

    def write_prov(self):
    """Logic for constructing the provenance document goes here"""
```
For the `write_prov()` method, refer to the [prov package documentation](https://prov.readthedocs.io/en/latest/) for information on how to construct provenance documents.
