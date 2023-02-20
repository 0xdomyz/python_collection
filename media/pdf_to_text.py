# convert pdf to text
from pathlib import Path

import pypdf

here = Path("media/")

# read pdf file
def read_pdf(filename):
    pdf_file = open(filename, "rb")
    read_pdf = pypdf.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    page = read_pdf.getPage(0)
    page_content = page.extractText()
    return page_content


# save text file
def save_to_file(text, filename):
    with open(filename, "w") as f:
        f.write(text)


if __name__ == "__main__":
    text = read_pdf(here / "test.pdf")
    save_to_file(text, here / "test.txt")
