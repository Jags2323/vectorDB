import fitz

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