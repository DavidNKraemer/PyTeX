import re

from typing import List, Optional, Tuple

from pytex.texdoc import TeXMacro


def strip_comments(text: str) -> str:
    """
    Return a version of provided LaTeX text with comments removed.
    """
    return '\n'.join(
        line.split('%')[0].strip() for line in text.splitlines()
    )


def get_newcommands(text: str) -> List[TeXMacro]:
    """
    Parse all macros defined by the expression 

        \\newcommand{\macro}[args]{definition}

    in a given text into TeXCommand objects, and return the list of documents

    Args:
        text: search text

    Returns:
        
    """
    pattern = r"\\(?:re)?newcommand{?\\(\w+)}?\[?(\d+)?\]?\[?([\w\s\d]+)?\]?(.*)$"
    expr = re.compile(pattern, re.MULTILINE)

    commands = []
    for name, n_args, first_arg, definition in expr.findall(text):
        
        n_args = int(n_args) if n_args else None

        definition = definition.strip()[1:-1]
        
        command = TeXMacro(name, n_args, first_arg, definition)

        commands.append(command)

    return commands   


