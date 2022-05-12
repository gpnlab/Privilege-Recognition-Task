from os import path
from exe import EXE
import json
from exe import EXE
class ConfigReader:

    #requires a json formated as in the default directory
    def parseToDict(filename,dirName = "default"):

        if dirName == "default":
            asset_url = EXE.resource_path(f"configs/{filename}.json")
        else:
            asset_url = EXE.resource_path(f"configs/levelconfigs/{filename}.json") 

        d = ConfigContainer(asset_url)
        
        return d

    @staticmethod
    def returnQuestionText(self):
        retList = []
        for q in self.config["questions"]:
            retList.append(q["question"])
        return retList
    
    @staticmethod
    def returnQuestionText(self):
        retList = []
        for q in self.config["questions"]:
            retList.append(q["question"])
        return retList
    

# copied from my files need to make package at sometime
class ConfigContainer(dict):
    """Class to load dict from json file

    Extends python dict to load from json files and adds usage of the `.`
    operator to call/set keys and values. When the dictonary is updated
    the json_file is updated to record the change. Print
    Some code referenced from
    [stackoverflow](https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary).

    Typical usage example:

    ```
    container = ConfigContainer(jsonfile)
    container.key
    container.key.subkey
    container.key = "something"
    del container.key
    container.update_json()
    ```

    """

    json_file: str = None
    """reference json file path
    """

    def __init__(self, json_filename: str = None, *args, **kwargs):
        super(ConfigContainer, self).__init__(*args, **kwargs)
        
        if json_filename is not None:
            self.set_json(json_filename)
            self.read_json()

        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    if isinstance(v, dict):
                        self[k] = ConfigContainer(None, v)
                    else:
                        self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    self[k] = ConfigContainer(None, v)
                else:
                    self[k] = v

    def set_json(self, filename: str) -> None:
        """Sets json filename for the container class

        Args:
            filename (str): path for the json file
        """
        self.json_file = filename

    def read_json(self) -> None:
        """Read in parameters from json file

        Read each level of dictionary as its own container recursively.
        """
        with open(self.json_file) as f:
            data = json.load(f)
            for k, v in data.items():
                if isinstance(v, dict):
                    self[k] = ConfigContainer(None, v)
                else:
                    self[k] = v

    def update_json(self) -> None:
        """Dumps parameters to json file
        """
        with open(self.json_file, "w") as f:
            dict_copy = self.copy()
            del dict_copy["json_file"]
            json.dump(dict_copy, f)

    def __getattr__(self, attr) -> None:
        """override dict '.' operator for access"""
        return self.get(attr)

    def __setattr__(self, key, value) -> None:
        """override dict '.' operator for setting keys"""
        self.__setitem__(key, value)

    def __setitem__(self, key, value) -> None:
        """allows use of '.' operator for setting key values"""
        if isinstance(value, dict):
            value = ConfigContainer(None, value)
        super(ConfigContainer, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(ConfigContainer, self).__delitem__(key)
        del self.__dict__[key]

    def __str__(self) -> str:
        string = ["{"]
        for k, v in self.items():
            if isinstance(v, dict):
                strv = "\n\t".join(str(v).splitlines())
                string.append(f"\t{k}: " + f"{strv}")
            elif isinstance(v, list):
                strv = "\n\t\t".join(str(v).split(", "))
                string.append(f"\t{k}: " + f"{strv}")
            else:
                string.append(f"\t{k}: {v},")
        string.append("}")
        return "\t\n".join(string)