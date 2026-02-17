from utils import get_todays_guess, guess_character, gather_feedback, compare_character_to_correct_answer
from setup import setup_game
import random
import json

if __name__ == "__main__":
    game_data, character_data = setup_game()
    correct_character = random.choice(character_data)
    print("Welcome to One Piece Character Guessing Game!")
    print("=" * 40)
    best_guess = get_todays_guess(character_data)
    print(f"Today's first guess: {best_guess['name']}")
    guess_count = 0
    while not game_data.game_over():
        guessed_character = best_guess['name']
       
        feedback = compare_character_to_correct_answer(best_guess, correct_character)
        print(f"Feedback for {guessed_character}: {feedback}")
        best_guess, score, ties = guess_character(character_data, game_data, guessed_character, feedback)

        guess_count += 1

        if game_data.game_over():
            print(f"Congratulations! You've guessed {best_guess['name']} in {guess_count} guesses")
        else:
          print(f"Best guess based on feedback: {best_guess['name']} (Score: {score})")
          if len(ties) > 1:
            print(f"Other tied guesses: {[tie['name'] for tie in ties if tie['name'] != best_guess['name']]}")
        
        



    
