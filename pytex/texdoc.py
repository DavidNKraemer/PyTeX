from dataclasses import dataclass

from typing import Optional, Union


@dataclass
class TeXEnv:

    name: str
    contents: str


@dataclass
class TeXMacro:

    name: str
    n_args: Optional[int]
    first_arg: Optional[str]
    definition: str

    def to_texdef(self):
        name = f'\\newcommand{{\{self.name}}}'
        n_args = f'[{self.n_args}]' if self.n_args else ''
        first_arg = f'[{self.first_arg}]' if self.first_arg else ''
        definition = f'{{{self.definition}}}'

        return ''.join([name, n_args, first_arg, definition])



class TeXDoc:

    def __init__(self, text: str):
        """
        """
        self.text = text

    def __contains__(self, other: Union[str, TeXMacro]) -> bool:
        if isinstance(other, str):
            return other in self.text
        elif isinstance(other, TeXMacro):
            return ('\\' + other.name) in self.text
        else:
            return False