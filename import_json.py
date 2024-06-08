import cv2
import pytesseract
import json

# Load the diagram image
image_path = "diagramme.png"
diagram_image = cv2.imread(image_path)

# Preprocess the image (resize, enhance contrast, etc.)
processed_image = cv2.resize(diagram_image, None, fx=1.5, fy=1.5)  # Resize image
processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

# Apply thresholding to create a binary image
_, binary_image = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Find contours in the binary image
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize a list to store extracted entities
entities = []

# Process each contour (assumed to be a table representing an entity)
for contour in contours:
    # Get the bounding box of the contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Check if the bounding box is valid
    if w > 0 and h > 0:
        # Extract the table region from the original image
        table_region = diagram_image[y:y+h, x:x+w]
        
        # Check if the table region is not empty
        if table_region is not None and table_region.size != 0:
            # Optional: Apply additional preprocessing to the table region
            # Example: Denoising
            table_region = cv2.fastNlMeansDenoisingColored(table_region, None, 10, 10, 7, 21)
            
            # Convert the table region to grayscale for OCR
            table_gray = cv2.cvtColor(table_region, cv2.COLOR_BGR2GRAY)
            
            # Perform OCR on the table region with language specification and custom OCR configurations
            custom_config = r'--oem 3 --psm 6'
            table_text = pytesseract.image_to_string(table_gray, lang='eng', config=custom_config)
            
            # Append the extracted text to the entities list
            entities.append({"table_text": table_text})

# Save the extracted entities to a JSON file
output_json_path = "extracted_entities.json"
with open(output_json_path, "w") as json_file:
    json.dump(entities, json_file, indent=4)

print("Entities extracted and saved to JSON file.")
