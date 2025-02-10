import requests
import json

# Base URL for the Flask app (assuming it is running locally)
base_url = 'http://127.0.0.1:5000'

# Test 1: Create a User (POST request)
def create_user(name):
    url = f"{base_url}/create_user"
    payload = {
        "name": name,
        "password": "password123"
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print the response
    if response.status_code == 201:
        print("User created successfully:", response.json())
    else:
        print(f"Failed to create user: {response.status_code} - {response.json()}")
    return response

# Test 2: Get a User (GET request)
def get_user(user_name):
    url = f"{base_url}/user/{user_name}"

    response = requests.get(url)

    # Print the response
    if response.status_code == 200:
        print(f"User {user_name} found:", response.json())
    else:
        print(f"Failed to retrieve user {user_name}: {response.status_code} - {response.json()}")
    return response

# Run the tests
if __name__ == "__main__":
    # Test creating a user
    # create_user()

    # Test getting the created user
    # get_user("Alice")
    Test=True
    while Test==True:
        print("Welcome to the infinite loop \n Please choose a option \n 1. Create a user \n 2. Get a user \n 3. Exit")
        choice = int(input())
        match choice:
            case 1:
                print("Creating a user \n Please enter the name of the user")
                name = str(input())
                response = create_user(name)
                if response.status_code == 201:
                    data = response.json()
                    print(data["message"])
                elif response.status_code == 400:
                    data = response.json()
                    print(f"Error: {data['error']}")
                else:
                    print("Unknown error occurred")
            case 2:
                print("Getting a user \n Please enter the name of the user")
                name = str(input())
                response = get_user(name)
                if response.status_code == 200:
                    data = response.json()
                    print(data)
                elif response.status_code == 404:
                    data = response.json()
                    print(f"Error: {data['error']}")
                else:
                    print("Unknown error occurred")
            case 3:
                Test = False
                break

        
