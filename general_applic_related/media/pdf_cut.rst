install pdftk on linux::

    sudo apt-get install pdftk

Remove page 13 from in1.pdf to create out1.pdf::

    pdftk in.pdf cat 1-12 14-end output out1.pdf
    pdftk A=in1.pdf cat A1-12 A14-end output out1.pdf

Out put the first 10 pages of in1.pdf to out1.pdf::

    pdftk in1.pdf cat 1-10 output out1.pdf

Get the number of pages in in1.pdf::

    pdftk in1.pdf dump_data | grep NumberOfPages

Combine 2 pdf::

    pdftk in1.pdf in2.pdf cat output out1.pdf

qpdf::
    
    qpdf in1.pdf --pages . 1-12 14-z -- out1.pdf