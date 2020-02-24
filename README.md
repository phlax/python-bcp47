
[![Build Status](https://travis-ci.org/phlax/python-bcp47.svg?branch=master)](https://travis-ci.org/phlax/python-bcp47)
[![codecov](https://codecov.io/gh/phlax/python-bcp47/branch/master/graph/badge.svg)](https://codecov.io/gh/phlax/python-bcp47)


## python-bcp47


A validating parser for bcp47 language codes

Data taken from IANA http://www.iana.org/assignments/language-subtag-registry/language-subtag-registry

bcp47 spec https://tools.ietf.org/html/bcp47

useful reading: https://www.w3.org/International/articles/language-tags/index.en

`extension` and `private-use` tag types are not currently supported


### Python example

You can read the `languages`, `extlangs`, `scripts`, `variants`, `regions`, `grandfathereds`, and `redundants` language tag parts from `dicts` on the `bcp47` object.

They return `OrderedDicts` containing the IANA database information

```
>>> from bcp47 import bcp47

>>> list(bcp47["languages"].items())[:2]
[('aa', {'Subtag': 'aa', 'Description': ['Afar'], 'Added': '2005-10-16'}), ('ab', {'Subtag': 'ab', 'Description': ['Abkhazian'], 'Added': '2005-10-16', 'Suppress-Script': 'Cyrl'})]

>>>  list(bcp47["regions"].items())[:2]
[('AA', {'Subtag': 'AA', 'Description': ['Private use'], 'Added': '2005-10-16'}), ('AC', {'Subtag': 'AC', 'Description': ['Ascension Island'], 'Added': '2009-07-29'})]
`
```

You can create a language code tag as follows

```
>>> tag = bcp47(language="en", region="GB")
>>> tag
<bcp47.code.BCP47Code 'en-GB' />

>>> tag.language
'en'
>>> tag.region
'GB'
>>> str(tag)
'en-GB'

```

You can also pass a `string` or `list`  of `args` to create a tag

```
>>> bcp47("en-GB")
<bcp47.code.BCP47Code 'en-GB' />

>>> bcp47("en", "GB")
<bcp47.code.BCP47Code 'en-GB' />

```

Creating a tag with invalid or unrecognized parameters raises an `BCP47Exception`

```
>>> tag = bcp47(language="NOTALANGUAGE", region="GB")
Traceback (most recent call last):
...
BCP47Exception: Language 'NOTALANGUAGE' not recognized

>>> tag = bcp47("en-NOTAREGION")
Traceback (most recent call last):
...
BCP47Exception: Unrecognized tag part 'NOTAREGION'

```
