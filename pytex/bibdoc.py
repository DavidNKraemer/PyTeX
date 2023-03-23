import bibtexparser as bib
import typing

from dataclasses import dataclass
from functools import total_ordering
from typing import List, Mapping, Tuple

from utils import str_union


standard_entry_types = {
    'article': {
        'required': {'author', 'title'},
        'optional': {'volume', 'number', 'pages', 'month', 'note'}
    },
    'book': {
        'required': {
            str_union('author', 'editor'), 'title', 'publisher', 'year'
        },
        'optional': {
            str_union('volume', 'number'), 'series', 'address', 'edition',
            'month', 'note'
        } 
    },
    'booklet': {
        'required': {'title'},
        'optional': {
            'author', 'howpublished', 'address', 'month', 'year', 'note'
        }
    },
    'conference': {
        'required': {'author', 'title'},
        'optional': {'volume', 'number', 'pages', 'month', 'note'}
    },
    'inbook': {
        'required': {
            str_union('author', 'editor'), 'title', 
            str_union('chapter', 'pages'), 'publisher', 'year'
        },
        'optional': {
            str_union('volume', 'number'), 'series', 'type', 'address',
            'edition', 'month', 'note'
        }
    },
    'incollection': {
        'required': {'author', 'title', 'booktitle', 'publisher', 'year'},
        'optional': {
            'editor', str_union('volume', 'number'), 'series', 'type', 
            'chapter', 'pages', 'address', 'eddition', 'month', 'note'
        }
    },
    'inproceedings': {
        'required': {'author', 'title', 'booktitle', 'year'},
        'optional': {
            'editor', str_union('volume', 'number'), 'series', 'pages',
            'address', 'month', 'organization', 'publisher', 'note'
        }
    },
    'manual': {
        'required': {'title'},
        'optional': {
            'author', 'organization', 'address', 'edition', 'month', 'year',
            'note'
        }
    },
    'mastersthesis': {
        'required': {'author', 'title', 'school', 'year'},
        'optional': {'type', 'address', 'month', 'note'}
    },
    'misc': {
        'required': {},
        'optional': {
            'author', 'title', 'howpublished', 'month', 'year', 'note'
        }
    },
    'phdthesis': {
        'required': {'author', 'title', 'school', 'year'},
        'optional': {'type', 'address', 'month', 'note'}
    },
    'proceedings': {
        'required': {'year', 'title'},
        'optional': {
            'editor', str_union('volume', 'number'), 'series', 'address',
            'month', 'organization', 'publisher', 'note'
        }
    },
    'techreport': {
        'required': {'author', 'title', 'institution', 'year'},
        'optional': {'type', 'number', 'address', 'month', 'note'}
    },
    'unpublished': {
        'required': {'author', 'title', 'note'},
        'optional': {'month', 'note'}
    }
}

@total_ordering
@dataclass
class BibEntry:
    """
    """
    entry_type: str
    cite_key: str
    fields: Mapping[str, str]

    @classmethod
    def from_dict(cls, info: dict):
        """
        """
        entry_type = info.pop('ENTRYTYPE')
        cite_key = info.pop('ID')

        return cls(entry_type, cite_key, info)

    def is_standard(self) -> bool:
        """
        """
        standard_entry = self.entry_type in standard_entry_types

        return standard_entry
    
    def validate(self) -> Tuple[bool, set, set]:
        """
        """
        is_standard = self.is_standard()

        missing_fields = set()
        extraneous_fields = set()

        if is_standard:
            std_fields = standard_entry_types[self.entry_type]

            for field_key in std_fields['required']:
                if field_key not in self.fields:
                    missing_fields.add(field_key)
            
            for field_key in self.fields:
                not_required = field_key not in std_fields['required']
                not_optional = field_key not in std_fields['optional']

                if not_required and not_optional:
                    extraneous_fields.add(field_key)
        
        return is_standard, missing_fields, extraneous_fields

    def __eq__(self, __o) -> bool:
        """
        Two BibEntries are equal iff their cite key are the same.

        TODO: think about this...
        """
        #entry_type_match = self.entry_type == __o.entry_type
        cite_key_match = self.cite_key == __o.entry_type

        return cite_key_match
    
    def __le__(self, __o) -> bool:
        #entry_type_le = self.entry_type < __o.entry_type
        cite_key_le = self.cite_key < __o.cite_key

        return cite_key_le

    def __str__(self) -> str:
        """
        """

        spacing = ' ' * 4
        contents = ',\n'.join(
            f"{spacing}{key} = \"{val}\"" for key, val in self.fields.items()
        )

        entry = "@{}{{{},\n{}\n}}".format(
            self.entry_type, 
            self.cite_key, 
            contents
        )

        return entry
    

class BibDoc(list):

    @classmethod
    def from_io(cls, io: typing.TextIO):
        
        db = bib.load(io)
        entries = [BibEntry.from_dict(entry) for entry in db.entries]

        return cls(*entries)


    def __init__(self, *entries: List[BibEntry]):
        super(BibDoc, self).__init__()
        for entry in entries:
            self.append(entry)


