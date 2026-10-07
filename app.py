import os
import json

DATA_DIR="data"
DATA=os.path.join(DATA_DIR, "karvands.json")

class Skill:
    def __init__(self,name,level,score):
        self.name=name
        self.level=level
        self.score=score
    def to_dict(self):
        return {"name": self.name, "level": self.level , "score": self.score }
class Education:
    def __init__(self,degree,field):
        self.degree=degree
        self.field=field
    def to_dict(self):
        return {"degree": self.degree, "field": self.field}
class Karvand:
    def __init__(self, id, full_name, email, city, education, skills):
        self.id =id
        self.full_name = full_name
        self.email=email
        self.city=city
        self.education=education
        self.skills=skills

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "city": self.city,
            "education": self.education.to_dict(),
            "skills": [s.to_dict() for s in self.skills],
        }

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

def generate_id(karvands):
    if not karvands:
        return 1
    return max(k["id"] for k in karvands)+1
def ask_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a number.")
def print_karvand(k):
    print(f"ID:{k['id']}")
    print(f"Name:{k['full_name']}")
    print(f"Email:{k['email']}")
    print(f"City:{k['city']}")
    print(f"Education:{k['education']['degree']} - {k['education']['field']}")
    print("Skills:")
    for s in k["skills"]:
        print(f"{s['name']}({s['level']}):{s['score']}")
def add_karvand():
    full_name=input("enter the fullname:")
    email=input("enter email:")
    city=input("enter city:")
    degree=input("enter education degree:")
    field=input("eneter education field:")
    education=Education(degree, field)
    skills=[]
    while True:
        name=input("enter skill name:")
        level=input("enter skill level:")
        while True:
            score=ask_int("enter skill score(0-100):")
            if 0 <= score <= 100:
                break
            print("enter a number between 0-100")
        skills.append(Skill(name, level, score))
        add_more=input("Add another skill? y/n : ").lower()
        while add_more not in ("y", "n"):
            print("Invalid input.")
            add_more = input("Add another skill? y/n: ").lower()
        if add_more=="n":
            break
    data=read_from_json()
    new_id=generate_id(data["karvands"])
    karvand = Karvand(new_id, full_name, email, city, education, skills)
    data["karvands"].append(karvand.to_dict())
    write_in_json(data)
    print("Karvand added.")

def show_karvands():
    data=read_from_json()
    if not data["karvands"]:
        print("No karvands registered.")
        return
    for k in data["karvands"]:
        print_karvand(k)

def main():
    read_from_json()
    while True:
        print("1) Add karvand")
        print("2) Show all karvands")
        print("3) Exit")
        print("4) Search by id")
        print("5) Search by skill")
        choice=input("Choose: ").strip()
        if choice=="1":
            add_karvand()
        elif choice=="2":
            show_karvands()
        elif choice=="3":
            print("Goodbye!")
            break
        elif choice == "4":
            search_by_id()
        elif choice == "5":
            search_by_skill()
        else:
            print("Invalid input.")

def find_by_id(karvands, karvand_id):
    for k in karvands:
        if k["id"]== karvand_id:
            return k
        return None
def search_by_id():
    karvand_id=ask_int("enter id:")
    data=read_from_json()
    k=find_by_id(data["karvands"], karvand_id)
    if k :
        print_karvand(k)
    else:
        print("there is no karvand with this id")
def search_by_skill():
    skill_name=input("enter skill name:").lower().strip()
    data=read_from_json()
    found=False
    for k in data["karvands"]:
        for s in k["skills"]:
            if s["name"].lower().strip()==skill_name:
                print_karvand(k)
                found=True
                break
    if not found:
        print("no karvand with this skill is found")
                

    
if __name__ == "__main__":
    main()



