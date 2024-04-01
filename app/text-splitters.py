from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("example.pdf")
pages = loader.load_and_split()
# # pages[4].page_content
# print(pages[0].metadata)

#
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=10,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)

"""
 separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200B",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ]
"""
#
# text_splitter = RecursiveCharacterTextSplitter(
#     # Set a really small chunk size, just to show.
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len,
#     is_separator_regex=False,
# )

segments = text_splitter.split_documents(pages)
print(len(segments))
for text in segments:
    print(text)
    print("---------------------------->")
print(len(segments))
