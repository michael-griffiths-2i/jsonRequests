# Program written by Ben Beglili and Michael Griffiths
# 21/11/2023

import json
import requests
import re
 
jsonFile = open('test.json')
data = json.load(jsonFile)
 
url = "http://localhost:3002/people"
 
headers = {
    'Content-Type': 'application/json'
}

"""
The checkStatusCode function takes in the type of request, the actual status code from the server and the desired response ie 201

""" 
 
def checkStatusCode(type, statusCode, desiredResponseCode):
    if statusCode == desiredResponseCode:
        print(f"{type} Status Code {statusCode}: Sucess")
        return True
    else:
        print(f"{type} Status Code {statusCode}: Fail")
        return False
 
 
 
 
""" This function, 'validateData', takes a dictionary 'data' as input and validates its fields.
 It checks if the 'fullName' and 'job' fields are strings, and if the 'email' and 'dob' fields match the specified formats.
 The 'email' field should match the regular expression for a valid email address.
 The 'dob' field should match the regular expression for a valid date in the format 'MM/DD/YYYY'.
 If a field does not meet its validation criteria, the function raises a ValueError with a descriptive error message.
"""
def validateData(data):
    # Define a regex for email validation
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # Define a regex for date validation (format: YYYY-MM-DD)
    date_regex = r'\b\d{2}[/]\d{2}[/]\d{4}\b'
    # print("DATA: ", data)
    # if not isinstance(data.get('id'), str):
    #     raise ValueError(f"Error in element {data}: id should be a string.")
    if not isinstance(data.get('fullName'), str):
        raise ValueError(f"Error in element {data}: fullName should be a string.")
    if not re.match(email_regex, data.get('email')):
        raise ValueError(f"Error in element {data}: email is not valid.")
    if not isinstance(data.get('job'), str):
        raise ValueError(f"Error in element {data}: job should be a string.")
    if not re.match(date_regex, data.get('dob')):
        raise ValueError(f"Error in element {data}: dob is not a valid date.")

   
""" This function, 'postData', takes a dictionary or list 'data' as input and posts it to a specified URL.
 If 'data' is a list, it iterates over each entry in the list, validates it using the 'validateData' function, and sends a POST request for each valid entry.
 If 'data' is a dictionary, it validates it using the 'validateData' function and sends a POST request.
 If 'data' is neither a list nor a dictionary, it prints an error message.
 The 'validateData' function is used to validate the data before sending the POST request, and the 'checkStatusCode' function is used to check the status code of the response. 
""" 
def postData(data):
    if type(data) == list:
        for entry in data:
            try:
                validateData(entry)
            except ValueError as e:
                print(e)
            else:
                peopleResponse = requests.post(url, json=entry, headers=headers)
                checkStatusCode("POST", peopleResponse.status_code, 201)
    elif type(data) == dict:
        try:
            validateData(data)
        except ValueError as e:
            print(e)
        else:
            peopleResponse = requests.post(url, json=data, headers=headers)
            response_data = peopleResponse.json()
            new_id = response_data.get('id')
            print("Newly created ID:", new_id)
    else:
        print("Cannot POST. Invalid data type.")
 
""" The function constructs the URL for the GET request. If an 'index' is provided, it is appended to the base URL. It uses a GET request to the constructed URL with specified headers.
 it checks the status code of the response with a function 'checkStatusCode'. If the status code is 200, indicating a successful HTTP request, the function proceeds to parse the JSON response 
 using the 'json' module and prints it in a pretty format with an indentation of 2 spaces. """
 
def getData(index=None):
    if index is not None:
        getURL = f"{url}/{index}"
    else:
        getURL = f"{url}"
 
    peopleResponse = requests.get(getURL, headers=headers)
 
    if checkStatusCode('GET', peopleResponse.status_code, 200):
        responseData = peopleResponse.json()
        print(json.dumps(responseData, indent=2))
 
