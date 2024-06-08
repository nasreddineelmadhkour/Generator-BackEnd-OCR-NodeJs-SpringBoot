import Service as service
import ServiceNode as serviceNode
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome To Generated BackEnd Spring boot'


@app.route('/GeneratedBackEndSpringBoot', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    DB_name = request.form['DB_name']
    TYPE_PROJECT = request.form['type_project']

    if file.filename == '':
        return 'No selected file'
    if file:
        if TYPE_PROJECT == "SPRING":
            # Save the uploaded file to a temporary directory
            filename = secure_filename(file.filename)
            file.save(filename)
            # Call your function to generate the Spring Boot project
            service.generate_spring_boot_project(filename, DB_name)
            # Path to the generated zip file
            zip_file_path = 'AppsSpring.zip'
            # Return the zip file to the client
            print("Hello SPRING ")
            return send_file(zip_file_path, as_attachment=True)
        else:
            # Save the uploaded file to a temporary directory
            filename = secure_filename(file.filename)
            file.save(filename)
            # Call your function to generate the Spring Boot project
            serviceNode.create_project_structure(filename, DB_name)
            # Path to the generated zip file
            zip_file_path = 'node.zip'
            # Return the zip file to the client
            print("Hello NODE")
            return send_file(zip_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
