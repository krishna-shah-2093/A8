# Personal Portfolio Website

A Flask-based personal portfolio website with project management functionality.

## Features

- **Project Management**: Add, view, and delete projects
- **Database Integration**: SQLite database for storing project data
- **Responsive Design**: Modern, mobile-friendly interface
- **Image Support**: Upload and display project images
- **Form Validation**: Client-side and server-side validation

## Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
A7/
├── app.py              # Flask application
├── DAL.py              # Database access layer
├── projects.db         # SQLite database
├── requirements.txt    # Python dependencies
├── css/
│   └── styles.css     # Stylesheet
├── static/
│   ├── images/        # Project images
│   └── assets/        # Resume and other files
└── templates/         # Jinja2 templates
    ├── base.html      # Base template
    ├── projects.html  # Projects page
    ├── form.html      # Add project form
    └── [other pages]
```

## Dependencies

- **Flask**: Web framework
- **SQLite3**: Database (built into Python)
- **Jinja2**: Template engine (included with Flask)

## Database

The application uses SQLite3 with the following table structure:

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image_file_name TEXT NOT NULL
);
```

## Adding Projects

1. Place your project images in the `static/images/` folder
2. Use the "Add Project" form to add new projects
3. Enter the exact filename of your image
4. Projects will appear immediately on the projects page


