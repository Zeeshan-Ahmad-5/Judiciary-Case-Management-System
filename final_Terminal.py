import os
import shutil
from datetime import datetime
import re

MAIN_DIR = 'cases/'
os.makedirs(MAIN_DIR, exist_ok=True)

# User credentials
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "judge": {"password": "judge456", "role": "committee"}
}

# Authenticate user
def authenticate():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    if username in USERS and USERS[username]["password"] == password:
        return USERS[username]["role"]
    else:
        print("Invalid input.")
        return None

# Log changes to version control
def log_version_control(case_directory, action, details, user_role):
    version_file = os.path.join(case_directory, "version_control.txt")
    timestamp = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    with open(version_file, 'a') as file:
        file.write(f"[{timestamp}] {action} by {user_role}: {details}\n")

# Create new case directory
def create_case_directory(case_code, case_type, guilty, location, time, user_role):
    case_directory = os.path.join(MAIN_DIR, case_code)
    if not all([case_code, case_type, guilty, location, time]):
        print("All fields must be filled.")
        return
    if not re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", time):
        print("Time must be in format YYYY-MM-DD HH:MM (e.g., 2023-10-01 14:30)")
        return
    if not os.path.exists(case_directory):
        os.makedirs(case_directory)
        # Save case details
        with open(os.path.join(case_directory, "case_info.txt"), 'w') as file:
            file.write(f"Case ID: {case_code}\n")
            file.write(f"Case Type: {case_type}\n")
            file.write(f"Guilty: {guilty}\n")
            file.write(f"Location: {location}\n")
            file.write(f"Time: {time}\n")
            file.write("Status: Active\n")
        log_version_control(case_directory, "Created", f"Case {case_code} created with type {case_type}", user_role)
        print(f"Case '{case_code}' created successfully!")
    else:
        print(f"Case code '{case_code}' already exists.")
    return case_directory

# Upload PDF evidence
def upload_evidence(case_code, evidence_file, user_role):
    case_directory = os.path.join(MAIN_DIR, case_code)
    if not os.path.exists(case_directory):
        print(f"Case '{case_code}' does not exist. Please create it first.")
        return
    if os.path.exists(evidence_file):
        if evidence_file.lower().endswith('.pdf'):
            evidence_path = os.path.join(case_directory, os.path.basename(evidence_file))
            shutil.move(evidence_file, evidence_path)
            log_version_control(case_directory, "Evidence Uploaded", f"File {os.path.basename(evidence_file)} added", user_role)
            print(f"Evidence '{evidence_file}' uploaded successfully.")
        else:
            print("Please upload a PDF file.")
    else:
        print(f"File '{evidence_file}' not found. Check the file path.")

# View case details
def view_case_details(case_code):
    case_directory = os.path.join(MAIN_DIR, case_code)
    if os.path.exists(case_directory):
        try:
            with open(os.path.join(case_directory, "case_info.txt"), 'r') as file:
                case_info = file.read()
                print(f"\nCase details for '{case_code}':")
                print(case_info)
                # List evidence files
                files = os.listdir(case_directory)
                evidence_files = [f for f in files if f != "case_info.txt" and f != "version_control.txt"]
                if evidence_files:
                    print(f"\nEvidence files for case '{case_code}':")
                    for file in evidence_files:
                        print(f" - {file}")
                else:
                    print(f"No evidence files found for case '{case_code}'.")
                # Show version history
                version_file = os.path.join(case_directory, "version_control.txt")
                if os.path.exists(version_file):
                    with open(version_file, 'r') as file:
                        print("\nVersion Control History:")
                        print(file.read())
        except FileNotFoundError:
            print(f"Case details file for '{case_code}' not found.")
    else:
        print(f"Case '{case_code}' does not exist.")

# Update case status
def update_case_status(case_code, user_role):
    case_directory = os.path.join(MAIN_DIR, case_code)
    if os.path.exists(case_directory):
        case_info_path = os.path.join(case_directory, "case_info.txt")
        if os.path.exists(case_info_path):
            status = input("Enter new status ('Active' or 'Solved'): ").strip().lower()
            if status in ['active', 'solved']:
                with open(case_info_path, 'r') as file:
                    lines = file.readlines()
                with open(case_info_path, 'w') as file:
                    for line in lines:
                        if line.startswith("Status:"):
                            file.write(f"Status: {status.capitalize()}\n")
                        else:
                            file.write(line)
                log_version_control(case_directory, "Status Updated", f"Status changed to {status.capitalize()}", user_role)
                print(f"Case '{case_code}' status updated to {status.capitalize()}.")
            else:
                print("Invalid status. Please enter 'Active' or 'Solved'.")
        else:
            print(f"Case details file for '{case_code}' not found.")
    else:
        print(f"Case '{case_code}' does not exist.")

