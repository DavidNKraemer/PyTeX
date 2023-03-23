from pytex.parsing import strip_comments, get_newcommands
from pytex.texdoc import TeXDoc


with open('demos/main.tex') as f:
    text = TeXDoc(strip_comments(f.read()))

for macro in get_newcommands(text.text):
    print(macro)
    print(macro in text)
