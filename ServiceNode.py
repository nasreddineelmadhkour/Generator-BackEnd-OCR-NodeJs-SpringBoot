import os
import json
import os
import json
import re
from img2table.document import Image
from img2table.ocr import TesseractOCR
import zipfile
import shutil
from werkzeug.utils import secure_filename

def zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

def create_node_js_file(entity_name, attributes, folder_path="node/NodeJS", package_name="models"):
    # Remove non-alphabetic characters from the entity name
    entity_name = re.sub(r'[^a-zA-Z]', '', entity_name)
    entity_name = entity_name.capitalize()
    
    # Create directory for Node.js files
    directory = os.path.join(folder_path, package_name)
    os.makedirs(directory, exist_ok=True)
    
    filename = os.path.join(directory, f"{entity_name.lower()}.js")
    
    with open(filename, 'w') as file:
        # Write file content
        file.write("const mongoose = require('mongoose');\n\n")
        file.write(f"// Define the {entity_name} Schema\n")
        file.write(f"const {entity_name.lower()}Schema = new mongoose.Schema({{\n")
        for attr in attributes:
            file.write(f"  {attr.strip()},\n")
        file.write("});\n\n")
        file.write(f"// Create the {entity_name} model\n")
        file.write(f"const {entity_name} = mongoose.model('{entity_name}', {entity_name.lower()}Schema);\n\n")
        file.write(f"module.exports = {entity_name};\n")

def create_controller(entity_name, folder_path="node/nodeJs/controllers", package_name="models"):
    # Create directory for controllers
    os.makedirs(folder_path, exist_ok=True)

    # Define file path
    filename = os.path.join(folder_path, f"{entity_name.lower()}Controller.js")

    # Write controller file content
    with open(filename, 'w') as file:
        # Write file content
        file.write("const express = require('express');\n")
        file.write(f"const router = express.Router();\n\n")
        file.write(f"const {entity_name} = require('../{package_name}/{entity_name}');\n\n")

        # Create routes

        # Create (POST)
        file.write("// Create\n")
        file.write(f"router.post('/', async (req, res) => {{\n")
        file.write(f"    try {{\n")
        file.write(f"        const {entity_name.lower()} = new {entity_name}(req.body);\n")
        file.write(f"        await {entity_name.lower()}.save();\n")
        file.write(f"        res.status(201).send({entity_name.lower()});\n")
        file.write(f"    }} catch (error) {{\n")
        file.write(f"        res.status(400).send(error);\n")
        file.write(f"    }}\n")
        file.write(f"}});\n\n")

        # Read (GET)
        file.write("// Read\n")
        file.write(f"router.get('/:id', async (req, res) => {{\n")
        file.write(f"    try {{\n")
        file.write(f"        const {entity_name.lower()} = await {entity_name}.findById(req.params.id);\n")
        file.write(f"        if (!{entity_name.lower()}) {{\n")
        file.write(f"            return res.status(404).send();\n")
        file.write(f"        }}\n")
        file.write(f"        res.send({entity_name.lower()});\n")
        file.write(f"    }} catch (error) {{\n")
        file.write(f"        res.status(500).send();\n")
        file.write(f"    }}\n")
        file.write(f"}});\n\n")

        # Update (PUT)
        file.write("// Update\n")
        file.write(f"router.put('/:id', async (req, res) => {{\n")
        file.write(f"    try {{\n")
        file.write(f"        const {entity_name.lower()} = await {entity_name}.findByIdAndUpdate(req.params.id, req.body, {{ new: true, runValidators: true }});\n")
        file.write(f"        if (!{entity_name.lower()}) {{\n")
        file.write(f"            return res.status(404).send();\n")
        file.write(f"        }}\n")
        file.write(f"        res.send({entity_name.lower()});\n")
        file.write(f"    }} catch (error) {{\n")
        file.write(f"        res.status(400).send(error);\n")
        file.write(f"    }}\n")
        file.write(f"}});\n\n")

        # Delete (DELETE)
        file.write("// Delete\n")
        file.write(f"router.delete('/:id', async (req, res) => {{\n")
        file.write(f"    try {{\n")
        file.write(f"        const {entity_name.lower()} = await {entity_name}.findByIdAndDelete(req.params.id);\n")
        file.write(f"        if (!{entity_name.lower()}) {{\n")
        file.write(f"            return res.status(404).send();\n")
        file.write(f"        }}\n")
        file.write(f"        res.send({entity_name.lower()});\n")
        file.write(f"    }} catch (error) {{\n")
        file.write(f"        res.status(500).send();\n")
        file.write(f"    }}\n")
        file.write(f"}});\n\n")

        file.write("module.exports = router;\n")


