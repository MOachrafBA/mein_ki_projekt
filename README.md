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
git clone <MEIN_GITHUB_REPOSITORY_LINK>
cd mein_ki_projekt

# 2. Virtuelle Umgebung erstellen
python -m venv .venv

# 3. Aktivieren
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (cmd.exe):
.\.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate

# 4. Abhängigkeiten installieren
pip install -r requirements.txt

# 5. Optional: Ollama-Modell ziehen
ollama pull qwen2.5:3b

# 6. Skript starten
python app.py


## Eigene PDF verwenden
- Hinweis: PDF-Dateien sind in diesem Repository per `.gitignore` ausgeschlossen. Das bedeutet, dass meine lokale PDF ( in dem Fall: `Bacheloarbeit_Mohamed_Achraf_Badaoui_638071.pdf`) nicht ins Git-Repository hochgeladen wird.
- Vorgehen:
	- Kopiere deine eigene PDF in das Projektverzeichnis.
	- Passe in `app.py` die Variable `PDF_FILE` an den Dateinamen deiner PDF an, oder benenne deine Datei entsprechend.
	- Optional: Setze eine Umgebungsvariable `PDF_FILE` und erweitere `app.py`, um diese zu lesen, falls du mehrere PDFs verwenden möchtest.
