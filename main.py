import logging
from worksheet.templates.word_bubbles import WordBubbles
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()


def main():
    wordBubbles = WordBubbles.builder() \
        .set_image_theme('Thanksgiving') \
        .build()
    wordBubbles.create_pdf('test_worksheet.pdf')
    
if __name__ == "__main__":
    main()
 
