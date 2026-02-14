from feedback import FeedbackType
from chapters import *
import math

class Category:
    def __init__(self, options: list):
        self.options = options
        self.correct = None
        self.wrongs = set()
        self.yellows = set()

    def update(self, category_guess: list, feedback_type: FeedbackType):
        raise NotImplementedError("Subclasses should implement this method")
    
    def evaluate_guess(self, option_name):
        raise NotImplementedError("Subclasses should implement this method")
        

class Gender(Category):
    def __init__(self, options: list):
        super().__init__(options)


    def update(self, category_guess: list, feedback_type: FeedbackType):
        option_name = category_guess[0]
        if self.correct is not None:
            return
        
        if feedback_type == FeedbackType.GREEN:
            self.correct = option_name
        elif feedback_type == FeedbackType.RED:
            self.correct = self.options[0] if option_name == self.options[1] else self.options[1]
            self.wrongs.add(option_name)
        elif feedback_type == FeedbackType.YELLOW:
            raise ValueError("Yellow feedback should not happen for Gender")
        else:
            raise ValueError(f"Invalid feedback type for Gender: {feedback_type}")
        
    def evaluate_guess(self, category_guess: list):
        """
        Docstring for evaluate_guess

        returns 1 if option_name is correct, -1 if it's wrong
        """
        option_name = category_guess[0]
        if self.correct is not None:
            return 1 if option_name == self.correct else -1
        
        return -1 if option_name in self.wrongs else 0
    
    def to_dict(self):
        return {
            "correct": self.correct,
            "wrongs": list(self.wrongs)
        }
        
class Affiliation(Category):
    def __init__(self, options: list):
        super().__init__(options)

    def update(self, category_guess: list, feedback_type: FeedbackType):
        option_name = category_guess[0]
        if self.correct is not None:
            return
        
        if feedback_type == FeedbackType.GREEN:
            self.correct = option_name
        elif feedback_type == FeedbackType.RED:
            self.wrongs.add(option_name)
        elif feedback_type == FeedbackType.YELLOW:
            raise ValueError("Yellow feedback should not happen for Affiliation")
        else:
            raise ValueError(f"Invalid feedback type for Affiliation: {feedback_type}")
        
    def evaluate_guess(self, category_guess: list):
        """
        Docstring for evaluate_guess

        returns 1 if option_name is correct, -1 if it's wrong
        """
        option_name = category_guess[0]
        if self.correct is not None:
            return 1 if option_name == self.correct else -1
        
        return -1 if option_name in self.wrongs else 0
    
    def to_dict(self):
        return {
            "correct": self.correct,
            "wrongs": list(self.wrongs)
        }
    
class DevilFruit(Category):
    def __init__(self, options: list):
        super().__init__(options)

    def update(self, category_guess: list, feedback_type: FeedbackType):
        option_name = category_guess[0]
        
        if feedback_type == FeedbackType.GREEN:
            self.correct = option_name
        elif feedback_type == FeedbackType.RED:
            self.wrongs.add(option_name)
        elif feedback_type == FeedbackType.YELLOW:
            raise ValueError("Yellow feedback should not happen for Devil Fruit")
        else:
            raise ValueError(f"Invalid feedback type for Devil Fruit: {feedback_type}")
        
    def evaluate_guess(self, category_guess: list):
        """
        Docstring for evaluate_guess
        
        returns 1 if option_name is correct, -1 if it's wrong
        """
        option_name = category_guess[0]
        if self.correct is not None:
            return 1 if option_name == self.correct else -1
        
        return -1 if option_name in self.wrongs else 0
    
    def to_dict(self):
        return {
            "correct": self.correct,
            "wrongs": list(self.wrongs)
        }
    
