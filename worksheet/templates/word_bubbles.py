from io import BytesIO
from typing import Any
from worksheet.templates.sound_word_template import SoundWordTemplate
from pydantic import Field
from worksheet.pdf_generator import create_worksheet
from worksheet.templates.word_bubbles_builder import WordBubblesBuilder
from model.sound_word import SoundWord
from agent.subject_agent import SubjectAgent

class WordBubbles(SoundWordTemplate):
    ''' 
    A grid of images with 3 bubbles underneath each. 
    Kids color in the bubble with the letter that matches the starting letter of the thing depicted in the image.
    '''
    image_count: int = Field(default=9)
    bubble_count: int = Field(default=3)

    @staticmethod
    def builder() -> WordBubblesBuilder:
        return WordBubblesBuilder()
    
    def model_post_init(self, __context: Any):
            ''' Post-init to build the rest of the fields that are dependent on others. '''
            # Generate sound words
            self.create_sound_words()
            # Generate bubbles and images for sound words
            for word in self.sound_words:
                word.generate_bubbles(self.bubble_count)
                word.generate_image()
    
    def create_sound_words(self):
        ''' Call Agent to generate the things to be displayed in the images. '''
        bases = SubjectAgent().generate_subjects(self.image_count, self.image_theme)
        self.sound_words = SoundWord.build_sound_words(bases)

    def create_pdf(self, file_name: str = 'test_worksheet.pdf') -> BytesIO:
        ''' Creates a PDF based with this WordBubbles template.
        Optionally, set a file name to save it locally.
        '''
        return create_worksheet(self.sound_words, file_name=file_name)

