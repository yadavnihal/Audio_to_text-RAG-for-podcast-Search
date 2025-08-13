# Audio-to-Text RAG for Podcast Search

## 📌 Project Overview
This project implements a **multimodal Retrieval-Augmented Generation (RAG) system** designed for podcasts.  
It converts audio episodes into **searchable text** and allows users to query topics across **multiple episodes**, retrieving precise timestamps and relevant context.

## 🚀 Features
- 🎙 **Audio-to-Text Conversion** – High-accuracy transcription of podcast episodes.
- 🔍 **Searchable Text Indexing** – Efficient indexing for multi-episode search.
- 🧠 **Context-Aware Retrieval** – Uses RAG to provide meaningful responses.
- ⏱ **Timestamp Mapping** – Direct jump to the exact moment in the audio.
- 📚 **Cross-Episode Topic Search** – Search for a topic across the entire podcast series.

## 🛠 Tech Stack
- **Speech-to-Text:** Whisper / SpeechRecognition API
- **Vector Database:** ChromaDB / Pinecone / Weaviate
- **Embedding Models:** OpenAI / HuggingFace Sentence Transformers
- **Framework:** Streamlit / Gradio
- **Language:** Python
- **Deployment:** HuggingFace Spaces / Streamlit Cloud

## 📂 Project Structure
📦 Audio-to-Text-RAG
┣ 📂 data # Podcast audio files

┣ 📂 transcripts # Generated transcripts

┣ 📂 embeddings # Vector embeddings for search

┣ 📜 app.py # Main application file

┣ 📜 requirements.txt # Dependencies

┗ 📜 README.md # Documentation


## ⚙️ How It Works
1. **Audio Preprocessing** – Clean and prepare podcast audio files (noise reduction).
2. **Speech-to-Text Conversion** – Convert audio into text with timestamps.
3. **Chunking & Embedding** – Split transcripts into chunks and generate embeddings.
4. **Vector Search** – Store embeddings in a vector DB for fast retrieval.
5. **Query Processing** – Accept user queries, retrieve relevant segments, and display timestamps.
6. **Contextual Response Generation** – Use RAG to provide meaningful responses.

## 📊 Evaluation Metrics
- Retrieval Accuracy
- Latency
- RAGAS Score


