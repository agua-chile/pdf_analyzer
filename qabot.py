# Library imports
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_ibm import WatsonxLLM, WatsonxEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('env/.env')

# Local imports
from utils import handle_error
from utils import list_ibm_models


# Global variables
GENERATION_MODEL_ID = 'ibm/granite-3-8b-instruct'       # Specify IBM's Granite 3 8B model
EMBEDDING_MODEL_ID = 'ibm/slate-125m-english-rtrvr'     # Specify IBM's Slate 125M model
URL = 'https://us-south.ml.cloud.ibm.com'

# Load API credentials from environment variables
APIKEY = os.getenv('APIKEY')
PROJECT_ID = os.getenv('PROJECT_ID')

# Validate that required environment variables are set
if not APIKEY:
    raise ValueError('APIKEY environment variable is not set. Please check your .env file.')
if not PROJECT_ID:
    raise ValueError('PROJECT_ID environment variable is not set. Please check your .env file.')
GENERATION_PARAMETERS = {
    GenParams.MAX_NEW_TOKENS: 512,                      # Specify the max tokens you want to generate
    GenParams.TEMPERATURE: 0.5,                         # This randomness or creativity of the model's responses
}
EMBEDDING_PARAMETERS = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {'input_text': True},
}


def get_llm():
    print('Setting up Watsonx LLM from global variables...')
    watsonx_llm = WatsonxLLM(
        model_id=GENERATION_MODEL_ID,
        url=URL,
        apikey=APIKEY,
        project_id=PROJECT_ID,
        params=GENERATION_PARAMETERS,
    )
    return watsonx_llm


def pdf_loader(file):
    print(f'Loading document from file: {file.name}...')
    loader = PyPDFLoader(file.name)
    loaded_document = loader.load()
    return loaded_document


def text_splitter(data, split_method='recursive', chunk_size=1000, chunk_overlap=100):
    print(f'Splitting document into chunks using {split_method} method into size {chunk_size} with overlap {chunk_overlap}...')
    if split_method == 'recursive':
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    elif split_method == 'character':
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    else:
        raise ValueError('Invalid split method. Choose "recursive" or "character".')
    chunks = text_splitter.split_documents(data)
    return chunks


def vector_database(chunks):
    print(f'Creating vector database from {len(chunks)} document chunks...')
    embedding_model = watsonx_embedding()
    vectordb = Chroma.from_documents(chunks, embedding_model)
    return vectordb


def watsonx_embedding():
    print('Setting up Watsonx Embedding model from global variables...')
    watsonx_embedding = WatsonxEmbeddings(
        model_id=EMBEDDING_MODEL_ID,
        url=URL,
        apikey=APIKEY,
        project_id=PROJECT_ID,
        params=EMBEDDING_PARAMETERS,
    )
    return watsonx_embedding


def retriever(file):
    print(f'Retrieving relevant documents from {file.name}...')
    splits = pdf_loader(file)
    chunks = text_splitter(splits)
    vectordb = vector_database(chunks)
    retriever = vectordb.as_retriever()
    return retriever


def retriever_qa(file, query):
    try:
        print(f'Running QA pipeline for query: {query}...')
        llm = get_llm()
        retriever_obj = retriever(file)
        prompt = PromptTemplate(
            input_variables=['context', 'question'],
            template=(
                'Use the following context to answer the question.\n\n'
                'Context:\n{context}\n\n'
                'Question: {question}\n\n'
                'Answer:'
            ),
        )
        qa_pipeline = (     # Using pipeline rather than chains for LangChain 1.0.1+
            {
                'context': lambda x: retriever_obj.get_relevant_documents(x['question']),
                'question': lambda x: x['question'],
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        response = qa_pipeline.invoke({'question': query})
        return response
    except Exception as e:
        return handle_error(e)


def create_gradio_interface():
    interface = gr.Interface(
        fn=retriever_qa,
        allow_flagging='never',
        inputs=[
            gr.File(label='Upload PDF File', file_count='single', file_types=['.pdf'], type='filepath'),  # Drag and drop file upload
            gr.Textbox(label='Input Query', lines=2, placeholder='Type your question here...')
        ],
        outputs=gr.Textbox(label='Response', lines=10, max_lines=50),
        title='PDF Document Question Answering',
        description='Upload a PDF document and ask any question. The chatbot will try to answer using the provided document.'
    )
    return interface


def main():
    rag_application = create_gradio_interface()
    rag_application.launch(server_name='127.0.0.1', server_port=7860)


if __name__ == '__main__':
    main()