import os
import io
import time
import base64
import streamlit as st
from src.transcribe import transcribe_episode
from src.index import Indexer
from src.search import QueryEngine

st.set_page_config(page_title="Podcast RAG Search", layout="wide")
if "index" not in st.session_state:
    st.session_state.index = Indexer(persist_dir="store")
if "engine" not in st.session_state:
    st.session_state.engine = QueryEngine(persist_dir="store")

st.title("Audio-to-Text RAG for Podcast Search")
with st.sidebar:
    st.header("Episodes")
    uploaded = st.file_uploader("Upload audio files", type=["mp3","wav","m4a"], accept_multiple_files=True)
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    if uploaded:
        for f in uploaded:
            path = os.path.join(data_dir, f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
        st.success("Uploaded")
    model_size = st.selectbox("ASR model", ["tiny","base","small","medium","large-v3"], index=2)
    build = st.button("Build Index")
    clear = st.button("Clear Index")

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("Episodes in data/")
    eps = [p for p in os.listdir("data") if p.lower().endswith((".mp3",".wav",".m4a"))]
    if not eps:
        st.info("Add audio files to the data/ folder or upload from the sidebar.")
    else:
        for e in eps:
            st.write(e)

with col2:
    st.subheader("Search")
    q = st.text_input("Ask a topic or question")
    k = st.slider("Top K", 1, 10, 5)
    if q:
        results = st.session_state.engine.search(q, top_k=k)
        for r in results:
            with st.container(border=True):
                st.markdown(f"**Episode:** {r['metadata'].get('episode','')}")
                st.markdown(f"**Timestamp:** {r['metadata'].get('start_time',0):.2f}s – {r['metadata'].get('end_time',0):.2f}s")
                st.markdown(r['text'])
                audio_path = r['metadata'].get('audio_path','')
                if os.path.exists(audio_path):
                    with open(audio_path, "rb") as af:
                        b64 = base64.b64encode(af.read()).decode()
                        st.markdown(f'<audio controls src="data:audio/mpeg;base64,{b64}"></audio>', unsafe_allow_html=True)

if clear:
    st.session_state.index.reset()
    st.session_state.engine.refresh()
    st.success("Cleared")

if build:
    eps = [p for p in os.listdir("data") if p.lower().endswith((".mp3",".wav",".m4a"))]
    if not eps:
        st.warning("No audio files found")
    else:
        for e in eps:
            audio_path = os.path.join("data", e)
            st.write(f"Transcribing {e}...")
            segs = transcribe_episode(audio_path, model_size=model_size)
            st.write(f"Indexing {e}...")
            st.session_state.index.add_episode(episode_id=e, audio_path=audio_path, segments=segs)
        st.session_state.index.persist()
        st.session_state.engine.refresh()
        st.success("Index built")