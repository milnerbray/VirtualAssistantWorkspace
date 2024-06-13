# Found at https://medium.com/@natashanewbold/automate-searching-google-using-python-fcbbb4342dfd
# try:
#     from googlesearch import search
# except ImportError:
#     print("No module named 'google' found")
 
# # to search
# query = "Star Wars"
 
# for j in search(query, tld="co.in", num=10, stop=10, pause=2):
#     print(j)

# from googlesearch import search

# # Define the search query
# query = "The Economist"

# # Perform the Google search and retrieve the top result
# search_results = search(query, num=1)

# # Print the top search result
# for result in search_results:
#     print(result)

import requests

# Define the search query
query = "The Economist"

# Send a GET request to DuckDuckGo search API
response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")

# Check if the request was successful
if response.status_code == 200:
    # Extract the top search result from the response JSON
    top_result = response.json()["AbstractURL"]

    # Print the top search result
    print(top_result)
else:
    print("Error occurred while performing the search.")