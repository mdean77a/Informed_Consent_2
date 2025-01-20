from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from langchain_qdrant import QdrantVectorStore
import hashlib
import defaults

embedding_model = defaults.default_embedding_model
qdrant_url = defaults.default_url

"""
This code creates a hash for every chunk and checks to see if that chunk already exists in the
vector database.  We only want one collection in Qdrant, but want to make sure that if a user
selects a document that has already been embedded and stored, it does not get stored again.  We
also add metadata for the document title, so that we can make our retriever focus on documents of
interest.  For example, after some usage, the application might have 20 documents for the user to 
select from.  We want the retriever to be exactly right for the documents that they selected.

This could also be useful if different versions of documents are in existence.  We would not want to
recreate a large vectorstore.  But the user could select the most recent version.
"""

def get_document_hash(doc_content):
    """Generate a unique hash for the document content."""
    return hashlib.md5(doc_content.encode()).hexdigest()

def getVectorstore(document, file_name):
    # Add a unique hash to your documents
    for doc in document:
        doc.metadata['content_hash'] = get_document_hash(doc.page_content)

    # Add the document title
    for doc in document:
        doc.metadata['document_title'] = file_name

    # Add page to metadata
    for i, doc in enumerate(document):
        doc.metadata['source'] = f"source_{i}"

    # collection_name = f"pdf_to_parse_{uuid.uuid4()}"
    collection_name = "protocol_collection"
    
    client = QdrantClient( url=qdrant_url)
    # client = QdrantClient(location=":memory:")  

    # If the collection exists, then we need to check to see if our document is already
    # present, in which case we would not want to store it again.
    if client.collection_exists(collection_name):
        print("Collection exists")
        qdrant_vectorstore = QdrantVectorStore.from_existing_collection(
            embedding=embedding_model,
            collection_name=collection_name,
            url=qdrant_url
            # location = ":memory:"
        )
        
        # Check for existing documents and only add new ones
        existing_hashes = set()
        new_docs = []
        
        # Get all existing hashes
        scroll_filter = rest.Filter(
            should=[
                rest.FieldCondition(
                    key="metadata.content_hash",
                    match=rest.MatchValue(value=doc.metadata['content_hash'])
                ) for doc in document
            ]
        )
        
        scroll_results = client.scroll(
            collection_name=collection_name,
            scroll_filter=scroll_filter,
            limit=len(document)  # Adjust this if you have a large number of documents
        )
        
        existing_hashes = set(point.payload.get('metadata', {}).get('content_hash') for point in scroll_results[0])
        
        for doc in document:
            if doc.metadata['content_hash'] not in existing_hashes:
                new_docs.append(doc)
        
        if new_docs:
            qdrant_vectorstore.add_documents(new_docs)
        
        print(f"Added {len(new_docs)} new documents")
        print(f"Skipped {len(existing_hashes)} existing documents")
    else: 
        print("Collection does not exist")                           #So we go ahead and just add the documents
        qdrant_vectorstore = QdrantVectorStore.from_documents(
            documents=document,
            embedding=embedding_model,
            collection_name=collection_name,
            # location = ":memory:"
            url=qdrant_url
        )
    return qdrant_vectorstore
