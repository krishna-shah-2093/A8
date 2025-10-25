import pytest
import tempfile
import os
from app import app
import DAL

class TestFlaskApp:
    """Test cases for Flask application routes and functionality."""
    
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
    
    def test_home_route(self):
        """Test the home page route."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_about_route(self):
        """Test the about page route."""
        response = self.client.get('/about')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_resume_route(self):
        """Test the resume page route."""
        response = self.client.get('/resume')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_contact_route_get(self):
        """Test the contact page GET request."""
        response = self.client.get('/contact')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_contact_route_post(self):
        """Test the contact page POST request."""
        response = self.client.post('/contact')
        assert response.status_code == 302  # Redirect to thankyou page
    
    def test_contact_route_post_redirect(self):
        """Test that POST to contact redirects to thankyou."""
        response = self.client.post('/contact', follow_redirects=True)
        assert response.status_code == 200
        assert b'thank you' in response.data.lower()
    
    def test_thankyou_route(self):
        """Test the thankyou page route."""
        response = self.client.get('/thankyou')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_form_route_get(self):
        """Test the form page GET request."""
        response = self.client.get('/form')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_form_route_post_valid_data(self):
        """Test form submission with valid data."""
        form_data = {
            'title': 'Test Project',
            'description': 'This is a test project',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/form', data=form_data)
        assert response.status_code == 302  # Redirect to projects page
    
    def test_form_route_post_invalid_data(self):
        """Test form submission with invalid data."""
        form_data = {
            'title': '',  # Empty title
            'description': 'This is a test project',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/form', data=form_data)
        assert response.status_code == 200  # Stay on form page
    
    def test_form_route_post_redirect(self):
        """Test that valid form submission redirects to projects."""
        form_data = {
            'title': 'Test Project',
            'description': 'This is a test project',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/form', data=form_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'projects' in response.data.lower()
    
    def test_delete_project_route(self):
        """Test the delete project route."""
        # First add a project
        DAL.add_project("Test Project", "Test Description", "test.jpg")
        projects = DAL.get_projects()
        project_id = projects[0]['id']
        
        # Delete the project
        response = self.client.post(f'/delete_project/{project_id}')
        assert response.status_code == 302  # Redirect to projects page
        
        # Verify project was deleted
        projects_after = DAL.get_projects()
        assert len(projects_after) == 0
    
    def test_delete_project_redirect(self):
        """Test that delete project redirects to projects page."""
        # Add a project
        DAL.add_project("Test Project", "Test Description", "test.jpg")
        projects = DAL.get_projects()
        project_id = projects[0]['id']
        
        # Delete and follow redirect
        response = self.client.post(f'/delete_project/{project_id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'projects' in response.data.lower()
    
    def test_css_file_route(self):
        """Test the CSS file serving route."""
        response = self.client.get('/css/styles.css')
        # This might return 404 if CSS file doesn't exist, which is expected
        assert response.status_code in [200, 404]
    
    def test_nonexistent_route(self):
        """Test accessing a non-existent route."""
        response = self.client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_app_configuration(self):
        """Test that the Flask app is properly configured."""
        assert app.config['TESTING'] == True
        assert app.name == 'app'
    
    def test_all_routes_return_html(self):
        """Test that all main routes return HTML content."""
        routes = ['/', '/about', '/projects', '/resume', '/contact', '/form', '/thankyou']
        
        for route in routes:
            response = self.client.get(route)
            assert response.status_code == 200
            assert b'<!DOCTYPE html>' in response.data
            assert b'<html' in response.data
            assert b'</html>' in response.data
    
    def test_form_data_validation(self):
        """Test form data validation."""
        # Test with missing title
        form_data = {
            'title': '',
            'description': 'Valid description',
            'image_file_name': 'valid.jpg'
        }
        response = self.client.post('/form', data=form_data)
        assert response.status_code == 200  # Should stay on form
        
        # Test with missing description
        form_data = {
            'title': 'Valid title',
            'description': '',
            'image_file_name': 'valid.jpg'
        }
        response = self.client.post('/form', data=form_data)
        assert response.status_code == 200  # Should stay on form
        
        # Test with missing image file name
        form_data = {
            'title': 'Valid title',
            'description': 'Valid description',
            'image_file_name': ''
        }
        response = self.client.post('/form', data=form_data)
        assert response.status_code == 200  # Should stay on form
    
    def test_project_creation_workflow(self):
        """Test the complete project creation workflow."""
        # Start at form page
        response = self.client.get('/form')
        assert response.status_code == 200
        
        # Submit valid form data
        form_data = {
            'title': 'Workflow Test Project',
            'description': 'Testing the complete workflow',
            'image_file_name': 'workflow.jpg'
        }
        
        response = self.client.post('/form', data=form_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Workflow Test Project' in response.data
        
        # Verify project exists in database
        projects = DAL.get_projects()
        assert len(projects) == 1
        assert projects[0]['title'] == 'Workflow Test Project'
