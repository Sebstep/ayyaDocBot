import os, sys
from langchain.text_splitter import RecursiveCharacterTextSplitter

# other idea: split on deepest heading level (e.g., "##" or "###") for quick summaries

booklist = os.listdir("documents/processed")
bookname = booklist[1]


with open(f"documents/processed/{bookname}") as f:
    my_book = f.read()


# todo: remove preamble, achknowledgments and closing stuff

# split my_book on every occurence of "\n\n"
chapters = my_book.split("\n\n")
print(chapters[0])
print(chapters[1])
print(chapters[2])


# text_splitter = RecursiveCharacterTextSplitter(
#     # Set a really small chunk size, just to show.
#     chunk_size = 2000,
#     chunk_overlap  = 20,
#     length_function = len,
# )


# texts = text_splitter.create_documents([my_book])
# print(texts[0])
# print(texts[1])
# print(texts[2])


