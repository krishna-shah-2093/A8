import sqlite3
import os

DB_FILE = 'projects.db'

def init_db():
    """Create DB/table if missing."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image_file_name TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_projects():
    """Return rows (latest first) as dicts/Rows."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This makes rows accessible as dicts
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projects ORDER BY id DESC')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def add_project(title, description, image_file_name):
    """Insert one row."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO projects (title, description, image_file_name)
        VALUES (?, ?, ?)
    ''', (title, description, image_file_name))
    
    conn.commit()
    conn.close()

def delete_project(project_id):
    """Delete a project by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    
    conn.commit()
    conn.close()

def update_project(project_id, title, description, image_file_name):
    """Update a project by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE projects 
        SET title = ?, description = ?, image_file_name = ?
        WHERE id = ?
    ''', (title, description, image_file_name, project_id))
    
    conn.commit()
    conn.close()
