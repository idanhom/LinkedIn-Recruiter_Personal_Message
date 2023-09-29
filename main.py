#TODO
"""
    #make so provides two versions in the same document.

    
Volvo Software tester (HiL)
Linkedin folder for test:
https://www.linkedin.com/talent/hire/1134091066/discover/recruiterSearch?searchContextId=091b02c1-2aa9-411b-9a2c-1c45fb93327e&searchHistoryId=10465098634&searchRequestId=20afa622-c257-4ae0-b08c-f1d75bdc5b13&start=0&uiOrigin=FACET_SEARCH

Job description
Your role will revolve around ensuring the functionality and attributes required for safety systems, particularly focusing on software verification. You'll lead the charge in exploring and defining innovative methodologies to accelerate development, all while enhancing system verification, with a primary focus on HiL (Hardware-in-the-Loop) fidelity and integration. Your scope will include Automatization and Continuous Integration and Testing across diverse environments – from HiL simulations to real-world car testing. The position: Conceptualize, demonstrate, and integrate groundbreaking virtual methodologies for brake software testing. Collaborate with concept development and suppliers in line with platform and vehicle targets. Breakdown comprehensive vehicle attribute requirements into system-level specifications and oversee their fulfillment. Ensure software verification aligns with project milestones. Develop cutting-edge verification methods. Leading collaborations with other teams and suppliers. Requirements: A master's degree in electrical, computational or automotive engineering (or a close equivalent). A passion for cars and chassis systems. Competence in developing virtual analysis tools for system engineering. Forward-thinking abilities to anticipate future needs and draw insights from simulation and real-world data analysis. Ideally, 2-5 years of experience in software testing or development, SiL/HiL tools, and chassis systems for passenger cars. Familiar with the following Tools: C++, Vector, GIT/Gerrit, CANalyzer, CANoe, Vtest studio, CAPL, SW Quality Assurance.
-----

Software Engineer (Testing/ verification) - (Volvo Cars)
https://www.linkedin.com/talent/hire/1134091066/discover/recruiterSearch?searchContextId=73fcdafe-e900-4e3d-8381-7adafcceb55a&searchHistoryId=10465098634&searchRequestId=3a7b5b69-f811-4261-8727-36a4ab129dd1&start=0

SE T/V (JOB AD)
If you're passionate about the automotive business and have a master's degree in electrical, computational or automotive engineering, we want you to be a part of our team at Sebratec. Your role will revolve around ensuring the functionality and attributes required for safety systems, particularly focusing on software verification. You'll lead the charge in exploring and defining innovative methodologies to accelerate development, all while enhancing system verification, with a primary focus on HiL (Hardware-in-the-Loop) fidelity and integration. Your scope will include Automatization and Continuous Integration and Testing across diverse environments – from HiL simulations to real-world car testing. The position: Conceptualize, demonstrate, and integrate groundbreaking virtual methodologies for brake software testing. Collaborate with concept development and suppliers in line with platform and vehicle targets. Breakdown comprehensive vehicle attribute requirements into system-level specifications and oversee their fulfillment. Ensure software verification aligns with project milestones. Develop cutting-edge verification methods. Leading collaborations with other teams and suppliers. Requirements: A master's degree in electrical, computational or automotive engineering (or a close equivalent). A passion for cars and chassis systems. Competence in developing virtual analysis tools for system engineering. Forward-thinking abilities to anticipate future needs and draw insights from simulation and real-world data analysis. Ideally, 2-5 years of experience in software testing or development, SiL/HiL tools, and chassis systems for passenger cars. Familiar with the following Tools: C++, Vector, GIT/Gerrit, CANalyzer, CANoe, Vtest studio, CAPL, SW Quality Assurance.


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

