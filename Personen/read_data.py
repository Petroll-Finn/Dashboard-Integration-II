import json
import pandas as pd

def load_person_data(link):
    # Eine Funktion, die weiß, wo sich die Personendatenbank befindet und ein Dictionary mit den Personen zurückgibt
    file = open(link)
    person_data = json.load(file)
    return person_data

def get_person_list(person_data_Dict):
    # Eine Funktion, die das Personen-Dictionary nimmt und eine Liste mit allen Personennamen zurückgibt
    # person_data = load_person_data(link)
    person_data = person_data_Dict
    
    list1 = []
    for Eintrag in person_data:
        list1.append(Eintrag['lastname']+ ", " +  Eintrag["firstname"])

    return list1


def find_person_data_by_name(suchstring, person_data_Dict):
    # Eine Funktion der Nachname, Vorname als ein String übergeben wird und die die Person als Dictionary zurück gibt
    # person_data = load_person_data(link)
    person_data = person_data_Dict

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
   
