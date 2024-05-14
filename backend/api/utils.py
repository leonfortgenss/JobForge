from openai import OpenAI
import os

# Egentligen ska api nyckeln ligga i en egen env fil så ingen kan nå den men aja
api_key = 'sk-proj-yCkaJ8kfSuHR6BwuhBy5T3BlbkFJVDwRL8jVkCX8dPImE9BR'

# Api setup
client = OpenAI(api_key=api_key)
MODEL = "gpt-3.5-turbo"

# Just nu tar jag grund in skills lägg till mottagare sen
def send_prompt_to_api(name, age, traits):
    response = client.chat.completions.create(
        model=MODEL,
        # För skriven prompt så man inte behöver skriva något annat än sina skills samt att man tränar upp systemet lite
        messages=[
            {"role": "system", "content": "Du är en konsult och rådgivare på hur man skriver personliga brev och CV för jobbansökningar"},
            {"role": "user", "content": f"Kan du skriva mig ett personlig brev med hjälp av kommande information om mig? Namn: {name}, Ålder: {age}, Egenskaper: {traits}"}
        ],
    )
    # Ta ut meddelandet ur datan man får tillbaka från OpenAIs api
    last_message = response.choices[0].message.content
    print(last_message)
    return last_message