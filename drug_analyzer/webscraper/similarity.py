import json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def remove_similar_items(items, similarity_threshold=0.5):
    items = [item.lower() for item in items]
    result = []

    for item in items:
        add_item = True
        for other in result:
            similarity = similar(item, other)
            if similarity > similarity_threshold:
                if len(item) > len(other):
                    result.remove(other)
                    result.append(item)
                add_item = False
                break
        if add_item:
            result.append(item)

    return result

def remover(json_file_path):
    # Read the JSON data from the file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Remove similar items from the "uses list" for each drug
    for drug in data:
        if "uses list" in data[drug]:
            data[drug]["uses list"] = remove_similar_items(data[drug]["uses list"])
        

    # Write the updated JSON data back to the file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)