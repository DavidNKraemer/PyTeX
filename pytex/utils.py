from dataclasses import dataclass


@dataclass
class str_union:
    a: str
    b: str
    
    def __eq__(self, __o: object) -> bool:
        return (self.a == __o) or (self.b == __o)
    
    def __hash__(self):
        if self.a < self.b:
            return hash((self.a, self.b))
        else:
            return hash((self.b, self.a))