class Haki(Category):
    def __init__(self, options: list):
        super().__init__(options)

    def update(self, category_guess: list, feedback_type: FeedbackType):
        if self.correct is not None:
            return
        
        if feedback_type == FeedbackType.GREEN:
            self.correct = category_guess
        elif feedback_type == FeedbackType.RED:
            for option in category_guess:
                self.wrongs.add(option)
        elif feedback_type == FeedbackType.YELLOW:
            for option in category_guess:
                self.yellows.add(option)
        else:
            raise ValueError(f"Invalid feedback type for Haki: {feedback_type}")
        
    def evaluate_guess(self, category_guess: list):
        """
        Docstring for evaluate_guess
        
        returns 1 if option_name is correct, 0 if it's yellow, -1 if it's wrong
        """

        if self.correct is not None:
            return 1 if category_guess == self.correct else -1
        
        if any(option in self.wrongs for option in category_guess):
            return -1
        
        if any(option in self.yellows for option in category_guess):
            return 0
        
        if all((option not in self.wrongs and option not in self.yellows) and option in self.options for option in category_guess):
            return 0
        
        if any(option not in self.options for option in category_guess):
            raise ValueError(f"Invalid option in category_guess for Haki: {category_guess}")
        
        return 0
    
    def to_dict(self):
        return {
            "correct": self.correct,
            "wrongs": list(self.wrongs),
            "yellows": list(self.yellows),
        }
    
class LastBounty(Category):
    def __init__(self, options: list):
        super().__init__(options)
        self.min_bounty = -math.inf
        self.max_bounty = math.inf

    def update(self, category_guess: list, feedback_type: FeedbackType):
        option_name = category_guess[0]
        if self.correct is not None:
            return
        
        if feedback_type == FeedbackType.GREEN:
            self.correct = option_name
        elif feedback_type == FeedbackType.UP:
            self.min_bounty = max(self.min_bounty, option_name)
        elif feedback_type == FeedbackType.DOWN:
            self.max_bounty = min(self.max_bounty, option_name)
        else:
            raise ValueError(f"Invalid feedback type for Last Bounty: {feedback_type}")
        
    def evaluate_guess(self, category_guess: list):
        """
        Docstring for evaluate_guess
        
        returns 1 if guess is correct, 0 if it's between min and max bounty, -1 if it's outside the range
        """
        option_name = category_guess[0]
        if self.correct is not None:
            return 1 if option_name == self.correct else -1
        
        return -1 if option_name < self.min_bounty or option_name > self.max_bounty else 0
    
    def to_dict(self):
        return {
            "correct": self.correct,
            "min_bounty": self.min_bounty,
            "max_bounty": self.max_bounty
        }

    
class Height(Category):
    def __init__(self, options: list):
        super().__init__(options)
        self.min_height = -math.inf
        self.max_height = math.inf

    def update(self, category_guess: list, feedback_type: FeedbackType):
        option_name = category_guess[0]
        if self.correct is not None:
            return
        
        if feedback_type == FeedbackType.GREEN:
            self.correct = option_name
        elif feedback_type == FeedbackType.UP:
            self.min_height = max(self.min_height, option_name+1)
        elif feedback_type == FeedbackType.DOWN:
            self.max_height = min(self.max_height, option_name-1)
        else:
            raise ValueError(f"Invalid feedback type for Height: {feedback_type}")
        
    def evaluate_guess(self, category_guess: list):
        """
        Docstring for evaluate_guess
        
        returns 1 if guess is correct, 0 if it's between min and max height, -1 if it's outside the range
        """
        option_name = category_guess[0]
        if self.correct is not None:
            return 1 if option_name == self.correct else -1
        
        return -1 if option_name < self.min_height or option_name > self.max_height else 0
    
    def to_dict(self):
        return {
            "correct": self.correct,
            "min_height": self.min_height,
            "max_height": self.max_height
        }

    

class Origin(Category):
    def __init__(self, options: list):
        super().__init__(options)

    def update(self, category_guess: list, feedback_type: FeedbackType):
        option_name = category_guess[0]
        if self.correct is not None:
            return
        
        if feedback_type == FeedbackType.GREEN:
            self.correct = option_name
        elif feedback_type == FeedbackType.RED:
            self.wrongs.add(option_name)
        elif feedback_type == FeedbackType.YELLOW:
            raise ValueError("Yellow feedback should not happen for Origin")
        else:
            raise ValueError(f"Invalid feedback type for Origin: {feedback_type}")
        
    def evaluate_guess(self, category_guess: list):
        """
        Docstring for evaluate_guess

        returns 1 if option_name is correct, -1 if it's wrong
        """
        option_name = category_guess[0]
        if self.correct is not None:
            return 1 if option_name == self.correct else -1
        
        return -1 if option_name in self.wrongs else 0

    def to_dict(self):
        return {
            "correct": self.correct,
            "wrongs": list(self.wrongs)
        }


