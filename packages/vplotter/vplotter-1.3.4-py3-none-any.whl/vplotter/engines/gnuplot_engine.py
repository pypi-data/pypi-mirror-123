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

# TODO:
    # Experimental
    # pandas
    # extend to several line at once
    # ...

from .bot_engine   import BotEngine
from dataclasses   import dataclass, field

try:
    from pygnuplot import gnuplot
    from pygnuplot.gnuplot import Gnuplot
except Exception as e:
    Gnuplot = object
    print(f"GNUPLOT is not available: {e}")

import pandas as pd
import numpy  as np

class GnuplotEngineError(Exception):
    pass

@dataclass
class GnuplotEngine(BotEngine):
    internal_name : str     = "[GnuplotEngine]"
    g             : Gnuplot = None

    def __post_init__(self):
        self.g = gnuplot.Gnuplot(log=False, terminal = 'dumb size 79, 24 aspect 2, 1 mono')
        self.g.set(
            title  = f"'{self.title}'",
            xlabel = f"'{self.xname}'",
            ylabel = f"'{self.yname}'",
            )
        if self.xlog: self.g.set("logscale x")
        if self.ylog: self.g.set("logscale y")

        # X
        if self.xmin.lower() != "auto" or self.xmax.lower() != "auto":
            # drop value
            xmin = "" if self.xmin == "Auto" else str(self.xmin)
            xmax = "" if self.xmax == "Auto" else str(self.xmax)
            self.g.set(f"xrange [{str(xmin)}:{str(xmax)}")
        # y
        if self.ymin.lower() != "auto" or self.ymax.lower() != "auto":
            # drop value
            ymin = "" if self.ymin == "Auto" else str(self.ymin)
            ymax = "" if self.ymax == "Auto" else str(self.ymax)
            self.g.set(f"yrange [{str(ymin)}:{str(ymax)}")

    def plot(self, x, y, key_name_f='', key_name="", **kwargs):
        _x, _y, _xerr, _yerr = None, None, None, None,
        if len(np.shape(y)) == 2: _y = y[0]; _yerr = y[1]
        else:                     _y = y
        if len(np.shape(x)) == 2: _x = x[0]; _xerr = x[1]
        else:                     _x = x

        df = pd.DataFrame(data = {
            'col1': _x,
            'col2': _xerr,
            'col3': _y,
            'col4': _yerr,
            }
        )
        using_str = ""
        if _x is not None: using_str += "1"
        if _y is not None: using_str += ":3"
        if _xerr is not None and _yerr is not None:
            raise GnuplotEngineError(NotImplemented)

        if _x is not None and _y is not None:
            using_str = "1:2"
            if self.plotLine: using_str += " with line"
        if _x is not None and _y is not None and _yerr is not None:
            using_str = "1:3:4 with yerr"

        if key_name_f: key = self.name_converter(key_name_f)
        else:          key = key_name

        self.g.plot_data(df, f"using {using_str} t '{key}' ")

