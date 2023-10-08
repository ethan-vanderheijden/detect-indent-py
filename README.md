# detect-indent for Python [![Test](https://github.com/Ethan-Vanderheijden/detect-indent-py/actions/workflows/CI.yml/badge.svg)](https://github.com/Ethan-Vanderheijden/detect-indent-py/actions/workflows/CI.yml)
Python port of
[sindresorhus/detect-indent](https://github.com/sindresorhus/detect-indent) All
attribution goes to that project.

> Detect the indentation of code

Pass in a string of any kind of text and get the indentation.


## Use cases

- Persisting the indentation when modifying a file.
- Have new content match the existing indentation.
- Setting the right indentation in your editor.

## Install

```
pip install detect-indent
```

## Usage

```py
from detect_indent import detect_indent

sample_string = '''
Example string
  with an indentation
    of two spaces
'''

indent = detect_indent(sample_string)
print(indent)  # {'amount': 2, 'type': 'space', 'indent': '  '}
```

## API

Returns a dictionary with the following stats about indentation:

 - `amount` {number} - Amount of indentation, for example 2. Will be 0 if indentation could not be detected.
 - `type` {'tab' | 'space' | None} - Type of indentation. Possible values are `'tab'`, `'space'` or `None` if no indentation is detected
 - `indent` {string} - A string representing the actual indentation, for example a string of two spaces.

## Algorithm

The current algorithm looks for the most common difference between two
consecutive non-empty lines. [More Details](https://github.com/sindresorhus/detect-indent)
