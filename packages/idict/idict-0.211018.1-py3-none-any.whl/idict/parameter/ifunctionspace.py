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
from ldict.parameter.base.absfunctionspace import AbstractFunctionSpace


class iFunctionSpace(AbstractFunctionSpace):
    """Aglutination of steps for future application

    >>> from idict import idict, empty
    >>> print(empty >> iFunctionSpace())
    {
        "id": "0000000000000000000000000000000000000000",
        "ids": {}
    }
    >>> fs = iFunctionSpace() >> empty
    >>> fs >>= {"x": 5}
    >>> fs
    «{
        "x": 5,
        "id": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
        }
    }»
    >>> print(idict(y=7) >> fs)
    {
        "y": 7,
        "x": 5,
        "id": "mP_2d615fd34f97ac906e162c6fc6aedadc4d140",
        "ids": {
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
        }
    }
    >>> fs >>= idict(y=7)
    >>> fs
    «{
        "x": 5,
        "id": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
        }
    } × {
        "y": 7,
        "id": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
        "ids": {
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }»
    >>> fs >>= lambda x,y: {"z": x*y}
    >>> fs
    «{
        "x": 5,
        "id": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
        }
    } × {
        "y": 7,
        "id": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
        "ids": {
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    } × λ»
    """

    def __init__(self, *args):
        from idict.iempty import iEmpty
        from idict.core.idict_ import Idict
        super().__init__(args, dict_type=Idict, empty_type=iEmpty)
