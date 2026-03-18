import streamlit as st
import sys
import os
import time

# app.py lives inside backend/ — add backend/ to path so all submodules resolve
_HERE = os.path.dirname(os.path.abspath(__file__))   # .../backend
_ROOT = os.path.dirname(_HERE)                        # project root
for _p in [_HERE, _ROOT]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

os.environ.setdefault("TOP_K", "3")

# Load .env early so qa_pipeline module-level code finds GOOGLE_API_KEY on import
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Learn Mate",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --card:      #16161f;
    --border:    #2a2a3a;
    --accent:    #6c63ff;
    --accent2:   #00e5ff;
    --accent3:   #ff6b9d;
    --text:      #e8e8f0;
    --muted:     #6b6b80;
    --success:   #00c896;
    --warning:   #ffb347;
    --mono:      'Space Mono', monospace;
    --sans:      'DM Sans', sans-serif;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg);
    color: var(--text);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent2);
    border: 1px solid var(--accent2);
    padding: 0.3rem 0.9rem;
    border-radius: 2px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: var(--mono);
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 60%, var(--accent3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem;
    line-height: 1.1;
}
.hero p {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── Section Labels ── */
.section-label {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Cards ── */
.info-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
}
.info-card .label {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

/* ── Status Pills ── */
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    font-family: var(--mono);
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.pill-green  { background: rgba(0,200,150,.12); color: var(--success); border: 1px solid rgba(0,200,150,.3); }
.pill-blue   { background: rgba(108,99,255,.12); color: var(--accent);  border: 1px solid rgba(108,99,255,.3); }
.pill-orange { background: rgba(255,179,71,.12); color: var(--warning); border: 1px solid rgba(255,179,71,.3); }
.pill-pink   { background: rgba(255,107,157,.12); color: var(--accent3); border: 1px solid rgba(255,107,157,.3); }

/* ── Answer box ── */
.answer-box {
    background: linear-gradient(135deg, rgba(108,99,255,.06), rgba(0,229,255,.04));
    border: 1px solid rgba(108,99,255,.35);
    border-left: 3px solid var(--accent);
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
    font-size: 0.95rem;
    line-height: 1.75;
    color: var(--text);
    margin-top: 1rem;
}

/* ── Source cards ── */
.source-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 0.65rem 1rem;
    margin-bottom: 0.5rem;
    transition: border-color .2s;
}
.source-item:hover { border-color: var(--accent2); }
.source-icon {
    font-size: 1rem;
    width: 28px;
    text-align: center;
    flex-shrink: 0;
}
.source-link {
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--accent2);
    text-decoration: none;
    word-break: break-all;
}

/* ── Pipeline steps ── */
.pipeline-step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--border);
}
.pipeline-step:last-child { border-bottom: none; }
.step-num {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--muted);
    width: 20px;
    flex-shrink: 0;
    padding-top: 2px;
}
.step-text { font-size: 0.85rem; color: var(--text); }
.step-sub  { font-size: 0.75rem; color: var(--muted); margin-top: 0.15rem; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 5px !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 5px !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity .2s, transform .1s !important;
}
.stButton > button:hover {
    opacity: .85 !important;
    transform: translateY(-1px) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--card);
    border: 1px dashed var(--border);
    border-radius: 6px;
    padding: 0.5rem;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}

/* ── Progress / spinner ── */
.stProgress > div > div > div { background: var(--accent) !important; }

/* ── Metric ── */
[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.8rem 1rem;
}

