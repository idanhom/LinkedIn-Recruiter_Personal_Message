# web_scraping.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

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
        profile_path = r"C:\Users\pson9\AppData\Roaming\Mozilla\Firefox\Profiles\8ewzfvju.SeleniumProfile"
        #private profile:
        # C:\Users\pson9\AppData\Roaming\Mozilla\Firefox\Profiles\8ewzfvju.SeleniumProfile
        options = FirefoxOptions()
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

    # Expand "Show all 42 skills"
    try:
        skills_button = browser.find_element(By.XPATH, "//button[contains(@aria-label, 'Show all') and contains(@class, 'expandable-list__button')]")
        skills_button.click()
        time.sleep(0.5)  # Wait for the content to expand
    except NoSuchElementException:
        print("Couldn't find the 'Show all skills' button.")

    # Click "Show more" for experiences
    try:
        show_more_button = browser.find_element(By.XPATH, "//button[contains(@class, 'expandable-list__button') and @aria-label='See more positions']")
        show_more_button.click()
        time.sleep(2)  # wait for the content to expand
    except NoSuchElementException:
        print("Couldn't find the 'Show more' button.")

    # Scroll down to the experience section to ensure all jobs are loaded. Adjust the range as needed.
    for _ in range(3):
        browser.execute_script("window.scrollBy(0, 800);")
        time.sleep(2)  # wait for the page to load


def extract_linkedin_details(browser):
    details = {}

    # Extract name
    try:
        name_element = browser.find_element(By.XPATH, "//div[contains(@class, 'artdeco-entity-lockup__title')]")
        details['name'] = name_element.text.strip()
    except NoSuchElementException:
        details['name'] = 'N/A'

    # Extract summary
    try:
        summary_element = browser.find_element(By.XPATH, "//blockquote[@data-test-summary-card-text]/div[@data-test-decorated-line-clamp]/div/span[@class='lt-line-clamp__raw-line']")
        details['summary'] = summary_element.text.strip()
    except NoSuchElementException:
        details['summary'] = 'N/A'

    # Extracting page source for BeautifulSoup
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Extract work history
    experiences = []

    # Find all job positions
    positions = soup.find_all('div', class_='background-entity')
    for position in positions:
        job = {}
        
        # Extract job title
        title_tag = position.find('h3', class_='background-entity__summary-definition--title')
        job['Position Title'] = title_tag.a.text if title_tag and title_tag.a else "N/A"
        
        # Extract company name
        company_tag = position.find('dd', class_='background-entity__summary-definition--subtitle')
        job['Company Name'] = company_tag.a.text if company_tag and company_tag.a else "N/A"
        
        # Extract job description
        description_tag = position.find('dd', class_='background-entity__summary-definition--description')
        job['Summary'] = description_tag.text if description_tag else "N/A"
        
        # Extract employment duration
        date_range_tag = position.find('span', class_='background-entity__date-range')
        job['Dates Employed'] = date_range_tag.text if date_range_tag else "N/A"
        
        experiences.append(job)
        
    details['experiences'] = experiences

    # After extracting the name and summary
    print(f"Name: {details['name'].strip()}")
    print(f"Summary: {details['summary'].strip() if details['summary'] != 'N/A' else 'N/A'}")
    
    # After extracting experiences
    if not details['experiences']:
        print("No experiences found!")
    else:
        for exp in details['experiences']:
            title = exp.get('Position Title', 'N/A').strip()
            company = exp.get('Company Name', 'N/A').strip()
            summary = exp.get('Summary', 'N/A').strip()
            dates_employed = exp.get('Dates Employed', 'N/A').strip()
            
            if title == 'N/A' and company == 'N/A' and summary == 'N/A' and dates_employed == 'N/A':
                continue  # Skip printing if all fields are 'N/A'
            
            print("\nExperience:")
            print(f"  Position Title: {title if title else 'N/A'}")
            print(f"  Company Name: {company if company else 'N/A'}")
            print(f"  Dates Employed: {dates_employed if dates_employed else 'N/A'}")
            print(f"  Summary: {summary if summary else 'N/A'}")
    
    return details


