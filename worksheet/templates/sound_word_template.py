from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from reportlab.pdfgen.canvas import Canvas
from model.sound_word import SoundWord

class SoundWordTemplate(BaseModel, ABC):
    ''' Interface for creating sound word templates. '''
    sound_words: list[SoundWord] = Field(default=[])
    image_theme: str

    @abstractmethod
    def create_pdf(self) -> Canvas:
        pass
        
