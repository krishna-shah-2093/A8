import pytest
import tempfile
import os
from app import app
import DAL

class TestProjectsPage:
    """Test cases for the projects page functionality."""
    
    def setup_method(self):
        """Set up test environment for each test."""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Store original DB_FILE and replace with temp file
        self.original_db_file = DAL.DB_FILE
        DAL.DB_FILE = self.temp_db.name
        
        # Initialize the test database
        DAL.init_db()
        
        # Configure Flask app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def teardown_method(self):
        """Clean up after each test."""
        # Restore original DB_FILE
        DAL.DB_FILE = self.original_db_file
        
        # Remove temporary database file
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_projects_page_loads(self):
        """Test that the projects page loads successfully."""
        response = self.client.get('/projects')
        assert response.status_code == 200
        assert b'projects' in response.data.lower()
    
    def test_projects_page_with_no_projects(self):
        """Test projects page with empty database."""
        response = self.client.get('/projects')
        assert response.status_code == 200
        
        # Should still load the page even with no projects
        assert b'projects' in response.data.lower()
    
    def test_projects_page_with_sample_projects(self):
        """Test projects page with sample data."""
        # Add sample projects
        DAL.add_project("AI Project", "Machine learning application", "ai.jpg")
        DAL.add_project("Web App", "Full-stack web application", "web.jpg")
        
        response = self.client.get('/projects')
        assert response.status_code == 200
        
        # Check that project data is displayed
        assert b'AI Project' in response.data
        assert b'Machine learning application' in response.data
        assert b'Web App' in response.data
        assert b'Full-stack web application' in response.data
    
    def test_projects_page_template_rendering(self):
        """Test that projects template renders correctly."""
        # Add a test project
        DAL.add_project("Test Project", "Test Description", "test.jpg")
        
        response = self.client.get('/projects')
        assert response.status_code == 200
        
        # Check for HTML structure
        assert b'<!DOCTYPE html>' in response.data
        assert b'<html' in response.data
        assert b'</html>' in response.data
    
    def test_projects_data_structure(self):
        """Test that projects data is properly structured."""
        # Add multiple projects
        DAL.add_project("Project 1", "Description 1", "image1.jpg")
        DAL.add_project("Project 2", "Description 2", "image2.jpg")
        
        # Get projects data directly
        projects = DAL.get_projects()
        
        # Verify data structure
        assert len(projects) == 2
        
        for project in projects:
            assert 'id' in project
            assert 'title' in project
            assert 'description' in project
            assert 'image_file_name' in project
            
            # Verify data types
            assert isinstance(project['id'], int)
            assert isinstance(project['title'], str)
            assert isinstance(project['description'], str)
            assert isinstance(project['image_file_name'], str)
    
    def test_projects_ordering(self):
        """Test that projects are ordered correctly (newest first)."""
        # Add projects with delays to ensure different IDs
        DAL.add_project("First Project", "First Description", "first.jpg")
        DAL.add_project("Second Project", "Second Description", "second.jpg")
        DAL.add_project("Third Project", "Third Description", "third.jpg")
        
        response = self.client.get('/projects')
        assert response.status_code == 200
        
        # Projects should be ordered newest first
        response_text = response.data.decode('utf-8')
        
        # Find positions of project titles
        first_pos = response_text.find("First Project")
        second_pos = response_text.find("Second Project")
        third_pos = response_text.find("Third Project")
        
        # Third project should appear first (newest)
        assert third_pos < second_pos < first_pos
    
    def test_projects_with_special_characters(self):
        """Test projects page with special characters in data."""
        # Add project with special characters
        DAL.add_project("Project with & symbols", "Description with <tags> and 'quotes'", "special.jpg")
        
        response = self.client.get('/projects')
        assert response.status_code == 200
        
        # Should handle special characters properly
        assert b'Project with & symbols' in response.data
        assert b'Description with <tags> and \'quotes\'' in response.data
    
    def test_projects_page_performance(self):
        """Test projects page performance with many projects."""
        # Add many projects
        for i in range(50):
            DAL.add_project(f"Project {i}", f"Description {i}", f"image{i}.jpg")
        
        response = self.client.get('/projects')
        assert response.status_code == 200
        
        # Should still load successfully with many projects
        assert b'Project 49' in response.data  # Newest project should be visible
