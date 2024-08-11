import json
import requests
from bs4 import BeautifulSoup

base_url = "https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "lxml")

start_element = soup.find(attrs={"data-node-id": 6})
end_element = soup.find(attrs={"data-node-id": 41})

content_dict = {}

if start_element:
    current_title = None
    for sibling in start_element.find_all_next():
        if sibling == end_element:
            break

        if sibling.name == "h2":
            current_title = sibling.get_text(strip=True)
            content_dict[current_title] = []

        if sibling.name == "ul" and current_title:
            li_elements = sibling.find_all("li")
            list_text = [item.get_text(strip=True) for item in li_elements]
            content_dict[current_title].extend(list_text)
else:
    print("Could not find the specified elements.")

if content_dict:
    last_title = list(content_dict.keys())[-1]
    del content_dict[last_title]

for title, li_list in content_dict.items():
    print(f"Title: {title}")
    for li in li_list:
        print(f" - {li}")
    print("-" * 50)

json_filename = "seyha.json"
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(content_dict, json_file, ensure_ascii=False, indent=4)

print(f"Data has been saved to {json_filename}.")
