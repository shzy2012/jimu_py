# https://pypdf.readthedocs.io/en/stable/
# pip install pypdf

from pypdf import PdfReader

reader = PdfReader("error4.pdf", strict=False)
# number_of_pages = len(reader.pages)
# page = reader.pages[1]
# text = page.extract_text()
# print(number_of_pages)
# print(text)

for page in reader.pages:
    text = page.extract_text()
    print(text)
