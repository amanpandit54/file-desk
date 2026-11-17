<<<<<<< HEAD
# File Desk

A Streamlit app for creating, reading, updating and deleting text files, built on top of a simple Python file-handling script.

## Features

- **Create** a new file with contents (existing names are protected)
- **Read** a file with a line-numbered preview and a download button
- **Update** by renaming, appending or overwriting
- **Delete** with an explicit confirmation step
- Light and dark mode toggle
- Live workspace panel showing file names, sizes and last-modified times
- Every file stays inside the `workspace/` folder, and names with slashes are rejected

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

## Project structure

```
file-desk/
├── .streamlit/
│   └── config.toml
├── app.py
├── requirements.txt
└── README.md
```

## Ideas for next steps

- Search and filter files
- Folder support
- Markdown preview
=======
# file-desk
>>>>>>> 9c6746e083a04052b9ef48cf88da2dcf1400b740
