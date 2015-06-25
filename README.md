# PRIS - Painless Representation of Information Store

Do you HATE YAML 'cuz it's like all whitespacey and stuff?

Does JSON ANNOY you because of its super sensitive syntax and
the lack of comments?

Are you AFRAID of XML because of bracket tax and all of the
ridiculous hacks that can be done to parsers?

Are you tired of rolling a new configuration file format every
time you need one?

PRIS is the solution!

PRIS IS:

* A human-writable object description format
* Completely UTF-8
* Super forgiving
* JSON compatible (well the parser can load JSON files)
* Never again have to remember nil/null/void, true/t/TRUE, etc.
* Represented as a top-level ordered dictionary (similar to how
  you put such a dictionary in a JSON file).
* Fully able to describe any dictionary as you would in Python

Sounds good?

## Overall Syntax

### Directives

Lines that start with ? are processing directives.

There are these directives defined:

* `?nofold` - Instructs the processor not to fold a top-level single object into the top level namespace. Under normal
  circumstances, a JSON file containing one dictionary is folded into the top-level namespace, this prevents that.
* `?reset` - Under normal circumstances, the processor assigns a sequential numeric key to each unlabeled value in the
  file. This resets that counter to 0 at the spot that it occurs. Useful for the `?include` directive.
* `?include "file"` - Include the contents of specified `file` at this position.
* `?encoding "encoding"` - Specify that this content should be seen as `encoding`. "utf-8" is the only supported value
  (and will always be the default).

### Top-level syntax

Objects are defined by an optional key and a value.

Values can be one of:

* Lists, denoted by [] or () containining a comma-separated list of values.
* Dictionaries, denoted by {} containing a comma-separated list of key-value pairs.
* Strings, enclosed with " or ', containing arbitrary strings, with pythonic escape characters.
* Numbers, either decimal, hex or scientific (73, 1.2, 0xDEADBEEF and 1.7e23 are valid numbers).
* Bools which are barewords in one of `true`, `false`, `True`, `False`, `TRUE`, `FALSE`, `t`, or `f`
* Null values which are {}, [], () or `void`, `nil`, `None`, `null`, or `NULL`

NOTE! Commas in sequence values are optional!

Keys are either:

* Strings (enquoted)
* Simple numbers in the form of one or more decimal digits
* Bools

Keys are separated from values by a `=` or a `:`.

## Example PRIS file

This example is something I just whipped together. It doesn't show the full
breadth of the language, but it does demonstrate a heirarchical configuration
file as would be typical of its use.


```
# this is a configuration file for the nuclear reactor.

'metadata':{
'name'='Reactor1'
'noExplode'=True
}

'rods':[
{'name'='rod1',
 'position'='up',
 'origin'='Z111E-3',
 'uuid'=(0x2602ba42, 0x1efd, 0x4e19, 0x9293, 0x9920843bc617)
}

{'name'='rod2',
 'position'='up',
 'origin'='Z111E-7',
 'uuid'=(0x9cac03e2, 0x0f08, 0x4337, 0x9042, 0x334d36ae4bb5)
}
]
```

Parsing this file returns an ordered dict containing:

```
metadata = OrderedDict([(u'name', u'Reactor1'),
                        (u'noExplode', True)])
rods = OrderedDict([(0, OrderedDict([(u'name', u'rod1'),
                                     (u'position', u'up'),
                                     (u'origin', u'Z111E-3'),
                                     (u'uuid', OrderedDict([(0, 637712962),
                                                            (1, 7933),
                                                            (2, 19993),
                                                            (3, 37523),
                                                            (4, 168364936513047)]))])),
                     (1, OrderedDict([(u'name', u'rod2'),
                                      (u'position', u'up'),
                                      (u'origin', u'Z111E-7'),
                                      (u'uuid', OrderedDict([(0, 2628518882),
                                                             (1, 3848),
                                                             (2, 17207),
                                                             (3, 36930),
                                                             (4, 56406722890677)]))]))])
```

It should be noted that this isn't far off from a JSON file, the main difference being that it does't occur inside of {}s, we
use = and : interchangably (in semantically appropriate ways in this case) and we leae off commas randomly (and there are comments).
These minor QOL things make it more convenient for humans to write. See the TODO for additional QOLs that would make this even
nicer to write.
