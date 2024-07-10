import json
from datetime import datetime

class Person:
    # Klasse zur Verwaltung von Personendaten und -operationen.
    @staticmethod
    def load_person_data(link):
        # Eine Funktion, die weiß, wo sich die Personendatenbank befindet und ein Dictionary mit den Personen zurückgibt
        file = open(link)
        person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        # Eine Funktion, die das Personen-Dictionary nimmt und eine Liste aller Personennamen zurückgibt
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        # Eine Funktion der Nachname, Vorname als ein String übergeben wird und die die Person als Dictionary zurück gibt

        person_data = Person.load_person_data()
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                print()

                return eintrag
        else:
            return {}
    
    @staticmethod   
    def load_by_id(search_id, person_data_Dict):
        # person_data = Person.load_person_data()
        person_data = person_data_Dict
        
        if search_id == "None":
            return "keien Eingabe"
    # Lädt Personendaten nach ID.

        for person in person_data:
            if person["id"] == search_id:
                return person
        return "falsche id"
    
    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
    # Initialisiert ein Person-Objekt.

    def calc_age(self):
        birth_year = int(self.date_of_birth)
        current_year = datetime.now().year
        age_years = current_year - birth_year
        return age_years
    # Berechnet das Alter der Person.

    def calc_max_heart_rate(self):
        max_hr_bpm = 220-self.calc_age()
        return (max_hr_bpm)
    # Berechnet die maximale Herzfrequenz der Person.
    

if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    # print(person_names)
    # print(Person.find_person_data_by_name("Huber, Julian"))

    a_dict = persons[2]
    
    a_person = Person(a_dict)

    # print (a_person.calc_age())
    # print(a_person.calc_max_heart_rate())
    # print(Person.load_by_id(1))
    
    Person_Dict = Person.load_by_id(3)
    print (Person_Dict)
    
    liste_ekg_tests = []
    for einträge in Person_Dict ['ekg_tests']:
        # print (i)
        liste_ekg_tests.append(einträge['result_link'])
    
    print (liste_ekg_tests)