# Sticky Notes Application

This project is a simple Django sticky notes app that allows a user to create, view, edit, and delete notes.

## Project overview

The application includes:
- a note list page
- a page to create a new note
- a page to edit an existing note
- a page to view note details
- a delete action for notes

## Requirements

This project uses Python and Django only.

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the project

1. Open a terminal in the project folder.
2. Activate your virtual environment if you are using one.
3. Run the development server:

```bash
python manage.py migrate
python manage.py runserver
```

4. Open the app in a browser at:

```text
http://127.0.0.1:8000/
```

## Project structure

```text
m6t5/
├── bulletin_board/
│   ├── manage.py
│   ├── notes/
│   ├── static/
│   └── sticky_notes/
├── README.md
├── requirements.txt
├── class diagram.png
├── sequence diagram.png
├── sticky_github.txt
└── .gitignore
```

## Features

- Create notes
- View all notes
- Open individual note details
- Edit note content
- Delete notes
- Store data in SQLite

## Notes

- The virtual environment folder should not be included in the final upload.
- The project GitHub link should be saved in `sticky_github.txt`.
