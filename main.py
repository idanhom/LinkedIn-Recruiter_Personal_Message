#TODO
"""

Easy access to job description: " "
Easy access to linkedin pipeline URL: " "

"""


from web_scraping import initialize_browser, expand_linkedin_sections, extract_linkedin_details
from user_interaction import monitor_url_and_prompt, get_output_language, open_notepad_with_message, open_independent_message_window
from api_interaction import generate_message_with_chatgpt
import threading

def main():
    # Set the browser choice in the code
    browser_choice = "firefox"  # Change this to "firefox" or "chrome" 
    
    # Initialize the browser based on the hardcoded choice
    browser = initialize_browser(browser_choice)
    
    # Get job description and LinkedIn URL
    job_description = input("Please enter the job description: ")
    linkedin_url = input("Please enter the initial LinkedIn folder URL (first profile's URL): ")
    
    # Navigate to the provided LinkedIn URL
    browser.get(linkedin_url)
    
    while True:
        if monitor_url_and_prompt(browser):
            # Get the desired output language BEFORE scraping the profile
            output_language = get_output_language()
            
            print("Activating script...")
            
            # Expand LinkedIn sections
            expand_linkedin_sections(browser)
            
            # Extract candidate information
            candidate_info = extract_linkedin_details(browser)
            print(f"\nProcessing profile of: {candidate_info['name']}")
            
            # Generate message with the adjusted function, using the previously selected output_language
            message = generate_message_with_chatgpt('OPENAI-API-KEY', job_description, candidate_info, output_language)

            if message:
                threading.Thread(target=open_independent_message_window, args=(message, candidate_info['name'])).start()
                browser.switch_to.window(browser.current_window_handle)
            
            print("\nwaiting for new profile to process...")



if __name__ == "__main__":
    main()

