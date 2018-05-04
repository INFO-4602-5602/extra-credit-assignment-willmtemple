# Experimentation

Find the data in the `Data` directory. The apparatus is [hosted in Google
Forms](https://goo.gl/forms/bV7kNmRwJKHoCGDn2). A full copy of the survey is
located in `assets/gform_out.pdf`.

## The Report

A report PDF is included in this directory. To build the report from scratch,
you will need [Pandoc](https://pandoc.org/)

```sh
$ pandoc -o report.pdf -V geometry:margin=1in -V header-includes="\usepackage{pdfpages}" report.md
```

