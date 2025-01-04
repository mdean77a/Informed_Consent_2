import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import chainlit as cl
import pymupdf
import tiktoken
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# def tiktoken_len(text):
#     tokens = tiktoken.encoding_for_model("gpt-4o").encode(
#         text,
#     )
#     return len(tokens)

@cl.on_chat_start
async def on_chat_start():
    files = await cl.AskFileMessage(
        content="Upload a file to proceed",
        accept=["application/pdf"],
        max_size_mb=50,
        timeout=180,
    ).send()

    file = files[0]

    doc = pymupdf.Document(file.path)
    toc = doc.get_toc()
    # Want to find the List Of Figures page because that is the last page I want to skip
    for _, title, page in toc:
        if title == "List of Figures":
            print(f"{title} on page {page}")
            start_page = page + 1

    # get the last page I want included
    for _, title, page in toc:
        if ("References" in title) or ("Bibliography" in title):
            print(f"{title} on page {page}")
            end_page = page

    print(f"Extraction should start on page {start_page} and end on page {end_page}")


    # need a rect that will exclude headers and footers
    rect = pymupdf.Rect(0.0, 100.0, 612.0, 650.0)

    #create the final text
    extracted_text = ""
    for page in doc.pages():
        if page.number in range(start_page-1, end_page):
            # print(page.get_text(clip=rect))
            extracted_text += page.get_text(clip=rect)
    msg = cl.Message(
        content=f"""Processing selected file: `{file.name}`...
        Extraction beginning on page {start_page} and ending on page {end_page}.
        Using a clipping rectangle to exclude headers and footers ({rect}).
        Processed {end_page - start_page} pages of PDF document.
        Length of extracted text string is {len(extracted_text)}
        """
    )
    await msg.send()

    chunk_size = 2000
    chunk_overlap = 200

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap = chunk_overlap,
        # length_function = tiktoken_len
    )

    text_chunks = text_splitter.split_text(extracted_text)
    # print(f"Number of chunks: {len(text_chunks)} ")
    document = [Document(page_content=chunk) for chunk in text_chunks]
    # print(f"Length of  document: {len(document)}")

    msg = cl.Message(
        content=f"""Splitting the text with a recursive character splitter.
        Set chunk size at {chunk_size} and overlap at {chunk_overlap}.
        Number of resulting chunks: {len(text_chunks)}.
        Document created from chunks to get stored in vector database.
        Length of the document: {len(document)} (should be same as number of chunks).
        """
    )

    await msg.send()