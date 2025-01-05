from dataclasses import dataclass, field


@dataclass
class Prompts:
    '''Holds prompts for image generation depending on subject category. TODO: move to config''' 
    subject: str = field(init=True)

    def __post_init__(self):
        self.shared = 'cartoon, simple form, soft bold outline, basic shapes, easy to color, simple, basic, minimal, black and white, pure white background'
        # TODO: more categories
        self.animal = f'Coloring page, {self.subject}, side view of entire body, standing, cute, {self.shared}'
        self.animal_neg = 'complex, realistic, color, detailed, drawing tools, art supplies, stationery'

        self.food = f'Coloring page, {self.subject}, {self.shared}'
        self.food_neg: str = 'complex, realistic, color, detailed, drawing tools, art supplies, stationery'

        self.object: str = f'Coloring page, {self.subject}, {self.shared}'
        self.object_neg: str = 'complex, realistic, color, detailed, drawing tools, art supplies, stationery'

    @staticmethod
    def get_prompts(subject: str, category: str):
        prompts = Prompts(subject)
        
        if category == 'animal':
            return prompts.animal, prompts.animal_neg
        elif category == 'food':
            return prompts.food, prompts.food_neg
        else:
            return prompts.object, prompts.object_neg