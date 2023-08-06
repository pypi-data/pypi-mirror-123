"""File and other stream i/o methods.

Writing to

- **text files**
- **stderr**

or reading from

- **text files** as lines
- **yaml** or **json** files as dictionaries
- **csv** files as array

or parsing data (dictionary, json/yaml) to and from a ``Parsable`` class object made easy!
"""


import os
import sys
import json
import yaml
import pandas
import exifread
import tifffile
import logging


logger = logging.getLogger()
"""A logger enabled by the logging module."""


### input


def read_txt(path, *args, **kwargs):
    """Read text as string from a file.
    
    Args:
        path (str): A path to a file.
        args, kwargs: Any other argument passed to `open`,
            such as mode, encoding, etc.

    Returns:
        str: The text (or bytestring, depending on the mode selected)
            from the selected file.
    """
    fs = open(path, *args, **kwargs)
    text = fs.read()
    fs.close()
    return text


def read_lines(path, strip = os.linesep, *args, **kwargs):
    """Read text as lines from a file.

    A file is read line by line and parsed as a list of strings.

    Args:
        path (str): File path.
        strip (str): Characters to strip from the end
            of each line. `None` to skip stripping.
        args, kwargs: Any other argument passed to `open`,
            such as mode, encoding, etc.

    Returns:
        list: Lines read from the file as a list of strings.
    """
    fs = open(path, *args, **kwargs)
    lines = fs.readlines()
    fs.close()
    if strip is not None:
        lines = [line.rstrip(strip) for line in lines]
    return lines


def read_json(path):
    """Read a JSON file.

    Read a JSON formatted file into a dictionary object.

    Args:
        path (str): File path to JSON formatted file.

    Returns:
        dict: Content of a JSON file parsed as dictionary.
    """
    fs = open(path, "r")
    d = json.load(fs)
    fs.close()
    return d


def read_yaml(path):
    """Read a YAML file.

    Read a YAML formatted file into a dictionary object.
    Supports logging (see :py:mod:`miscset`).

    Args:
        path (str): File path.

    Returns:
        dict: Content of a YAML file parsed as dictionary.

    .. exec_code::
        :caption: Example code:
        :caption_output: Result:

        import miscset
        print(miscset.io.read_yaml("tests/example.yml"))
    """
    d = {}
    if not os.path.isfile(path):
        logging.error("missing YAML file at {}".format(path))
        return d
    with open(path, "r") as fs:
        try:
            logging.info("parsing YAML from file {}".format(path))
            d = yaml.safe_load(fs)
        except yaml.YAMLError as e:
            logging.error("failed importing {} YAML {}".format(path, e))
    logging.debug("parsed YAML content as {}".format(d))
    return d


def read_csv(path, *args, **kwargs):
    """Read a CSV file.

    Parse a csv file to a pandas DataFrame.

    Args:
        path (str): File path.
        args, kwargs: Arguments passed to `pandas.read_csv`.

    Returns:
        DataFrame: A table containing the values read from the file.
    """
    csv = pandas.read_csv(path, *args, **kwargs)
    return csv


def read_xl(path, *args, **kwargs):
    """Read an EXCEL table.

    Import tables in EXCEL format.

    Args:
        path (str): File path.
        args, kwargs: Arguments passed to `pandas.read_excel`.

    Returns:
        DataFrame: A table containing the values read from the file's selected sheet.
    """
    xl = pandas.read_excel(path, *args, **kwargs)
    return xl


def read_tiff(path):
    """Read TIFF image using tifffile.
    
    Args:
        path (str): File path to a TIFF file.
    """
    img = tifffile.imread(path)
    return img


def read_tiff_tags(path, parser = "tifffile", prefix = False):
    """Read TIFF metadatad.
    
    Args:
        path (str): Path to a TIFF file.
        parser (str): Parser to use for reading the file metadata with.
            One of 'tifffile' or 'exifread'.
    
    Returns:
        tbd
    """
    if parser == "tifffile":
        tags = {}
        with tifffile.TiffFile(path) as tif:
            for i, page in enumerate(tif.pages):
                for j, tag in enumerate(page.tags):
                    key = str(tag.name)
                    if prefix:
                        key = ".".join([str(i), str(j), key])
                    tags[key] = tag.value
        return tags
    elif parser == "exifread":
        f = open(path, 'rb')
        return exifread.process_file(f)
    else:
        raise Exception("There is no such parser")


### output


