import fitz
import xml.etree.ElementTree as ET
import re
import json

# Function to process text file
def process_text_file(file_path):
    with open(file_path, 'r') as file:
        paragraphs = file.read().strip().split('\n\n')
    return paragraphs

# Function to process PDF file
def process_pdf_file(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    
    # Split text into lines
    lines = text.split('\n')

    # Group lines into paragraphs based on typical paragraph formatting
    paragraphs = []
    paragraph = ""
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            # Empty line indicates a new paragraph
            if paragraph:
                paragraphs.append(paragraph.strip())
                paragraph = ""
        else:
            if paragraph and (stripped_line[0].isupper() or stripped_line[0].isdigit()):
                # New paragraph if the line starts with an uppercase letter or a number and the paragraph is not empty
                paragraphs.append(paragraph.strip())
                paragraph = stripped_line
            else:
                # Continue the current paragraph
                paragraph += " " + stripped_line

    # Add the last paragraph if not empty
    if paragraph:
        paragraphs.append(paragraph.strip())
    
    return paragraphs

def process_xml_file_by_tag(file_path, tag="Device"):
    text_segments = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for element in root.findall(f'.//{tag}'):
            # Convert the element to a string
            element_string = ET.tostring(element, encoding='unicode', method='xml')
            # Remove new lines and excessive spaces
            clean_string = re.sub(r'\s+', ' ', element_string).strip()
            text_segments.append(clean_string)
                
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    
    return text_segments

def process_json_file(file_path):
    json_segments = []
    print("started process_json_file")
    
    try:
        with open(file_path, 'r') as file:
            json_data = file.read()
        
        # Check if the JSON data is empty
        if not json_data.strip():
            return json_segments
        
        # Parse the JSON data
        data = json.loads(json_data)
        
        # Check if the parsed data is a list (array) or a single dictionary (object)
        if isinstance(data, list):
            # If it's a list, iterate through each JSON object in the array
            for obj in data:
                if obj:  # Check if the object is not empty
                    # Convert the JSON object to a string
                    obj_string = json.dumps(obj)
                    # Remove new lines and excessive spaces
                    clean_string = re.sub(r'\s+', ' ', obj_string).strip()
                    json_segments.append(clean_string)
        elif isinstance(data, dict):
            # If it's a single JSON object, process it directly if it's not empty
            if data:
                obj_string = json.dumps(data)
                clean_string = re.sub(r'\s+', ' ', obj_string).strip()
                json_segments.append(clean_string)
        else:
            print("Unsupported JSON format")
            
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print(json_segments)
    return json_segments