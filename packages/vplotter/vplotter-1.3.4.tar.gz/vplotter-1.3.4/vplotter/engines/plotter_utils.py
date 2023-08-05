##*
## MIT License
##
## Plotter - Copyright (c) 2021 Aleksandr Kazakov, Varvara Prokacheva
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

COLOR_DICT = {
    1: 'black',     2: 'red',      3: 'green',    4: 'blue',
    5: 'magenta',   6: '#01A9DB',  7: '#006F74',  8: '#8904B1',
    9: '#B4045F',   10: '#585858', 11: '#DF3A01', 12: '#DBA901',
    13: '#74DF00',  14: '#CEF6F5', 15: '#0041FB', 16: '#00FB91',
    17: '#887D64',  18: '#00C9FF', 19: '#7625B6', 20: '#B08EA0',
}

LINE_TYPE_DICT = {
    1: 'solid',    2: 'dashed',       3: 'dotted',
    4: 'dash-dot', 5: 'dash-dot-dot', 6: 'dotted-fine', 7: 'dashed-fine', 8: 'dash-dot-fine',
    9: 'dot1',     10: 'dot2',       11: 'dot3',       12: 'dot4',
    13: 'dash1',   14: 'dash2',      15: 'dash3',      16: 'dash4',      17: 'dash5', 18: 'dash6',
}

MARKER_TYPE_DICT = {
    0: 'none',           1: 'circle',        2: 'square',         3: 'cross',       4: 'plus', 5: 'star',
    6: 'pentagon',       7: 'hexagon',       8: 'tievert',        9: 'tiehorz',    10: 'triangle',
    11: 'triangledown', 12: 'triangleleft', 13: 'triangleright', 14: 'circledot',
    15: 'bullseye',     16: 'circlehole',   17: 'squarehole',    18: 'diamondhole', 19: 'pentagonhole',
    20: 'squarerounded', 21: 'diamond',
}

# feel free to add new
LABELS_DICT = dict(
    cs= "\\italic{c}_{s}",       pK="p\\italic{K}",   pH="pH",                    lB="\\italic{l}_{B}",
    alpha="\\alpha",            chi="\\chi",           f="\\italic{f}",      epsilon="\\italic{\\epsilon}",
    sigma="\\italic{\\sigma}", dmpc="\\italic{n}", chain="\\italic{l}_{n}",    rcutg="\\italic{r}_{cut} = 2^{1/6}",
    rcut ="\\italic{r}_{cut} = 2.5",
)

def get_line_color(num):
    t = "black"
    if num <= len(COLOR_DICT) - 1 : t =  COLOR_DICT[num]
    return t

def get_line_type(num):
    t = "solid"
    if num <= len(LINE_TYPE_DICT) - 1 : t =  LINE_TYPE_DICT[num]
    return t

def get_marker_type(num):
    t = "circle"
    if num <= len(MARKER_TYPE_DICT) - 1: t =  MARKER_TYPE_DICT[num]
    return t

def get_label(name: str) -> str:
    return LABELS_DICT[name]