/* ── Link buttons (sources) ── */
[data-testid="stLinkButton"] > a {
    background: var(--card) !important;
    color: var(--accent2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    font-family: var(--mono) !important;
    font-size: 0.73rem !important;
    letter-spacing: 0.03em !important;
    text-transform: none !important;
    padding: 0.4rem 0.9rem !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
[data-testid="stLinkButton"] > a:hover {
    border-color: var(--accent2) !important;
    background: rgba(0,229,255,.06) !important;
    color: var(--accent2) !important;
}

/* ── Toast-style notice ── */
.notice {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.05em;
    padding: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Session State ──────────────────────────────────────────────────────────────
for key, default in {
    "pipeline_ready": False,
    "embedded_docs": None,
    "doc_summary": {},
    "chat_history": [],
    "processing": False,
    "yt_inputs": [""],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


@st.cache_resource
def load_qa_modules():
    """Import QA modules once and cache — prevents repeated module-level execution."""
    from rag.qa_pipeline import qa_pipeline
    from rag.citation_handler import format_citations
    return qa_pipeline, format_citations


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_link_from_source(citation) -> str:
    """Extract link from a format_citations() dict."""
    if isinstance(citation, dict):
        ctype = citation.get("type", "")
        if ctype == "YouTube":
            return citation.get("link", "")
        elif ctype == "PDF":
            # citation["file"] comes from meta.get("file_name") in citation_handler
            # but actual metadata key is "filename" — so also check raw metadata
            return citation.get("file", "") or citation.get("filename", "")
        return citation.get("link", citation.get("display", str(citation)))
    return str(citation)

def is_youtube(link: str) -> bool:
    return "youtube.com" in link or "youtu.be" in link


def source_icon(link: str) -> str:
    if is_youtube(link):
        return "▶"
    if link.lower().endswith(".pdf") or "pdf" in link.lower():
        return "📄"
    return "🔗"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label">System</div>', unsafe_allow_html=True)

    if st.session_state.pipeline_ready:
        st.markdown(
            '<span class="pill pill-green">● PIPELINE READY</span>',
            unsafe_allow_html=True,
        )
        s = st.session_state.doc_summary
        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(2)
        with cols[0]:
            st.metric("PDFs", s.get("pdf_count", "—"))
        with cols[1]:
            st.metric("Videos", s.get("youtube_count", "—"))

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="info-card"><div class="label">Total chunks</div>{s.get("total_chunks","—")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="info-card"><div class="label">Embedded docs</div>{s.get("embedded_count","—")}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↺  Reset pipeline"):
            for k in ("pipeline_ready", "embedded_docs", "doc_summary", "chat_history", "processing"):
                st.session_state[k] = False if isinstance(st.session_state[k], bool) else (
                    [] if isinstance(st.session_state[k], list) else
                    ({} if isinstance(st.session_state[k], dict) else None)
                )
            st.rerun()
    else:
        st.markdown(
            '<span class="pill pill-orange">○ NOT READY</span>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="notice">Add sources in the main panel and run the pipeline to enable Q&A.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Pipeline Steps</div>', unsafe_allow_html=True)
    steps = [
        ("01", "Load Sources", "PDFs + YouTube transcripts"),
        ("02", "Clean", "Normalise & de-noise text"),
        ("03", "Chunk", "Split into semantic windows"),
        ("04", "Embed", "Vector representations"),
        ("05", "QA", "Retrieve & generate answers"),
    ]
    for num, title, sub in steps:
        st.markdown(
            f"""<div class="pipeline-step">
                  <span class="step-num">{num}</span>
                  <div><div class="step-text">{title}</div>
                  <div class="step-sub">{sub}</div></div>
                </div>""",
            unsafe_allow_html=True,
        )


# ── Main Layout ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">Your AI Study Companion</div>
  <h1>Learn Mate</h1>
  <p>Multi-source knowledge extraction · PDF &amp; Video · Semantic Q&amp;A</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_ingest, tab_qa = st.tabs(["⬆  Sources & Ingest", "💬  Ask Questions"])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — INGEST
# ═══════════════════════════════════════════════════════════════════════════════
with tab_ingest:
    col_pdf, col_yt = st.columns(2, gap="large")

    # ── PDF column ────────────────────────────────────────────────────────────
    with col_pdf:
        st.markdown('<div class="section-label">PDF Documents</div>', unsafe_allow_html=True)
        uploaded_pdfs = st.file_uploader(
            "Drop PDFs here",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload one or more PDF files to include in the knowledge base.",
            label_visibility="collapsed",
        )
        if uploaded_pdfs:
            for f in uploaded_pdfs:
                st.markdown(
                    f'<div class="info-card">📄 <strong>{f.name}</strong>'
                    f'<span style="float:right;color:var(--muted);font-size:.75rem">'
                    f'{f.size/1024:.1f} KB</span></div>',
                    unsafe_allow_html=True,
                )

    # ── YouTube column ────────────────────────────────────────────────────────
    with col_yt:
        st.markdown('<div class="section-label">YouTube Videos</div>', unsafe_allow_html=True)

        def render_yt_inputs():
            for i, url in enumerate(st.session_state.yt_inputs):
                cols = st.columns([10, 1])
                with cols[0]:
                    new_val = st.text_input(
                        f"URL {i+1}",
                        value=url,
                        key=f"yt_{i}",
                        placeholder="https://www.youtube.com/watch?v=...",
                        label_visibility="collapsed",
                    )
                    st.session_state.yt_inputs[i] = new_val
                with cols[1]:
                    if len(st.session_state.yt_inputs) > 1:
                        if st.button("✕", key=f"del_{i}"):
                            st.session_state.yt_inputs.pop(i)
                            st.rerun()

        render_yt_inputs()

        if st.button("+ Add another URL"):
            st.session_state.yt_inputs.append("")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Run pipeline ─────────────────────────────────────────────────────────
    col_btn, col_hint = st.columns([3, 7])
    with col_btn:
        run_btn = st.button("▶  Run Pipeline", use_container_width=True)
    with col_hint:
        st.markdown(
            '<div class="notice" style="padding-top:.9rem">Loads, cleans, chunks, and embeds all sources.</div>',
            unsafe_allow_html=True,
        )

    if run_btn:
        yt_urls = [u.strip() for u in st.session_state.yt_inputs if u.strip()]
        pdf_paths = []

        # Save uploaded PDFs to temp files
        if uploaded_pdfs:
            import tempfile, shutil
            tmp_dir = tempfile.mkdtemp()
            for f in uploaded_pdfs:
                tmp_path = os.path.join(tmp_dir, f.name)
                with open(tmp_path, "wb") as out:
                    out.write(f.read())
                pdf_paths.append(tmp_path)

        if not pdf_paths and not yt_urls:
            st.error("Please add at least one PDF or YouTube URL before running.")
        else:
            try:
                from ingestion.document_manager import DocumentManager
                from processing.transcript_cleaner import clean_documents
                from processing.chunking import chunk_documents
                from embeddings.embedding_model import EmbeddingModel

                progress_bar = st.progress(0, text="Starting pipeline…")

                with st.status("Running pipeline…", expanded=True) as status:

                    # Step 0 — Load
                    st.write("📥 Loading sources — may take a moment for YouTube videos…")
                    progress_bar.progress(5, text="📥  Loading sources…")
                    manager = DocumentManager()
                    documents = manager.load_all_sources(
                        pdf_paths=pdf_paths,
                        youtube_urls=yt_urls,
                    )
                    progress_bar.progress(20, text="📥  Sources loaded!")
                    st.write(f"✅ Loaded {len(documents)} document(s)")

                    if not documents:
                        status.update(label="❌ No documents loaded", state="error")
                        progress_bar.empty()
                        st.stop()

                    raw_summary = manager.summarize(documents)

                    # Step 1 — Clean
                    st.write("🧹 Cleaning and normalising text…")
                    progress_bar.progress(30, text="🧹  Cleaning text…")
                    clean_docs = clean_documents(documents)
                    progress_bar.progress(45, text="🧹  Text cleaned!")
                    st.write("✅ Text cleaned")

                    # Step 2 — Chunk
                    st.write("✂️ Chunking documents…")
                    progress_bar.progress(50, text="✂️  Chunking…")
                    chunks = chunk_documents(clean_docs)
                    progress_bar.progress(62, text=f"✂️  {len(chunks)} chunks created!")
                    st.write(f"✅ Created {len(chunks)} chunks")

                    # Step 3 — Embed
                    st.write("🧠 Generating embeddings — this is the slow step…")
                    progress_bar.progress(65, text="🧠  Embedding…")
                    embedding_model = EmbeddingModel()
                    embedded_docs = embedding_model.embed_documents(chunks)
                    progress_bar.progress(95, text="🧠  Embeddings ready!")
                    st.write(f"✅ Embedded {len(embedded_docs)} documents")

                    # Done
                    progress_bar.progress(100, text="✅  Pipeline complete!")
                    status.update(label="✅ Pipeline complete — go to Ask Questions tab!", state="complete", expanded=False)

                st.session_state.embedded_docs = embedded_docs
                st.session_state.pipeline_ready = True
                st.session_state.doc_summary = {
                    "pdf_count":      len(pdf_paths),
                    "youtube_count":  len(yt_urls),
                    "total_chunks":   len(chunks),
                    "embedded_count": len(embedded_docs),
                }

                time.sleep(1.2)
                st.rerun()

            except Exception as e:
                progress_bar.empty()
                st.error(f"❌ Pipeline error: {e}")
                st.exception(e)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Q&A
# ═══════════════════════════════════════════════════════════════════════════════
with tab_qa:
    if not st.session_state.pipeline_ready:
        st.markdown(
            '<div class="answer-box" style="border-left-color:var(--warning);text-align:center;color:var(--muted)">'
            'Pipeline not ready. Add sources and run ingest first.'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        # Chat history
        if st.session_state.chat_history:
            st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)
            for entry in st.session_state.chat_history:
                # User bubble
                st.markdown(
                    f'<div style="text-align:right;margin-bottom:.5rem">'
                    f'<span style="background:rgba(108,99,255,.18);border:1px solid rgba(108,99,255,.3);'
                    f'border-radius:16px 16px 4px 16px;padding:.45rem 1rem;display:inline-block;'
                    f'font-size:.88rem;max-width:80%">{entry["question"]}</span></div>',
                    unsafe_allow_html=True,
                )
                # Answer
                st.markdown(
                    f'<div class="answer-box">{entry["answer"]}</div>',
                    unsafe_allow_html=True,
                )
                # Sources
                if entry.get("sources"):
                    with st.expander(f"📎  {len(entry['sources'])} source(s)  — click to expand"):
                        for src in entry["sources"]:
                            stype = src.get("type", "")
                            display = src.get("display", "")
                            link = src.get("link", "")
                            fname = src.get("file", "")
                            timestamp = src.get("timestamp", "")

                            if stype == "YouTube" and link:
                                label = f"▶  {display}" if display else link
                                label = label if len(label) <= 70 else label[:67] + "..."
                                st.link_button(label, link, use_container_width=True)
                            elif stype == "PDF":
                                # Use fname (from meta["file_name"]) directly — avoids the
                                # citation_handler "filename" vs "file_name" typo in display
                                # "file" comes from citation_handler's meta.get("file_name")
                                # actual key in metadata is "filename" (no underscore)
                                pdf_label = fname or src.get("filename", "") or src.get("display", "Document")
                                page = src.get("page", "N/A")
                                st.markdown(
                                    f'<div class="source-item">'
                                    f'<span class="source-icon">📄</span>'
                                    f'<span style="font-family:var(--mono);font-size:.75rem;color:var(--text)">'
                                    f'{pdf_label} — Page {page}</span>'
                                    f'</div>',
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.markdown(
                                    f'<div class="source-item">'
                                    f'<span class="source-icon">🔗</span>'
                                    f'<span style="font-family:var(--mono);font-size:.75rem;color:var(--muted)">{display}</span>'
                                    f'</div>',
                                    unsafe_allow_html=True,
                                )
                st.markdown("<br>", unsafe_allow_html=True)

        # Question input
        st.markdown('<div class="section-label">Ask</div>', unsafe_allow_html=True)
        question = st.text_area(
            "Question",
            placeholder="What would you like to know from your documents and videos?",
            height=90,
            label_visibility="collapsed",
        )

        col_ask, col_clear = st.columns([3, 1])
        with col_ask:
            ask_btn = st.button("Ask →", use_container_width=True)
        with col_clear:
            if st.button("Clear history", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        if ask_btn and question.strip():
            with st.spinner("🔍  Searching knowledge base & generating answer…"):
                try:
                    qa_pipeline, format_citations = load_qa_modules()

                    answer, sources = qa_pipeline(
                        question.strip(),
                        st.session_state.embedded_docs,
                    )
                    citations = format_citations(sources)

                    # Build source list directly from retrieved_docs metadata
                    # avoids citation_handler key typos entirely
                    links = []
                    for doc in sources:
                        meta = doc.get("metadata", {})
                        src_type = meta.get("source", "unknown")
                        if src_type == "youtube":
                            links.append({
                                "type": "YouTube",
                                "title": meta.get("title", "YouTube Video"),
                                "timestamp": meta.get("timestamp", "N/A"),
                                "link": meta.get("link", meta.get("video_url", "")),
                                "display": f"{meta.get('title','YouTube Video')} ({meta.get('timestamp','N/A')})"
                            })
                        elif src_type == "pdf":
                            fname = (meta.get("filename")
                                     or meta.get("file_name")
                                     or meta.get("file")
                                     or "Document")
                            page = meta.get("page", "N/A")
                            links.append({
                                "type": "PDF",
                                "file": fname,
                                "page": page,
                                "display": f"{fname} — Page {page}"
                            })
                        else:
                            links.append({
                                "type": src_type,
                                "display": meta.get("title", str(meta))
                            })
                    links = links[:3]

                    # Hide sources if LLM couldn't find answer in context
                    cant_answer = "i don't have enough information" in answer.lower()
                    st.session_state.chat_history.append({
                        "question": question.strip(),
                        "answer":   answer.strip(),
                        "sources":  [] if cant_answer else links,
                    })
                    st.rerun()

                except Exception as e:
                    st.error(f"QA error: {e}")

        elif ask_btn:
            st.warning("Please enter a question.")