def create_routes(entity_name, folder_path="node/nodeJs/routes", package_name="controllers"):
    # Create directory for routes
    os.makedirs(folder_path, exist_ok=True)

    # Define file path
    filename = os.path.join(folder_path, f"{entity_name.lower()}Routes.js")

    # Write route file content
    with open(filename, 'w') as file:
        # Write file content
        file.write("const express = require('express');\n")
        file.write(f"const router = express.Router();\n\n")
        file.write(f"const {entity_name}Controller = require('../{package_name}/{entity_name.lower()}Controller');\n\n")

        # Create routes

        # Create (POST)
        file.write("// Create\n")
        file.write(f"router.post('/', {entity_name}Controller.create);\n\n")

        # Read (GET)
        file.write("// Read\n")
        file.write(f"router.get('/:id', {entity_name}Controller.read);\n\n")

        # Update (PUT)
        file.write("// Update\n")
        file.write(f"router.put('/:id', {entity_name}Controller.update);\n\n")

        # Delete (DELETE)
        file.write("// Delete\n")
        file.write(f"router.delete('/:id', {entity_name}Controller.delete);\n\n")

        file.write("module.exports = router;\n")

def create_project_structure(img_path, DB_name):
    project_name = "node/nodeJs"
    # Create project directory
    os.makedirs(project_name)

    # Create package directories
    os.makedirs(os.path.join(project_name, 'models'))
    os.makedirs(os.path.join(project_name, 'controllers'))
    os.makedirs(os.path.join(project_name, 'routes'))
    mongo_connection_url = f"mongodb://localhost:27017/{DB_name}"  # MongoDB connection URL with database name
    
    with open(os.path.join(project_name, 'app.js'), 'w') as file:
    # Write content for app.js
        file.write("const express = require('express');\n")
        file.write("const cors = require('cors');\n")
        file.write("const mongoose = require('mongoose');\n\n")
        file.write("const app = express();\n\n")
        file.write("app.use(cors());\n\n")
        file.write("// MongoDB connection\n")
        file.write(f"mongoose.connect('{mongo_connection_url}', " +
               "{ useNewUrlParser: true, useUnifiedTopology: true })\n")
        file.write(".then(() => console.log('MongoDB connected'))\n")
        file.write(".catch((err) => console.error('MongoDB connection error:', err));\n\n")
        file.write("// Your routes and middleware setup goes here\n\n")
        file.write("const PORT = process.env.PORT || 3000;\n")
        file.write("app.listen(PORT, () => console.log(`Server running on port ${PORT}`));")

    with open(os.path.join(project_name, 'package.json'), 'w') as file:
        # Write content for package.json
        package_json = {
            "name": project_name,
            "version": "1.0.0",
            "main": "app.js",
            "scripts": {
                "start": "node app.js"
            },
            "dependencies": {
                "express": "^4.17.1",
                "cors": "^2.8.5"
            }
        }
        json.dump(package_json, file, indent=2)
    
# OCR and table extraction
    ocr = TesseractOCR(n_threads=1, lang="eng")
    img = Image(src=img_path)  # Use the provided image path
    extracted_tables = img.extract_tables(ocr=ocr, implicit_rows=True, borderless_tables=False, min_confidence=50)

    # Convert extracted tables to JSON
    tables_json = json.dumps(extracted_tables, indent=4, default=lambda x: x.__dict__)

    # Write JSON data to a file
    with open("extracted_tables.json", "w") as json_file:
        json_file.write(tables_json)

    print("Tables extracted and saved to extracted_tables.json")

    # Load JSON data from the extracted_tables.json file
    with open("extracted_tables.json", "r") as json_file:
        data = json.load(json_file)

    entity_names = []

    # Process each element in the JSON data
    for element in data:
        bbox = element['bbox']
        content = element['content']

        # Extract entity name
        entity_name = content['0'][0]['value']
        entity_names.append(entity_name)
        print("hello " + entity_name)
        # Remove non-alphabetic characters from the entity name
        entity_name = re.sub(r'[^a-zA-Z]', '', entity_name)

        # Extract attributes
        attributes_with_symbols = content['1'][0]['value'].split('\n') + content['2'][0]['value'].split('\n')
        # Replace "-" and ":" with " "
        attributes_with_spaces = [re.sub(r'[-]', ' ', attr) for attr in attributes_with_symbols]
        # Remove empty strings and attributes without expected format
        attributes = [attr for attr in attributes_with_spaces if len(attr.split()) == 2]

        # Create Java file for the entity
        create_node_js_file(entity_name, attributes)
    
    for entity_name in entity_names:
        create_controller(entity_name)
        create_routes(entity_name)
    folder_to_zip = "node"
    zip_file_name = "node.zip"
    zip_folder(folder_to_zip, zip_file_name)
