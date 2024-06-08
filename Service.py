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


def create_services_package(package_name="services"):
    package_path = "AppsSpring/AppsSpring/src/main/java/com.example.appspringboot/" + package_name
    os.makedirs(package_path, exist_ok=True)  # Create package directory if not exists


def create_controllers_package(package_name="controllers"):
    package_path = "AppsSpring/AppsSpring/src/main/java/com.example.appspringboot/" + package_name
    os.makedirs(package_path, exist_ok=True)  # Create package directory if not exists


def generate_service_class(entity_name, package_name="services"):
    # Create the service class file
    entity_name_ca = entity_name.capitalize()
    service_name = entity_name + "Service"
    filename = f"AppsSpring/AppsSpring/src/main/java/com.example.appspringboot/{package_name}/{entity_name_ca}Service.java"
    with open(filename, 'w') as file:
        file.write(f"package com.example.appspringboot.{package_name};\n\n")
        file.write(f"import org.springframework.stereotype.Service;\n")
        file.write(f"import org.springframework.beans.factory.annotation.Autowired;\n")
        file.write(f"import java.util.List;\n")
        file.write(f"import java.util.Optional;\n")
        file.write(f"import com.example.appspringboot.entities.{entity_name_ca};\n")
        file.write(f"import com.example.appspringboot.repository.{entity_name}Repository;\n\n")
        file.write(f"@Service\n")
        file.write(f"public class {entity_name_ca}Service {{\n")
        file.write(f"    @Autowired\n")
        file.write(f"    private {entity_name}Repository {entity_name.lower()}Repository;\n\n")
        file.write(f"    public List<{entity_name_ca}> getAll{entity_name}s() {{\n")
        file.write(f"        return {entity_name.lower()}Repository.findAll();\n")
        file.write(f"    }}\n\n")
        file.write(f"    public Optional<{entity_name_ca}> get{entity_name}ById(Long id) {{\n")
        file.write(f"        return {entity_name.lower()}Repository.findById(id);\n")
        file.write(f"    }}\n\n")
        file.write(f"    public {entity_name_ca} add{entity_name}({entity_name_ca} {entity_name.lower()}) {{\n")
        file.write(f"        return {entity_name.lower()}Repository.save({entity_name.lower()});\n")
        file.write(f"    }}\n\n")
        file.write(f"    public {entity_name_ca} update{entity_name}({entity_name_ca} {entity_name.lower()}) {{\n")
        file.write(f"        return {entity_name.lower()}Repository.save({entity_name.lower()});\n")
        file.write(f"    }}\n\n")
        file.write(f"    public void delete{entity_name}(Long id) {{\n")
        file.write(f"        {entity_name.lower()}Repository.deleteById(id);\n")
        file.write(f"    }}\n")
        file.write(f"}}\n")


def generate_controller_class(entity_name, package_name="controllers"):
    # Create the controller class file
    controller_name = entity_name + "Controller"
    entity_name_ca = entity_name.capitalize()

    filename = f"AppsSpring/AppsSpring/src/main/java/com.example.appspringboot/{package_name}/{controller_name}.java"
    with open(filename, 'w') as file:
        file.write(f"package com.example.appspringboot.{package_name};\n\n")
        file.write(f"import org.springframework.beans.factory.annotation.Autowired;\n")
        file.write(f"import org.springframework.web.bind.annotation.*;\n")
        file.write(f"import java.util.List;\n")
        file.write(f"import java.util.Optional;\n")
        file.write(f"import com.example.appspringboot.entities.{entity_name_ca};\n")
        file.write(f"import com.example.appspringboot.services.{entity_name_ca}Service;\n\n")
        file.write(f"@RestController\n")
        file.write(f"@RequestMapping(\"/{entity_name.lower()}\")\n")
        file.write(f"public class {controller_name} {{\n")
        file.write(f"    @Autowired\n")
        file.write(f"    private {entity_name_ca}Service {entity_name.lower()}Service;\n\n")
        file.write(f"    @GetMapping\n")
        file.write(f"    public List<{entity_name_ca}> getAll{entity_name}s() {{\n")
        file.write(f"        return {entity_name.lower()}Service.getAll{entity_name}s();\n")
        file.write(f"    }}\n\n")
        file.write(f"    @GetMapping(\"/{{id}}\")\n")
        file.write(f"    public Optional<{entity_name_ca}> get{entity_name}ById(@PathVariable Long id) {{\n")
        file.write(f"        return {entity_name.lower()}Service.get{entity_name}ById(id);\n")
        file.write(f"    }}\n\n")
        file.write(f"    @PostMapping\n")
        file.write(
            f"    public {entity_name_ca} add{entity_name}(@RequestBody {entity_name_ca} {entity_name.lower()}) {{\n")
        file.write(f"        return {entity_name.lower()}Service.add{entity_name}({entity_name.lower()});\n")
        file.write(f"    }}\n\n")
        file.write(f"    @PutMapping\n")
        file.write(
            f"    public {entity_name_ca} update{entity_name}(@RequestBody {entity_name_ca} {entity_name.lower()}) {{\n")
        file.write(f"        return {entity_name.lower()}Service.update{entity_name}({entity_name.lower()});\n")
        file.write(f"    }}\n\n")
        file.write(f"    @DeleteMapping(\"/{{id}}\")\n")
        file.write(f"    public void delete{entity_name}(@PathVariable Long id) {{\n")
        file.write(f"        {entity_name.lower()}Service.delete{entity_name}(id);\n")
        file.write(f"    }}\n")
        file.write(f"}}\n")

# Function to create Java files for each entity


