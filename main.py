#TODO
"""
    #make so provides two versions in the same document.

Linkedin folder for test:
https://www.linkedin.com/talent/search/profile/AEMAACRLmGkBvbWWoxy97ZdGZs3_QMrmvfdtcVk?highlightedPatternSource=%255Cbaosp&searchContextId=703aadf7-a287-4015-b7f6-54304289277e&searchHistoryId=10466418464&searchKeyword=aosp%20&searchRequestId=cd4b32ea-2813-492e-bf67-9a2e2b398e12&start=0&trk=SEARCH_GLOBAL

Job description
The company is growing and as a part of this, we are now looking for a skilled Android Developer for one of our clients! In your role, you will work with Android platform development (AOS) and customizing the operating system for the client's requirements. Would you like to work within a company that shares a startup mentality and a commitment to be a great workplace? Be a part of our Team! Who are you? You are social, open-minded, flexible, and thrive under challenging and changing conditions. As a person you are a curious, innovative, and analytical problem solver. You enjoy teamwork and have an inclusive approach to your work. You are not afraid to propose new ideas and promote them to the team. You deliver high-quality code and feel significant ownership of the code you produce. You are willing to cater to the complete lifecycle of the code. Mandatory requirements: 4+ years working with Software Development focusing on Android, Java, Kotlin, AOSP, Experience working with Android Platform development. Desired skills: CAN Architecture, GIT. 

&aBd%YaHX4

"""


from web_scraping import initialize_browser, expand_linkedin_sections, extract_linkedin_details
from user_interaction import monitor_url_and_prompt, get_output_language, open_notepad_with_message, open_independent_message_window
from api_interaction import generate_message_with_chatgpt

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
            message = generate_message_with_chatgpt('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', job_description, candidate_info, output_language)

            if message:
                open_independent_message_window(message, candidate_info['name'])
                browser.switch_to.window(browser.current_window_handle)
            
            print("\nwaiting for new profile to process...")



if __name__ == "__main__":
    main()

