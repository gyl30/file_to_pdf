code file to pdf

# Install dependencies

```bash

brew install highlight wkhtmltopdf

```

# Usage

```bash

usage: file_to_pdf.py [-h] [-i I] [-o O]

Convert files to pdf

optional arguments:
  -h, --help  show this help message and exit
  -i I        input directory
  -o O        output file

```

## Example

```bash

cd example && python file_to_pdf.py -i . -o example.pdf

or

python file_to_pdf.py -i ./example -o example.pdf

```
