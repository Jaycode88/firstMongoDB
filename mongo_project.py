import os
import pymongo
if os.path.exists("env.py"):
    import env


MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")

    option = input("Enter option: ")
    return option


def get_record(coll):
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")

    try:
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except Exception as e:
        print("Error accessing the database", e)

    if doc is None:
        print("")
        print("No results found.")
    else:
        return doc


def add_record(coll):
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    dob = input("Enter date of birth > ")
    gender = input("Enter gender > ")
    hair_color = input("Enter hair color > ")
    occupation = input("Enter occupation > ")
    nationality = input("Enter nationality > ")

    new_doc = {
        "first": first.lower(),
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "hair_color": hair_color,
        "occupation": occupation,
        "nationality": nationality
    }

    try:
        insert_result = coll.insert_one(new_doc)
        print("")
        print("Document inserted", insert_result.inserted_id)
    except Exception as e:
        print("Error accessing the database", e)


def find_record(coll):
    doc = get_record(coll)
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())


def edit_record(coll):
    doc = get_record(coll)
    if doc:
        print("")
        update_doc = {}  # Initialize the update_doc dictionary
        for k, v in doc.items():
            if k != "_id":
                update_value = input(k.capitalize() + "[" + v + "] > ")

                if update_value == "":
                    update_value = v
                update_doc[k] = update_value

        try:
            coll.update_one({"_id": doc["_id"]}, {"$set": update_doc})
            print("")
            print("Document updated")
        except Exception as e:
            print("Error accessing the database", e)


def delete_record(coll):
    doc = get_record(coll)
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())
        print("")
        confirmation = input("Is this the document you want to delete?\nY or N")
        print("")

        if confirmation.lower() == "y":
            try:
                coll.delete_one(doc)
                print("Document deleted!")
            except Exception as e:
                print("Error accessing the database", e)
        else:
            print("Document not deleted")


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record(coll)
        elif option == "2":
            find_record(coll)
        elif option == "3":
            edit_record(coll)
        elif option == "4":
            delete_record(coll)
        elif option == "5":
            print("You have selected option 5")
            conn.close()
            break
        else:
            print("Invalid option")
        print("")


conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()
