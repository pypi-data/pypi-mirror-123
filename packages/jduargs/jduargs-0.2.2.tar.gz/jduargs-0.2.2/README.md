# jduargs

Simple command line argument parser.

## Installation
```bash
> pip(3) install (-U) jduargs
```

and

``` python
from jduargs import ArgumentParser
```

## Methods


```python
def add(self, key: str, short: str, type: type = Type[str], required: bool = True, description: str = "")
```
... to add an expected argument. The parameters are:
- key: the name of the parameter
- short: the short version of the key, as a single caracter
- type: the parameter type class
- required: define if the argument is mandatory or not. If set to False and the parameter is not provided, the default value is set by the type constructor
- description: explanation of what this parameter is used for. If no description is provided, an empty string is used instead

```python
def from_json(self, path: str)
```
... to import the expected parameters from a json file. The dictionnary keys are the parameters name. For each key, it should contains the "short" and "type" keys as strings, and a required key as a boolean.
```python
def to_json(self, filename: str)
```
... to export the parameter dictionnary to a json file.
```python
def compile(self, args: List[str])
```
... to parse the provided argument list with respect to the defined parameters.

## Usage

First create an instance of the parser:

``` python
parser = ArgumentParser()
```

Then add the expected arguments to parse:

``` python
parser.add("path", "p", str, False)
parser.add("offset", "o", int, True)
```

Compile the parser with the input arguments provided from command line:

``` python
parser.compile(sys.argv[1:])
```

From here you can access each parameters with the simple bracket operator:

``` python
path = parser["path"]
offset = parser["offset"]
```
