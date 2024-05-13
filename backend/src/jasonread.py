import json
import csv
import zipfile

# Define the zip file path and the name of the jsonl file inside it
zip_file_path = '2023_beta1_jsonl.zip'
jsonl_file_name = '2023.enriched.jsonl'
# input_file_path = '2023.sample.jsonl'
output_file_path = 'skills.csv'
count = 0
# Open the output CSV file for writing
with open(output_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    
    # Write the header row to the CSV file
    headers = ['headline', 'skills']
    csv_writer.writerow(headers)
    
    # Open the zip file and extract the JSON Lines file
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        # Check to see if the jsonl file is indeed in the zip file
        if jsonl_file_name in z.namelist():
        # Open the JSON Lines file from within the zip file
            with z.open(jsonl_file_name, 'r') as jsonl_file:
                for line in jsonl_file:
                    # Decode bytes to string and load JSON
                    data = json.loads(line.decode('utf-8'))
                    
                    # Extract data from the 'enriched' part if it exists
                    enriched = data.get('keywords', {}).get('enriched', {})
                    extracted = data.get('keywords', {}).get('extracted', {})
                    
                    # Prepare data for CSV output
                    headline = data.get('headline', 'No Headline Available')
                    # occupations_ext = ', '.join(extracted.get('occupation', []))
                    # occupations_enr = ', '.join(enriched.get('occupation', []))
                    skills = ', '.join(enriched.get('skill', []))
                    # traits = ', '.join(enriched.get('trait', []))
                    # locations = ', '.join(enriched.get('location', []))
                    # compounds = ', '.join(enriched.get('compound', []))
                    count += 1
                    print(count)
                    # Write the extracted data to the CSV
                    csv_writer.writerow([headline, skills])

print("Data extraction and CSV writing completed successfully.")