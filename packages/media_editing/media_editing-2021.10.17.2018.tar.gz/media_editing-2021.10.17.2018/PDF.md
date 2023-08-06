# PDF

# extract pages of a PDF

The following example extracts page 9 only:

```Bash
pdftk A=ATLAS-CONF-2011-151.pdf cat A9-9 output ATLAS-CONF-2011-151_9.pdf
```

The following example extracts the pages in the range 307--310:

```Bash
pdftk A=ATL-COM-PHYS-2014-1471.pdf cat A307-310 output ATL-COM-PHYS-2014-1471_307--310.pdf
```

#  merge pages of PDFs

The following examples merge multiple PDF documents:

```Bash
pdftk 1.pdf 2.pdf cat output output.pdf
```

```Bash
pdftk *.pdf cat output output.pdf
```

# split PDF pages in two

This procedure is to take a PDF that is, for example, a scan of a book that has resulted in two pages of the book being encoded as a single page of the PDF, and to convert it to a new PDF that has each page split vertically in two.

```Bash
sudo apt install mupdf-tools
mutool poster -x 2 input.pdf output.pdf
```

The `-y` option can be used for vertical splits.

# convert PDF pages to PNG

```Bash
pdftoppm -png -r 600 input.pdf outputname
```

This results in files of the form `outputname-01.png` etc.

# convert images and text to PDF

```Bash
convert image_1.png image_2.png text.txt PDF_file.pdf output.pdf
```

Note that this may require a change of the `/etc/ImageMagick-6/policy.xml` line from the following

```XML
  <policy domain="coder" rights="none" pattern="PDF" />
```

to the following:

```XML
  <policy domain="coder" rights="read|write" pattern="PDF" />
```

```Bash
pdftk *.png cat output output.pdf
```

An ordered list of files can be obtained in the following way:

```Bash
list_of_files="$(find -type f -name '*.png' -or -name '*.jpg' -or -name '*.JPG' | sort -V)"
```

Using this, GraphicsMagick or ImageMagick can be used to convert images to a single PDF:

```Bash
list_of_files=$(find -type f -name '*.png' -or -name '*.jpg' -or -name '*.JPG' | sort -V)

gm convert ${list_of_files} out.pdf
#convert -quality 85 ${list_of_files} out.pdf
```

# shrink PDF

## skrinkpdf.sh

Use the script [shrinkpdf.sh](shrinkpdf.sh) with the input PDF, output PDF and DPI as arguments.

```Bash
./shrinkpdf.sh in.pdf out.pdf 200
```
