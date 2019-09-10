# What is this?

[My Jupyter/IPython-based blog](https://thoughts.johnbnelson.com/).

# Should I use it, too?

Eventually, sure! Right now -- almost certainly not.

# How does it work?

A `Makefile` compiles each notebook into an HTML page via
`nbconvert`, my `dissertate` extension, and `pandoc`.

# Notes

Use,

```
jupyter labextension install jupyterlab_nbmetadata
```

so you can edit notebook metadata. It passes through to the 
Markdown-ed source before compilation to `.html` via `pandoc`.
