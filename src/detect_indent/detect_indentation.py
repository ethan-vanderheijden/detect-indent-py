import re

# Detect either spaces or tabs but not both to properly handle tabs for indentation and spaces for alignment
INDENT_REGEX = r"^(?:( )+|\t+)"

INDENT_TYPE_SPACE = "space"
INDENT_TYPE_TAB = "tab"

"""
Make a Map that counts how many indents/unindents have occurred for a given size and how many lines follow a given indentation.

The key is a concatenation of the indentation type (s = space and t = tab) and the size of the indents/unindents.

```
indents = {
    t3: [1, 0],
    t4: [1, 5],
    s5: [1, 0],
    s12: [1, 0],
}
```
"""


def make_indents_map(string, ignore_single_spaces):
    indents = {}

    # Remember the size of previous line's indentation
    previous_size = 0
    previous_indent_type = ""

    # Indents key (ident type + size of the indents/unindents)
    key = None

    for line in string.splitlines():
        if not line:
            # Ignore empty lines
            continue

        matches = re.search(INDENT_REGEX, line)

        if not matches:
            previous_size = 0
            previous_indent_type = ""
        else:
            indent = len(matches[0])
            indent_type = INDENT_TYPE_SPACE if matches[1] else INDENT_TYPE_TAB

            # Ignore single space unless it's the only indent detected to prevent common false positives
            if (
                ignore_single_spaces
                and indent_type == INDENT_TYPE_SPACE
                and indent == 1
            ):
                continue

            if indent_type != previous_indent_type:
                previous_size = 0

            previous_indent_type = indent_type

            use = 1
            weight = 0

            indent_difference = indent - previous_size
            previous_size = indent

            # Previous line have same indent?
            if indent_difference == 0:
                # Not a new "use" of the current indent:
                use = 0
                # But do add a bit to it for breaking ties:
                weight = 1
                # We use the key from previous loop
            else:
                key = encode_indents_key(indent_type, abs(indent_difference))

            # Update the stats
            entry = indents.get(key)
            if entry:
                entry = [entry[0] + use, entry[1] + weight]
            else:
                entry = [1, 0]

            indents[key] = entry

    return indents


# Encode the indent type and amount as a string (e.g. 's4') for use as a compound key in the indents Map.
def encode_indents_key(indent_type, indent_amount):
    type_character = "s" if indent_type == INDENT_TYPE_SPACE else "t"
    return type_character + str(indent_amount)


# Extract the indent type and amount from a key of the indents Map.
def decode_indents_key(indents_key):
    type = INDENT_TYPE_SPACE if indents_key.startswith("s") else INDENT_TYPE_TAB
    amount = int(indents_key[1:])
    return (type, amount)


# Return the key (e.g. 's4') from the indents Map that represents the most common indent,
# or return None if there are no indents.
def get_most_used_key(indents):
    result = None
    max_used = 0
    max_weight = 0

    for key, value in indents.items():
        used_count = value[0]
        weight = value[1]
        if used_count > max_used or (used_count == max_used and weight > max_weight):
            max_used = used_count
            max_weight = weight
            result = key

    return result


def make_indent_string(type, amount):
    indent_character = " " if type == INDENT_TYPE_SPACE else "\t"
    return indent_character * amount


def detect_indent(string):
    if not isinstance(string, str):
        raise TypeError("Expected a string")

    # Identify indents while skipping single space indents to avoid common edge cases (e.g. code comments)
    # If no indents are identified, run again and include all indents for comprehensive detection
    indents = make_indents_map(string, True)
    if len(indents) == 0:
        indents = make_indents_map(string, False)

    key_of_most_used_indent = get_most_used_key(indents)

    indent_type = None
    amount = 0
    indent = ""

    if key_of_most_used_indent is not None:
        indent_type, amount = decode_indents_key(key_of_most_used_indent)
        indent = make_indent_string(indent_type, amount)

    return {
        "amount": amount,
        "type": indent_type,
        "indent": indent,
    }
