import streamlit as st
# import huggingface_hub as 
from dotenv import load_dotenv
from PyPDF2 import PdfReader


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text




def main():
    load_dotenv()
    st.set_page_config("Chat with PDF's", page_icon = ":parrot::link:")

    st.header('Chat with Your PDF\'s:parrot::link:')
    st.text_input('Hey, What\'s going on??')

    with st.sidebar:
        st.subheader('Your documents Please')
        pdf_docs = st.file_uploader("Upload your pdf's here please", accept_multiple_files= True)
        if st.button("Provide"):
            with st.spinner('Processing...'):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
            

                # get the text chunks


                #create vector store


if __name__ == '__main__':
    main()