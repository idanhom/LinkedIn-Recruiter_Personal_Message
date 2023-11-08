#TODO
"""
    #make so provides two versions in the same document.

    
SAAB

Join our group specializing in Embedded Design. We primarily work on FPGA programming with a focus on embedded processors. We are excited to expand our team to tackle a range of thrilling projects including Low-Level Hardware Programming with a Firmware Focus (VHDL) where you can dive deep into hardware programming with a focus on Firmware development using VHDL, Implementation, Integration, and Lab Testing where you can collaborate on the implementation and integration of embedded systems, putting your solutions to the test in our lab environment, Develop Test Functions to create innovative test functions for both in-house designs and to evaluate the functionality of others' creations, Utilize Tools as we rely on tools like Matlab, Python, and SAFT (FitNesse) to craft comprehensive test cases, and Troubleshooting where you can engage in troubleshooting activities spanning both new and legacy functionalities. Requirements include FPGA Understanding where a solid grasp of how FPGA (Field-Programmable Gate Array) technology functions is crucial, Proficiency in VHDL as a proven track record in VHDL is a mandatory requirement, Additional Skills where knowledge of programming languages like C, C++, Matlab, and Python is highly advantageous, Agile Team Player where comfort and enthusiasm for working in agile teams is a must, and FPGA Programming Passion where a genuine desire and passion for programming FPGA devices is highly valued.

https://www.linkedin.com/talent/hire/1133038714/discover/recruiterSearch?searchContextId=63b54328-6ace-40cc-b686-eed49ccd498b&searchHistoryId=10476218414&searchRequestId=7c4fb0d6-ea35-451c-9263-8acbff3ba3ae&start=0


&aBd%YaHX4

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
            message = generate_message_with_chatgpt('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', job_description, candidate_info, output_language)

            if message:
                threading.Thread(target=open_independent_message_window, args=(message, candidate_info['name'])).start()
                browser.switch_to.window(browser.current_window_handle)
            
            print("\nwaiting for new profile to process...")



if __name__ == "__main__":
    main()

