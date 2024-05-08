import requests
import json
import pandas as pd
from requests.exceptions import HTTPError

"""
Install python packages:
pip install -r requirements.txt

"""

url = 'https://jobsearch.api.jobtechdev.se'
url_for_search = f"{url}/search"


def _get_ads(params):
    headers = {'accept': 'application/json'}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode('utf-8'))


def search_return_number_of_hits(query):
    # limit: 0 means no ads, just a value of how many ads were found.
    search_params = {'q': query, 'limit': 0}
    json_response = _get_ads(search_params)
    number_of_hits = json_response['total']['value']
    print(f"\nNumber of hits = {number_of_hits}")
    return number_of_hits


def search_loop_through_hits(query, num):
    # limit = 100 is the max number of hits that can be returned.
    # If there are more (which you find with ['total']['value'] in the json response)
    # you have to use offset and multiple requests to get all ads.

    df = pd.DataFrame(columns=['name', 'employer', 'url', 'experience', 'description', 'must_have', 'nice_to_have'])

    offset = 0
    limit = 100
    while offset < num-limit:
        try:
            search_params = {'q': query, 'limit': limit, 'offset':offset}
            json_response = _get_ads(search_params)
            hits = json_response['hits']
            if not hits:  # Check if no hits are returned
                print(f"No more data returned at offset {offset}.")
                break
            for hit in hits:
                job_dict = {
                        'name': hit['headline'],
                        'employer': hit['employer']['name'],
                        'url': hit['webpage_url'],
                        'experience': hit['experience_required'],
                        'description':hit['description']['text_formatted'],
                        'must_have':hit['must_have'],
                        'nice_to_have':hit['nice_to_have']
                    }
                new_df = pd.DataFrame([job_dict])  # Create a new DataFrame from the dictionary
                df = pd.concat([df, new_df], ignore_index=True)  # Concatenate with the existing DataFrame
            print(df)
                

            offset += limit
        except HTTPError as e:
            print(f"HTTP error at offset {offset}: {e.response.status_code} - {e.response.text}")
            break
        except Exception as e:
            print(f"Unexpected error at offset {offset}: {str(e)}")
            break
        except:
            offset += limit
        print(offset, num)
    return df


if __name__ == '__main__':
    query = 'it'
    num = search_return_number_of_hits(query)
    jobs = search_loop_through_hits(query, num)
    jobs.to_csv('jobs.csv', index=False)
    
    
