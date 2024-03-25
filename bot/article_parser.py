import requests
import concurrent.futures
import json


if __name__ == "__main__":


    num_requests = 1

    url = "" 


    # Input
    
    def send_request(num_requests):

        #    Payload for text embeddings # zPao Embed
     
        payload = {
            "url": "https://www.goodto.com/recipes/gordon-ramsay-roast-potatoes",
        }
        
        response = requests.post(url, data=json.dumps(payload))
        
      
        if response.status_code == 200:
            # Parse the response content as JSON
            response_json = response.json()
            
            # Access the 'success' key if present
            if 'success' in response_json:
                print("Response Status Code:", response.status_code)
                print("Success:", response_json['success'])

            # If 'success' key is not present, print the entire response JSON
            else:
                print("Response Status Code:", response.status_code)
                # print("Response Content:", response_json)
                print("Title: ",response_json['data'][0]['article_title'])
                print("Content: ",response_json['data'][0]['article_content'])

        else:
            print(f"Error: {response.status_code}")

    max_workers = 300

    # Use the number of CPU cores as the max_workers value
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(send_request, range(num_requests))


