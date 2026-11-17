"""File Desk: a Streamlit interface for creating, reading, updating and deleting text files.

All files live inside a ./workspace folder, and file names are sanitised so nothing
outside that folder can be touched. Use the toggle at the top right to switch
between light and dark mode.
"""

from datetime import datetime
from pathlib import Path

import streamlit as st

WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

st.set_page_config(page_title="File Desk", page_icon="🗂️", layout="wide")

# ----------------------------------------------------------------------------
# Themes
# ----------------------------------------------------------------------------
THEMES = {
    "light": {
        "bg": "#EDF1F5",
        "surface": "#FFFFFF",
        "surface2": "#F4F7FA",
        "ink": "#14213D",
        "muted": "#5B6B82",
        "line": "#D5DDE8",
        "accent": "#0F766E",
        "on_accent": "#FFFFFF",
        "danger": "#B42318",
        "on_danger": "#FFFFFF",
        "code_bg": "#F4F7FA",
        "tab_text": "#111111",
    },
    "dark": {
        "bg": "#0E151D",
        "surface": "#16202B",
        "surface2": "#1D2A38",
        "ink": "#E6EDF5",
        "muted": "#93A4B8",
        "line": "#2B3A4A",
        "accent": "#2DD4BF",
        "on_accent": "#06201D",
        "danger": "#F87171",
        "on_danger": "#2A0A08",
        "code_bg": "#0E151D",
        "tab_text": "#E6EDF5",
    },
}

STATIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, .stApp { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: var(--bg) !important; color: var(--ink); }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { padding-top: 2.2rem; max-width: 1180px; }

h1.title {
    font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
    font-size: 2.6rem; letter-spacing: -0.02em; margin: 0 0 .15rem 0; color: var(--ink);
}
p.subtitle { color: var(--muted); font-size: 1.02rem; margin: 0 0 1.6rem 0; max-width: 56ch; }

/* Workspace panel */
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 1.1rem 1.1rem .6rem 1.1rem; }
.panel-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: .7rem; }
.panel-head h3 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.15rem; margin: 0; color: var(--ink); }
.panel-head span { color: var(--muted); font-size: .85rem; }
.file-row { display: flex; justify-content: space-between; gap: .8rem; padding: .55rem 0; border-top: 1px solid var(--line); }
.file-name { font-family: 'IBM Plex Mono', monospace; font-size: .88rem; font-weight: 500; word-break: break-all; color: var(--ink); }
.file-meta { color: var(--muted); font-size: .78rem; white-space: nowrap; text-align: right; }
.empty { color: var(--muted); font-size: .92rem; padding: .6rem 0 1rem 0; border-top: 1px solid var(--line); }

/* Labels and text */
label, label p,
[data-testid="stWidgetLabel"] p, [data-testid="stCheckbox"] p,
[data-testid="stRadio"] p, [data-testid="stToggle"] p { color: var(--ink) !important; }
[data-testid="stCaptionContainer"] { color: var(--muted) !important; }

/* Tabs (selectors avoid class names so they work across Streamlit versions) */
[data-baseweb="tab-list"] { gap: .3rem; }
[role="tab"] { background: transparent !important; opacity: 1 !important; padding: .6rem 1rem !important; }
[role="tab"], [role="tab"] * { color: var(--tab-text) !important; opacity: 1 !important; font-weight: 600 !important; }
[role="tab"]:hover, [role="tab"]:hover * { color: var(--accent) !important; }
[role="tab"][aria-selected="true"], [role="tab"][aria-selected="true"] * { color: var(--accent) !important; }
[role="tab"]:focus, [role="tab"]:focus-visible { outline: none !important; box-shadow: none !important; }
[data-baseweb="tab-highlight"] { background-color: var(--accent) !important; }
[data-baseweb="tab-border"] { background-color: var(--line) !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: var(--surface) !important; color: var(--ink) !important;
    border: 1px solid var(--line) !important; border-radius: 10px !important;
}
.stTextInput [data-baseweb="input"], .stTextArea [data-baseweb="textarea"] {
    background: var(--surface) !important; border-radius: 10px !important; border-color: var(--line) !important;
}
.stTextArea textarea { font-family: 'IBM Plex Mono', monospace; font-size: .9rem; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px var(--accent) !important; }
::placeholder { color: var(--muted) !important; opacity: .8 !important; }

