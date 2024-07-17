import requests

def send_request(prompt):
    url = 'http://localhost:5001/process_prompt'  # Update the endpoint to match your Flask route
    data = {
        'prompt': prompt
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Response:")
            print(response.json())
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")

if __name__ == "__main__":
    # Replace this with your actual prompt
    prompt = 'Info Related AI as list of points'
    send_request(prompt)
