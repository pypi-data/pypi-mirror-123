# Plotter

- [General](#plotter)
	- [Engines](#engines) 	
	- [Installation](#install)
	- [Usage](#usage)
	- [Contribution](#contribution)
	- [License](#license)

Plotter is a minimalistic class for plotting. Feel free to use it and contribute (see [contribution section](#12-contribution)).

## Engines

Next engines supported:

* [Veusz](https://veusz.github.io/)
* [Gnuplot](http://www.gnuplot.info/) (experimental)

## Installation

Note: before usage make sure that the engine is installed.

```
pip install vplotter

```

## Usage

```python
>>> from vplotter import Plotter
>>> p = Plotter()
===> [Plotter: (engine:veusz)] is initialized [v.X.Y.Z]
>>> p.plot(x=[i**2 for i in range(10)], y=[i**3 for i in range(10)], key_name="first line")

```

If you see something similar to this:

![VeuszEngine](./asserts/figs/first_run.png)

So you have it. Nice! 

Similarly you can use another engine: Gnuplot engine. 

```python
>>> from vplotter import Plotter
>>> p = Plotter(engine="gnuplot", xname="X", yname="Y", title="My Title")
===> [Plotter: (engine:gnuplot)] is initialized [v.1.3.0]
>>> p.plot(x=[i**2 for i in range(10)], y=[i**3 for i in range(10)], key_name="first line")
>>>

```
```
                                     My Title
     90 +------------------------------------------------------------------+
        |      +       +      +       +      +       +      +       +      |
     80 |-+                                             first line ********|
        |                                                               ** |
     70 |-+                                                           ** +-|
        |                                                          ***     |
     60 |-+                                                     ***      +-|
        |                                                     **           |
     50 |-+                                                ***           +-|
  Y  40 |-+                                            ****              +-|
        |                                          ****                    |
     30 |-+                                    ****                      +-|
        |                                   ***                            |
     20 |-+                             ****                             +-|
        |                         ******                                   |
     10 |-+                *******                                       +-|
        |      +   ********   +       +      +       +      +       +      |
      0 +------------------------------------------------------------------+
        0      1       2      3       4      5       6      7       8      9
                                         X
```

Currently GnuplotEngine is in experimental mode.
It is plotting the graph only to your terminal. Further releases would expand the functionality.

## Contribution

Feel free to contribute to the project, but please initially create an issue with detailed problem and way how to resolve it. 

## License
----

MIT
