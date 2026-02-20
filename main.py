from setup import setup_game
from utils import get_todays_guess, guess_character, gather_feedback

if __name__ == "__main__":
    game_data, character_data = setup_game()
    print("Welcome to One Piece Character Guessing Game!")
    print("=" * 40)
    best_guess = get_todays_guess(character_data)
    print(f"Today's first guess: {best_guess['name']}")
    while True:
        guessed_character = best_guess['name']
        guessed = input(f"Was {guessed_character} your guess? (y/n): ").strip().lower()
        if guessed == 'y':
            print("Great! Now you can provide feedback to improve future guesses.")
        else:
            guessed_character = input("Who was your guessed character? ").strip()

        if not guessed_character:
            break
        
        feedback = gather_feedback()
        best_guess, score, ties = guess_character(character_data, game_data, guessed_character, feedback)

        print(f"Best guess based on feedback: {best_guess['name']} (Score: {score})")
        print(f"Other tied guesses: {[tie['name'] for tie in ties if tie['name'] != best_guess['name']]}")
        
        correct_guess = input("Is this the correct character? (y/n): ").strip().lower()
        if correct_guess == 'y':
            print(f"Congratulations! You've guessed the character: {best_guess['name']}")
            break


    