/* Select box and its dropdown */
[data-baseweb="select"] > div { background: var(--surface) !important; border: 1px solid var(--line) !important; border-radius: 10px !important; }
[data-baseweb="select"] * { color: var(--ink) !important; }
[data-baseweb="select"] svg { fill: var(--muted) !important; }
[data-baseweb="popover"] > div, [data-baseweb="popover"] ul { background: var(--surface) !important; }
[data-baseweb="popover"] li, [data-baseweb="popover"] li * { background: var(--surface) !important; color: var(--ink) !important; }
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] { background: var(--surface2) !important; }

/* Buttons: colors are set on the button and its text so they show in both themes */
.stButton button, .stDownloadButton button {
    background: var(--accent) !important; border: 1px solid var(--accent) !important;
    border-radius: 10px !important; padding: .5rem 1.3rem !important; font-weight: 600 !important;
}
.stButton button, .stButton button *, .stDownloadButton button, .stDownloadButton button * { color: var(--on-accent) !important; }
.stButton button:hover, .stDownloadButton button:hover { filter: brightness(.92); }
.stButton button:focus-visible, .stDownloadButton button:focus-visible { outline: 3px solid var(--muted) !important; outline-offset: 2px; }
.stButton button:disabled { background: var(--line) !important; border-color: var(--line) !important; }
.stButton button:disabled, .stButton button:disabled * { color: var(--muted) !important; }

/* Delete button (inside the container keyed "danger_zone") */
.st-key-danger_zone .stButton button { background: var(--danger) !important; border-color: var(--danger) !important; }
.st-key-danger_zone .stButton button, .st-key-danger_zone .stButton button * { color: var(--on-danger) !important; }
.st-key-danger_zone .stButton button:disabled { background: var(--line) !important; border-color: var(--line) !important; }
.st-key-danger_zone .stButton button:disabled, .st-key-danger_zone .stButton button:disabled * { color: var(--muted) !important; }

/* Messages */
[data-testid="stAlert"] { background: var(--surface2) !important; border: 1px solid var(--line); border-radius: 10px; }
[data-testid="stAlert"], [data-testid="stAlert"] * { color: var(--ink) !important; }

/* Buttons by test id, for Streamlit versions where the .stButton class is missing */
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-primary"], [data-testid="stDownloadButton"] button {
    background: var(--accent) !important; border: 1px solid var(--accent) !important;
    border-radius: 10px !important; padding: .5rem 1.3rem !important; font-weight: 600 !important;
}
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondary"] *,
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primary"] *,
[data-testid="stDownloadButton"] button, [data-testid="stDownloadButton"] button * { color: var(--on-accent) !important; }
[data-testid="stBaseButton-secondary"]:disabled { background: var(--line) !important; border-color: var(--line) !important; }
[data-testid="stBaseButton-secondary"]:disabled, [data-testid="stBaseButton-secondary"]:disabled * { color: var(--muted) !important; }
.st-key-danger_zone [data-testid="stBaseButton-secondary"] { background: var(--danger) !important; border-color: var(--danger) !important; }
.st-key-danger_zone [data-testid="stBaseButton-secondary"], .st-key-danger_zone [data-testid="stBaseButton-secondary"] * { color: var(--on-danger) !important; }
.st-key-danger_zone [data-testid="stBaseButton-secondary"]:disabled { background: var(--line) !important; border-color: var(--line) !important; }
.st-key-danger_zone [data-testid="stBaseButton-secondary"]:disabled, .st-key-danger_zone [data-testid="stBaseButton-secondary"]:disabled * { color: var(--muted) !important; }

