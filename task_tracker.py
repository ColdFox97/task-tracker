import argparse
import json
import sys
import time

parser = argparse.ArgumentParser(description="CLI for managing tasks")

subparsers = parser.add_subparsers(dest="action", required=True)

add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("description", type=str, help="The text description of a task")

delete_parser = subparsers.add_parser("delete", help="Delete a task")
delete_parser.add_argument("id", type=int, help="ID of a specific task")

update_parser = subparsers.add_parser("update", help="Update a description of a task")
update_parser.add_argument("id", type=int, help="ID of a task to update")
update_parser.add_argument("description", type=str, help="The new desctiption of a task")

list_parser = subparsers.add_parser("list", help="List all tasks")
list_parser.add_argument(
    "status",
    nargs="?",
    choices=["todo", "in-progress", "done"],
    help="Optional: filter tasks by status"
)

mark_parser = subparsers.add_parser("mark", help="Change status of a task")
mark_parser.add_argument("id", type=int, help="ID of a task to update")
mark_parser.add_argument(
    "status",
    choices=["todo", "in-progress", "done"],
    help="The new status for the task"
)

args = parser.parse_args()

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

modified = False
    
if args.action == "add":

    id = data["next_id"]

    data["tasks"][id] = {}

    data["tasks"][id]["description"] = args.description
    data["tasks"][id]["status"] = "todo"
    data["tasks"][id]["created_at"] = time.ctime()
    data["tasks"][id]["updated_at"] = time.ctime()

    data["next_id"] = str(int(id) + 1)
    modified = True
    print("SUCCESS: task added")

elif args.action == "delete":

    id = str(args.id)

    if data["tasks"].pop(id, None) is not None:
        print(f"SUCCESS: task {id} removed")
        modified = True

    else:
        print(f"Error: task {id} not found")

elif args.action == "update":
    
    id = str(args.id)
    description = args.description

    if data["tasks"].get(id, None) is not None:
        data["tasks"][id]["description"] = description
        data["tasks"][id]["updated_at"] = time.ctime()
        modified = True
        
        print(f"SUCCESS: task {id} updated")

    else:
        print(f"ERROR: task {id} not found")            

elif args.action == "list":

    status = args.status

    if status == None:
        for id in data["tasks"]:
            description = data["tasks"][id].get("description")
            print(f"[{id}] {description}")

    elif status == "todo":
        for id in data["tasks"]:
            if data["tasks"][id].get("status") == "todo":
                description = data["tasks"][id].get("description")
                print(f"[{id}] {description}")

    elif status == "in-progress":
        for id in data["tasks"]:
            if data["tasks"][id].get("status") == "in-progress":
                description = data["tasks"][id].get("description")
                print(f"[{id}] {description}")

    elif status == "done":
        for id in data["tasks"]:
            if data["tasks"][id].get("status") == "done":
                description = data["tasks"][id].get("description")
                print(f"[{id}] {description}")

elif args.action == "mark":
    
    id = str(args.id)

    if data["tasks"].get(id, None) is None:
        print(f"Error: task {id} not found")
        sys.exit(1)

    if args.status == "in-progress":
        data["tasks"][id]["status"] = "in-progress"
        data["tasks"][id]["updated_at"] = time.ctime()
        modified = True
        
        print(f"SUCCESS: task {id} status changed to 'in-progress'")

    elif args.status == "done":
        data["tasks"][id]["status"] = "done"
        data["tasks"][id]["updated_at"] = time.ctime()
        modified = True

        print(f"SUCCESS: task {id} status changed to 'done'")

    elif args.status == "todo":
        data["tasks"][id]["status"] = "todo"
        data["tasks"][id]["updated_at"] = time.ctime()
        modified = True

        print(f"SUCCESS: task {id} status changed to 'todo'")

if modified:
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)