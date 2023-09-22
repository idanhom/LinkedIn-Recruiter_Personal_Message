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

	    0. "Hi {candidate_info['name']}"
    
        1. Introduction:
        "Hi, I'm Oscar and I work at Sebratec."

        2. Company Pitch (Hook):
        "We specialize in identifying top-tier talent who are not just looking for a job, but a place where they are valued and cared for. We care about swift hiring processes, without unnecessary extra steps."

        3. Personalized Message:
        "Your profile is very interesting because of your experience with [Insert one paragraph, around 2 short and impactful sentences detailing the candidate's most relevant expertise according to the job description. Base it on their {candidate_info['summary']} and/or {candidate_info['experiences']}. Make sure to also include their relevant technical skills, such as coding languages from their profile that fit the job description. Do not output any text that is not tailored to their profile. Prioritize being original to break free from the recruiter noise software developers receive on a daily basis.]"

        4. Call to Action:
        "I am contacting you because we are hiring for a position that you have highly relevant expertise for. I offer to pitch your profile directly to Troy, who is in charge of the recruitment process.
        Alternatively, if you know someone who might be a better fit for this role, feel free to pass this along to them."

        5. Outro:
        "You can find more information on our website: [link]
        
        How do you want to proceed, {candidate_info['name']}?
        
        Do reply regardless,"

        *note 1: remove all citation marks and headers, such as "1. Introduction", "2. Company Pitch (Hook):", "3. Personalized Message:", "4. Call to Action:", "5. Outro:" from the final block of text.
        note 2: keep the formatting, with line breaks etc.
        note 3: keep the "Title: Sebratec - Your Growth. Our Goal." without change. 
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
