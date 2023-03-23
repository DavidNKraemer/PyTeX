from pytex.utils import str_union

def test_str_union():
    
    a = 'hello'
    b = 'world'

    union = str_union(hello, world)

    assert a == union
    assert b == union
    
