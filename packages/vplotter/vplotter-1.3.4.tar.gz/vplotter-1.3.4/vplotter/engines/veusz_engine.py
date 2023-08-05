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

from .bot_engine    import BotEngine
from .plotter_utils import get_line_color, get_line_type, get_marker_type
from dataclasses    import dataclass, field
from typing         import Any, List, Union

import numpy as np
import os, sys, re

try:
    import veusz.embed as veusz
    from veusz.embed   import Embedded
except Exception as e:
    Embedded = object
    print(f"Veusz is not available: {e}")

try:    from storer import Storer
except: print("Storer is not available. Aborting..."); sys.exit(1)

class VeuszEngineError(Exception):
    pass

@dataclass
class VeuszEngine(BotEngine):
    internal_name : str    = "[VeuszEngine]"
    #
    g             : Embedded = None
    title         : str      = field(default="Notitle")
    pages_info    : dict     = field(default_factory=dict)
    _xy           : Any      = None # flag for animation
    #
    showkey       : bool     = True
    keyBorderHide : bool     = True
    keyFontSize   : int      = 14
    plotLine      : bool     = True
    #
    xname         : str      = "x"
    yname         : str      = "y"
    xlog          : bool     = False
    ylog          : bool     = False
    ymin          : str      = "Auto"
    ymax          : str      = "Auto"
    xmin          : str      = "Auto"
    xmax          : str      = "Auto"
    #
    transparency   : float    = 50.0

    def __post_init__(self):
       self.storer = Storer(exit_dump=False)

       self.g = veusz.Embedded(name=self.title, hidden=self.hidden)
       self.g.EnableToolbar()
       self.init_pages()

    def _init(self, page_name=""):
        # creating initial values for plotting per page.
        self.storer.put(what="xname", name=page_name+"/xname")
        self.storer.put(what="yname", name=page_name+"/yname")
        self.storer.put(what=False,   name=page_name+"/xlog")
        self.storer.put(what=False,   name=page_name+"/ylog")
        self.storer.put(what="Auto",  name=page_name+"/xmin")
        self.storer.put(what="Auto",  name=page_name+"/xmax")
        self.storer.put(what="Auto",  name=page_name+"/ymin")
        self.storer.put(what="Auto",  name=page_name+"/ymax")

    def init_pages(self):
        if self.pages_info:
                for page in self.pages_info:
                    self._init(page_name=page)
                    for prop in self.pages_info[page]:
                        self.storer.put(what=self.pages_info[page][prop] , name=page+"/"+prop)
        else:
            self._init(page_name="page1")
            self.storer.put(what=self.xname , name="page1/xname")
            self.storer.put(what=self.yname , name="page1/yname")

            self.storer.put(what=self.xlog  , name="page1/xlog")
            self.storer.put(what=self.ylog  , name="page1/ylog")

            self.storer.put(what=self.xmin  , name="page1/xmin")
            self.storer.put(what=self.xmax  , name="page1/xmax")

            self.storer.put(what=self.ymax  , name="page1/ymax")
            self.storer.put(what=self.ymin  , name="page1/ymin")


    def get_page(self, name="page1"):

        try:
            self.page = self.g.Root[name]
            _num_lines  = self.storer.get(name=name+ "/_num_lines")
            __num_lines = self.storer.get(name=name+"/__num_lines")  # if save_previous_state is applied
        except KeyError:
            self.page = self.g.Root.Add("page")
            self.page.Rename(name)
            __num_lines = 1; _num_lines = 1
            self.storer.put(what=_num_lines, name=name+ "/_num_lines")
            self.storer.put(what=__num_lines, name=name+ "/__num_lines")

        self.page.width.val = '15cm'
        self.page.height.val = '10cm'

        try:    self.graph = self.g.Root[name + '/graph1']
        except: self.graph = self.page.Add('graph')

        try:
            # key exist
            self.key = self.g.Root[name + "/graph1/key1"]
        except:
            if self.showkey:
                self.graph.Add('key')
                self.graph.key1.Border.hide.val = self.keyBorderHide
                self.graph.key1.Text.size.val   = f"{str(self.keyFontSize)}pt"

        return _num_lines, __num_lines

    def plot(
        self,
        x                  : List,
        y                  : List,
        key_name_f         : str             = "",
        key_name           : str             = "",
        markersize         : str             = "2.5pt",
        plotLine           : bool            = True,
        color_num          : Union[str, int] = "auto",
        marker_type        : Union[str, int] = "auto",
        line_type          : Union[str, int] = "auto",
        save_previous_state: bool            = False,
        animation          : bool            = False,
        errorStyle         : str             = None,
        internal_text      : str             = "",
        page               : str             = "page1",
        ):

        _num_lines, __num_lines = self.get_page(name=page)

        if animation:
            color_num = _num_lines
            line_type = _num_lines
            save_previous_state = True
            xy = self._xy

        if save_previous_state: _num_lines -= 1

        if color_num == "auto": color_num = _num_lines
        if line_type == "auto": line_type = _num_lines

        if not animation:
            x_dataname = self.xname + str(_num_lines) + str(save_previous_state) + str(__num_lines) + str(page)
            y_dataname = self.yname + str(_num_lines) + str(save_previous_state) + str(__num_lines) + str(page)
        else:
            x_dataname = self.xname + str(_num_lines) + str(save_previous_state) + str(page)
            y_dataname = self.yname + str(_num_lines) + str(save_previous_state) + str(page)

        x_dataname += internal_text
        y_dataname += internal_text

        if len(np.shape(x)) == 2:
            x_arr = np.array(x)
            x_data, x_data_err = x_arr[:,0], x[:,1]
            self.g.SetData(x_dataname, x_data, symerr=x_data_err)
        else:
            x_arr = np.array(x)
            x_data = x_arr
            self.g.SetData(x_dataname, x_data)

        if len(np.shape(y)) == 2:
            y_arr = np.array(y)
            y_data, y_data_err = y_arr[:,0], y_arr[:,1]
            self.g.SetData(y_dataname, y_data, symerr=y_data_err)
        else:
            y_arr = np.array(y)
            y_data = y_arr
            self.g.SetData(y_dataname, y_data)

        # self.graph = self.g.Root[name + '/graph1']
        if animation:
            if not self._xy: self._xy = xy = self.g.Root[page + '/graph1'].Add('xy')
        else: xy = self.g.Root[page + '/graph1'].Add('xy')

        # nn.plotter_progress.g.Root.xyz_file.graph1.xy1.Clone(nn.plotter_progress.g.Root.xyz_file.graph1, 'xy7')
        xy.xData.val = x_dataname
        xy.yData.val = y_dataname
        if marker_type != "auto": xy.marker.val = get_marker_type(marker_type)
        else: xy.marker.val = get_marker_type(line_type)

        if color_num % 2: xy.MarkerFill.color.val = get_line_color(color_num)
        else: xy.MarkerFill.color.val = 'white'

        xy.MarkerLine.color.val = get_line_color(color_num)
        xy.markerSize.val     = markersize
        xy.PlotLine.width.val = '1pt'
        xy.PlotLine.style.val = get_line_type(line_type)
        xy.PlotLine.color.val = get_line_color(color_num)
        xy.PlotLine.hide.val  = not plotLine

        if errorStyle:
            xy.errorStyle.val             = errorStyle
            xy.FillBelow.color.val        = get_line_color(color_num)
            xy.FillBelow.transparency.val = self.transparency
            xy.FillAbove.color.val        = get_line_color(color_num)
            xy.FillAbove.transparency.val = self.transparency

            #ErrorBarLine/style
            xy.ErrorBarLine.color.val = get_line_type(line_type)
            xy.ErrorBarLine.style.val = get_line_type(line_type)
        else:
            xy.errorStyle.val = 'none'

        xy.ErrorBarLine.width.val = '1pt'
        xy.ErrorBarLine.color.val = get_line_color(color_num)
        if self.showkey and key_name_f: xy.key.val = self.name_converter(key_name_f)
        if self.showkey and key_name: xy.key.val = key_name

        x_axis = self.graph.x
        y_axis = self.graph.y

        x_axis.label.val = self.storer.get(page+"/xname") # self.xname
        y_axis.label.val = self.storer.get(page+"/yname") # self.yname

        x_axis.log.val = self.storer.get(page+"/xlog") # self.xlog
        y_axis.log.val = self.storer.get(page+"/ylog") # self.ylog

        x_axis.min.val = self.storer.get(page+"/xmin") # self.xmin
        x_axis.max.val = self.storer.get(page+"/xmax") # self.xmax

        y_axis.min.val = self.storer.get(page+"/ymin") # self.ymin
        y_axis.max.val = self.storer.get(page+"/ymax") # self.ymax

        _num_lines  += 1
        __num_lines += 1
        self.storer.put(_num_lines, name=page+ "/_num_lines")
        self.storer.put(__num_lines, name=page+ "/__num_lines")

    def export(self, filename:str = "output.pdf", extension:str = "pdf", color:bool = True, page:int = 0, dpi:int = 100, antialias:bool = True, quality:int = 85, backcolor:str = '#ffffff00', pdfdpi:int = 150, svgtextastext:bool = False):
        if not filename or not extension:
            print(f"{self.internal_name} You have to specify filename and extension!")
            print(f"{self.internal_name} For example: filename='my_amazing_figure', extension='pdf'")
            print(f"{self.internal_name}              color=True, extension='pdf', quality='85', pdfdpi='150'")
            print(f"{self.internal_name} Available extensions: [pdf]/[eps]/[ps]/[svg]/[jpg]/[jpeg]/[bmp]/[png]")
        else: self.g.Export(filename, color=color, page=page, dpi=dpi, antialias=antialias, quality=quality, backcolor=backcolor, pdfdpi=pdfdpi, svgtextastext=svgtextastext)

    def save(self, filename=None):
        if not filename:
            print(f"{self.internal_name} You have to specify filename! [Labels from Y and X will be added automatically]")
        else:
            if filename.find(".") != -1 or filename.find(":") or filename.find("\\") or filename.find("*") or filename.find("/") or filename.find("\\\\"):
                print(f"{self.internal_name} I found forbidden symbols [.]/[:]...")
                filename.replace(".", "").replace(":", "_").replace("\\\\","").replace("*", "").replace("/", "_").replace("\\", "")

            # latex reduction
            xname = self.xname.replace("\\italic", "").replace("{", "").replace("}","").replace("_", "").replace("^", "").replace("\\\\", "").replace("\\", "").replace("/", "_").replace("*", "")
            yname = self.yname.replace("\\italic", "").replace("{", "").replace("}","").replace("_", "").replace("^", "").replace("\\\\", "").replace("\\", "").replace("/", "_").replace("*", "")
            # space reduction
            xname = xname.replace(" ", "")
            yname = yname.replace(" ", "")

            name4saving = filename+"_"+yname+"_"+xname

            if not os.path.exists(name4saving+".vsz"): self.g.Save(name4saving+".vsz")
            else:
                print(f"{self.internal_name} The file exists!")
                i = 0
                while os.path.exists(name4saving+str(i)+".vsz"): i+=1
                name4saving += str(i) + ".vsz"
                self.g.Save(name4saving)
                print(f"{self.internal_name} Saved! filename: {name4saving}")
