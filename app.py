
"""
File Vault - a Streamlit UI for basic file CRUD operations.
Run with:  streamlit run app.py
"""
 
from datetime import datetime
from pathlib import Path
 
import streamlit as st
 
# ---------------------------------------------------------------- config
st.set_page_config(page_title="File Vault", page_icon="🗂️", layout="wide")
 
STORAGE = Path("vault")  # every file lives inside this folder
STORAGE.mkdir(exist_ok=True)
 
# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');
 
:root {
    --paper: #EEF2F7;
    --ink: #14213D;
    --muted: #5B6B86;
    --blue: #2F5BEA;
    --mint: #1E9E76;
    --rose: #D6455D;
    --line: #D5DDEA;
}
 
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; color: var(--ink); }
.stApp { background: var(--paper); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.2rem; max-width: 1100px; }
 
h1, h2, h3 { font-family: 'Bricolage Grotesque', sans-serif !important; letter-spacing: -0.02em; }
 
.hero { margin-bottom: 1.6rem; }
.hero h1 { font-size: 3.1rem; font-weight: 800; margin: 0; line-height: 1.05; }
.hero p { color: var(--muted); font-size: 1.05rem; margin: .5rem 0 0 0; max-width: 46ch; }
 
/* sidebar */
section[data-testid="stSidebar"] { background: var(--ink); }
section[data-testid="stSidebar"] * { color: #E8EDF7; }
.side-title { font-family: 'Bricolage Grotesque'; font-size: 1.3rem; font-weight: 700; margin-bottom: .2rem; }
.side-stats { display: flex; gap: .6rem; margin: .8rem 0 1.2rem 0; }
.side-stat { flex: 1; background: rgba(255,255,255,.07); border-radius: 10px; padding: .6rem .8rem; }
.side-stat b { display: block; font-family: 'Bricolage Grotesque'; font-size: 1.5rem; }
.side-stat span { font-size: .78rem; color: #9FB0CF !important; }
.file-row { display: flex; justify-content: space-between; padding: .45rem 0;
            border-bottom: 1px solid rgba(255,255,255,.08); font-family: 'IBM Plex Mono'; font-size: .82rem; }
.file-row span:last-child { color: #9FB0CF; }
 
/* tabs */
.stTabs [data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { font-weight: 600; padding: .6rem 1.1rem; border-radius: 8px 8px 0 0; }
.stTabs [aria-selected="true"] { color: var(--blue) !important; }
 
/* inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div {
    background: #fff; border: 1px solid var(--line); border-radius: 10px;
}
.stTextArea textarea { font-family: 'IBM Plex Mono', monospace; font-size: .9rem; }
 
/* buttons */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background: var(--blue); color: #fff; border: 0; border-radius: 10px;
    padding: .55rem 1.3rem; font-weight: 600;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { background: #2348C0; color: #fff; }
.stButton > button:focus-visible { outline: 3px solid #9DB4FF; }
.danger .stButton > button { background: var(--rose); }
.danger .stButton > button:hover { background: #B5334A; }
 
.meta { font-family: 'IBM Plex Mono'; font-size: .8rem; color: var(--muted); margin: .2rem 0 .8rem 0; }
.empty { border: 1.5px dashed var(--line); border-radius: 14px; padding: 2rem; text-align: center;
         color: var(--muted); background: rgba(255,255,255,.5); }
</style>
""",
    unsafe_allow_html=True,
)
 
 
# ---------------------------------------------------------------- helpers
def safe_path(name: str):
    """Keep every file inside the vault (blocks '../' tricks)."""
    clean = Path(name.strip()).name
    return STORAGE / clean if clean else None
 
 
def list_files():
    files = [p for p in STORAGE.iterdir() if p.is_file()]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)
 
 
def fmt_size(num: int) -> str:
    for unit in ("B", "KB", "MB"):
        if num < 1024:
            return f"{num:.0f} {unit}" if unit == "B" else f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} GB"
 
 
def modified(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%d %b %Y, %H:%M")
 
 
 
def flash(message: str):
    """Show a success message after the page refreshes (keeps the sidebar in sync)."""
    st.session_state["flash"] = message
    st.rerun()
 
 
def empty_state(text: str):
    st.markdown(f'<div class="empty">{text}</div>', unsafe_allow_html=True)
 
 
# ---------------------------------------------------------------- sidebar
files = list_files()
total_bytes = sum(p.stat().st_size for p in files)
 
with st.sidebar:
    st.markdown('<div class="side-title">🗂️ Your vault</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="side-stats">
            <div class="side-stat"><b>{len(files)}</b><span>files</span></div>
            <div class="side-stat"><b>{fmt_size(total_bytes)}</b><span>used</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if files:
        rows = "".join(
            f'<div class="file-row"><span>{p.name}</span><span>{fmt_size(p.stat().st_size)}</span></div>'
            for p in files
        )
        st.markdown(rows, unsafe_allow_html=True)
    else:
        st.caption("Nothing here yet. Create your first file.")
 
# ---------------------------------------------------------------- header
st.markdown(
    """
    <div class="hero">
        <h1>File Vault</h1>
        <p>Create, read, update and delete text files from one clean screen.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
 
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))
 
tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["Create", "Read", "Update", "Delete"]
)
 
# ---------------------------------------------------------------- CREATE
with tab_create:
    st.subheader("Create a file")
    with st.form("create_form"):
        name = st.text_input("File name", placeholder="notes.txt")
        content = st.text_area("Content", height=220, placeholder="Start typing...")
        submitted = st.form_submit_button("Create file")
 
    if submitted:
        path = safe_path(name)
        if path is None:
            st.error("Enter a file name.")
        elif path.exists():
            st.error(f"'{path.name}' already exists. Pick another name or use the Update tab.")
        else:
            try:
                path.write_text(content, encoding="utf-8")
                flash(f"Created '{path.name}'.")
            except Exception as err:
                st.error(f"Could not create the file: {err}")
 
# ---------------------------------------------------------------- READ
with tab_read:
    st.subheader("Read a file")
    files = list_files()
    if not files:
        empty_state("No files yet. Create one in the Create tab.")
    else:
        choice = st.selectbox("Choose a file", [p.name for p in files], key="read_choice")
        path = STORAGE / choice
        try:
            text = path.read_text(encoding="utf-8")
            st.markdown(
                f'<div class="meta">{fmt_size(path.stat().st_size)} &nbsp;|&nbsp; '
                f"modified {modified(path)}</div>",
                unsafe_allow_html=True,
            )
            if text:
                st.code(text, language=None, line_numbers=True)
            else:
                empty_state("This file is empty.")
            st.download_button("Download", data=text, file_name=path.name)
        except UnicodeDecodeError:
            st.error("This file is not plain text, so it can't be displayed.")
        except Exception as err:
            st.error(f"Could not read the file: {err}")
 
# ---------------------------------------------------------------- UPDATE
with tab_update:
    st.subheader("Update a file")
    files = list_files()
    if not files:
        empty_state("No files yet. Create one in the Create tab.")
    else:
        choice = st.selectbox("Choose a file", [p.name for p in files], key="update_choice")
        path = STORAGE / choice
        action = st.radio(
            "What do you want to do?",
            ["Rename", "Append text", "Overwrite"],
            horizontal=True,
        )
 
        if action == "Rename":
            new_name = st.text_input("New file name", key="rename_input")
            if st.button("Rename file"):
                new_path = safe_path(new_name)
                if new_path is None:
                    st.error("Enter a new file name.")
                elif new_path.exists():
                    st.error(f"'{new_path.name}' already exists.")
                else:
                    try:
                        path.rename(new_path)
                        flash(f"Renamed to '{new_path.name}'.")
                    except Exception as err:
                        st.error(f"Could not rename the file: {err}")
 
        elif action == "Append text":
            extra = st.text_area("Text to add at the end", height=160, key="append_input")
            if st.button("Append text"):
                if not extra:
                    st.error("Enter some text to append.")
                else:
                    try:
                        with open(path, "a", encoding="utf-8") as fs:
                            fs.write("\n" + extra)
                        flash(f"Added text to '{path.name}'.")
                    except Exception as err:
                        st.error(f"Could not append: {err}")
 
        else:
            try:
                current = path.read_text(encoding="utf-8")
            except Exception:
                current = ""
            new_text = st.text_area(
                "New content (replaces everything)", value=current, height=220, key=f"over_{choice}"
            )
            if st.button("Overwrite file"):
                try:
                    path.write_text(new_text, encoding="utf-8")
                    flash(f"Overwrote '{path.name}'.")
                except Exception as err:
                    st.error(f"Could not overwrite: {err}")
 
# ---------------------------------------------------------------- DELETE
with tab_delete:
    st.subheader("Delete a file")
    files = list_files()
    if not files:
        empty_state("Nothing to delete.")
    else:
        choice = st.selectbox("Choose a file", [p.name for p in files], key="delete_choice")
        path = STORAGE / choice
        st.markdown(
            f'<div class="meta">{fmt_size(path.stat().st_size)} &nbsp;|&nbsp; '
            f"modified {modified(path)}</div>",
            unsafe_allow_html=True,
        )
        sure = st.checkbox(f"Yes, permanently delete '{choice}'")
        st.markdown('<div class="danger">', unsafe_allow_html=True)
        if st.button("Delete file", disabled=not sure):
            try:
                path.unlink()
                flash(f"Deleted '{choice}'.")
            except Exception as err:
                st.error(f"Could not delete the file: {err}")
        st.markdown("</div>", unsafe_allow_html=True)