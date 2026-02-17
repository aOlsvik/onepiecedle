from playwright.sync_api import sync_playwright
from utils import get_todays_guess, guess_character
from setup import setup_game
from feedback import Feedback, FeedbackType
import os

CLASS_TO_FEEDBACK = {
    "square-good": FeedbackType.GREEN,
    "square-bad": FeedbackType.RED,
    "square-partial": FeedbackType.YELLOW,
    "square-inferior": FeedbackType.DOWN,
    "square-superior": FeedbackType.UP
}

def generate_state_file():
    with sync_playwright() as p_state:
        browser = p_state.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://onepiecedle.net/classic")
        # Click cookie button
        page.locator(".fc-cta-consent").click(timeout=10000)
        
        # Select "seen anime"
        page.locator("select").select_option("anime")  

        context.storage_state(path="state.json")
        browser.close()
        

if __name__ == "__main__":
    game_data, character_data = setup_game()
    
    if not os.path.exists("state.json"):
        print("State file not found. Generating new state file...")
        generate_state_file()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()
        page.goto("https://onepiecedle.net/classic")
        
        # Make first guess
        
        input_selector = "input[placeholder='Character name, alias, epithet ...']"
        guess_selector = "div[class='guess-button']"
        
        guess = get_todays_guess(character_data)
 
        # Wait for solve
        while not game_data.game_over():
            guess = guess['name']
            page.fill(input_selector, guess)
            page.wait_for_timeout(500)  # wait for the suggestions to load
            page.click(guess_selector)
            page.wait_for_timeout(4000)
            
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
            
            guess = new_guess
        
        page.wait_for_timeout(4000)
        # Press copy paste button to save the result
        share_buttons = page.locator(".share-button")
        share_buttons.nth(0).click()
        page.wait_for_timeout(2000)
            
        page.wait_for_timeout(2000)  # wait a bit before closing
        context.storage_state(path="state.json")
        browser.close()
