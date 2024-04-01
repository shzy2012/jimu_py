# https://pypdf.readthedocs.io/en/stable/
# pip install pypdf

from pypdf import PdfReader

reader = PdfReader("example.pdf")
# number_of_pages = len(reader.pages)
# page = reader.pages[1]
# text = page.extract_text()
# print(number_of_pages)
# print(text)

for page in reader.pages:
    text = page.extract_text()
    print(text)
