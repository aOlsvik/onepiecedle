from playwright.sync_api import sync_playwright
from utils import get_todays_guess, load_json, guess_character
from game_data import GameData
from feedback import Feedback, FeedbackType

CLASS_TO_FEEDBACK = {
    "square-good": FeedbackType.GREEN,
    "square-bad": FeedbackType.RED,
    "square-partial": FeedbackType.YELLOW,
    "square-inferior": FeedbackType.DOWN,
    "square-superior": FeedbackType.UP
}

with sync_playwright() as p:
    onepiece_data = load_json('onepiece_data.json')
    character_data = onepiece_data['characters']
    character_data = [{key.lower().replace(" ", "_"): value for key, value in character.items()} for character in character_data]
    category_data = onepiece_data['categories']
    category_data = {key.lower().replace(" ", "_"): value for key, value in category_data.items()}
    game_data_options = {key.lower().replace(" ", "_") + "_options": list(value.get("options", [])) for key, value in category_data.items()}
    game_data = GameData(**game_data_options)
    
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.goto("https://onepiecedle.net/classic")
    
    # Make first guess
    guess = get_todays_guess(character_data)['name']
    page.fill("input[placeholder='Character name, alias, epithet ...']", guess)
    page.wait_for_timeout(500)  # wait for the suggestions to load
    page.click("div[class='guess-button']")
    page.wait_for_timeout(4000)
    
    # Wait for solve
    while True:
        result = page.locator(".classic-answer").last
        squares = result.locator(".square")
        feedback = []
        for i in range(1, squares.count()):
            sqr = squares.nth(i)
            for cls in CLASS_TO_FEEDBACK.keys():
                if sqr.get_attribute("class").find(cls) != -1:
                    feedback.append(CLASS_TO_FEEDBACK[cls])
                    break
        
        feedback_obj = Feedback(
            gender=feedback[0],
            affiliation=feedback[1],
            devil_fruit=feedback[2],
            haki=feedback[3],
            last_bounty=feedback[4],
            height=feedback[5],
            origin=feedback[6],
            first_arc=feedback[7]
        )
        
        new_guess, score, ties = guess_character(character_data, game_data, guess, feedback_obj)
        
        if game_data.game_over():
            page.wait_for_timeout(4000)
            # Press copy paste button to save the result
            share_buttons = page.locator(".share-button")
            share_buttons.nth(0).click()
            page.wait_for_timeout(2000)
            break
        else:
            guess = new_guess['name']
            page.fill("input[placeholder='Character name, alias, epithet ...']", guess)
            page.wait_for_timeout(500)  # wait for the suggestions to load
            page.click("div[class='guess-button']")
            page.wait_for_timeout(4000)
            
          
    page.wait_for_timeout(2000)  # wait a bit before closing
    browser.close()

