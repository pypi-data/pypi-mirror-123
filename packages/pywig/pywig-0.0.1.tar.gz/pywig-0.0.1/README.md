# PyWig

Welcome to PyWig, a Python library that helps you build HTML webpages saemlessly. PyWig stands for Python Webpage Interactive Generator. This package allows you to set headers, text, links, lists, and more. Learn more about PyWig and how you can use it in our [documentation](https://pywig.readthedocs.io).

## Install The Package

`pip install pywig`

## Examples

**Import Py2HTML:**

`from pywig import webpage`

**Define your Builder:**

`builder = PyWig()`

**Create Your Page:**

`builder.create(title="Your webpage title")`

After following these three steps, you are free to do anything you want with your webpage! Remember to save your file when you are done:

`builder.save(filename="sample.html")`