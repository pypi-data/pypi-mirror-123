#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the ldict project.
#  Please respect the license - more about this in the section (*) below.
#
#  ldict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ldict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ldict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.

import re
from inspect import signature
from io import StringIO
from pprint import pprint
from typing import Callable

from decompyle3.main import decompile
from lange import AP, GP
from orjson import OPT_SORT_KEYS, dumps

from ldict.data import fhosh, removal_id
from ldict.exception import NoInputException, DependenceException, FunctionETypeException, NoReturnException, \
    BadOutput, InconsistentLange, MultipleIdsForFunction
from ldict.history import extend_history
from ldict.lazy import Lazy


def delete(d, clone, k):
    """
    >>> from ldict import Ø, setup
    >>> setup(history=True)  # Keep history of ids of all applied functions.
    >>> d = Ø >> {"x": 5, "y": 7}
    >>> d.show(colored=False)
    {
        "id": "I0_39c94b4dfbc7a8579ca1304eba25917204a5e",
        "ids": {
            "x": "Tz_d158c49297834fad67e6de7cdba3ea368aae4",
            "y": "Rs_92162dea64a7462725cac7dcee71b67669f69"
        },
        "x": 5,
        "y": 7
    }
    >>> d >>= {"x": None}  # Delete content by key
    >>> d.show(colored=False)
    {
        "id": "orh.lboHQhzNnrjrircOoPYzfk0000000000000y",
        "ids": {
            "x": "7jItH06N6TKPQ2ikAXqnlk38S69000000000000y",
            "y": "Rs_92162dea64a7462725cac7dcee71b67669f69"
        },
        "x": null,
        "y": 7
    }
    >>> from ldict import decolorize
    >>> decolorize(str(d.history)) == '{I0_39c94b4dfbc7a8579ca1304eba25917204a5e: {Tz_d158c49297834fad67e6de7cdba3ea368aae4, Rs_92162dea64a7462725cac7dcee71b67669f69}, --------------------...................x: None}'
    True

    Parameters
    ----------
    d
    clone
    k

    Returns
    -------

    """

    def f(**kwargs):
        return {k: None}

    f.hosh = d.identity * removal_id(d, k)
    f.input_fields = f.output_fields = [k]
    application(d, clone, f, {}, d.rnd)
    _ = clone[k]


def input_fields(f, previous_fields):
    """Extract input fields (and parameters, when default values are present).

    >>> input_fields(lambda x,y: {"z": x*y, "w": x+y}, {"x":None, "y":None})
    (['x', 'y'], {})
    >>> def f(x, y, a=[1,2,3,...,10], b=[1,2,4,...,32]):
    ...     return {
    ...         "z": a*x + b*y,
    ...         "w": x+y
    ...     }
    >>> input_fields(f, {"x":None, "y":None})
    (['x', 'y'], {'a': [1, 2, 3, Ellipsis, 10], 'b': [1, 2, 4, Ellipsis, 32]})

    Returns
    -------

    """
    parameters = {}
    if hasattr(f, "input_fields"):
        input = f.input_fields
        if hasattr(f, "parameters"):
            parameters = f.parameters
    else:
        pars = dict(signature(f).parameters)
        input = []
        if "kwargs" in pars:
            del pars["kwargs"]
        for k, v in pars.items():
            if v.default is v.empty:
                input.append(k)
            else:
                parameters[k] = v.default
    if not input and not parameters:
        raise NoInputException(f"Missing function input parameters.")
    for field in input:
        if field not in previous_fields:
            # TODO: stacktrace para apontar toda a cadeia de dependências, caso seja profunda
            # # TODO criar PartialDict qnd deps não existem ainda
            raise DependenceException(f"Function depends on inexistent field [{field}]. Current",
                                      list(previous_fields.keys())[2:])
    return input, parameters