""" This takes an 'index' as a parameter and sends a PATCH request to a specified URL to update the data of the resource at that index.
 The function constructs the URL for the PATCH request by appending the 'index' to the base URL. It then defines the data to be updated in the 'patch_data' dictionary.
 Before sending the PATCH request, it sends a GET request to the same URL to check if the resource exists. If the status code of the GET response is 200, indicating a successful HTTP request, the function proceeds to send the PATCH request with the 'patch_data' and specified headers.
 After sending the PATCH request, it checks the status code of the PATCH response with the function 'checkStatusCode'. If the status code is 200, it indicates that the PATCH request was successful. """

def patchDataByIndex(index):
    patchURL = f"{url}/{index}"
    patch_data = {
        "fullName": "Michael Griffiths"
    }
 
    peopleResponse = requests.get(patchURL, headers=headers)
 
    if checkStatusCode('GET', peopleResponse.status_code, 200):
        peopleResponse = requests.patch(patchURL, json=patch_data, headers=headers)
        checkStatusCode('PATCH', peopleResponse.status_code, 200)
 
""" This function deletes a resource at a specified index from a server. 
It constructs the URL for the DELETE request by appending the 'index' to the base URL. 
Before sending the DELETE request, it sends a GET request to the same URL to check if the resource exists. 
If the status code of the GET response is 200, indicating a successful HTTP request, the function proceeds to send the DELETE request. 
After sending the DELETE request, it checks the status code of the DELETE response. If the status code is 200, it indicates that the DELETE request was successful.
"""

def deleteDataByIndex(index):
    deleteURL = f"{url}/{index}"
    peopleResponse = requests.get(deleteURL, headers=headers)
    statusCode = peopleResponse.status_code
    if checkStatusCode('GET', statusCode, 200):
        peopleResponse = requests.delete(deleteURL, headers=headers)
        statusCode = peopleResponse.status_code
        checkStatusCode('DELETE', statusCode, 200)

"""
The 'deleteDuplicates' function sends a GET request to a server to retrieve a list of resources, identifies any duplicates based on the 'id' field, 
and sends DELETE requests to remove these duplicates. If no duplicates are found, it prints a message stating "No duplicates found."

"""
 
def deleteDuplicates():
    peopleResponse = requests.get(url, headers=headers)
    responseData = peopleResponse.json()
    id_array = [obj["id"] for obj in responseData]
    seen = set()
    duplicates = []
   
    for item in id_array:
        if item in seen:  
            duplicates.append(item)
        else:
            seen.add(item)
   
    if len(duplicates) > 0:
        for item in duplicates:
            deleteURL = f"{url}/{item}"
            peopleResponse = requests.delete(deleteURL, headers=headers)
    else:
        print("No duplicates found.")


## This code is the menu that drives the program allowing users to select whichever formatting they want to use of the JSON server.
 
while True:
    print("""
    Please select an option:
    1. Option 1 (POST DATA)
    2. Option 2 (GET DATA)
    3. Option 3 (PATCH DATA)
    4. Option 4 (DELETE DATA)
    5. Option 5 (REMOVE DUPLICATES)
    6. Exit
    """)
 
    choice = input("Enter your choice: ")
 
    if choice == "1":
        print("You selected Option 1.")
        postData(data)
       
    elif choice == "2":
        print("You selected Option 2.")
        index = input("Enter the index of data required. Alternatively, enter nothing to get all data back: ")
        getData(index)
       
    elif choice == "3":
        print("You selected Option 3.")
        index = input("Enter the index of data to patch: ") # we could ask what info to change and to what (if we had time)
        if index:
            patchDataByIndex(index)
        else:
            print("No index supplied, please try again.")
       
    elif choice == "4":
        print("You selected Option 4.")
        index = input("Enter the index of data to delete: ")
        deleteDataByIndex(index)
       
    elif choice == "5":
        print("You selected Option 5.")
        deleteDuplicates()
       
    elif choice == "6":
        print("Exiting the program.")
        break
   
    else:
        print("Invalid choice. Please try again.")
 