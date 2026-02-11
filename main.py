from utils import load_json, get_todays_guess, guess_character, gather_feedback
from game_data import GameData

if __name__ == "__main__":
    onepiece_data = load_json('onepiece_data.json')
    character_data = onepiece_data['characters']
    character_data = [{key.lower().replace(" ", "_"): value for key, value in character.items()} for character in character_data]
    category_data = onepiece_data['categories']
    category_data = {key.lower().replace(" ", "_"): value for key, value in category_data.items()}
    game_data_options = {key.lower().replace(" ", "_") + "_options": list(value.get("options", [])) for key, value in category_data.items()}
    game_data = GameData(**game_data_options)
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


    
