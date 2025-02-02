import os
from dotenv import load_dotenv
import time
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')

import chainlit as cl
import pymupdf
import tiktoken
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import getVectorstore
from getVectorstore import getVectorstore
from qdrant_client.http import models as rest
from langchain.prompts import ChatPromptTemplate
import prompts
from prompts import rag_prompt_template
from defaults import default_llm
from operator import itemgetter
from langchain.schema.output_parser import StrOutputParser
from datetime import date
from queries import summary_query
from queries import background_query
from queries import number_of_participants_query
from queries import study_procedures_query
from queries import alt_procedures_query
from queries import risks_query
from queries import benefits_query

import os
from uuid import uuid4

# unique_id = uuid4().hex[0:8]

# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = f"LangSmith - {unique_id}"

@cl.on_chat_start
async def on_chat_start():
    files = await cl.AskFileMessage(
        content="Upload a file to proceed",
        accept=["application/pdf"],
        max_size_mb=50,
        timeout=1800,
    ).send()

    file = files[0]
    print(f"filename is {file.name}")

    doc = pymupdf.Document(file.path)
    toc = doc.get_toc()
    # Want to find the List Of Figures page because that is the last page I want to skip
    # Default is 1 if I do not find better start location
    start_page = 1
    # for _, title, page in toc:
    #     if title == "List of Figures":
    #         print(f"{title} on page {page}")
    #         start_page = page + 1


    # get the last page I want included
    # default is last page of document
    end_page = len(doc)
    for _, title, page in toc:
        if ("References" in title) or ("Bibliography" in title):
            print(f"{title} on page {page}")
            end_page = page


    print(f"Extraction should start on page {start_page} and end on page {end_page}")


    # need a rect that will exclude headers and footers
    rect = pymupdf.Rect(0.0, 100.0, 612.0, 650.0)

    #capture the first 2 page
    extracted_text = ""

    for page in doc.pages():
        if page.number in range(start_page-1, end_page):
            extracted_text += page.get_text(clip=rect)


    # for page in doc.pages():
    #     if (start_page != 1 and page.number in [0, 1, 2]):
    #         extracted_text += page.get_text()
    #     elif page.number in range(start_page-1, end_page):
    #         # print(page.get_text(clip=rect))
    #         extracted_text += page.get_text(clip=rect)


    msg = cl.Message(
        content=f"""Processing selected file: `{file.name}`...
        Extraction beginning on page {start_page} and ending on page {end_page}.
        Using a clipping rectangle to exclude headers and footers ({rect}).
        Processed {end_page - start_page} pages of PDF document.
        Length of extracted text string is {len(extracted_text)}
        """
    )
    await msg.send()

    chunk_size = 800
    chunk_overlap = 400

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap = chunk_overlap,
        # length_function = tiktoken_len
    )

    text_chunks = text_splitter.split_text(extracted_text)
    document = [Document(page_content=chunk) for chunk in text_chunks]

    msg = cl.Message(
        content=f"""Splitting the text with a recursive character splitter.
        Set chunk size at {chunk_size} and overlap at {chunk_overlap}.
        Number of resulting chunks: {len(text_chunks)}.
        Document created from chunks to get stored in vector database.
        Length of the document: {len(document)} (should be same as number of chunks).
        """
    )

    await msg.send()

    qdrant_vectorstore = getVectorstore(document, file.name)

    # My vectorstore may have multiple protocols or documents that have been stored and persisted.
    # But I only want the context of the current session to relate to a document that I just processed
    # so I need to pass in the title of the document.  This will act as a filter for the retrieved
    # chunks.
    protocol_retriever = qdrant_vectorstore.as_retriever(
        search_kwargs={
            'filter': rest.Filter(
                 must=[
                    rest.FieldCondition(
                        key="metadata.document_title",
                         match=rest.MatchAny(any=[file.name])
                    )
                ]
            ),
            'k': 20,                                       
        }
    )
 
    # Create prompt
    rag_prompt = ChatPromptTemplate.from_template(prompts.rag_prompt_template)

    llm = default_llm

    rag_chain = (
        {"context": itemgetter("question") | protocol_retriever, "question": itemgetter("question")}
        | rag_prompt 
        | llm
        | StrOutputParser()
    ).with_config({"run_mode": "stream"})  # Enable streaming mode

    from datetime import date
    # Heading for top of ICF document
    protocol_title = rag_chain.invoke({"question": "What is the exact title of this protocol?  Only return the title itself without any other description."})
    principal_investigator = rag_chain.invoke({"question":"What is the name of the principal investigator of the study?  Only return the name itself without any other description."})
    support = rag_chain.invoke({"question":"What agency is funding the study?  Only return the name of the agency without any other description."})
    version_date = date.today().strftime("%B %d, %Y")

    msg = cl.Message(
        content=f""" 
        **Study Title:** {protocol_title}
        **Principal Investigator:** {principal_investigator}
        **Version Date:** {version_date}
        **Source of Support:** {support}
        ---
        """
    )

    await msg.send()
    
        # Sending an action button within a chatbot message
    actions = [
        cl.Action(
            name="summary_button",
            icon="mouse-pointer-click",
            payload={"value": "summary"},
            label="Write summary"
        ),
        cl.Action(
            name="risk_button",
            icon="mouse-pointer-click",
            payload={"value": "risks"},
            label="Write risk section"
        ),
        cl.Action(
            name="benefits_button",
            icon="mouse-pointer-click",
            payload={"value": "benefits"},
            label="Write benefits section"
        ),
        cl.Action(
            name="file_button",
            icon="mouse-pointer-click",
            payload={"value": "markdown"},
            label="Create final file"
        )
    ]
    await cl.Message(content="Select consent form sections:", actions=actions).send()

    @cl.action_callback("summary_button")
    async def on_action(action: cl.Action):
        summary = rag_chain.invoke({"question":summary_query()})
        await cl.Message(content=summary).send()
        await cl.Message(content=f"Executed {action.payload["value"]}").send()
        # await action.remove()

    @cl.action_callback("risk_button")
    async def on_action(action: cl.Action):
        # risks = rag_chain.invoke({"question":risks_query()})
        risks = rag_chain.invoke({"question":risks_query})
        # risks = rag_chain.invoke({"question":"Write a summary of the risks of participating in the study.  This will be used for the 'Risks' section of the informed consent document.  The summary should include potential risks for the patient (addressed as 'you'), and potential risks for others.  Since this is a research study and it is not known if the intervention is helpful, it is important to not overstate potential risks for the patient.  The length of this risks summary is usually 500 to 750 words.  Start the summary with a level 2 Markdown header (##) titled 'Risks', and then continue the section with subheadings that will help organize the information for the reader.  Do not go more than two subheadings deep."})
        await cl.Message(content=risks).send()
        await cl.Message(content=f"Executed {action.payload["value"]}").send()
        # await action.remove()

    @cl.action_callback("benefits_button")
    async def on_action(action: cl.Action):
        benefits = rag_chain.invoke({"question":benefits_query()})
        await cl.Message(content=benefits).send()
        await cl.Message(content=f"Executed {action.payload["value"]}").send()
        # await action.remove()

    # @cl.action_callback("file_button")
    # async def on_action(action: cl.Action):
    #     await cl.Message(content=f"Executed {action.payload["value"]}").send()
    #     await action.remove()


    # # Now let's test the application to make a consent document
    # start_time = time.time()
    # # Brute force method that just saves each generated section as string
    # summary = rag_chain.invoke({"question":summary_query()})
    # background = rag_chain.invoke({"question":background_query()})
    # number_of_participants = rag_chain.invoke({"question":number_of_participants_query()})
    # study_procedures = rag_chain.invoke({"question":study_procedures_query()})
    # alt_procedures = rag_chain.invoke({"question":alt_procedures_query()})
    # risks = rag_chain.invoke({"question":risks_query()})
    # benefits = rag_chain.invoke({"question":benefits_query()})

    # end_time = time.time()
    # execution_time = end_time - start_time

    # msg = cl.Message(
    #     content=f"""
    #     Brute force (sequential) execution time: {execution_time:.2f} seconds.
    #     {summary}
    #     {background}  
    #     {number_of_participants} 
    #     {study_procedures}
    #     {alt_procedures}
    #     {risks}
    #     {benefits}
    #     """

    # )
   
    # await msg.send() 