# generator3

generator3 is a Python package to export Scratch sprite scripts to the well known scratchblocks syntax.
## Installation
```bash
$ python3 -m pip install generator3
```
or manually (not recommended):
```bash
$ git clone https://github.com/themysticsavages/generator3
$ cd generator3
$ python3 setup.py install
```
## Usage
```python
import generator3
# Converts to scratchblocks and puts each sprites' scripts in a HTML file
generator3.Generator(pid).toBlocks()
# Serve the generated HTML
generator3.serveHTML()
```
This is still in progress so not every block will be rendered!<br>
Made with ❤️ by themysticsavages