def output_and_implicit_fields(f, parameters):
    """Extract output fields.

    https://stackoverflow.com/a/68753149/9681577

    >>> output_and_implicit_fields(lambda x,y: {"z": x*y, "w": x+y}, {"a":5})
    (['z', 'w'], [])
    >>> def f(x,y):
    ...     return {
    ...         "z": x*y,
    ...         "w": x+y
    ...     }
    >>> output_and_implicit_fields(f, ["a"])
    (['z', 'w'], [])

    Returns
    -------

    """
    if hasattr(f, "output_fields"):
        return f.output_fields, []
    out = StringIO()
    decompile(bytecode_version=(3, 8), co=f.__code__, out=out)
    ret = "".join([line for line in out.getvalue().split("\n") if not line.startswith("#")])
    if "return" not in ret:
        raise NoReturnException(f"Missing return statement:")
    dicts = re.findall("(?={)(.+?)(?<=})", ret)
    if len(dicts) != 1:
        raise BadOutput(
            "Cannot detect output fields, or missing dict (with proper pairs 'identifier'->result) as a return value.",
            dicts,
            ret,
        )
    explicit = re.findall(r"(?:[\"'])([a-zA-Z]+[a-zA-Z0-9]*)(?:[\"']):", dicts[0])
    implicit = re.findall(r"([a-zA-Z]+[a-zA-Z0-9]*):", dicts[0])
    explicit.extend(parameters[field] for field in implicit)
    if not explicit:
        pprint(dicts)
        pprint(ret)
        raise BadOutput("Cannot find output fields that are valid identifiers (or kwargs[...]):")

    implicit_input = re.findall(r"(?:kwargs\[)([a-zA-Z]+[a-zA-Z0-9_]*)(?:\])[^:]", dicts[0])
    return explicit, implicit_input


def substitute(hoshes, fields, uf):
    """
    >>> from ldict import ldict
    >>> a = ldict(x=3)
    >>> a.show(colored=False)
    {
        "id": "kr_4aee5c3bcac2c478be9901d57fd1ef8a9d002",
        "ids": {
            "x": "kr_4aee5c3bcac2c478be9901d57fd1ef8a9d002"
        },
        "x": 3
    }
    >>> a >>= (lambda x: {"x": x+2})
    >>> a.show(colored=False)
    {
        "id": "xzj-xzbxBldbiwP8yXDDSj12lSQYDDRQkGiQ6qJ8",
        "ids": {
            "x": "xzj-xzbxBldbiwP8yXDDSj12lSQYDDRQkGiQ6qJ8"
        },
        "x": "→(x)"
    }
    >>> a = ldict(x=3, y=5) >> (lambda x: {"x": x+2})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["y"]
    True
    >>> a = ldict(w=2, x=3) >> (lambda x: {"x": x+2})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["w"]
    True
    >>> a = ldict(w=2, x=3, z=1, y=4) >> (lambda x: {"x": x+2})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["w"] * a.hoshes["z"] * a.hoshes["y"]
    True
    >>> a = ldict(w=2, x=3, z=1, y=4) >> (lambda w,x,y: {"x": x+2, "a": w*x*y})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["a"] * a.hoshes["w"] * a.hoshes["z"] * a.hoshes["y"]
    True
    >>> a = ldict(w=2, x=3, z=1, y=4) >> (lambda w,x,y: {"x": x+2, "y": w*x*y})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["y"] * a.hoshes["w"] * a.hoshes["z"]
    True
    >>> a.show(colored=False)
    {
        "id": "uyEwj.W6933EIaQX8N3NzmjY4oEzkEFdqK4B1zjh",
        "ids": {
            "x": "8mmKFSlfac8iJypOJMng9SYoJ1qgmEFdqG4B1zji",
            "y": "ofEb.nRSYsUsgAnnyp4KYFovZaUOV6000sv....-",
            "w": "wI_a7efbd0e93a259465f280b47ba1310d928122",
            "z": "nv_4f699aa0d069410b23dcb462b64fe26acc2a2"
        },
        "x": "→(w x y)",
        "y": "→(w x y)",
        "w": 2,
        "z": 1
    }

    Parameters
    ----------
    uf
    hoshes
    fields

    Returns
    -------

    """
    others = uf.ø
    for k, v in hoshes.items():
        if k not in fields:
            others *= v
    return uf * ~others


def expand(lst):
    """Evaluate list representing A. or G. progression

    >>> expand([1,2,3,...,9])
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> expand([1,2,4,...,20])
    [1, 2, 4, 8, 16]

    Parameters
    ----------
    lst

    Returns
    -------

    """
    return list(list2progression(lst))


def list2progression(lst):
    """Convert list representing A. or G. progression to lange

    >>> list2progression([1,2,3,...,9])
    [1 2 .+. 9]
    >>> list2progression([1,2,4,...,16])
    [1 2 .*. 16]

    Parameters
    ----------
    lst

    Returns
    -------

    """
    # TODO move this to lange package
    diff1 = lst[1] - lst[0]
    diff2 = lst[2] - lst[1]
    ratio1 = lst[1] / lst[0]
    ratio2 = lst[2] / lst[1]
    newlst = [lst[0], lst[1], ..., lst[-1]]
    if diff1 == diff2:
        return AP(*newlst)
    elif ratio1 == ratio2:
        return GP(*newlst)
    else:
        raise InconsistentLange(f"Cannot identify whether this is a G. or A. progression: {lst}")


