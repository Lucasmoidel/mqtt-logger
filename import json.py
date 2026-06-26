import json

# --- Parse JSON String to Python Dict (Deserialization) ---
f = open("NodeList.json", "r")
data = json.load(f)

print(data["nodes"][0]["age"])  # Output: Alice
data["nodes"][0]["age"]+=1
print(data["nodes"][0]["age"])    # Output: <class 'dict'>
data["nodes"].append({"name": "a", "age": 7, "skills": ["Python", "SQL"]})

# --- Convert Python Dict to JSON String (Serialization) ---
f = open("NodeList.json", "w")
json.dump(data, f,indent=4)  # indent adds readable formatting

