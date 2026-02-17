import json
from feedback import Feedback, FeedbackType
from game_data import GameData
import random
from chapters import arc_before


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
def get_todays_guess(character_data):
    from datetime import datetime
    import random

    today = datetime.now().date()
    random.seed(today.toordinal())
    return random.choice(character_data)

def guess_character(character_data, game_data: GameData, guess: str, feedback: Feedback):
    random.seed()  # Reset seed to system time for tie-breaking randomness
    guessed_character = None
    for character in character_data:
        if character['name'].lower() == guess.lower():
            guessed_character = character
            break

    if guessed_character is None:
        return None, "Character not found in the dataset.", []
    
    fb = feedback.__dict__
    gd = game_data.to_dict(printable=False)

    for category_name, feedback_type in fb.items():
        gd_cat = gd[category_name]
        category_guess = guessed_character[category_name]
        category_guess = category_guess if isinstance(category_guess, list) else [category_guess]

        gd_cat.update(category_guess, feedback_type)

    if game_data.game_over():
        return guessed_character, 1000, []

    best_guess = None
    best_score = -1
    ties = []
    for character in character_data:
        score = game_data.evaluate_guess(character)
        if score > best_score:
            ties = [character]
            best_score = score
            best_guess = character
        elif score == best_score:
            ties.append(character)
            # pick random
            if random.random() < 0.5:
                best_guess = character

    if best_guess is None:
        raise ValueError("No valid guesses found.")

    return best_guess, best_score, ties


def parse_feedback(prompt: str, allowed: set[FeedbackType]) -> FeedbackType:
    shortcuts = {
        "g": FeedbackType.GREEN,
        "r": FeedbackType.RED,
        "y": FeedbackType.YELLOW,
        "u": FeedbackType.UP,
        "d": FeedbackType.DOWN,
    }

    allowed_values = {ft.value: ft for ft in allowed}

    while True:
        raw = input(prompt).strip().lower()

        if raw in shortcuts and shortcuts[raw] in allowed:
            return shortcuts[raw]

        if raw in allowed_values:
            return allowed_values[raw]

        print(
            f"Invalid input. Allowed: "
            + ", ".join(sorted(ft.value for ft in allowed))
        )


def gather_feedback() -> Feedback:
    return Feedback(
        gender=parse_feedback(
            "Gender feedback (g/r): ",
            {FeedbackType.GREEN, FeedbackType.RED}
        ),
        affiliation=parse_feedback(
            "Affiliation feedback (g/r): ",
            {FeedbackType.GREEN, FeedbackType.RED}
        ),
        devil_fruit=parse_feedback(
            "Devil fruit feedback (g/r): ",
            {FeedbackType.GREEN, FeedbackType.RED}
        ),
        haki=parse_feedback(
            "Haki feedback (g/y/r): ",
            {FeedbackType.GREEN, FeedbackType.YELLOW, FeedbackType.RED}
        ),
        last_bounty=parse_feedback(
            "Last bounty (u/d/g): ",
            {FeedbackType.UP, FeedbackType.DOWN, FeedbackType.GREEN}
        ),
        height=parse_feedback(
            "Height (u/d/g): ",
            {FeedbackType.UP, FeedbackType.DOWN, FeedbackType.GREEN}
        ),
        origin=parse_feedback(
            "Origin (g/r): ",
            {FeedbackType.GREEN, FeedbackType.RED}
        ),
        first_arc=parse_feedback(
            "First arc (u/d/g): ",
            {FeedbackType.UP, FeedbackType.DOWN, FeedbackType.GREEN}
        )
    )


def compare_character_to_correct_answer(guess_character, correct_character):
    feedbacks = []

    def true_false_to_feedback(field_name):
        guess_value = guess_character[field_name]
        correct_value = correct_character[field_name]
        if guess_value == correct_value:
            feedbacks.append(FeedbackType.GREEN)
        else:
            feedbacks.append(FeedbackType.RED)
            
    def up_down_to_feedback(field_name):
        guess_value = guess_character[field_name]
        correct_value = correct_character[field_name]
        if guess_value == correct_value:
            feedbacks.append(FeedbackType.GREEN)
        elif guess_value < correct_value:
            feedbacks.append(FeedbackType.UP)
        else:
            feedbacks.append(FeedbackType.DOWN)
    
    def multiple_choice_to_feedback(field_name):
        guess_value = guess_character[field_name]
        correct_value = correct_character[field_name]
        if set(guess_value) == set(correct_value):
            feedbacks.append(FeedbackType.GREEN)
        elif any(item in correct_value for item in guess_value):
            feedbacks.append(FeedbackType.YELLOW)
        else:
            feedbacks.append(FeedbackType.RED)
            
    
    true_false_to_feedback("gender")
    true_false_to_feedback("affiliation")
    true_false_to_feedback("devil_fruit")
    multiple_choice_to_feedback("haki")
    up_down_to_feedback("last_bounty")
    up_down_to_feedback("height")
    true_false_to_feedback("origin")
    
    if guess_character["first_arc"] == correct_character["first_arc"]:
        feedbacks.append(FeedbackType.GREEN)
    elif arc_before(guess_character["first_arc"], correct_character["first_arc"]):
        feedbacks.append(FeedbackType.UP)
    else:
        feedbacks.append(FeedbackType.DOWN)
        
    return Feedback(*feedbacks)
    
    
    
        
    