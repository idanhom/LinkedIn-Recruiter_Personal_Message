import requests

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
        prompt_text = f"""
        Givet jobbbeskrivningen:
        {job_description}

        Och LinkedIn-profilen av {candidate_info['name']} med sammanfattningen:
        {candidate_info['summary']}
        
        Och erfarenheter: 
        {' '.join([f"{exp['Position Title']} på {exp['Company Name']} under {exp['Dates Employed']}" for exp in candidate_info['experiences']])}



        Generera ett meddelande som följer denna mall:
                ***Title: Sebratec - Your Growth. Our Goal.

        0. Hej {candidate_info['name']},

        1. Introduktion:
        "Hej, jag heter Oscar och jag jobbar på Sebratec."

        2. Företagspitch (Hook):
        "Vi specialiserar oss på att identifiera topptalang som inte bara letar efter ett jobb, utan en plats där de värderas och tas om hand. Vi värderar en snabb rekryteringsprocess utan onödiga extrasteg."

        3. Personligt Meddelande:
        "Jag pratar med dig på grund av din erfarenhet med [Infoga ett stycke, cirka 2 korta och slagkraftiga meningar som beskriver kandidatens mest relevanta expertis enligt jobbeskrivningen. Baserat på deras {candidate_info['summary']} och/eller {candidate_info['experiences']}. Se till att också inkludera deras relevanta tekniska färdigheter, såsom programmeringsspråk från deras profil som passar jobbeskrivningen. Skriv inte ut någon text som inte är skräddarsydd för deras profil. Prioritera att vara originell för att bryta igenom det brus som mjukvaruutvecklare får från rekryterare dagligen.]"

        4. Uppmaning till handling:
        "Jag kontaktar dig då vi anställer för en position som du har väldigt relevant erfarenhet inom. Låter detta intressant presenterar jag gärna din profil direkt för Troy, som ansvarar för rekryteringsprocessen.
        Alternativt, om du känner någon som kanske passar bättre för denna roll, tveka inte att vidarebefordra detta till dem."

        5. Avslut:
        "Du kan hitta mer information på vår webbplats: [link].
        Hur vill du gå vidare, {candidate_info['name']}?
        
        Svara gärna oavsett,"


        *notera: ta bort alla citattecken och rubriker, som "1. introduktion", "2. Företagspitch (Hook):", "3. Personligt meddelande:", "4. Call to Action:", "5. Outro:" från den slutliga textutmatningen*
        **notera: behåll formateringen, med radbrytningar etc.
        ***notera: behåll "Titel: Sebratec - Din tillväxt. Vårt mål." utan ändringar.

        
    """
        
    else:
            prompt_text = f"""
        Given the job description:
        {job_description}

        And the LinkedIn profile of {candidate_info['name']} with the summary:
        {candidate_info['summary']}
        
        And experiences: 
        {' '.join([f"{exp['Position Title']} at {exp['Company Name']} during {exp['Dates Employed']}" for exp in candidate_info['experiences']])}

        Generate a message that follows this template:

        ***Title: Sebratec - Your Growth. Our Goal.

        1. Personalized Message:
        "Your profile is very interesting because of your experience with [Craft a succinct, compelling, and original message for [Candidate Name]. Highlight their unique experience in [Specific Experience or Skill from LinkedIn] and their impactful contributions at [Previous Company/Role from LinkedIn], tying these to the unique requirements of the [Job Title] role at [Your Company]. Invoke curiosity and convey a sense of exclusivity by subtly referencing the unique and influential aspects of the role and our selective outreach. Ensure the message stands out, is personalized, and makes the candidate feel particularly valued and intrigued to learn more. Prioritize their experiences that best matches the job requirement (preferrably their most recent experiences). Consider subtle integration of  Robert Cialdinis' principles of Commitment and Consistency, Social Proof, and Scarcity where applicable, to enhance engagement and response rate.]

        note 1: remove all citation marks and headers, such as "3. Personalized Message:" from the final block of text.
        note 2: create two versions using the same job description and scraped data. separate them by header "Version 1" and "Version 2"
        note 3: keep the personalized message to 1 paragraph and max 4 sentences.
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
