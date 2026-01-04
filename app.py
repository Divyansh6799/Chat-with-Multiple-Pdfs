import streamlit as st
# from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
# from sentence_transformers import SentenceTransformer # Use SentenceTransformer module to use Hugging face Model
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from transformers import AutoTokenizer, AutoModel
import os
import uuid
import streamlit.components.v1 as components
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import shutil

# openai_api_key = st.secrets["OPENAI_API_KEY"]
hf_token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

def get_pdf_text(uploaded_files):
    """Extract text from the uploaded PDF files."""
    pdf_text = ""
    for pdf in uploaded_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            # st.write(page.extract_text())
            page_text = page.extract_text()
            # st.write(page_text)  # Display the text on the Streamlit app
            if page_text:  # Check if there is text to add
                pdf_text += page_text  # Append the text to pdf_text
    return pdf_text

def get_text_chunks(pdf_text):
    """Split the raw text into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        separators= "\n",
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(pdf_text)
    return chunks


AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_vectorstore(text_chunks, reset_index=False):
    # embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                    model_kwargs={"device": "cpu"},
                                    encode_kwargs={"normalize_embeddings": True})
    # embeddings = model.encode(text_chunks)
    # similarities = model.similarity(embeddings, embeddings)
    if reset_index and os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")

    if os.path.exists("faiss_index"):
        vectorstore = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_texts(text_chunks, embeddings)
        vectorstore.save_local("faiss_index")
    return vectorstore

def get_conversation_chain(vectorstore):
    # llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature":0.3, "max_length":100},task="text2text-generation")
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-large",
        max_new_tokens=100,
        temperature=0.3
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    try:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                message_id = str(uuid.uuid4()).replace("-", "")
                rendered_html = user_template.replace("{{MSG}}", message.content).replace("{{ID}}", message_id)
                components.html(rendered_html, height=70, scrolling=False)
            else:
                message_id = str(uuid.uuid4()).replace("-", "")
                rendered_html = bot_template.replace("{{MSG}}", message.content).replace("{{ID}}", message_id)
                components.html(rendered_html, height=70, scrolling=False)
    except TypeError as e:
        # Handle the TypeError and display an error message
        print(f"TypeError: {e}")
        st.session_state.chat_history = []
        st.warning("Please upload PDF files in the left sidebar and process them before asking questions. Thank you!")
    except Exception as e:
        # Handle any other exceptions and display an error message
        st.error(f"An error occurred: {e}")
        st.session_state.chat_history = []


def main():
    # load_dotenv()
    # Set the page configuration
    st.set_page_config(page_title="PDF's Gyani | Chat with us",page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("PDF's Gyani :books:")
    st.subheader("Chat with your PDF's using Langchain and Streamlit")
    user_question = st.chat_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Upload PDF files")
        uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
        if st.button("Process PDFs"):
            st.success("PDFs processed successfully!")
            with st.spinner("Embedding Processing..."):
                
                #get pdf text
                pdf_text = get_pdf_text(uploaded_files)
                # st.write("Extracted Text from PDFs:",pdf_text)
            
                # get the text chunks
                text_chunks = get_text_chunks(pdf_text)
                # st.write("Text Chunks:", text_chunks)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)
                # st.write("Vectorstore created successfully!", vectorstore)
                st.write("Vectorstore created successfully! Now you can ask questions about your documents!")
                
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
        

if __name__ == "__main__":
    main()