# Delete case with backup
def delete_case(case_code):
    case_directory = os.path.join(MAIN_DIR, case_code)
    backup_dir = 'backups/'
    os.makedirs(backup_dir, exist_ok=True)
    if os.path.exists(case_directory):
        confirm = input(f"Are you sure you want to delete case '{case_code}'? (yes/no): ").strip().lower()
        if confirm == 'yes':
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"{case_code}_{timestamp}")
            shutil.copytree(case_directory, backup_path)
            shutil.rmtree(case_directory)
            print(f"Case '{case_code}' deleted successfully. Backup created at {backup_path}.")
        else:
            print("Deletion cancelled.")
    else:
        print(f"Case '{case_code}' does not exist.")

# List all cases
def list_cases():
    cases = os.listdir(MAIN_DIR)
    if cases:
        active_cases = 0
        solved_cases = 0
        print("\nList of all cases:")
        for case in cases:
            case_directory = os.path.join(MAIN_DIR, case)
            if os.path.isdir(case_directory):
                case_info_path = os.path.join(case_directory, "case_info.txt")
                if os.path.exists(case_info_path):
                    with open(case_info_path, 'r') as file:
                        status = 'Active'
                        for line in file:
                            if line.startswith("Status:"):
                                status = line.split(":")[1].strip()
                        if status.lower() == 'active':
                            active_cases += 1
                        else:
                            solved_cases += 1
                    print(f" - {case} (Status: {status})")
        print(f"\nActive cases: {active_cases}")
        print(f"Solved cases: {solved_cases}")
    else:
        print("No cases available.")

# Main program
if __name__ == "__main__":
    role = authenticate()
    if not role:
        print("Access denied. Exiting.")
        exit()
    while True:
        print("\n=== Case Management System ===")
        if role == "admin":
            print("1. Admin Menu")
        elif role == "committee":
            print("1. Committee Menu")
        print("2. Exit")
        choice = input("Choose an option (1-2): ").strip()
        if choice == "1":
            if role == "admin":
                while True:
                    print("\n=== Admin Menu ===")
                    print("1. Create New Case")
                    print("2. Upload Evidence")
                    print("3. Update Case Status")
                    print("4. List All Cases")
                    print("5. Back to Main Menu")
                    admin_choice = input("Choose an option (1-5): ").strip()
                    if admin_choice == "1":
                        case_code = input("Enter case code: ").strip()
                        if case_code:
                            case_type = input("Enter case type: ").strip()
                            guilty = input("Enter guilty person name: ").strip()
                            location = input("Enter location: ").strip()
                            time = input("Enter time: ").strip()
                            create_case_directory(case_code, case_type, guilty, location, time, role)
                        else:
                            print("Case code cannot be empty.")
                    elif admin_choice == "2":
                        case_code = input("Enter case code: ").strip()
                        if case_code:
                            evidence_file = input("Enter evidence file path (Only PDF File): ").strip()
                            upload_evidence(case_code, evidence_file, role)
                        else:
                            print("Case code cannot be empty.")
                    elif admin_choice == "3":
                        case_code = input("Enter case code: ").strip()
                        if case_code:
                            update_case_status(case_code, role)
                        else:
                            print("Case code cannot be empty.")
                    elif admin_choice == "4":
                        list_cases()
                    elif admin_choice == "5":
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 5.")
            elif role == "committee":
                while True:
                    print("\n=== Committee Menu ===")
                    print("1. View Case Details")
                    print("2. Delete Case")
                    print("3. Back to Main Menu")
                    committee_choice = input("Choose an option (1-3): ").strip()
                    if committee_choice == "1":
                        case_code = input("Enter case code: ").strip()
                        if case_code:
                            view_case_details(case_code)
                        else:
                            print("Case code cannot be empty.")
                    elif committee_choice == "2":
                        case_code = input("Enter case code: ").strip()
                        if case_code:
                            delete_case(case_code)
                        else:
                            print("Case code cannot be empty.")
                    elif committee_choice == "3":
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 3.")
        elif choice == "2":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
































            