class FirstArc(Category):
    def __init__(self, options: list):
        super().__init__(options)
        self.earliest_arc = options[0]
        self.oldest_arc = options[-1]

    def update(self, category_guess: list, feedback_type: FeedbackType):
        option_name = category_guess[0]
        if self.correct is not None:
            return
        
        if feedback_type == FeedbackType.GREEN:
            self.correct = option_name
        elif feedback_type == FeedbackType.UP:
            self.earliest_arc = ORDER_TO_ARC[min(ARC_TO_ORDER[option_name] + 1, len(ARC_CHAPTERS) - 1)] if arc_before(self.earliest_arc, option_name) else self.earliest_arc
        elif feedback_type == FeedbackType.DOWN:
            self.oldest_arc = ORDER_TO_ARC[max(0, ARC_TO_ORDER[option_name] - 1)] if arc_before(option_name, self.oldest_arc) else self.oldest_arc
        else:
            raise ValueError(f"Invalid feedback type for First Arc: {feedback_type}")
        
    def evaluate_guess(self, category_guess: list):
        """
        Docstring for evaluate_guess

        returns 1 if guess is correct, 0 if it's between earliest and oldest arc, -1 if it's outside the range
        """
        option_name = category_guess[0]
        if self.correct is not None:
            return 1 if option_name == self.correct else -1
        
        return -1 if arc_before(option_name, self.earliest_arc) or arc_before(self.oldest_arc, option_name) else 0
        
    def to_dict(self):
        return {
            "correct": self.correct,
            "earliest_arc": self.earliest_arc,
            "oldest_arc": self.oldest_arc
        }

class GameData:
    def __init__(self, gender_options: list, affiliation_options: list, devil_fruit_options: list, haki_options: list, origin_options: list, **kwargs):
        self.gender = Gender(gender_options)
        self.affiliation = Affiliation(affiliation_options)
        self.devil_fruit = DevilFruit(devil_fruit_options)
        self.haki = Haki(haki_options)
        self.last_bounty = LastBounty([])
        self.height = Height([])
        self.origin = Origin(origin_options)
        self.first_arc = FirstArc([arc for arc, _, _ in ARC_CHAPTERS])

    def to_dict(self, printable=True):
        if printable:
            return {
                "gender": self.gender.to_dict(),
                "affiliation": self.affiliation.to_dict(),
                "devil_fruit": self.devil_fruit.to_dict(),
                "haki": self.haki.to_dict(),
                "last_bounty": self.last_bounty.to_dict(),
                "height": self.height.to_dict(),
                "origin": self.origin.to_dict(),
                "first_arc": self.first_arc.to_dict()
            }
        else:
            return {
                "gender": self.gender,
                "affiliation": self.affiliation,
                "devil_fruit": self.devil_fruit,
                "haki": self.haki,
                "last_bounty": self.last_bounty,
                "height": self.height,
                "origin": self.origin,
                "first_arc": self.first_arc
            }
    
    def evaluate_guess(self, character):
        score = 0
        score += self.gender.evaluate_guess([character['gender']])
        score += self.affiliation.evaluate_guess([character['affiliation']])
        score += self.devil_fruit.evaluate_guess([character['devil_fruit']])
        score += self.haki.evaluate_guess(character['haki'])
        score += self.last_bounty.evaluate_guess([character['last_bounty']])
        score += self.height.evaluate_guess([character['height']])
        score += self.origin.evaluate_guess([character['origin']])
        score += self.first_arc.evaluate_guess([character['first_arc']])
        return score

    def game_over(self):
        if self.gender.correct is None:
            return False
        if self.affiliation.correct is None:
            return False
        if self.devil_fruit.correct is None:
            return False
        if self.haki.correct is None:
            return False
        if self.last_bounty.correct is None:
            return False
        if self.height.correct is None:
            return False
        if self.origin.correct is None:
            return False
        if self.first_arc.correct is None:
            return False
        return True