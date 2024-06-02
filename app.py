import streamlit as st
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from html_template import css, bot_template, user_template


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks



def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embedding  = INSTRUCTOR("hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(text_chunks, embedding = embeddings)
    return vectorstore



def get_conversation_chain(vector_store):
    llm = ChatOpenAI(temperature = 0)
    memory = ConversationBufferMemory(memory_key = 'chat_history', return_messages = True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vector_store.as_retriever(),
        memory = memory
    )
    return conversation_chain


def handle_userquestion(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, msg in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config("Chat with PDF's", page_icon = ":parrot::link:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    st.header('Chat with Your PDF\'s:parrot::link:')
    user_question = st.text_input('Hey, What\'s going on??')
    if user_question:
        handle_userquestion(user_question)
        st.text_input(value = "")


    # st.write(user_template.replace("{{MSG}}", 'Hey what\'s up robo?'), unsafe_allow_html=True)
    # st.write(bot_template.replace("{{MSG}}", 'Hey what\'s up Parrot?'), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader('Your documents Please')
        pdf_docs = st.file_uploader("Upload your pdf's here please", accept_multiple_files= True)
        if st.button("Provide"):
            with st.spinner('Processing...'):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)        
                #create vector store
                vector_store = get_vector_store(text_chunks)
                #create convo chain
                st.session_state.conversation = get_conversation_chain(vector_store)  #it is object of class ConversationalRetrievalChain
    # st.session_state.conversation




if __name__ == '__main__':
    main()