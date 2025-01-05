from typing import Literal
from model.prompts import Prompts
from pydantic import BaseModel, Field, field_validator


class SoundWordBase(BaseModel):
    ''' Base version of a sound word. No additional properties so this schema can be returned by LangChain OpenAi Structured Outputs'''

    word: str = Field(init=True, description='The word to be represented in the image. Must be a single word.')
    first_letter: str = Field(init=True, description='The first letter in the word.')
    category: Literal['animal', 'food', 'object'] = Field(init=True, description='The category the word belongs to.')


    @field_validator('word')
    def validate_word(cls, word):
        if not word:
            raise ValueError("The 'word' field must contain at least one letter.")
        return word
    
    @field_validator('first_letter')
    def validate_first_letter(cls, first_letter: str, info):
        # Use info so we get the post-validation version of the word
        word = info.data.get('word')
        if word and first_letter.lower() != word[0].lower():
            raise ValueError(f"first_letter '{first_letter}' does not match the first letter of the word '{word[0]}'")
        return first_letter.lower()

      
class SoundWordBases(BaseModel):
    '''List of SoundWordBase. Wrapping this way so to pass a Pydantic class to the structured outputs for validation.'''
    bases: list[SoundWordBase] = Field(init=True)

    def validate_first_letters(self, expected_first_letter: str):
        for sound_word in self.bases:
            if sound_word.first_letter.lower() != expected_first_letter.lower():
                raise ValueError(f"First letter '{sound_word.first_letter.lower()}' in word '{sound_word}' does not match the expected first letter '{expected_first_letter}'")
            