def write_txt(text, path):
    """Write text to a file.

    A file at a path is opened writable,
    and the text from a string variable is inserted.

    Args:
        text (str): Text to write to a file at `path`.
        path (str): File path.
    """
    fs = open(path, "w")
    fs.write(text)
    fs.close()
    return


def write_stdout(text, newline = True):
    """Write text to the standard output file stream.
    
    A text string is written to the system standard output file stream,
    and optionally a newline is added.

    Args:
        text (str): Output text.
        newline (bool): Add a os specific line separator to
            the end of the text.

    .. exec_code::
        :caption: Example code:
        :caption_output: Result:

        import miscset
        miscset.io.write_stdout("Hello, world!")
    """
    sys.stdout.write(text)
    if newline:
        sys.stdout.write(os.linesep)
    sys.stdout.flush()
    return


def write_stderr(text, newline = True):
    """Write text to the standard error file stream.
    
    A text string is written to the system standard error file stream,
    and optionally a newline is added.

    Args:
        text (str): Output text.
        newline (bool): Add a os specific line separator to
            the end of the text.
    """
    sys.stderr.write(text)
    if newline:
        sys.stderr.write(os.linesep)
    sys.stderr.flush()
    return


def write_json(path, obj, default = repr):
    """Write an object representation to a json file.
    
    See https://docs.python.org/3/library/json.html#json.dump
    """
    fs = open(path, "w")
    fs.write(json.dumps(obj, default = default))
    fs.close()


class Parsable(object):
    """A class where slots are parsable.

    Provides methods to import and export values for data slots from dictionaries.

    Use case:
        - Get a dictionary from any object structure.
        - Get a JSON or YAML string from any object structure.
        - Parse a dictionary to add/overwrite object slots with values.

    .. exec_code::
        :caption: Example code:
        :caption_output: Result:

        import miscset
        class Container(miscset.io.Parsable):
            def __init__(self, value):
                self.value = value
        c = Container([1,2,3])
        c.import_dict({"foo": "bar"}, add = True)
        print(c.get_json())

    """

    def __init__(self):
        """Initialize a Parsable object.

        Initializes the object and calls the `reset` function.
        """
        self.reset()

    def reset(self):
        """Reset slots to default values.

        This method implemented here does not affect anything.

        It is a placeholder for subclasses implementing this method.
        When calling the class constructor, this method will be called.
        """
        return

    def __str__(self):
        """Create a string representation of the object data slots."""
        return self.description()

    def get_text(self, name = None, sep = os.linesep + "  ", private = True):
        """Return a description.

        Args:
            name (str): Provide a custom name of the class shown as prefix.
            sep (str): A string separating the values.
            private (bool): Show privat slots (starting with an underscore "_").

        Returns:
            str: A text representation of the object data slots.
        """
        if name is None:
            name = "miscset.io.Parsable"
        txt = "<{}:".format(name)
        for var in vars(self):
            if not private and var.startswith("_"):
                continue
            value = getattr(self, var)
            if type(value) == type([]):
                value = [ str(i) for i in value ]
            if type(value) == type({}):
                value = { k: str(v) for k,v in value.items() }
            txt += "{}{}={}".format(sep, var, value)
        txt += ">"
        return txt

    def get_dict(self):
        """Return values of the data slots as dictionary.

        Same as accessing the `__dict__` slot from a class instance.

        Returns:
            dict: A dictionary with keys named as the class instance slots
                containing the respective values.
        """
        return self.__dict__

    def get_json(self):
        """"Return values of the data slots as a json string.

        Returns:
            str: A JSON formatted string.
        """
        return json.dumps(self.get_dict())

    def get_yaml(self):
        """"Return values of the data slots as a yaml string.

        Returns:
            str: A YAML formatted string.
        """
        return yaml.dump(self.get_dict())

    def import_dict(self, obj, add = False):
        """Import a dictionary into data slots.

        Args:
            obj (dict): A dictionary from which keys become
               slots and assigned the values.
            add (bool): Whether to add a key as slot if it
               did not yet exist.
        """
        self.reset()
        if not type(obj) == type({}):
            return
        if obj is None:
            return
        if not callable(getattr(obj, "keys", None)):
            return
        varnames = [key for key, value in vars(self).items()]
        #obj = { key: obj.get(key) for key in obj.keys() if key in varnames }
        for key, value in obj.items():
            if key not in varnames and not add:
                continue
            setattr(self, key, value)
