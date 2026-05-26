import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions
import ollama

PDF_FILE = "Bacheloarbeit_Mohamed_Achraf_Badaoui_638071.pdf"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "bachelorarbeit_index"
MODEL_NAME = "qwen2.5:3b"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

#-- PDF laden und in Chunks aufteilen
def get_chunk_from_pdf(file_path):
    print ("Lade PDF und extrahiere Text...")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_text(text)

#-- ChromaDB initialisieren und befüllen
def setup_vector_db(chunks):
    print("Initialisiere ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)

    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=sentence_transformer_ef)

    if collection.count() == 0:
        print(f"Generiere Embeddings und speichere {len(chunks)} Chunks in ChromaDB...")
        ids = [f"id_{i}" for i in range(len(chunks))]
        collection.add(documents=chunks, ids=ids)
        print("ChromaDB erfolgreich befüllt.")
    else:
        print("ChromaDB enthält bereits Daten. Überspringe Ingestion.")

    return collection

#-- Abfrage Pipeline für RAG
def ask_question(collection, user_query):
    print(f"\nSuche in der Bachelorarbeit nach: '{user_query}'....")

    results = collection.query(query_texts=[user_query], n_results=5)

    context = "\n\n".join(results['documents'][0])

    #-- Prompt
    prompt = f"""
Du bist ein KI-Assistent. Beantworte die Frage des Nutzers AUSSCHLIESSLICH basierend auf dem bereitgestellten Kontext aus Mohamed Achraf Badaoui Bachelorarbeit.
Wenn die Antwort nicht im Kontext zu finden ist, antworte höflich mit "Diese Information ist in der Bachelorarbeit nicht enthalten."

Kontext:
{context}

Frage: {user_query}
Antwort:
"""

    #-- Anfrage an Ollama senden
    print("Ollama generiert Antwort....")
    response = ollama.chat(
        model= MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']

def main():
    chunks = get_chunk_from_pdf(PDF_FILE)
    if not chunks:
        print("Fehler: Konnte den PDF-Inhalt nicht extrahieren.")
        return

    collection = setup_vector_db(chunks)

    print("\n RAG-System bereit! Du kannst jetzt Fragen zur Bachelorarbeit stellen.")
    while True:
        user_query = input("\nStelle eine Frage zur Bachelorarbeit (oder 'exit' zum Beenden): ")
        if user_query.lower() == "exit":
            print("Programm wird beendet.")
            break
        if user_query.strip() == "":
            print("Bitte gib eine gültige Frage ein.")
            continue

        answer = ask_question(collection, user_query)
        print(f"\nAntwort: {answer}")
        print("-" * 50)


if __name__ == "__main__":
    main()
