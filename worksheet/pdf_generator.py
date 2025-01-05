from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from model.sound_word import SoundWord
import os

# Constants for the grid layout
GRID_SIZE = 3
MARGIN = 1 * inch
BORDER_THICKNESS = 2

# Calculate the remaining space for grid squares and define their size
GRID_SPACE = letter[0] - 2 * MARGIN
IMAGE_WIDTH = GRID_SPACE / GRID_SIZE  # Width of each grid cell
IMAGE_HEIGHT = IMAGE_WIDTH * 1.2  # Make rectangles taller
BUBBLE_SIZE = IMAGE_WIDTH / 4
BOTTOM_SPACE = BUBBLE_SIZE / 4  # Space at the bottom for bubbles

# Define the path to the font
font_dir = "./worksheet/fonts"
font_path = os.path.join(font_dir, "DynaPuff-Regular.ttf")

# Function to draw the grid
def draw_grid(c: Canvas, sound_words: list[SoundWord]):
    x_offset = MARGIN
    y_offset = 10 * inch - MARGIN

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            index = row + GRID_SIZE*col
            sound_word = sound_words[index]
            
            # Draw the grid rectangle
            c.setLineWidth(BORDER_THICKNESS)
            x = x_offset + col * IMAGE_WIDTH
            y = y_offset - (row + 1) * IMAGE_HEIGHT
            c.rect(x, y, IMAGE_WIDTH, IMAGE_HEIGHT, stroke=1, fill=0)

            # Placing an image in the grid
            c.drawImage(sound_word.image_path, x + BUBBLE_SIZE / 2, y + BUBBLE_SIZE * 1.5, 
                        width=IMAGE_WIDTH - BUBBLE_SIZE,
                        height=IMAGE_HEIGHT - BUBBLE_SIZE * 2)

            # Draw the bubbles spaced out above the bottom margin
            bubble_y = y + BOTTOM_SPACE
            spacing = (IMAGE_WIDTH - GRID_SIZE * BUBBLE_SIZE) / 4
            for i in range(GRID_SIZE):
                bubble_x = x + spacing + i * (BUBBLE_SIZE + spacing)
                c.circle(bubble_x + BUBBLE_SIZE/2, bubble_y + BUBBLE_SIZE/2, BUBBLE_SIZE/2, stroke=1, fill=0)
                c.setFont("Helvetica", 16)

                c.drawCentredString(bubble_x + BUBBLE_SIZE/2, bubble_y + BUBBLE_SIZE/2 - 4, sound_word.bubbles[i])

def create_worksheet(sound_words: list[SoundWord], file_name: str) -> BytesIO:
    ''' Creates the worksheet pdf. Writes to a byte stream and saves locally before returning the byte stream.s'''
    byte_stream = BytesIO()
    c = Canvas(byte_stream, pagesize=letter)

    # Register the custom font
    pdfmetrics.registerFont(TTFont('CustomFont', font_path))

    # Draw the "Name" section with a solid line
    c.setFont("CustomFont", 24)
    c.drawString(MARGIN, 10.8 * inch - MARGIN / 2, "Name:")
    line_start = MARGIN + 70  # Adjusting for the label width
    line_end = letter[0] - MARGIN
    y_position = 10.8 * inch - MARGIN / 2 - 10  # Slightly lower than text
    c.setLineWidth(1)
    c.line(line_start, y_position, line_end, y_position)

    # Draw the title, centered
    c.setFont("CustomFont", 40)
    title_text = "First Sound BUBBLES"
    text_width = c.stringWidth(title_text, "CustomFont", 40)
    c.drawString((letter[0] - text_width) / 2, 10.4 * inch - MARGIN, title_text)

    # Add a simple border using asterisks
    border_char = "*"
    c.setFont("CustomFont", 15)
    for x in range(0, int(letter[0]), 30):
        c.drawString(x, 0, border_char)
        c.drawString(x, letter[1] - 10, border_char)
    for y in range(0, int(letter[1]), 30):
        c.drawString(0, y, border_char)
        c.drawString(letter[0] - 10, y, border_char)

    # Draw the grid
    draw_grid(c, sound_words)

    # Save the PDF to the byte stream
    c.showPage()
    c.save()

    # Save the in-memory PDF to a local file
    byte_stream.seek(0)  # Rewind the buffer before saving
    file_path = 'worksheet/generated_sheets/'
    os.makedirs(file_path, exist_ok=True)

    with open(os.path.join(file_path, file_name), 'wb') as f:
        f.write(byte_stream.getbuffer())
        
    # Rewind the buffer again before sending as response
    byte_stream.seek(0)
    return byte_stream


