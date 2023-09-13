#TODO
    #make so that message adheres to Cialdini's principles of persuation
    #perhaps not all... but a few selected chosen ones...
    #also, provide examples of how i want the message to look like



    #linkedin folder for test:
    # https://www.linkedin.com/talent/hire/913959218/manage/all/profile/AEMAAB_1PmsBzg6HYQ2J_fKtV8eFRnWrVJTuc0A?project=913959218&trk=PROJECT_PIPELINE

    #job description
    #Sebratec is a Software and Engineering company specializing in services for the tech industry. We deliver expertise to our clients and help people to reach the next challenge in their careers. Our goal is to create a bridge between Sweden and Brazil, delivering both consulting, offshore, and in-house services. The company is growing and as a part of this, we are now looking for a skilled Android Developer for one of our clients! In your role, you will work with Android platform development (AOS) and customizing the operating system for the client's requirements. Would you like to work within a company that shares a startup mentality and a commitment to be a great workplace? Be a part of our Team! Who are you? You are social, open-minded, flexible, and thrive under challenging and changing conditions. As a person you are a curious, innovative, and analytical problem solver. You enjoy teamwork and have an inclusive approach to your work. You are not afraid to propose new ideas and promote them to the team. You deliver high-quality code and feel significant ownership of the code you produce. You are willing to cater to the complete lifecycle of the code. Mandatory requirements: 4+ years working with Software Development focusing on Android, Java, Kotlin, AOSP, and experience working with Android Platform development. Desired skills: CAN Architecture and GIT.
    



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import requests
import subprocess
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver

