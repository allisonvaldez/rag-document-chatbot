""" 
Install and import dependencies:
    * flask: creates the web server and handles URL routes
    * dotenv: reads the .env file so API keys stay a secret
    * PyPDF: extracts text from uploaded PDF files
    * chromadb: vector database that stores text for AI to search it
    * openai: talks to the OpenAI API
    * os: allows Python to read environment variables from my system
"""
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from PyPDF import PdfReader
import chromadb
from openai import OpenAI
import os

# Load the .env file so the openai key is available
load_dotenv()

# Creates the Flask webapp
app = Flask(__name__)
# Connects to OpenAI via my key in .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Starts the ChromaDB running in memory
chroma_client = chromadb.Client()
# Creates a bucket for us to store document chunks
collection = chroma_client_get_or_create_collection(name="documents")

"""
Create the PDF processing function that takes in a file as a parameter:
    * reader = PdfReader(file): opens the PDF file to read
    * text = "": create an empty string to store the text
    * for page in reader.pages: create a for loop to go through each page of the document
    * text += page.extract_text(): Takes the text off the page and add it to the string
    * Return the collected text back to the function
"""
def process_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

"""
Create a chunking function that takes in text and limits the chunk size to 500 as a parameters:
    * chunk_size(500): splits the text into 500 digestible word chunks
    * words = text.split(): put the text into indivdual words
    * chunks = []: create an empty list to put the chunks
    * for i in range(0, len(words), chunk_size): loop through the wordlist 500 words at a time
    * chunk = " ".join(words[i:i + chunk_size]): get the next 500 words and join them to a string
    * chunk.append(chunk): add the chunks to the list
"""
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = "".join(words[i:i + chunk_size])
        chunk.append(chuck)
    return chunks