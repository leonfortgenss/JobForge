import pandas as pd
from collections import Counter
from itertools import combinations

# Load the CSV file
df = pd.read_csv('skills.csv')

# Display the first few rows of the DataFrame to confirm proper loading
print(df.head())


# Normalize and split the skills, then flatten the list
skills_series = df['skills'].dropna().str.lower().str.split(', ')

# Flatten the list of lists into a single list of skills
all_skills = [skill.strip() for sublist in skills_series for skill in sublist if skill]

# Count occurrences of each skill
skill_counts = Counter(all_skills)

# Normalize, clean data, and handle synonyms
def clean_skill(skill):
    skill_mapping = {
        'c++': 'cpp',  # Normalize different spellings or variations
        'big data': 'bigdata'  # Handle compound words
    }
    skill = skill.strip().lower()
    return skill_mapping.get(skill, skill)  # Return the mapped skill if it exists, else the original

# Apply the cleaning function to each skill
all_skills = [clean_skill(skill) for sublist in skills_series for skill in sublist if skill]
skill_counts = Counter(all_skills)




# Define a set of skills to ignore
ignore_skills = {'svenska', 'engelska'}

# Assuming skills are separated by commas and are in a single column called 'skills'
skill_pairs = Counter()

for skills in df['skills'].dropna():
    # Split skills and strip whitespace
    skills_list = [skill.strip().lower() for skill in skills.split(',') if skill.strip().lower() not in ignore_skills]
    # Generate all combinations of skill pairs within each row and count them
    for combo in combinations(skills_list, 2):
        if combo[0] != combo[1]:  # Ensure we don't pair the same skill with itself
            skill_pairs[combo] += 1

# Print the most common skill pairs
print(skill_pairs.most_common(10))

# Display the results
print(skill_counts.most_common(10))

# input_skill_1 = input("Enter the first skill: ").strip().lower()
# input_skill_2 = input("Enter the second skill: ").strip().lower()
# input_skill_3 = input("Enter the third skill: ").strip().lower()

# input_skills = {input_skill_1, input_skill_2, input_skill_3}
input_skills = {'python', 'css', 'javascript'}


# Normalize and split the skills, then flatten the list
all_skills = (df['skills'].dropna().str.lower().str.split(', ')
              .apply(lambda skills: [skill.strip() for skill in skills if skill.strip()not in ignore_skills]))


# Define a Counter to hold our results
related_skill_counts = Counter()

# Analyze skill pairs
for skills_list in all_skills:
    # Find all possible pairs
    pairs = combinations(skills_list, 2)
    # Filter pairs where at least one skill matches the input skills
    for skill1, skill2 in pairs:
        if skill1 in input_skills:
            related_skill_counts[skill2] += 1
        elif skill2 in input_skills:
            related_skill_counts[skill1] += 1

# Print the skills most frequently paired with the specified input skills
for skill, count in related_skill_counts.most_common(10):
    print(f"{skill}: {count}")

