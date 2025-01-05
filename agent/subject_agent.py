from typing import Optional
from langchain_openai import ChatOpenAI
from model.sound_word_base import SoundWordBases

import os
import logging
logger = logging.getLogger()

class SubjectAgent():
    '''Simple agent to generate image subjects. Has no memory or tools, just 1 off calls to OpenAI.'''

    def __init__(self):
        self.chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPEN_AI_API_KEY"), # type: ignore
            # temperature=0,
            max_tokens=200,
            timeout=5,
            max_retries=2,
        ).with_structured_output(schema=SoundWordBases, method='json_schema')

        self.system_message = (
                "system",
                '''
                You are a very experienced kindergarten teacher and writer.
                Your job is to help users generate indiviual nouns that will represent images appropriate for a kindergartener's coloring book.
                Make sure the nouns are commonly seen things that a 5 year old can recognize from an image. 
                The nouns must start with the letter defined by the user. 
                The nouns must be single words.
                The nouns must not be names of characters proper names such as 'Ryan' or 'Rudolph'.
                The nouns must not be colors such as 'Red Ornament' or 'Blue Ball'.
                Think step by step.
                ''',
            )

    def generate_subjects_same_first(self, starting_with: str, count: int, theme: Optional[str] = None) -> SoundWordBases:
        theming = '' if theme is None else f' Try to stick to the theme of {theme}.'
        user_message = (
                "user",
                f"Give me {count} indiviual nouns that are appropriate for a kindergartener's coloring book. The nouns must start with the letter {starting_with.lower()}.{theming}",
            )
        logger.info('User Message: %s', user_message)

        response: SoundWordBases = self.chat_model.invoke([self.system_message, user_message]) # type: ignore
        logger.info('Response from chat model: %s', response)

        # Ensure the reponse has words starting with the letters we expect
        response.validate_first_letters(starting_with)
        return response
    
    def generate_subjects(self, total: int, theme: Optional[str] = None) -> SoundWordBases:
        theming = '' if theme is None else f' Try to stick to the theme of {theme}.'
        user_message = (
                "user",
                f"Give me {total} indiviual nouns that are appropriate for a kindergartener's coloring book.{theming}",
            )
        logger.info('User Message: %s', user_message)

        response: SoundWordBases = self.chat_model.invoke([self.system_message, user_message]) # type: ignore
        logger.info('Response from chat model: %s', response)
        return response
