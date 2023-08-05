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

from dataclasses             import dataclass, field
from typing                  import Any, Union
from .engines.veusz_engine   import VeuszEngine
from .engines.gnuplot_engine import GnuplotEngine
import os, sys, re

VEUSZ   = True
GNUPLOT = True
try: import veusz.embed as veusz
except: VEUSZ   = False
try: from pygnuplot import gnuplot
except: GNUPLOT = False
if not VEUSZ and not GNUPLOT: print("No plotters available. Aborting."); sys.exit(1)

@dataclass
class Plotter:
    __version__    : str                               = "1.3.4"
    internal_name  : str                               = "[Plotter]"
    hidden         : bool                              = False
    engine         : str                               = "veusz"
    plotter_engine : Union[VeuszEngine, GnuplotEngine] = None

    title         : str    = field(default="Notitle")
    showkey       : bool   = True
    plotLine      : bool   = True
    keyFontSize   : int    = 14
    xname         : str    = "x"
    yname         : str    = "y"
    xlog          : bool   = False
    ylog          : bool   = False
    ymin          : str    = "Auto"
    ymax          : str    = "Auto"
    xmin          : str    = "Auto"
    xmax          : str    = "Auto"

    # Veusz dependent
    pages_info    : dict   = field(default_factory=dict)
    keyBorderHide : bool   = True
    transparency  : float  = 50.0

    def __post_init__(self):
        if self.engine.lower() == "veusz" and VEUSZ:
            self.plotter_engine = VeuszEngine(
                hidden        = self.hidden,
                title         = self.title,
                pages_info    = self.pages_info,
                showkey       = self.showkey,
                keyFontSize   = self.keyFontSize,
                keyBorderHide = self.keyBorderHide,
                plotLine      = self.plotLine,
                xname         = self.xname,
                yname         = self.yname,
                ylog          = self.ylog,
                xlog          = self.xlog,
                ymin          = self.ymin,
                ymax          = self.ymax,
                xmin          = self.xmin,
                xmax          = self.xmax,
                transparency  = self.transparency
            )
        if self.engine.lower() == "gnuplot" and GNUPLOT:
            self.plotter_engine = GnuplotEngine(
                hidden        = self.hidden,
                title         = self.title,
                showkey       = self.showkey,
                plotLine      = self.plotLine,
                xname         = self.xname,
                yname         = self.yname,
                ylog          = self.ylog,
                xlog          = self.xlog,
                ymin          = self.ymin,
                ymax          = self.ymax,
                xmin          = self.xmin,
                xmax          = self.xmax,
            )

        print(f"===> [Plotter: (engine:{self.engine})] is initialized [v.{self.__version__}]")

    def plot(self, x, y, **kwargs):
        self.plotter_engine.plot(x=x, y=y, **kwargs)

    def export(self, **kwargs):
        if type(self.plotter_engine) == VeuszEngine:
            self.plotter_engine.export(**kwargs)

    def save(self, filename=None):
        if type(self.plotter_engine) == VeuszEngine:
            self.plotter_engine.save(filename=filename)
        else:
            print("Saving is not implemented for this engine.")


#
if __name__ == "__main__":
    p = Plotter(
        title= "My_Mega_Title",
        pages_info={
            "page1" : {
                "xname" : "page1_x",  "yname" : "page1_y",
                "xlog"  : False, "ylog" : False,
                "ymin" : "Auto", "ymax" : "Auto",
                "xmin" : "Auto", "xmax" : "Auto",
                },
           "page2" :{
                "xname" : "page2_x",  "yname" : "page2_y",
                "xlog"  : True, "ylog" : True,
                }
        }
    )

    p.plot(x=[1,1,2], y=[1,2,3], key_name="first", page="page1")
    p.plot(x=[0,0,6], y=[1,2,3], key_name="second", page="page1")

    p.plot(x=[i**2 for i in range(10)], y=[i**3 for i in range(10)], key_name="first", page="page2")
    p.plot(x=[1,3,7], y=[6,2,2], key_name="second", page="page2")

    p_one_page = Plotter(xname="A", yname="B", xlog=True, ylog=False, )
    p_one_page.plot(x=[i for i in range(100)], y=[j for j in range(100)], key_name_f="MyName")
    p_one_page.plot(x=[i for i in range(100)], y=[j for j in range(100)], key_name_f="MyName1")
    p_one_page.plot(x=[i for i in range(100)], y=[j for j in range(100)], key_name="MyName1")
