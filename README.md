# LaTeX Template with Gitlab CI

This repository features a simple template for building and checking LaTeX documents with additional integration into Gitlab CI.

Some of the features are:

* It contains a Makefile for building the document as well as zipping all source files.
* Images in the formats SVG and ODG/FODG are supported and automatically converted to PDF.
    For this, SVG files can be placed into the `figs/` folder.
    They will be converted using [Inkscape].

    ODG/FODG files are created with [Libreoffice Draw][draw].
    They will be converted if they are placed into the `figs/raw/` folder.

    Generated PDFs automatically get trimmed to the correct image size using pdfcrop.
* Many [pre-commit] rules are already configured.
    These rules cover LaTeX writing styles, for example, consistent spelling of naive/naïve or how to typeset "et al.".

    A second set of rules covers the files of the CI system, e.g., formatting for the Python and Yaml files.
* There is a fully configured Gitlab CI pipeline.
    The pipeline build the document.
    It runs all the [pre-commit] check and some additional ones, which ensure that common error cannot slip through.
    It upload the build artifacts to the CI system, such that you can always check the state of your document for every commit.

[draw]: https://www.libreoffice.org/discover/draw/
[Inkscape]: https://inkscape.org/
[pre-commit]: https://pre-commit.com
