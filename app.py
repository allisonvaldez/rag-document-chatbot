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

"""
Create the upload route and upload function for the PDF to be uploaded. This breaks the article down into searchable peices and stores them in a vector database for the AI to find the information it is looking for. 

This is the point in the app where the RAG actually happens. This is where we actually upload a PDF document, break it down into searchable peices, store it in a vector database for AI to find the correct information later:
    * @app.route("/upload", methods=["POSTS"]): create an URL endpoint at /upload that can only take post requests (we should only be able to send data TO the app)
    * if "file" not in request.file: perform error handling to check if the file is in the request
    * return jsonify(...), 400: perform error handling to send an error JSON message
    * file = request.files["file"]: get the uploaded file from the request
    * in not file.filename.endswith(".pdf"): perform error handling to make sure the file ends with .pdf
    * text = process_pdf(file): call the functino to extraact all of the text
    * chunks = chunk_text(text): call the chunker to split text into 500 word pieces
    * collection.add(documents = chunks, ids=[...]): store the chunksin ChromaDB but each chunk needs it unique id (it will be names chunk_0, chunk_1, chunk_2)
    * return jsonify({"message": ...}): send a success message with how mnany chunks were stored
"""

@app.route("/upload", methods=["POST"])

def upload():
    if "file" not in request.files"
        return jsonify("{error": "No file was uploaded"}), 400
    
    file = request.files["file"]

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Sorry, only PDF files are supported"}), 400
    
    text = process_pdf(file)
    chunks = chunk_text(text)

    collection.add(
        documents = chunks,
        ids = [f"chunk_{i}" for i in range(len(chunks))]
    )

    return jsonify({"message": f"Document was processed! {len(chunks)} chunks stored."})

"""
Create the chat route and . The

This is the point in the app where:
    * 
"""

@app.route("/chat", methods=["POST"])

def chat():

    data = request.json
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    # (1) RETREIVAL: find the most relevant chunks from ChromeDB
    results = collection.query(
        # Get the top 3 most relevant pieces of text
        query_texts = [user_query], n_results = 3
    )

    # Flatten or collasp the results into one string of context
    context = " ".join(result["documents"][0])

    # (2) GENERATION: Send the context + question to OpenAI
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        message = [
            {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer the user's question. If the answer isn't in the context, say you don't know."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_query}"}
        ]
    )

    answer = response.choice[0].message.content
    return jsonify({"answer": answer})

@app.route("/")

def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
