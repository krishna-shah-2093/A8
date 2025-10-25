import pytest
import sqlite3
import os
import tempfile
import DAL

class TestDatabase:
    """Test cases for database operations."""
    
    def setup_method(self):
        """Set up a temporary database for each test."""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Store original DB_FILE and replace with temp file
        self.original_db_file = DAL.DB_FILE
        DAL.DB_FILE = self.temp_db.name
        
        # Initialize the test database
        DAL.init_db()
    
    def teardown_method(self):
        """Clean up after each test."""
        # Restore original DB_FILE
        DAL.DB_FILE = self.original_db_file
        
        # Remove temporary database file
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_database_connection(self):
        """Test that database connection works."""
        conn = sqlite3.connect(DAL.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        # Check that projects table exists
        table_names = [table[0] for table in tables]
        assert 'projects' in table_names
    
    def test_init_db_creates_table(self):
        """Test that init_db creates the projects table with correct schema."""
        conn = sqlite3.connect(DAL.DB_FILE)
        cursor = conn.cursor()
        
        # Get table schema
        cursor.execute("PRAGMA table_info(projects)")
        columns = cursor.fetchall()
        conn.close()
        
        # Check table structure
        column_names = [col[1] for col in columns]
        expected_columns = ['id', 'title', 'description', 'image_file_name']
        
        for expected_col in expected_columns:
            assert expected_col in column_names
    
    def test_add_project(self):
        """Test adding a project to the database."""
        title = "Test Project"
        description = "This is a test project"
        image_file_name = "test.jpg"
        
        DAL.add_project(title, description, image_file_name)
        
        # Verify the project was added
        projects = DAL.get_projects()
        assert len(projects) == 1
        assert projects[0]['title'] == title
        assert projects[0]['description'] == description
        assert projects[0]['image_file_name'] == image_file_name
    
    def test_get_projects_empty(self):
        """Test getting projects from empty database."""
        projects = DAL.get_projects()
        assert len(projects) == 0
    
    def test_get_projects_multiple(self):
        """Test getting multiple projects ordered by ID DESC."""
        # Add multiple projects
        DAL.add_project("Project 1", "Description 1", "image1.jpg")
        DAL.add_project("Project 2", "Description 2", "image2.jpg")
        DAL.add_project("Project 3", "Description 3", "image3.jpg")
        
        projects = DAL.get_projects()
        
        # Should have 3 projects
        assert len(projects) == 3
        
        # Should be ordered by ID DESC (newest first)
        assert projects[0]['title'] == "Project 3"
        assert projects[1]['title'] == "Project 2"
        assert projects[2]['title'] == "Project 1"
    
    def test_delete_project(self):
        """Test deleting a project."""
        # Add a project
        DAL.add_project("Test Project", "Test Description", "test.jpg")
        projects = DAL.get_projects()
        project_id = projects[0]['id']
        
        # Delete the project
        DAL.delete_project(project_id)
        
        # Verify it's deleted
        projects_after = DAL.get_projects()
        assert len(projects_after) == 0
    
    def test_update_project(self):
        """Test updating a project."""
        # Add a project
        DAL.add_project("Original Title", "Original Description", "original.jpg")
        projects = DAL.get_projects()
        project_id = projects[0]['id']
        
        # Update the project
        DAL.update_project(project_id, "Updated Title", "Updated Description", "updated.jpg")
        
        # Verify the update
        projects_after = DAL.get_projects()
        assert projects_after[0]['title'] == "Updated Title"
        assert projects_after[0]['description'] == "Updated Description"
        assert projects_after[0]['image_file_name'] == "updated.jpg"
    
    def test_project_id_auto_increment(self):
        """Test that project IDs auto-increment."""
        DAL.add_project("Project 1", "Description 1", "image1.jpg")
        DAL.add_project("Project 2", "Description 2", "image2.jpg")
        
        projects = DAL.get_projects()
        
        # IDs should be different and incrementing
        assert projects[0]['id'] != projects[1]['id']
        assert projects[0]['id'] > projects[1]['id']  # Newer project has higher ID
