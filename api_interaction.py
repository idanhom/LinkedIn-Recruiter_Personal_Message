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

        1. Personligt meddelande:
        "Din profil är mycket intressant på grund av din erfarenhet av [Skapa ett kortfattat, övertygande och originellt meddelande för [Kandidatens namn]. Lyft fram deras unika erfarenhet av [specifik erfarenhet eller färdighet från LinkedIn] och deras betydelsefulla bidrag på [tidigare företag/roll från LinkedIn] och koppla dessa till de unika kraven för rollen [jobbtitel] på [ditt företag]. Väck nyfikenhet och förmedla en känsla av exklusivitet genom att subtilt hänvisa till de unika och inflytelserika aspekterna av rollen och vår selektiva uppsökande verksamhet. Se till att budskapet sticker ut, är personligt och får kandidaten att känna sig särskilt uppskattad och nyfiken på att lära sig mer. Prioritera deras erfarenheter som bäst matchar jobbkraven (helst deras senaste erfarenheter). Överväg en subtil integrering av Robert Cialdinis principer om engagemang och konsekvens, sociala bevis och knapphet där det är tillämpligt, för att öka engagemanget och svarsfrekvensen].
        
        Vänligen generera ett personligt meddelande enligt dessa riktlinjer:
        - Meddelandet ska vara övertygande och originellt och lyfta fram {candidate_info['name']}:s unika erfarenheter och bidrag, särskilt de som stämmer överens med jobbkraven.
        - Meddelandet ska väcka nyfikenhet och förmedla en känsla av exklusivitet, med hänvisning till de unika aspekterna av rollen och vår selektiva uppsökande verksamhet.
        - Meddelandet ska skrivas i första person, med ett språk på åttonde klassnivå och med vanliga ord och fraser.
        - Integrera subtilt Robert Cialdinis principer om engagemang och konsekvens, sociala bevis och knapphet för att öka engagemanget och svarsfrekvensen.
        - Håll budskapet till ett stycke och max 4 meningar.

        Skapa två versioner av meddelandet och märk dem med "Version 1" och "Version 2". 
        Börja alltid texten med: Din profil är mycket intressant på grund av din erfarenhet av...
        Använda inga citattecken och apostrofer i den färdiga texten.
        
        Det är viktigt att all text du formulerar är på svenska.


        """
        
    else:
            prompt_text = f"""
        Given the job description:
        {job_description}

        And the LinkedIn profile of {candidate_info['name']} with the summary:
        {candidate_info['summary']}
        
        And experiences: 
        {' '.join([f"{exp['Position Title']} at {exp['Company Name']} during {exp['Dates Employed']}" for exp in candidate_info['experiences']])}

        Please generate a personalized message following these guidelines:
        - The message should be compelling and original, highlighting the unique experiences and contributions of {candidate_info['name']}, particularly those that align with the job requirements.
        - The message should invoke curiosity and convey a sense of exclusivity, referencing the unique aspects of the role and our selective outreach.
        - The message should be written in first person, using 8th-grade level language and regular words and phrases.
        - Integrate subtly Robert Cialdini's principles of Commitment and Consistency, Social Proof, and Scarcity to enhance engagement and response rate.
        - Keep the message to one paragraph and a maximum of 4 sentences.

        Create two versions of the message and label them as 'Version 1' and 'Version 2'. 
        Remove all citation marks and apostrophes.
        Start the message with: "Your profile is very interesting because of your experience with"

        """


    messages = [
        {"role": "system", "content": "You are a recruiter composing a message to approach potential candidates on LinkedIn for a job match. Use relevant details from the candidates profile that match the job requirement and ensure the message is personalized, making the candidate feel valued and intrigued to learn more."},
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
