import sys
import json
import time


try:
    with open("tasks.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    print("file tasks.json does not exit or is empty")
    print("creating tasks.json...")
    
    data = {
        "next_id": "1",
        "tasks": {}
    }

    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    
    print("tasks.json created")


if len(sys.argv) < 2:
    print("please provide actions")
    sys.exit(1)


action = sys.argv[1].lower()
modified = False
    
if action == "add":

    if len(sys.argv) < 3:
        print("ERROR: missing description")
        sys.exit(1)

    description = sys.argv[2]
    id = data["next_id"]

    data["tasks"][id] = {}

    data["tasks"][id]["description"] = description
    data["tasks"][id]["status"] = "todo"
    data["tasks"][id]["created_at"] = time.ctime()
    data["tasks"][id]["updated_at"] = time.ctime()

    data["next_id"] = str(int(id) + 1)
    modified = True
    print("SUCCESS: task added")

elif action == "delete":

    if len(sys.argv) < 3:
        print("ERROR: missing ID ")
        sys.exit(1)

    id = sys.argv[2]

    if not id.isdigit():
        print("ERROR: not valid ID")
        sys.exit(1)

    if data["tasks"].pop(id, None) is not None:
        print(f"SUCCESS: task {id} removed")
        modified = True

    else:
        print(f"Error: task {id} not found")

elif action == "update":
    
    if len(sys.argv) < 3:
        print("ERROR: missing ID")
        sys.exit(1)

    id = sys.argv[2]

    if not id.isdigit():
        print("ERROR: not valid ID")
        sys.exit(1)

    if len(sys.argv) < 4:
        print("ERROR: missing description")
        sys.exit(1)

    description = sys.argv[3]

    if data["tasks"].get(id, None) is not None:
        data["tasks"][id]["description"] = description
        data["tasks"][id]["updated_at"] = time.ctime()
        modified = True

        print(f"SUCCESS: task {id} updated")

    else:
        print(f"ERROR: task {id} not found")            

elif action == "list":

    if len(sys.argv) < 3:
        for id in data["tasks"]:
            description = data["tasks"][id].get("description")
            print(f"[{id}] {description}")
        sys.exit(0)

    option = sys.argv[2]

    if option == "todo":
        for id in data["tasks"]:
            if data["tasks"][id].get("status") == "todo":
                description = data["tasks"][id].get("description")
                print(f"[{id}] {description}")

    elif option == "in-progress":
        for id in data["tasks"]:
            if data["tasks"][id].get("status") == "in-progress":
                description = data["tasks"][id].get("description")
                print(f"[{id}] {description}")

    elif option == "done":
        for id in data["tasks"]:
            if data["tasks"][id].get("status") == "done":
                description = data["tasks"][id].get("description")
                print(f"[{id}] {description}")

elif action.startswith("mark"):
    
    if len(sys.argv) < 3:
        print("ERROR: missing ID")
        sys.exit(1)

    id = sys.argv[2]

    if not id.isdigit():
        print("ERROR: not valid ID")
        sys.exit(1)

    if id not in data["tasks"]:
        print(f"ERROR: task {id} not found")
        sys.exit(1)

    if action.endswith("-in-progress"):
        data["tasks"][id]["status"] = "in-progress"
        data["tasks"][id]["updated_at"] = time.ctime()
        modified = True

    elif action.endswith("-done"):
        data["tasks"][id]["status"] = "done"
        data["tasks"][id]["updated_at"] = time.ctime()
        modified = True           
    else:
        print("ERROR: wrong option")    

else:
    print("ERROR: wrong action")

if modified:
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)