/* Code viewer */
[data-testid="stCode"] { border: 1px solid var(--line); border-radius: 10px; }
[data-testid="stCode"] pre, [data-testid="stCode"] pre * { background: var(--code_bg) !important; color: var(--ink) !important; }
</style>
"""


def apply_theme(mode: str):
    colors = THEMES[mode]
    variables = "".join(f"--{key.replace('_', '-')}: {value};" for key, value in colors.items())
    # The code viewer rule uses --code_bg, so define that name too.
    variables += f"--code_bg: {colors['code_bg']};"
    st.markdown(f"<style>:root {{{variables}}}</style>", unsafe_allow_html=True)
    st.markdown(STATIC_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def safe_path(name: str):
    """Return a path inside the workspace, or None if the name is not allowed."""
    name = name.strip()
    if not name or name in {".", ".."} or name != Path(name).name:
        return None
    return WORKSPACE / name


def list_files():
    files = [p for p in WORKSPACE.iterdir() if p.is_file()]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB"):
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def flash(kind: str, message: str):
    st.session_state["flash"] = (kind, message)
    st.rerun()


def show_flash():
    if "flash" in st.session_state:
        kind, message = st.session_state.pop("flash")
        getattr(st, kind)(message)


def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


# ----------------------------------------------------------------------------
# Header with theme toggle
# ----------------------------------------------------------------------------
head_left, head_right = st.columns([5, 1])
with head_right:
    dark_mode = st.toggle("Dark mode", value=False, key="dark_mode")

apply_theme("dark" if dark_mode else "light")

with head_left:
    st.markdown('<h1 class="title">File Desk</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Create, read, update and delete text files in a safe workspace folder.</p>',
        unsafe_allow_html=True,
    )

left, right = st.columns([1, 2], gap="large")

# ---- File explorer ----------------------------------------------------------
with left:
    files = list_files()
    total = sum(p.stat().st_size for p in files)
    rows = ""
    for p in files:
        stat = p.stat()
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%d %b, %H:%M")
        rows += (
            f'<div class="file-row"><div class="file-name">{p.name}</div>'
            f'<div class="file-meta">{human_size(stat.st_size)}<br>{modified}</div></div>'
        )
    if not files:
        rows = '<div class="empty">No files yet. Create your first one from the Create tab.</div>'

    st.markdown(
        f'<div class="panel"><div class="panel-head"><h3>Workspace</h3>'
        f"<span>{len(files)} files, {human_size(total)}</span></div>{rows}</div>",
        unsafe_allow_html=True,
    )

# ---- Operations -------------------------------------------------------------
with right:
    show_flash()
    tab_create, tab_read, tab_update, tab_delete = st.tabs(["Create", "Read", "Update", "Delete"])
    names = [p.name for p in files]

    # CREATE
    with tab_create:
        new_name = st.text_input("File name", placeholder="notes.txt", key="create_name")
        new_content = st.text_area("Contents", height=220, key="create_content")
        if st.button("Create file"):
            path = safe_path(new_name)
            if path is None:
                st.error("Enter a file name without slashes, for example notes.txt.")
            elif path.exists():
                st.error(f"{path.name} already exists. Pick another name or update the existing file.")
            else:
                path.write_text(new_content, encoding="utf-8")
                flash("success", f"Created {path.name}.")

    # READ
    with tab_read:
        if not names:
            st.info("There are no files to read yet.")
        else:
            chosen = st.selectbox("File", names, key="read_choice")
            path = WORKSPACE / chosen
            text = read_text(path)
            if text is None:
                st.warning("This file is not plain text, so it can't be previewed.")
            else:
                if text:
                    st.code(text, language=None, line_numbers=True)
                else:
                    st.caption("This file is empty.")
                st.download_button("Download file", data=text, file_name=chosen)

    # UPDATE
    with tab_update:
        if not names:
            st.info("There are no files to update yet.")
        else:
            chosen = st.selectbox("File", names, key="update_choice")
            path = WORKSPACE / chosen
            action = st.radio("Action", ["Rename", "Append", "Overwrite"], horizontal=True)

            if action == "Rename":
                renamed = st.text_input("New name", value=chosen, key=f"rename_{chosen}")
                if st.button("Rename file"):
                    target = safe_path(renamed)
                    if target is None:
                        st.error("Enter a file name without slashes.")
                    elif target.exists():
                        st.error(f"{target.name} already exists.")
                    else:
                        path.rename(target)
                        flash("success", f"Renamed {chosen} to {target.name}.")

            elif action == "Append":
                extra = st.text_area("Text to add at the end", height=160, key=f"append_{chosen}")
                if st.button("Append text"):
                    if not extra:
                        st.error("Enter some text to append.")
                    else:
                        with open(path, "a", encoding="utf-8") as fs:
                            fs.write("\n" + extra)
                        flash("success", f"Added text to {chosen}.")

            else:
                current = read_text(path)
                if current is None:
                    st.warning("This file is not plain text, so it can't be edited here.")
                else:
                    new_text = st.text_area("Contents", value=current, height=240, key=f"over_{chosen}")
                    if st.button("Save changes"):
                        path.write_text(new_text, encoding="utf-8")
                        flash("success", f"Saved changes to {chosen}.")

    # DELETE
    with tab_delete:
        if not names:
            st.info("There are no files to delete yet.")
        else:
            chosen = st.selectbox("File", names, key="delete_choice")
            st.warning(f"Deleting {chosen} can't be undone.")
            confirmed = st.checkbox(f"I want to permanently delete {chosen}", key=f"confirm_{chosen}")
            with st.container(key="danger_zone"):
                if st.button("Delete file", disabled=not confirmed):
                    (WORKSPACE / chosen).unlink()
                    flash("success", f"Deleted {chosen}.")