USER_AGENTS = {
    "firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def initialize_browser(agent_key="firefox"):
    """
    Initialize the selected browser using Selenium's WebDriver with the desired user agent.
    Args:
    - agent_key (str): Key to select the user agent from the USER_AGENTS dictionary.
    
    Returns:
    - browser instance.
    """
    user_agent = USER_AGENTS.get(agent_key, USER_AGENTS["firefox"])  # Default to Firefox if key not found
    
    if agent_key == "firefox":
        profile_path = r"C:\Users\OscarPettersson\AppData\Roaming\Mozilla\Firefox\Profiles\8ewzfvju.SeleniumProfile"
        options = Options()
        options.set_preference("general.useragent.override", user_agent)
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference('useAutomationExtension', False)
        options.profile = profile_path
        browser = webdriver.Firefox(options=options)
        # Hide selenium
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



    elif agent_key == "chrome":
        options = ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "load-extension"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('useAutomationExtension', False)
        browser = ChromeDriver(options=options)

    else:
        raise ValueError(f"Unsupported browser choice: {agent_key}")

    browser.set_window_size(1366, 768)
    return browser



def monitor_url_and_prompt(browser):
    """
    Monitor the browser URL for changes. If a change is detected, prompt the user to activate the script.
    Returns True if the user wants to activate the script, False otherwise.
    """
    current_url = browser.current_url
    while True:
        # If the URL has changed, ask the user if they want to activate the script
        if browser.current_url != current_url:
            current_url = browser.current_url
            # Extract the candidate's name
            try:
                name_element = browser.find_element(By.XPATH, "//div[contains(@class, 'artdeco-entity-lockup__title')]")
                candidate_name = name_element.text.strip()
            except NoSuchElementException:
                candidate_name = 'Unknown Profile'

            decision = input(f"URL changed to profile of {candidate_name}. Do you want to activate the script on this profile? (y/n): ")
            if decision.lower() == 'y':
                return True
        time.sleep(2)  # Check every 2 seconds
        
def expand_linkedin_sections(browser):
    """
    Expand all relevant sections of the LinkedIn profile.
    """
    # Expand "See more of summary"
    try:
        summary_button = browser.find_element(By.XPATH, "//a[@id='line-clamp-show-more-button' and @aria-expanded='false' and @role='button' and text()='See more of summary']")
        summary_button.click()
        time.sleep(0.5)  # Wait for the content to expand
    except NoSuchElementException:
        print("Couldn't find the 'See more of summary' button.")
        pass

    # Continuously click "See more positions" until it no longer exists
    while True:
        try:
            experience_button = browser.find_element(By.XPATH, "//button[@aria-label='See more positions']")
            experience_button.click()
            time.sleep(0.5)  # Wait for the content to expand
        except NoSuchElementException:
            break  # Exit the loop when the button is no longer found

    # Expand "Show all 42 skills"
    try:
        skills_button = browser.find_element(By.XPATH, "//button[contains(@aria-label, 'Show all') and contains(@class, 'expandable-list__button')]")
        skills_button.click()
        time.sleep(0.5)  # Wait for the content to expand
    except NoSuchElementException:
        pass


def extract_linkedin_details(browser):
    """
    Extract relevant details from the LinkedIn profile.
    """
    details = {}

    # Extract name
    try:
        name_element = browser.find_element(By.XPATH, "//div[contains(@class, 'artdeco-entity-lockup__title')]")
        details['name'] = name_element.text.strip()
    except NoSuchElementException:
        details['name'] = 'N/A'

    # Extract summary
    try:
        summary_element = browser.find_element(By.XPATH, "//blockquote[@data-test-summary-card-text]")
        details['summary'] = summary_element.text.strip()
    except NoSuchElementException:
        details['summary'] = 'N/A'

    # Extract experience
    experiences = []
    try:
        experience_elements = browser.find_elements(By.XPATH, "//section[contains(@class, 'experience-section')]//ul/li")
        for exp in experience_elements:
            experience_data = {}
            try:
                experience_data['title'] = exp.find_element(By.TAG_NAME, "h3").text.strip()
            except:
                experience_data['title'] = 'N/A'

            try:
                experience_data['company'] = exp.find_element(By.TAG_NAME, "p").text.strip()
            except:
                experience_data['company'] = 'N/A'

            try:
                experience_data['date'] = exp.find_element(By.TAG_NAME, "h4").text.strip()
            except:
                experience_data['date'] = 'N/A'

            try:
                experience_data['description'] = exp.find_element(By.CLASS_NAME, "description").text.strip()
            except:
                experience_data['description'] = 'N/A'

            experiences.append(experience_data)
    except NoSuchElementException:
        pass

    details['experiences'] = experiences

    return details

def get_output_language():
    """
    Prompt the user for the desired output language: Swedish or English.
    Returns 'swedish' or 'english' based on the user's choice.
    """
    while True:
        lang_choice = input("Do you want the output in Swedish (s) or English (e)? ").lower()
        if lang_choice == 's':
            return 'swedish'
        elif lang_choice == 'e':
            return 'english'
        else:
            print("Invalid choice. Please enter 's' for Swedish or 'e' for English.")


def generate_message_with_chatgpt(api_key, job_description, candidate_info, language):

    # Define the endpoint for the ChatGPT API
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "OpenAI-Python/0.27.0"
    }

    # Adjusting the prompt based on language choice
    if language == 'swedish':
        # This is a basic translation for demonstration. Depending on the desired content,
        # you might want to get a professional translation or further customize it.
        prompt_text = f"""
        Givet jobbbeskrivningen:
        {job_description}

        Och LinkedIn-profilen av {candidate_info['name']} med sammanfattningen:
        {candidate_info['summary']}
        
        Och erfarenheter: 
        {' '.join([f"{exp['title']} på {exp['company']} under {exp['date']} med beskrivning: {exp['description']}" for exp in candidate_info['experiences']])}

        Generera ett meddelande som följer denna mall:

        0. Hej {candidate_info['name']},

        1. Introduktion:
        "Hej, jag heter Oscar och jag jobbar på Sebratec."

        2. Företagspitch (Hook):
        "Vi specialiserar oss på att identifiera topptalang som inte bara letar efter ett jobb, utan en plats där de värderas och tas om hand. Vi värderar en snabb rekryteringsprocess utan onödiga extrasteg."

        3. Personligt Meddelande:
        "Jag pratar med dig på grund av din erfarenhet med [Infoga ett stycke, cirka 2 korta och slagkraftiga meningar som beskriver kandidatens mest relevanta expertis enligt jobbeskrivningen. Baserat på deras {candidate_info['summary']} och/eller {candidate_info['experiences']}. Se till att också inkludera deras relevanta tekniska färdigheter, såsom programmeringsspråk från deras profil som passar jobbeskrivningen. Skriv inte ut någon text som inte är skräddarsydd för deras profil. Prioritera att vara originell för att bryta igenom det brus som mjukvaruutvecklare får från rekryterare dagligen.]"

        4. Uppmaning till handling:
        "Låter det intressant?
        Då presenterar jag gärna din profil direkt för Troy, som ansvarar för rekryteringsprocessen.
        Alternativt, om du känner någon som kanske passar bättre för denna roll, tveka inte att vidarebefordra detta till dem."

        5. Avslut:
        "Du kan hitta mer information på vår webbplats: [link].
        Vad tycker du att detta låter, {candidate_info['name']}?
        Svara gärna oavsett,"


        *notering: ta bort alla citat-tecken från den färdiga texten*
        **note: behåll formatteringen enligt mallen, inklusive de olika radbrytningar.

        
    """
        
    else:
            prompt_text = f"""
        Given the job description:
        {job_description}

        And the LinkedIn profile of {candidate_info['name']} with the summary:
        {candidate_info['summary']}
        
        And experiences: 
        {' '.join([f"{exp['title']} at {exp['company']} during {exp['date']} with description: {exp['description']}" for exp in candidate_info['experiences']])}

        Generate a message that follows this template:

	0. "Hi {candidate_info['name']}"

        1. Introduction:
        "Hi, I'm Oscar and I work at Sebratec."

        2. Company Pitch (Hook):
        "We specialize in identifying top-tier talent who are not just looking for a job, but a place where they are valued and cared for. We care about swift hiring processes, without unnecessary extra steps."

        3. Personalized Message:
        "I'm speaking with you, because of your experience with [Insert one paragraph, around 2 short and impactful sentences detailing the candidate's most relevant expertise according to the job description. Base it on their {candidate_info['summary']} and/or {candidate_info['experiences']}. Make sure to also include their relevant technical skills, such as coding languages from their profile that fit the job description. Do not output any text that is not tailored to their profile. Prioritize being original to break free from the recruiter noise software developers receive on a daily basis.]"

        4. Call to Action:
        "Sounds interesting? I'd be happy to pitch your profile directly to Troy, who is in charge of the recruitment process.
        Alternatively, if you know someone who might be a better fit for this role, feel free to pass this along to them."

        5. Outro:
        "You can find more information on our website: [link].
        How do you think this sounds {candidate_info['name']}?
        Do reply regardless,"

        *note: remove all quotation marks from the final text output*
        **note: keep the formatting, with line breaks etc.


        """

    messages = [
        {"role": "system", "content": "You are a recruiter reaching out to relevant tech talent on linkedin for a potential job match. Aim to break through the noise software recruiters get from linkedin recruiters."},
        {"role": "user", "content": prompt_text}
    ]

    payload = {
        "model": "gpt-4",
        "messages": messages
    }

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        message = response.json()["choices"][0]["message"]["content"].strip()
        return message
    else:
        print("Error calling ChatGPT API:", response.text)
        return None




def open_notepad_with_message(message):
    """
    Open Notepad and paste the generated message.
    """
    with open('temp_message.txt', 'w') as file:
        file.write(message)
    
    subprocess.run(['notepad.exe', 'temp_message.txt'])



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
            print(f"Processing profile of: {candidate_info['name']}")
            
            # Generate message with the adjusted function, using the previously selected output_language
            message = generate_message_with_chatgpt('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', job_description, candidate_info, output_language)

            if message:
                open_notepad_with_message(message)

if __name__ == "__main__":
    main()