def create_java_file(entity_name, attributes, package_name="entities"):
    # Remove non-alphabetic characters from the entity name
    entity_name = re.sub(r'[^a-zA-Z]', '', entity_name)
    entity_name = entity_name.capitalize()
    filename = f"AppsSpring/AppsSpring/src/main/java/com.example.appspringboot/{package_name}/{entity_name}.java"
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create package directory if not exists
    with open(filename, 'w') as file:
        # Package statement
        file.write(f"package com.example.appspringboot.entities;\n\n")

        # Class declaration
        file.write(f"import jakarta.persistence.Entity;\n")
        file.write(f"import jakarta.persistence.Id;\n")
        file.write(f"import java.util.Date;\n")
        file.write(f"import lombok.Getter;\n")
        file.write(f"import lombok.Setter;\n")
        file.write(f"import jakarta.persistence.GeneratedValue;\n")
        file.write(f"import jakarta.persistence.GenerationType;\n")

        file.write("\n")
        file.write(f"@Entity\n")
        file.write(f"@Getter\n")
        file.write(f"@Setter\n")
        file.write(f"public class {entity_name} {{\n")
        file.write("\n")
        file.write(f"    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)\n")

        # Attributes declaration
        for attr in attributes:
            attr_parts = attr.split()
            if len(attr_parts) != 2:
                print(f"Error: Attribute {attr} doesn't have the expected format.")
                continue
            file.write(f"    private {attr_parts[1]} {attr_parts[0]} ;\n")
        file.write("\n")
        file.write("}\n")

# Function to create Repository interface


def create_repository_interface(entity_name, package_name="repository"):
    repository_name = entity_name + "Repository"
    filename = f"AppsSpring/AppsSpring/src/main/java/com.example.appspringboot/{package_name}/{repository_name}.java"
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create package directory if not exists
    with open(filename, 'w') as file:
        entity_name = entity_name.capitalize()
        # Package statement
        file.write(f"package {"com.example.appspringboot.repository"};\n\n")

        # Imports
        file.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
        file.write("import com.example.appspringboot.entities." + entity_name + ";\n")
        # Repository interface declaration
        file.write(f"public interface {repository_name} extends JpaRepository<{entity_name}, Long> {{\n")
        file.write("}\n")


# Function to generate application.properties file
def generate_application_properties(DB_name):
    filename = "AppsSpring/AppsSpring/src/main/resources/application.properties"
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if not exists
    with open(filename, 'w') as file:
        file.write("### Database Configuration\n")
        file.write("spring.datasource.url=jdbc:mysql://localhost:3306/" + DB_name + "?createDatabaseIfNotExist=true\n")
        file.write("spring.datasource.username=root\n")
        file.write("spring.datasource.password=\n")
        file.write("### JPA / HIBERNATE ###\n")
        file.write("spring.jpa.show-sql=true\n")
        file.write("spring.jpa.hibernate.ddl-auto=update\n")


# Function to generate pom.xml file
def generate_pom_xml(entity_names, package_name="com.example"):
    pom_xml = f"""<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>{package_name}</groupId>
    <version>1.0.0</version>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.1</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <artifactId>appspringboot</artifactId>
    <name>appspringboot</name>
    <description>appspringboot</description>


    <properties>
        <java.version>17</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>2.3.0</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Maven Compiler Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>
            <!-- Spring Boot Maven Plugin -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"""
    with open("AppsSpring/AppsSpring/pom.xml", "w") as file:
        file.write(pom_xml)

# Function to generate main Application class


def generate_main_class(package_name="com.example.appspringboot"):
    main_class_content = f"""package {package_name};

    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;

    @SpringBootApplication
    public class Application {{
    public static void main(String[] args) {{
        SpringApplication.run(Application.class, args);
        }}
    }}
    """
    filename = f"AppsSpring/AppsSpring/src/main/java/com.example.appspringboot/Application.java"
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create package directory if not exists
    with open(filename, 'w') as file:
        file.write(main_class_content)


def generate_spring_boot_project(img_path, DB_name):
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
        attributes_with_spaces = [re.sub(r'[-:]', ' ', attr) for attr in attributes_with_symbols]
        # Remove empty strings and attributes without expected format
        attributes = [attr for attr in attributes_with_spaces if len(attr.split()) == 2]

        # Create Java file for the entity
        create_java_file(entity_name, attributes)
        # Create repository interface
        create_repository_interface(entity_name)

    create_services_package()
    create_controllers_package()

    for entity_name in entity_names:
        generate_service_class(entity_name)
        generate_controller_class(entity_name)

    # Generate application.properties file
    generate_application_properties(DB_name)
    # Generate pom.xml file
    generate_pom_xml(entity_names)
    # Generate main Application class
    generate_main_class()

    folder_to_zip = "AppsSpring"
    zip_file_name = "AppsSpring.zip"

    zip_folder(folder_to_zip, zip_file_name)
    # OCR and table extraction
    ocr = TesseractOCR(n_threads=1, lang="eng")
    img = Image(src=img_path)
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
        attributes_with_spaces = [re.sub(r'[-:]', ' ', attr) for attr in attributes_with_symbols]
        # Remove empty strings and attributes without expected format
        attributes = [attr for attr in attributes_with_spaces if len(attr.split()) == 2]

        # Create Java file for the entity
        create_java_file(entity_name, attributes)
        # Create repository interface
        create_repository_interface(entity_name)
    create_services_package()
    create_controllers_package()

    for entity_name in entity_names:
        generate_service_class(entity_name)
        generate_controller_class(entity_name)

    # Generate application.properties file
    generate_application_properties(DB_name)
    # Generate pom.xml file
    generate_pom_xml(entity_names)
    # Generate main Application class
    generate_main_class()

    folder_to_zip = "AppsSpring"
    zip_file_name = "AppsSpring.zip"
    zip_folder(folder_to_zip, zip_file_name)
