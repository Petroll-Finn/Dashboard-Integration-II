import json
import pandas as pd

def load_person_data():
    """A Function that knows where the person database is and returns a dictionary with the persons"""
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data

def get_person_list():
    """A Function that takes the persons-dictionary and returns a list auf all person names"""
    person_data = load_person_data()

    list1 = []
    for Eintrag in person_data:
        list1.append(Eintrag['lastname']+ ", " +  Eintrag["firstname"])

    return list1


def find_person_data_by_name(suchstring):
    """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
    und die die Person als Dictionary zurück gibt"""

    person_data = load_person_data()
    #print(suchstring)
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        # print(eintrag)
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            # print (eintrag)
            return eintrag
        
    return {}

def txt_to_df (path):
    df = pd.read_csv(path)
    return df

# def list_pathes ()

if __name__ == "__main__":
    print (load_person_data ())
    # print(get_person_list())
    # print (find_person_data_by_name("Huber, Julian"))

    
    # print (txt_to_df('..\data/ekg_data/01_Ruhe.txt'))




    Dict_CurrentUser = find_person_data_by_name("Huber, Julian")
    list_ekg = Dict_CurrentUser['ekg_tests']
    # print (type(a))
    # print (Dict_CurrentUser['ekg_tests'])
   
