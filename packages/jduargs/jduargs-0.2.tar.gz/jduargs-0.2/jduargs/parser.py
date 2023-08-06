from typing import Any, List, Type
import builtins
import json


class ArgumentParser:
    """A simple argument parser.
    It allows you to specify the type of each expected argument.

    The key-shorts and their values have to be given together.
    For example: if an integer \"offset\" with short being \"o\" has to take the value 100, in the command-line you would type \"-o100\".
    """

    def __init__(self):
        """
        Initialisation of the class.
        """
        self.arguments: dict = {}
        self.__results: dict = {}

    def from_json(self, path: str):
        """Use the content of the json file at path to fill list of arguments to parse.

        Parameters
        ----------
        path: string
            Path (absolute or relative) to the json file.
        """
        with open(path, "r") as f:
            data = json.load(f)

        for key, value in data.items():
            short = value["short"]
            type = getattr(builtins, value["type"])
            required = value["required"]

            self.add(key, short, type, required)

    def add(
        self, key: str, short: str, type: type = Type[str], required: bool = True
    ) -> None:
        """Add an argument to parse.

        Parameters
        ----------
        key: string
            key of the new argument. It has to be new.
        short: string
            short representation of the key, without dash.
        type: type
            type of the argument. (default is str)
        required: boolean
            flag that specify if a key is mandatory. (default is True)
        """
        assert key not in self.arguments.keys(), "Key already used."
        assert isinstance(key, str), "Key must be a string."
        assert isinstance(short, str), "Short must be a string."
        assert isinstance(type, Type), "Type must be a class type."
        assert isinstance(required, bool), "Required must be a boolean."
        assert len(short) == 1, "Short must be a single character."

        self.arguments[key] = {"short": f"-{short}", "required": required, "type": type}

    def compile(self, args: List[str]):
        """Parse the input arguments with the keys previously specified.

        Parameters
        ----------
        args: list of string
            Arguments to parse

        """
        if len(args) == 0:
            print("To get help, use -h or --help command line options.")
            exit()

        if len(args) == 1 and args[0] in ["--help", "-h"]:
            self.show_help()
            exit()

        keys = [key for key, _ in self.arguments.items()]
        shorts = [value["short"] for _, value in self.arguments.items()]

        for arg in args:
            if arg[:2] in shorts:
                key = keys[shorts.index(arg[:2])]
                self.__results[key] = arg[2:]

        for key in keys:
            if self.arguments[key]["required"] and key not in self.__results.keys():
                print(
                    f"{__class__.__name__} error: '{key}' command line argument is required. Add it using '{self.arguments[key]['short']}value'"
                )
                exit()

    def show_help(self):
        n_arg = len(self.arguments)
        length_str = max([len(arg) for arg in self.arguments.keys()])

        print(f"{n_arg} argument{'s' if n_arg>1 else ''} expected: ")
        for key, value in self.arguments.items():
            req_str = "required" if value["required"] else ""
            print(f"{value['short']} {value['type']}: {key:{length_str+10}s}{req_str}")

        print("")
        print("Usage:")
        print("Short keys and their values must be together. For example:")
        print("- '-o12' for a short key being 'o' and value '12'.")
        print("- '-dpath' for a short key being 'd' and value 'path'.")
        print("")
        print(
            "Non-necessary arguments with no values provided will take the default constructor value."
        )

    def __getitem__(self, key: str) -> Any:
        """Returns the value (with the right type) associated with a given key. If the key correspond to an optional argument that has not been given, the method returns None.

        Parameters
        ----------
        key: string
            key to retrieve the value for.

        Returns
        -------
        Any
            The value related to the given key, with the right type.

        """
        assert len(self.__results), "First compile the parser."
        assert key in self.arguments, f'Key "{key}" not found.'

        if key not in self.__results:
            return self.arguments[key]["type"]()

        try:
            return self.arguments[key]["type"](self.__results[key])
        except ValueError as e:
            print(
                f"{__class__.__name__} error with '{key}': {e}. Using default constructor value."
            )
            return self.arguments[key]["type"]()
