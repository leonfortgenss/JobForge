import json
import csv

# Define the input and output file paths
input_file_path = '2023.sample.jsonl'
output_file_path = 'skills.csv'

# Open the output CSV file for writing
with open(output_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    
    # Write the header row to the CSV file
    headers = ['headline', 'occupations_ext', 'occupations_enr', 'skills', 'traits', 'locations', 'compounds']
    csv_writer.writerow(headers)
    
    # Open and read the JSON Lines file
    with open(input_file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            # Load the JSON object from the line
            data = json.loads(line)
            
            # Extract data from the 'enriched' part if it exists
            enriched = data.get('keywords', {}).get('enriched', {})
            extracted = data.get('keywords', {}).get('extracted', {})
            
            # Prepare data for CSV output
            headline = data.get('headline', 'No Headline Available')
            occupations_ext = ', '.join(extracted.get('occupation', []))
            occupations_enr = ', '.join(enriched.get('occupation', []))
            skills = ', '.join(enriched.get('skill', []))
            traits = ', '.join(enriched.get('trait', []))
            locations = ', '.join(enriched.get('location', []))
            compounds = ', '.join(enriched.get('compound', []))
            
            # Write the extracted data to the CSV
            csv_writer.writerow([headline, occupations_ext, occupations_enr, skills, traits, locations, compounds])

print("Data extraction and CSV writing completed successfully.")