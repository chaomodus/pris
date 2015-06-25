# TODO

* Obviously this initially targets Python, but there's no reason it shouldn't work for
  other lanugages.

* There are probably tons of corner cases in JSON that this barfs on. It works with random
  JSON files I've thrown at it from my system, but I'm sure there are syntactically correct
  JSON files that break something. JSON compatibility is a nice to have, but not absolutely
  a deal breaker.

* An output routine to take a Python object and stream it out to a PRIS file - for now at
  least you can write a JSON file. Of course PRIS is mostly for humans to write comfortably
  so this isn't a huge priority.

* Support atom-style keys (unquoted alphanumerics that follow python symbol syntax), eg.
  [A-Za-z_][A-Za-z0-9_]*.

* Along those lines, support for heirarchical atom-style keys that introduce layering in
  the output dict (eg myobject.thing.deepkey).

* Basically if something annoys you in writing configuration files, we can try to address
  it in the format (as long as it maintains JSON-read compatibility).

* Implement ?include directive.

* Make parser validate files and not just stop when it encounters a syntax error (my
  inexperience with Grako is palpable).
