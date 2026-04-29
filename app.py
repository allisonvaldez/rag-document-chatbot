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