import streamlit as st
# import huggingface_hub as 
from dotenv import load_dotenv




def main():
    load_dotenv()
    st.set_page_config("Chat with PDF's", page_icon = ":parrot::link:")

    st.header('Chat with Your PDF\'s:parrot::link:')
    st.text_input('Hey, What\'s going on??')

    with st.sidebar:
        st.subheader('Your documents Please')
        st.file_uploader("Upload your pdf's here please")
        st.button("Provide")


if __name__ == '__main__':
    main()