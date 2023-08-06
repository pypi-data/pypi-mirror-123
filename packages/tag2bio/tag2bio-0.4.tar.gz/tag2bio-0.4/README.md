
# Tag2Bio

Tag2Bio is a python package aimed to parse tag annotated text 
into BIO annotated text.




## Installation

To install the package just run:

```bash
pip install tag2bio
```
    
## Usage

```python

text = """
    My name is <name>John Doe</name>. and this is just an
    example for the demonstration in <country>Brazil</country>.
"""

tb = Tag2Bio(text)
parsed = tb.parse()

print(parsed)
```

### Output

```
My O 
name O 
is O 
John B-name
Doe I-name
. O 
and O 
this O 
is O 
just O 
an O 
example O 
for O 
the O 
demonstration O 
in O 
Brazil B-country
. O 
```

## Saving the output

```
output_path = './output.txt'
tb.save(output_path)

```
