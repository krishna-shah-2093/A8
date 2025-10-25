from flask import Flask, render_template, send_from_directory, redirect, url_for, request
import DAL

app = Flask(__name__)

# Initialize database on startup
DAL.init_db()

# Serve CSS files from root-level css folder
@app.route('/css/<path:filename>')
def css_file(filename):
    return send_from_directory('css', filename)

# Pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    projects_data = DAL.get_projects()
    return render_template('projects.html', projects=projects_data)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
   
    if request.method == 'POST':
    
        return redirect(url_for('thankyou'))
    return render_template('contact.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_file_name = request.form.get('image_file_name', '').strip()
        
        # Validate non-empty fields
        if title and description and image_file_name:
            DAL.add_project(title, description, image_file_name)
            return redirect(url_for('projects'))
    
    return render_template('form.html')

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    DAL.delete_project(project_id)
    return redirect(url_for('projects'))

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
