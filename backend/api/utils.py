from openai import OpenAI
import os

# Egentligen ska api nyckeln ligga i en egen env fil så ingen kan nå den men aja
api_key = 'sk-proj-yCkaJ8kfSuHR6BwuhBy5T3BlbkFJVDwRL8jVkCX8dPImE9BR'

# Api setup
client = OpenAI(api_key=api_key)
MODEL = "gpt-3.5-turbo"

# Just nu tar jag bara in skills
def send_prompt_to_api(skills):
    response = client.chat.completions.create(
        model=MODEL,
        # För skriven prompt så man inte behöver skriva något annat än sina skills samt att man tränar upp systemet lite
        messages=[
            {"role": "system", "content": "You are a professional consultant in helping people getting jobs"},
            {"role": "user", "content": f"Can you write me a personal letter based on my skills? {skills}"}
        ],
    )
    # Ta ut meddelandet ur datan man får tillbaka från OpenAIs api
    last_message = response.choices[0].message.content
    return last_message