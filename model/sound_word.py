import random, string
from PIL.Image import Image
from model.sound_word_base import SoundWordBase, SoundWordBases
from model.prompts import Prompts
from image_generator import generate_sync


class SoundWord(SoundWordBase, extra='allow'):
    '''Word with a starting sound represented in a grid of images with bubbles for first letter selections.
    Extends SoundWordBase, init like: sound_word = SoundWord(**sound_word_base.model_dump())
    '''

    @staticmethod
    def build_sound_words(bases: SoundWordBases) -> list['SoundWord']:
        # Makes all SoundWordBases into SoundWord and sets the prompts
        sound_words = [SoundWord(**base.model_dump()) for base in bases.bases]
        for word in sound_words:
            word.set_prompts()
        return sound_words
                
    def generate_image(self):
        images, image_paths = generate_sync([self.prompt], [self.neg_prompt])
        self.set_image(images[0], image_paths[0])
              
    def set_prompts(self):
        self.prompt, self.neg_prompt = Prompts.get_prompts(self.word, self.category)

    def set_image(self, image: Image, file_path: str):
        self.image: Image = image
        self.image_path: str = file_path
        

    def generate_bubbles(self, total_choice_count: int):
        ''' Mutates the bubbles in self.'''

        # Select a letter for the bubble while excluding those that have already been used to avoid duplicates 
        remaining_letters = list(string.ascii_lowercase.replace(self.first_letter, ''))
        random_letters = [self.first_letter]
        for _ in range(total_choice_count - 1):
            random_letter = random.choice(remaining_letters)
            random_letters.append(random_letter)
            remaining_letters.remove(random_letter)
        
        # Shuffle order so the real answer is in a random bubble
        random.shuffle(random_letters)
        self.bubbles = random_letters

