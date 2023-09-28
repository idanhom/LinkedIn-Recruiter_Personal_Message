# LinkedIn Recruiter Tool: README

## Overview
This tool is designed to help recruiters automate the process of extracting data from LinkedIn profiles using Selenium. The extracted data is then used to create a personalized message for potential candidates, which can be tailored to match the job description provided by the recruiter. The goal is to create unique and personalized messages to break through the noise that software developers often receive from recruiters on LinkedIn.

## Features
- **Browser Initialization**: Supports both Firefox and Chrome browsers with user agents.
- **URL Monitoring**: Checks for URL changes to detect when a LinkedIn profile is accessed.
- **LinkedIn Data Extraction**: Grabs essential details like name, summary, experience, etc.
- **Personalized Message Creation**: Uses ChatGPT API to generate a personalized message based on the extracted LinkedIn data and provided job description.
- **Notepad Output**: Displays the generated message using Notepad for easy copying and sending.

## Prerequisites
- **Python**: Make sure Python is installed.
- **Selenium**: This tool uses Selenium for web scraping. Ensure you have the appropriate drivers for Firefox and Chrome.
- **Requests**: For API calls.
- **OpenAI API Key**: Required for generating messages with ChatGPT.

## Setting up Selenium Drivers

Before you can run the tool, you'll need the appropriate drivers for the browsers you intend to use.

### Chrome:
1. Determine which version of Chrome you're using. You can do this by navigating to the three vertical dots at the top-right corner of your Chrome browser > Help > About Google Chrome.
2. Once you've identified your Chrome version, download the corresponding ChromeDriver from the [official site](https://sites.google.com/a/chromium.org/chromedriver/downloads).
3. Extract the downloaded file and place the `chromedriver` executable in a location of your choice. Make sure to add this location to your system's PATH or reference it directly in your script.

### Firefox (GeckoDriver):
1. Determine which version of Firefox you're using. Open Firefox, click on the three horizontal lines at the top-right corner > Help > About Firefox.
2. Download the corresponding GeckoDriver for your platform and Firefox version from the [official GitHub releases](https://github.com/mozilla/geckodriver/releases).
3. Extract the downloaded file and place the `geckodriver` executable in a location of your choice. Again, ensure this location is added to your system's PATH or reference it directly in your script.

**Note**: Always ensure that the driver's version is compatible with your browser's version to avoid inconsistencies or errors.

## How to use
1. **Choose Browser**: Set the `browser_choice` in the code to either "firefox" or "chrome".
2. **Run the Script**: Execute the main function.
3. **Enter Job Description**: When prompted, input the job description for the position you're recruiting for.
4. **Provide LinkedIn URL**: Input the LinkedIn profile URL of the first candidate you're interested in.
5. **Monitor URL Changes**: The tool will keep monitoring for URL changes. When it detects a different LinkedIn profile, it will prompt you to decide whether to activate the script for that profile.
6. **Generated Message**: If you choose to activate, the tool will extract data from the LinkedIn profile, generate a personalized message, and display it in Notepad.

## TODO
-ad url to script (asking at start) so it's automatically inserted in the end text
- Look more closely at https://github.com/bonigarcia/webdrivermanager/ for automated driver download
-fix depreciation warning (ff). does it work afterwards?
-make it not crash if i cut the text from the box, then close it, then want to paste it to a different window.
  meaning: i want to be able to save the text to clipboard regardless of if the window is open or not. 
-i also want to be able to save the location of the window (that pops from Python) so it opens at the same position each time (as the last time it was closed)
-make change so can swap job ad in the middle of the program without having to restart it

-to be checked further.... this is the situation: i activate the script on a profile. it provides me with a text. currentl, i must close the window AND THEN press to next profile for the script to recognize that the url has changed.
    instead, what i want is that the script goes into "monitor mode" as soon as the python window has been presented. this might also mean that either (1) it opens up the windows in a new process or (2) it replaces the previous window 




## Message Template Examples
The tool is designed to produce messages that stand out. Here's an example of the format:

### English
To accomplish this, we're interested in speaking with you, because of your experience with [specific details about the candidate's expertise Make sure to also include their relevant technical skills. Prioritize being original to break free from the recruiter noise software developers receive on a daily basis.]

### Swedish (translated for demonstration purposes)
För att uppnå detta är vi intresserade av att tala med dig på grund av din erfarenhet med [specific details about the candidate's expertise. Se till att också inkludera deras relevanta tekniska färdigheter. Prioritera att vara original för att bryta fri från det rekryteringsbrus mjukvaruutvecklare får dagligen.]
