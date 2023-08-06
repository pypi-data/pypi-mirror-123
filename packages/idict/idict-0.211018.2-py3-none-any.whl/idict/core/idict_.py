#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the idict project.
#  Please respect the license - more about this in the section (*) below.
#
#  idict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  idict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with idict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
#
import operator
from functools import reduce
from random import Random
from typing import Dict, TypeVar, Union, Callable

from garoupa import ø40
from ldict.core.base import AbstractMutableLazyDict
from ldict.exception import WrongKeyType
from ldict.parameter.base.abslet import AbstractLet

from idict.parameter.ifunctionspace import iFunctionSpace

VT = TypeVar("VT")


class Idict(AbstractMutableLazyDict):
    """Mutable lazy identified dict for serializable (picklable) pairs str->value

    Usage:

    >>> from idict import idict
    >>> print(idict())
    {
        "id": "0000000000000000000000000000000000000000",
        "ids": {}
    }
    >>> d = idict(x=5, y=3)
    >>> print(d)
    {
        "x": 5,
        "y": 3,
        "id": "Xt_6cc13095bc5b4c671270fbe8ec313568a8b35",
        "ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "XB_1cba4912b6826191bcc15ebde8f1b960282cd"
        }
    }
    >>> d["y"]
    3
    >>> print(idict(x=123123, y=88))
    {
        "x": 123123,
        "y": 88,
        "id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "ids": {
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> print(idict(y=88, x=123123))
    {
        "y": 88,
        "x": 123123,
        "id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "ids": {
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660",
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e"
        }
    }
    >>> d = idict(x=123123, y=88)
    >>> d2 = d >> (lambda x: {"z": x**2})
    >>> d2.ids
    {'z': '.JXmafqx65TZ-laengA5qxtk1fUJBi6bgQpYHIM8', 'x': '4W_3331a1c01e3e27831cf08b7bde9b865db7b2e', 'y': '9X_c8cb257a04eba75c381df365a1e7f7e2dc660'}
    >>> d2.hosh == d2.identity * d2.ids["z"] * d2.ids["x"] * d2.ids["y"]
    True
    >>> e = d2 >> (lambda x,y: {"w": x/y})
    >>> print(e)
    {
        "w": "→(x y)",
        "z": "→(x)",
        "x": 123123,
        "y": 88,
        "id": "96PdbhpKgueRWa.LSQWcSSbr.ZMZsuLzkF84sOwe",
        "ids": {
            "w": "1--sDMlN-GuH4FUXhvPWNkyHmTOfTbFo4RK7M5M5",
            "z": ".JXmafqx65TZ-laengA5qxtk1fUJBi6bgQpYHIM8",
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> a = d >> (lambda x: {"z": x**2}) >> (lambda x, y: {"w": x/y})
    >>> b = d >> (lambda x, y: {"w": x/y}) >> (lambda x: {"z": x**2})
    >>> dic = d.asdict  # Converting to dict
    >>> dic
    {'x': 123123, 'y': 88, 'id': 'dR_5b58200b12d6f162541e09c570838ef5a429e', 'ids': {'x': '4W_3331a1c01e3e27831cf08b7bde9b865db7b2e', 'y': '9X_c8cb257a04eba75c381df365a1e7f7e2dc660'}}
    >>> d2 = idict(dic)  # Reconstructing from a dict
    >>> print(d2)
    {
        "x": 123123,
        "y": 88,
        "id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "ids": {
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> d == d2
    True
    >>> from idict import Ø
    >>> d = Ø >> {"x": "more content"}
    >>> print(d)
    {
        "x": "more content",
        "id": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff",
        "ids": {
            "x": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff"
        }
    }
    >>> d = idict() >> {"x": "more content"}
    >>> print(d)
    {
        "x": "more content",
        "id": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff",
        "ids": {
            "x": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff"
        }
    }
    >>> e.ids.keys()
    dict_keys(['w', 'z', 'x', 'y'])
    >>> del e["z"]
    >>> print(e)
    {
        "w": "→(x y)",
        "x": 123123,
        "y": 88,
        "id": "GAgXkH4fTORLS1ijp.SQg-6gRa0gTbFo4RK7M5M5",
        "ids": {
            "w": "1--sDMlN-GuH4FUXhvPWNkyHmTOfTbFo4RK7M5M5",
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> e.hosh == e.identity * e.ids["w"] * e.ids["x"] * e.ids["y"]
    True
    >>> e["x"] = 77
    >>> print(e)
    {
        "w": "→(x y)",
        "x": 77,
        "y": 88,
        "id": "aGMqf9GsQ.SBkKYKE-l21EjPX4YfTbFo4RK7M5M5",
        "ids": {
            "w": "1--sDMlN-GuH4FUXhvPWNkyHmTOfTbFo4RK7M5M5",
            "x": "JF_093a985add7d5e2d319c2662db9ae954648b4",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    """

    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, id=None, ids=None, rnd=None, identity=ø40, _cloned=None, **kwargs):
        self.identity = identity
        from idict.frozenidentifieddict import FrozenIdentifiedDict
        self.frozen: FrozenIdentifiedDict = FrozenIdentifiedDict(_dictionary, id, ids, rnd, identity, _cloned, **kwargs)

    @property
    def hosh(self):
        return self.frozen.hosh

    @property
    def blobs(self):
        return self.frozen.blobs

    @property
    def hashes(self):
        return self.frozen.hashes

    @property
    def hoshes(self):
        return self.frozen.hoshes

    def __delitem__(self, key):
        if not isinstance(key, str):
            raise WrongKeyType(f"Key must be string, not {type(key)}.", key)
        data, blobs, hashes, hoshes = self.data.copy(), self.blobs.copy(), self.hashes.copy(), self.hoshes.copy()
        del data[key]
        for coll in [blobs, hashes, hoshes]:
            if key in coll:
                del coll[key]
        hosh = reduce(operator.mul, [self.identity] + list(hoshes.values()))
        self.frozen = self.frozen.clone(data, _cloned=dict(blobs=blobs, hashes=hashes, hoshes=hoshes, hosh=hosh))

    def __getattr__(self, item):
        return self.frozen[item]

    def __repr__(self):
        return repr(self.frozen)

    def __str__(self):
        return str(self.frozen)

    def evaluate(self):
        """
        >>> from idict import idict
        >>> f = lambda x: {"y": x+2}
        >>> d = idict(x=3)
        >>> a = d >> f
        >>> print(a)
        {
            "y": "→(x)",
            "x": 3,
            "id": "tFkvrmyHlXSnstVFIFktJjD7K91yW4AU0sYuSnwe",
            "ids": {
                "y": "BZz1P5xA5r0gfAqOtHySEb.m0HTxW4AU0sYuSnwe",
                "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
            }
        }
        >>> a.evaluate()
        >>> print(a)
        {
            "y": 5,
            "x": 3,
            "id": "tFkvrmyHlXSnstVFIFktJjD7K91yW4AU0sYuSnwe",
            "ids": {
                "y": "BZz1P5xA5r0gfAqOtHySEb.m0HTxW4AU0sYuSnwe",
                "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
            }
        }
        """
        self.frozen.evaluate()

    @property
    def asdict(self):
        """
        >>> from idict import idict
        >>> d = idict(x=7, y=8)
        >>> e = idict(x=7, y=8, d=d)
        >>> e.asdict
        {'x': 7, 'y': 8, 'd': {'x': 7, 'y': 8, 'id': 'sl_e71f88df59515edb262b26ea29b4c6470e3a7', 'ids': {'x': 'lX_9e55978592eeb1caf8778e34d26f5fd4cc8c8', 'y': '6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde'}}, 'id': '5F_a0d66f8882d3b43a5c4676da42798d242c74f', 'ids': {'x': 'lX_9e55978592eeb1caf8778e34d26f5fd4cc8c8', 'y': '6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde', 'd': 'Fj_7dc836b829c2eb5e262b00ef19b4c6fc1e3a7'}}
        >>> from idict.core.identification import key2id
        >>> d.hosh == e.hoshes["d"]
        False
        >>> d.hosh == e.hoshes["d"] // key2id("d", e.hosh.digits)
        True
        """
        return self.frozen.asdict

    def clone(self, data=None, rnd=None, _cloned=None):
        cloned_internals = _cloned or dict(blobs=self.blobs, hashes=self.hashes, hoshes=self.hoshes, hosh=self.hosh)
        return Idict(data or self.data, rnd=rnd or self.rnd, identity=self.identity, _cloned=cloned_internals)

    def __rrshift__(self, other: Union[Dict, Callable, iFunctionSpace]):
        """
        >>> print({"x": 5} >> Idict(y=2))
        {
            "x": 5,
            "y": 2,
            "id": "o8_4c07d34b8963338a275e43bfcac9c37f125cc",
            "ids": {
                "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
                "y": "pg_7d1eecc7838558a4c1bf9584d68a487791c45"
            }
        }
        >>> print((lambda x: {"y": 5*x}) >> Idict(y=2))
        «λ × {
            "y": 2,
            "id": "pg_7d1eecc7838558a4c1bf9584d68a487791c45",
            "ids": {
                "y": "pg_7d1eecc7838558a4c1bf9584d68a487791c45"
            }
        }»
        """
        if isinstance(other, Dict):
            return Idict(other) >> self
        if callable(other):
            return iFunctionSpace(other, self)
        return NotImplemented  # pragma: no cover

    def __rshift__(self, other: Union[Dict, 'Idict', Callable, AbstractLet, iFunctionSpace, Random]):
        """
        >>> d = Idict(x=2) >> (lambda x: {"y": 2 * x})
        >>> d.ids
        {'y': 'zJmLy1B8VQU8.Kji0iqU0zIrDWpWqcXxhrGWdepm', 'x': 'og_0f0d4c16437fb2a4c1bff594d68a486791c45'}
        """
        from idict import iEmpty
        if isinstance(other, iEmpty):
            return self
        clone = Idict(identity=self.identity)
        clone.frozen = self.frozen >> other
        return clone
        # if isinstance(other, AbstractLazyDict):
        #     return self.clone(handle_dict(self.frozen.data, other, other.rnd), rnd=other.rnd)
        # if isinstance(other, Dict):
        #     return self.clone(handle_dict(self.frozen.data, other, self.rnd))
        # if isinstance(other, iFunctionSpace):
        #     return reduce(operator.rshift, (self,) + other.functions)
        # if callable(other) or isinstance(other, Let):
        #     return NotImplemented

    def __ne__(self, other):
        """
        >>> from idict.frozenidentifieddict import FrozenIdentifiedDict
        >>> {"x": 5} == Idict({"x": 5})
        True
        >>> {"w": 5} == Idict({"x": 5})
        False
        >>> {"x": 4} == Idict({"x": 5})
        False
        >>> {"x": 5} == FrozenIdentifiedDict({"x": 5})
        True
        >>> {"w": 5} == FrozenIdentifiedDict({"x": 5})
        False
        >>> {"x": 4} == FrozenIdentifiedDict({"x": 5})
        False
        """
        return not (self == other)

    def __eq__(self, other):
        return self.frozen == other

    def show(self, colored=True):
        self.frozen.show(colored)
