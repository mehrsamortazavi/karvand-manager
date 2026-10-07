import os
import json

DATA_DIR="data"
DATA=os.path.join(DATA_DIR, "karvands.json")


def bootcamp_data():
    return {"bootcamp": {"title": "Karvand AI", "year": 2026}, "karvands":[]}


def write_in_json(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def read_from_json():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA):
        data=bootcamp_data()
        write_in_json(data)
        return data
    try:
        with open(DATA, "r", encoding="utf-8") as file:
            data=json.load(file)
        if not isinstance(data, dict) or not isinstance(data.get("karvands"), list):
            raise ValueError
        return data
    except (json.JSONDecodeError, ValueError):
        print("File is empty or broken")
        data=bootcamp_data()
        write_in_json(data)
        return data
def main():
    read_from_json()
    print("Storage is ready.")
if __name__ == "__main__":
    main()