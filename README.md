# Flask Project for Generating Spring Boot or Node.js Projects from Image Diagrams 

This Flask-based web application allows users to upload an image diagram and generates a complete project structure in either Spring Boot or Node.js based on the input image.

## Features

- **Image Upload**: Upload an image diagram through the web interface.
- **OCR Processing**: Extract relevant information from the image using OCR.
- **Project Generation**: Generate a complete Spring Boot or Node.js project based on the extracted information.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.x
- Node.js and npm (for generating Node.js projects)
- Java Development Kit (JDK) (for generating Spring Boot projects)
- MySQL (if your generated projects need database integration)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for image text extraction

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/votre-utilisateur/votre-repo.git
    cd votre-repo
    ```

2. Set up a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Install Tesseract OCR:
    - On Ubuntu:
        ```bash
        sudo apt-get install tesseract-ocr
        ```
    - On macOS (using Homebrew):
        ```bash
        brew install tesseract
        ```

5. Configure environment variables in the `.env` file:

    ```bash
    FLASK_APP=test.py
    FLASK_ENV=development
    ```

6. Run the Flask application:

    ```bash
    flask run
    ```

The application will be available at `http://localhost:5000`.

## Project Structure

- `app.py`: The main Flask application file.
- `templates/`: Contains HTML templates for the web interface.
- `static/`: Contains static files like CSS and JavaScript.
- `ocr/`: Contains modules and scripts for OCR processing.
- `generators/`: Contains scripts for generating Spring Boot and Node.js projects.
- `uploads/`: Temporary storage for uploaded images.
- `generated_projects/`: Directory where generated projects are saved.

## Usage

1. **Upload an Image**: Navigate to the homepage and upload an image diagram through the web interface.
2. **Select Project Type**: Choose whether to generate a Spring Boot or Node.js project.
3. **Generate Project**: Click the generate button to process the image and generate the project.
4. **Download Project**: Once the generation is complete, download the generated project from the provided link.

## Example Routes

### Upload Image and Generate Project

```python
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
