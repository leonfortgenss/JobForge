from openai import OpenAI
import os
import pandas as pd
from collections import Counter
from itertools import combinations

# Egentligen ska api nyckeln ligga i en egen env fil så ingen kan nå den men aja
api_key = 'sk-proj-yCkaJ8kfSuHR6BwuhBy5T3BlbkFJVDwRL8jVkCX8dPImE9BR'

# Api setup
client = OpenAI(api_key=api_key)
MODEL = "gpt-3.5-turbo"

def write_clear(listing_information):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user", "content": f"""Detta är text från en sida som innehåller en arbetsannons {listing_information}, 
                skulle du kunne behålla endast det viktigaste och skriv ut ren infomration från denna. Om det går beskriv även arbetet lite mer. Du behöver inte skriva självklart eller någon anna typ av information utan endast den omskriva informationen, det kan även komma in länkar som hem eller sociala medier men fokusera endast på arbets beskrivningen och ta bort allt annat"""
             }
        ]
    )

    return response.choices[0].message.content

# Just nu tar jag grund in skills lägg till mottagare sen
def send_prompt_to_api(name, age, traits, listing_information):
    response = client.chat.completions.create(
        model=MODEL,
        # För skriven prompt så man inte behöver skriva något annat än sina skills samt att man tränar upp systemet lite
        messages=[
            {"role": "system", "content": "Du är en konsult och rådgivare på hur man skriver personliga brev och CV för jobbansökningar"},
            {"role": "user", "content": f"Kan du skriva mig ett personlig brev med hjälp av kommande information om mig? Namn: {name}, Ålder: {age}, Egenskaper: {traits}. Kan du även anpassa den för denna informationen på jobb anonsen {listing_information}"}
        ],
    )
    # Ta ut meddelandet ur datan man får tillbaka från OpenAIs api
    last_message = response.choices[0].message.content
    print(last_message)
    return last_message


def get_related_skills(programming_language):
    input_skills = [language.strip().lower() for language in programming_language.split(',')]


    df = pd.read_csv('skills.csv')
    ignore_skills = {'svenska', 'engelska'}
    all_skills = (df['skills'].dropna().str.lower().str.split(', ').apply(lambda skills: [skill.strip() for skill in skills if skill.strip()not in ignore_skills]))
    related_skill_counts = Counter()

    for skills_list in all_skills:
        pairs = combinations(skills_list, 2)
        for skill1, skill2 in pairs:
            if skill1 in input_skills:
                related_skill_counts[skill2] += 1
            elif skill2 in input_skills:
                related_skill_counts[skill1] += 1
    
    top_related_skills = [skill for skill, count in related_skill_counts.most_common(5)]
    return top_related_skills