def application(self, clone, other: Callable, config, rnd):
    """
    >>> from ldict import ldict
    >>> from random import Random
    >>> d = ldict(x=3,y=4,z=5)
    >>> f = lambda x, y: {"w": x*y, "u": x/y, "y": x+y}
    >>> print(d >> f)
    {
        "id": "m4PwBcUvfzsOmE6wwcKr-RU04aO1HYiMhE166Amm",
        "ids": "jNfgTIKM6fniikhysPKB-zkmLDHKIYiMhA166Amn... +3 ...Vz_d467c65677734fad67e6de7cdba3ea368aae4",
        "w": "→(x y)",
        "u": "→(x y)",
        "y": "→(x y)",
        "x": 3,
        "z": 5
    }
    >>> f = lambda x, y, a=5, b=[1,2,3,...,10]: {"w": x*y, "u": x/y, "y": x+y}
    >>> print(d >> Random(0) >> f)
    {
        "id": "kxALR4v9RaAegi1R84KycANvWV.OOVeiSbr-HD0i",
        "ids": "lVSVzRr2mgCczqreGyt3tQViHZYvQVeiS7r-HD0j... +3 ...Vz_d467c65677734fad67e6de7cdba3ea368aae4",
        "w": "→(a b x y)",
        "u": "→(a b x y)",
        "y": "→(a b x y)",
        "x": 3,
        "z": 5
    }
    >>> from garoupa import ø
    >>> f = lambda x, y: {"w": x*y, "u": x/y, "y": x+y}
    >>> f.hosh = ø * "1234567890123456789012345678901234567890"
    >>> (d >> f).id == (d.hosh * "1234567890123456789012345678901234567890").id
    True

    Parameters
    ----------
    self
    clone
    other
    config
    rnd

    Returns
    -------

    """
    hosh = other.hosh if hasattr(other, "hosh") else fhosh(other, version=self.version)
    if hosh.etype != "ordered":
        raise FunctionETypeException(f"Functions are not allowed to have etype {hosh.etype}.")

    input, parameters = input_fields(other, self.data)

    # Handle parameterized function.
    if parameters:
        if hasattr(other, "hosh"):
            raise MultipleIdsForFunction(f"Function cannot have both hosh {other.hosh} and parameters.", parameters)
        for k, v in parameters.items():
            if k in config:
                parameters[k] = config[k]
            elif isinstance(v, list):
                parameters[k] = rnd.choice(expand(v))
        hosh *= dumps(parameters, option=OPT_SORT_KEYS)

    output, implicit_input = output_and_implicit_fields(other, parameters)

    deps = parameters
    deps.update({k: self.data[k] for k in input})
    deps.update({(k := parameters[par]): self.data[k] for par in implicit_input})

    u = clone.hosh
    uf = clone.hosh * hosh
    ufu_ = uf * ~u

    # Add triggers for future evaluation.
    clone.data = {"id": uf.id, "ids": {}}
    clone.hoshes = {}
    # clone.hashes = {}    atualiza hashes e blobs?
    clone.hosh = uf

    if len(output) == 1:
        field = output[0]
        clone.hoshes[field] = substitute(self.hoshes, [field], uf) if field in self.data else ufu_
        clone.data[field] = Lazy(field, other, deps)
        clone.data["ids"][field] = clone.hoshes[field].id
    else:
        acc = self.identity
        c = 0
        ufu__ = substitute(self.hoshes, output, uf)
        for i, field in enumerate(output):
            if i < len(output) - 1:
                field_hosh = ufu__ * (self.digits // 2 * "-" + str(c).rjust(self.digits // 2, "."))
                c += 1
                acc *= field_hosh
            else:
                field_hosh = ~acc * ufu__
            clone.hoshes[field] = field_hosh
            clone.data[field] = Lazy(field, other, deps)
            clone.data["ids"][field] = field_hosh.id

    for k, v in self.data.items():
        if k not in clone.data:
            clone.data[k] = v
            clone.data["ids"][k] = self.data["ids"][k]
    for k, v in self.hoshes.items():
        if k not in clone.hoshes:
            clone.hoshes[k] = v

    clone.last = extend_history(clone.history, clone.last, hosh)
    return clone
