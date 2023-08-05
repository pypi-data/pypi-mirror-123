##*
## MIT License
##
## Plotter - Copyright (c) 2020-2021 Aleksandr Kazakov, Varvara Prokacheva
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
##*

from dataclasses    import dataclass, field
from .plotter_utils import get_label
import sys, re, os

try:    from storer import Storer
except: print("Storer is not available. Aborting..."); sys.exit(1)


@dataclass
class BotEngine:
    hidden        : bool   = False
    internal_name : str    = "[BotEngine]"
    storer        : Storer = None

    # Veusz_engine specific
    title         : str    = field(default="Notitle")
    pages_info    : dict   = field(default_factory=dict)
    #
    showkey       : bool   = True
    keyBorderHide : bool   = True
    plotLine      : bool   = True
    #
    xname         : str    = "x"
    yname         : str    = "y"
    xlog          : bool   = False
    ylog          : bool   = False
    ymin          : str    = "Auto"
    ymax          : str    = "Auto"
    xmin          : str    = "Auto"
    xmax          : str    = "Auto"
    #
    transparency  : float  = 50.0

    def __post_init__(self):
        ...

    def name_converter(self: object, name: str) -> str:
        if name.find(" ") != -1: print("Please, use notation: `varX_var2Y.YY_var3ZZ.Z`")
        name = name.replace(" ", "").replace("=","")

        res = []
        parts = name.split("_")

        for part in parts:
            if part[0:4] == "time": res.append(part); continue
            m = re.search(r"[+-]?[\d.]*\d+", part)
            if m:
                try: symbol = get_label(part[:m.start()])
                except KeyError: symbol = part[:m.start()]
                #part_ = symbol + "_{" + m.string[m.start():m.end()] + "}"
                part_ = symbol + " = " + m.string[m.start():m.end()]
            else:
                #part_ = part
                try: part_ = get_label(part)
                except KeyError: part_ = part
            res.append(part_)

        return " ".join(res)

    def plot(self, x, y, key_name_f='', key_name="", **kwargs):
        ...

