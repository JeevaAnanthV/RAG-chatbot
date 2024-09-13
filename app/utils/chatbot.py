import streamlit as st
from collections import defaultdict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import os
def get_context_retriever_chain(vectordb):
    """
    Create a context retriever chain for generating responses based on the chat history and vector database

    Parameters:
    - vectordb: Vector database used for context retrieval

    Returns:
    - retrieval_chain: Context retriever chain for generating responses
    """
    # Load environment variables (gets api keys for the models)
    load_dotenv()
    # Initialize the model, set the retreiver and prompt for the chatbot
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2, convert_system_message_to_human=True)
    retriever = vectordb.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a chatbot. You'll receive a prompt that includes a chat history and retrieved content from the vectorDB based on the user's question. Your task is to respond to the user's question using the information from the vectordb, relying as little as possible on your own knowledge. If for some reason you don't know the answer for the question, or the question cannot be answered because there's no context, ask the user for more details. Do not invent an answer. Answer the questions from this context: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    # Create chain for generating responses and a retrieval chain
    chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    retrieval_chain = create_retrieval_chain(retriever, chain)
    return retrieval_chain

def get_response(question, chat_history, vectordb):
    """
    Generate a response to the user's question based on the chat history and vector database

    Parameters:
    - question (str): The user's question
    - chat_history (list): List of previous chat messages
    - vectordb: Vector database used for context retrieval

    Returns:
    - response: The generated response
    - context: The context associated with the response
    """
    chain = get_context_retriever_chain(vectordb)
    response = chain.invoke({"input": question, "chat_history": chat_history})
    return response["answer"], response["context"]

def chat(chat_history, vectordb):
    """
    Handle the chat functionality of the application

    Parameters:
    - chat_history (list): List of previous chat messages
    - vectordb: Vector database used for context retrieval

    Returns:
    - chat_history: Updated chat history
    """
    user_query = st.chat_input("Ask a question:")
    if user_query is not None and user_query != "":
        # Generate response based on user's query, chat history and vectorstore
        response, context = get_response(user_query, chat_history, vectordb)
        # Update chat history. The model uses up to 10 previous messages to incorporate into the response
        chat_history = chat_history + [HumanMessage(content=user_query), AIMessage(content=response)]
        # Display source of the response on sidebar
        with st.sidebar:
                metadata_dict = defaultdict(list)
                for metadata in [doc.metadata for doc in context]:
                    metadata_dict[metadata['source']].append(metadata['page'])
                for source, pages in metadata_dict.items():
                    st.write(f"Source: {source}")
                    st.write(f"Pages: {', '.join(map(str, pages))}")
    # Display chat history
    for message in chat_history:
            with st.chat_message("AI" if isinstance(message, AIMessage) else "Human"):
                st.write(message.content)
    return chat_history

from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_text_response(user_input):
    """
    Generate a response for a text-based input query directly using LLM.

    Parameters:
    - user_input (str): The text input from the user

    Returns:
    - response: The generated response from LLM
    """
    # Load environment variables (gets API keys for the models)
    load_dotenv()

    vectordb = st.session_state.vectordb
    if vectordb is None:
        return "Vector database is not available."
    
    response = vectordb.query(user_input)
    return response if response else "No relevant information found."


    # Initialize the model with system message conversion to human message
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro", 
        temperature=0,
        convert_system_message_to_human=True
    )
    
    # Create messages
    messages = [
        ("human", user_input)
    ]
    
    # Debugging: Print the type and content of the messages
    print(f"Messages type: {type(messages)}")
    print(f"First message type: {type(messages[0])}")
    
    try:
        # Generate a response
        response = llm.invoke(messages)
    except Exception as e:
        print(f"Error during LLM generation: {e}")
        return "An error occurred while generating the response."

    # Debugging: Print the response structure
    print(f"Response: {response}")
    
    # Extract and return the text from the response
    try:
        # Ensure the response structure matches expectations
        return response.content
    except AttributeError:
        return "An unexpected response format was received."