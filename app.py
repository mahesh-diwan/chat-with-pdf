import streamlit as st
import pickle 
from dotenv import load_dotenv
from  PyPDF2 import PdfReader 
# from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# Sidebar Contents
with st.sidebar:
    st.title("Chat With Pdf")
    st.markdown(
        '''
        ## About
       This app is an LLM powered chatbot built using :
       - [Streamlit](https://streamlit.io/)        
       - [LangChain](https://python.langchain.com/)        
       - [HuggingFace](https://huggingface.co/)        

    ''')
    # add_vertical_space(5)
    
    st.write("Made by Mahesh")
    
def main():
        st.header("Chat with PDF")
        
        load_dotenv()
        
        # upload a pdf 
        pdf = st.file_uploader("Upload your PDF file" , type="pdf")

        # st.write(pdf)
        if pdf :
            pdf_reader=PdfReader(pdf);
        
            text = ""
            if pdf_reader is not None:
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            #st.write(text)
            
            
            text_splitter=RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
                
                )
            
            chunks = text_splitter.split_text(text=text)
            
            #st.write(chunks)
            
            # Embeddings 
            store_name=pdf.name[:-4]


            if os.path.exists(f"{store_name}.pkl"):
                with open(f"{store_name}.pkl","rb") as f:
                    VectoreStore = pickle.load(f)
                # st.write("Reading from disk")

            else:
                # embeddings = OpenAIEmbeddings()
                embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
                VectoreStore = FAISS.from_texts(chunks,embedding=embeddings)
                with open(f"{store_name}.pkl","wb") as f :
                    pickle.dump(VectoreStore,f)

            # Questions
            query = st.text_input("Ask Questions about your pdf file")  
            # st.write(query)


            if query :
                docs = VectoreStore.similarity_search(query,k=3)
                # st.write(docs)
                model_name = "deepset/roberta-base-squad2"
                
                # b) Load model & tokenizer
                model = AutoModelForQuestionAnswering.from_pretrained(model_name)
                tokenizer = AutoTokenizer.from_pretrained(model_name)

                # a) Get predictions
                nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

                context=str(docs[0])
                # st.write(context)

                QA_input = {
                    'question': query,
                    'context': context
                }

                res = nlp(QA_input)

                
                # st.write(res)
                st.write(res['answer'])

                
if __name__ == '__main__':
    main()
