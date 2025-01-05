from __future__ import annotations

from typing import TYPE_CHECKING
from pydantic import ValidationError

# Avoid circular import
if TYPE_CHECKING: 
    from worksheet.templates.word_bubbles import WordBubbles


class WordBubblesBuilder():
    def set_image_count(self, image_count: int):
        self.image_count = image_count
        return self
    
    def set_bubble_count(self, bubble_count: int):
        self.bubble_count = bubble_count
        return self
    
    def set_image_theme(self, theme: str):
        self.image_theme = theme
        return self

    
    def build(self) -> WordBubbles:
        from worksheet.templates.word_bubbles import WordBubbles

        try:
            # Prepare the arguments for the WordBubbles constructor to allow defaults to work properly
            init_args = {}
            
            if hasattr(self, 'image_count'):
                init_args['image_count'] = self.image_count
            
            if hasattr(self, 'bubble_count'):
                init_args['bubble_count'] = self.bubble_count
            
            # Enforce image_theme as a required 
            if not hasattr(self, 'image_theme'):
                raise ValidationError('image_theme not set when building.')
            else:                 
                init_args['image_theme'] = self.image_theme

            # Create the WordBubbles instance using only the set attributes
            wordBubbles = WordBubbles(**init_args)
            return wordBubbles
        except ValidationError as e:
            # TODO: Handle any validation errors that arise during instance creation
            print(f"Validation error during build: {e}")
            raise
