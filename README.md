# Local RAG System for Document Analysis

Ein funktionsfähiges **Retrieval-Augmented Generation (RAG)** System, das Dokumente lokal verarbeitet, indexiert und mittels eines Large Language Models (LLM) abfragbar macht. 

## Technologie Stack
* **Python 3.14**
* **ChromaDB**: Lokale Vektordatenbank (Embedded Vektorstore)
* **Sentence-Transformers (`all-MiniLM-L6-v2`)**: Generierung der semantischen Einbettungen (Embeddings)
* **Ollama (`qwen2.5:3b`)**: Lokale KI-Inferenz für datenschutzkonforme Antworten
* **LangChain & PyPDF**: Dokumenten-Parsing und rekursives Text-Splitting

## Funktionsweise
1. **Parsing & Chunking**: PDFs werden eingelesen und mittels `RecursiveCharacterTextSplitter` in semantisch sinnvolle Häppchen (1000 Zeichen, 200 Zeichen Overlap) zerlegt.
2. **Vector Ingestion**: Die Chunks werden vektorisiert und persistent in einer lokalen ChromaDB gespeichert.
3. **Retrieval & Generation**: Bei einer Benutzeranfrage sucht ChromaDB die Top-5 relevantesten Textstellen heraus. Ollama generiert basierend *ausschließlich* auf diesem Kontext die finale Antwort.

## Installation & Start
```bash
# 1. Repository klonen
git clone <DEIN_GITHUB_REPOSITORY_LINK>
cd mein_ki_projekt

# 2. Virtuelle Umgebung erstellen & aktivieren
python -m venv .venv
source .venv/bin/Scripts/activate  # Unter Windows: .venv\Scripts\activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Skript starten
python app.py