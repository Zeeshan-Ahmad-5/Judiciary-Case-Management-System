import os
import shutil
from datetime import datetime
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from ttkthemes import ThemedTk

# Main directory where all case files (PDFs) will be stored
MAIN_DIR = 'cases/'
BACKUP_DIR = 'backups/'

# Create directories if they don't exist
os.makedirs(MAIN_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# Simple user credentials
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "judge": {"password": "judge456", "role": "committee"}
}

class JudiciarySystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Judiciary Case Management System")
        # Increased window size to ensure all elements, including buttons, are visible
        self.root.geometry("1000x900")
        self.root.resizable(False, False)
        self.role = None
        self.style = ttk.Style()
        self.configure_styles()
        self.create_login_screen()

    def configure_styles(self):
        # Configure formal styles with dark black font for visibility
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("Content.TFrame", background="#ecf0f1")
        self.style.configure("TLabel", font=("Times New Roman", 12), background="#ecf0f1", foreground="#000000")
        self.style.configure("Title.TLabel", font=("Times New Roman", 20, "bold"), background="#2c3e50", foreground="#f1c40f")
        self.style.configure("Footer.TLabel", font=("Times New Roman", 10, "italic"), background="#2c3e50", foreground="#bdc3c7")
        self.style.configure("TEntry", font=("Times New Roman", 12), foreground="#000000")
        self.style.configure("TButton", font=("Times New Roman", 12, "bold"), padding=10, foreground="#000000")
        self.style.configure("Menu.TButton", font=("Times New Roman", 12, "bold"), padding=15, background="#3498db", foreground="#000000")
        self.style.map("Menu.TButton",
                       background=[('active', '#2980b9'), ('pressed', '#1f618d')],
                       foreground=[('active', '#000000'), ('pressed', '#000000')])
        self.style.configure("Action.TButton", font=("Times New Roman", 12, "bold"), padding=10, background="#2ecc71", foreground="#000000")
        self.style.map("Action.TButton",
                       background=[('active', '#27ae60'), ('pressed', '#219653')],
                       foreground=[('active', '#000000'), ('pressed', '#000000')])
        self.style.configure("Back.TButton", font=("Times New Roman", 12), padding=10, background="#e74c3c", foreground="#000000")
        self.style.map("Back.TButton",
                       background=[('active', '#c0392b'), ('pressed', '#992d22')],
                       foreground=[('active', '#000000'), ('pressed', '#000000')])
        self.style.configure("TCombobox", font=("Times New Roman", 12), foreground="#000000")
        self.style.configure("TScrolledText", font=("Times New Roman", 12), foreground="#000000")
        # Ensure LabelFrame titles are visible
        self.style.configure("TLabelframe", font=("Times New Roman", 14, "bold"), foreground="#000000", padding=10)
        self.style.configure("TLabelframe.Label", font=("Times New Roman", 14, "bold"), foreground="#f1c40f", background="#ecf0f1")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#2c3e50")

    def add_header_footer(self):
        header_frame = ttk.Frame(self.root, style="TFrame")
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="Judiciary Case Management System", style="Title.TLabel").pack(pady=10)
        
        footer_frame = ttk.Frame(self.root, style="TFrame")
        footer_frame.pack(side="bottom", fill="x")
        ttk.Label(footer_frame, text="Version 1.0 | Developed for Judicial Administration", style="Footer.TLabel").pack(pady=5)

    def create_login_screen(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        login_frame = ttk.LabelFrame(content_frame, text="System Login", padding=20)
        login_frame.pack(pady=20, padx=20, fill="x")

        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        username_entry = ttk.Entry(login_frame, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        password_entry = ttk.Entry(login_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        def authenticate():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if username in USERS and USERS[username]["password"] == password:
                self.role = USERS[username]["role"]
                self.create_main_menu()
            else:
                messagebox.showerror("Authentication Failed", "Invalid username or password.", parent=self.root)

        button_frame = ttk.Frame(login_frame, style="Content.TFrame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="🔒 Login", style="Action.TButton", command=authenticate).pack()

    def create_main_menu(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        menu_frame = ttk.LabelFrame(content_frame, text="Main Menu", padding=20)
        menu_frame.pack(pady=20, fill="x")

        if self.role == "admin":
            ttk.Button(menu_frame, text="🛠 Administrator Menu", style="Menu.TButton", command=self.create_admin_menu).pack(pady=10, fill="x")
        elif self.role == "committee":
            ttk.Button(menu_frame, text="⚖ Committee Menu", style="Menu.TButton", command=self.create_committee_menu).pack(pady=10, fill="x")
        ttk.Button(menu_frame, text="🚪 Exit System", style="Back.TButton", command=self.root.quit).pack(pady=10, fill="x")

    def create_admin_menu(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        menu_frame = ttk.LabelFrame(content_frame, text="Administrator Menu", padding=20)
        menu_frame.pack(pady=20, fill="x")

        buttons = [
            ("📝 Create New Case", self.create_case_form),
            ("📎 Upload Evidence", self.upload_evidence_form),
            ("🔄 Update Case Status", self.update_status_form),
            ("📋 List All Cases", self.list_cases),
            ("🔍 Search Cases", self.search_cases_form),
            ("⬅ Return to Main Menu", self.create_main_menu)
        ]
        for text, command in buttons:
            style = "Menu.TButton" if "Return" not in text else "Back.TButton"
            ttk.Button(menu_frame, text=text, style=style, command=command).pack(pady=10, fill="x")

    def create_committee_menu(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        menu_frame = ttk.LabelFrame(content_frame, text="Committee Menu", padding=20)
        menu_frame.pack(pady=20, fill="x")

        buttons = [
            ("📄 View Case Details", self.view_case_details_form),
            ("🗑 Delete Case", self.delete_case_form),
            ("⬅ Return to Main Menu", self.create_main_menu)
        ]
        for text, command in buttons:
            style = "Menu.TButton" if "Return" not in text else "Back.TButton"
            ttk.Button(menu_frame, text=text, style=style, command=command).pack(pady=10, fill="x")

    def log_version_control(self, case_directory, action, details, user_role):
        version_file = os.path.join(case_directory, "version_control.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(version_file, 'a') as file:
            file.write(f"[{timestamp}] {action} by {user_role}: {details}\n")

    def create_case_form(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        form_frame = ttk.LabelFrame(content_frame, text="Create New Case", padding=20)
        form_frame.pack(pady=20, fill="x")

        fields = [
            ("Case Code (e.g., CASE001):", "case_code"),
            ("Case Type (e.g., Theft):", "case_type"),
            ("Guilty (or 'Unknown'):", "guilty"),
            ("Location (e.g., Main Street):", "location"),
            ("Time (YYYY-MM-DD HH:MM):", "time")
        ]
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry

        def submit():
            case_code = entries["case_code"].get().strip()
            case_type = entries["case_type"].get().strip()
            guilty = entries["guilty"].get().strip()
            location = entries["location"].get().strip()
            time = entries["time"].get().strip()

            if not all([case_code, case_type, guilty, location, time]):
                messagebox.showerror("Error", "All fields must be filled.", parent=self.root)
                return
            if not re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", time):
                messagebox.showerror("Error", "Time must be in format YYYY-MM-DD HH:MM (e.g., 2023-10-01 14:30)", parent=self.root)
                return

            case_directory = os.path.join(MAIN_DIR, case_code)
            if not os.path.exists(case_directory):
                os.makedirs(case_directory)
                with open(os.path.join(case_directory, "case_info.txt"), 'w') as file:
                    file.write(f"Case ID: {case_code}\n")
                    file.write(f"Case Type: {case_type}\n")
                    file.write(f"Guilty: {guilty}\n")
                    file.write(f"Location: {location}\n")
                    file.write(f"Time: {time}\n")
                    file.write("Status: Active\n")
                self.log_version_control(case_directory, "Created", f"Case {case_code} created with type {case_type}", self.role)
                messagebox.showinfo("Success", f"Case '{case_code}' created successfully.", parent=self.root)
                self.create_admin_menu()
            else:
                messagebox.showerror("Error", f"Case code '{case_code}' already exists.", parent=self.root)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="✔ Submit", style="Action.TButton", command=submit).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⬅ Back", style="Back.TButton", command=self.create_admin_menu).pack(side="left", padx=5)

    def upload_evidence_form(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        form_frame = ttk.LabelFrame(content_frame, text="Upload Evidence", padding=20)
        form_frame.pack(pady=20, fill="x")

        ttk.Label(form_frame, text="Case Code:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        case_code_entry = ttk.Entry(form_frame, width=30)
        case_code_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(form_frame, text="Evidence File (PDF):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        file_label = ttk.Label(form_frame, text="No file selected")
        file_label.grid(row=1, column=1, padx=10, pady=10)

        def select_file():
            file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file_path:
                file_label.config(text=os.path.basename(file_path))
                file_label.file_path = file_path

        ttk.Button(form_frame, text="📁 Browse", style="Action.TButton", command=select_file).grid(row=1, column=2, padx=10, pady=10)

        def submit():
            case_code = case_code_entry.get().strip()
            if not case_code:
                messagebox.showerror("Error", "Case code cannot be empty.", parent=self.root)
                return

            case_directory = os.path.join(MAIN_DIR, case_code)
            if not os.path.exists(case_directory):
                messagebox.showerror("Error", f"Case '{case_code}' does not exist. Please create it first.", parent=self.root)
                return

            if hasattr(file_label, 'file_path'):
                evidence_file = file_label.file_path
                if evidence_file.lower().endswith('.pdf'):
                    evidence_path = os.path.join(case_directory, os.path.basename(evidence_file))
                    shutil.move(evidence_file, evidence_path)
                    self.log_version_control(case_directory, "Evidence Uploaded", f"File {os.path.basename(evidence_file)} added", self.role)
                    messagebox.showinfo("Success", f"Evidence '{os.path.basename(evidence_file)}' uploaded successfully.", parent=self.root)
                    self.create_admin_menu()
                else:
                    messagebox.showerror("Error", "Please upload a PDF file.", parent=self.root)
            else:
                messagebox.showerror("Error", "No file selected.", parent=self.root)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        ttk.Button(button_frame, text="✔ Submit", style="Action.TButton", command=submit).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⬅ Back", style="Back.TButton", command=self.create_admin_menu).pack(side="left", padx=5)

    def update_status_form(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        form_frame = ttk.LabelFrame(content_frame, text="Update Case Status", padding=20)
        form_frame.pack(pady=20, fill="x")

        ttk.Label(form_frame, text="Case Code:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        case_code_entry = ttk.Entry(form_frame, width=30)
        case_code_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(form_frame, text="New Status:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        status_var = tk.StringVar(value="Active")
        ttk.OptionMenu(form_frame, status_var, "Active", "Active", "Solved").grid(row=1, column=1, padx=10, pady=10)

        def submit():
            case_code = case_code_entry.get().strip()
            status = status_var.get().lower()

            if not case_code:
                messagebox.showerror("Error", "Case code cannot be empty.", parent=self.root)
                return

            case_directory = os.path.join(MAIN_DIR, case_code)
            if not os.path.exists(case_directory):
                messagebox.showerror("Error", f"Case '{case_code}' does not exist.", parent=self.root)
                return

            case_info_path = os.path.join(case_directory, "case_info.txt")
            if os.path.exists(case_info_path):
                with open(case_info_path, 'r') as file:
                    lines = file.readlines()
                with open(case_info_path, 'w') as file:
                    for line in lines:
                        if line.startswith("Status:"):
                            file.write(f"Status: {status.capitalize()}\n")
                        else:
                            file.write(line)
                self.log_version_control(case_directory, "Status Updated", f"Status changed to {status.capitalize()}", self.role)
                messagebox.showinfo("Success", f"Case '{case_code}' status updated to {status.capitalize()}.", parent=self.root)
                self.create_admin_menu()
            else:
                messagebox.showerror("Error", f"Case details file for '{case_code}' not found.", parent=self.root)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="✔ Submit", style="Action.TButton", command=submit).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⬅ Back", style="Back.TButton", command=self.create_admin_menu).pack(side="left", padx=5)

    def list_cases(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        list_frame = ttk.LabelFrame(content_frame, text="List All Cases", padding=20)
        list_frame.pack(pady=20, fill="both", expand=True)

        text_area = scrolledtext.ScrolledText(list_frame, width=80, height=25, wrap=tk.WORD, font=("Times New Roman", 12))
        text_area.pack(padx=10, pady=10)

        cases = os.listdir(MAIN_DIR)
        if cases:
            active_cases = 0
            solved_cases = 0
            text_area.insert(tk.END, "List of all cases:\n\n")
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
                        text_area.insert(tk.END, f"- {case} (Status: {status})\n")
            text_area.insert(tk.END, f"\nActive cases: {active_cases}\n")
            text_area.insert(tk.END, f"Solved cases: {solved_cases}\n")
        else:
            text_area.insert(tk.END, "No cases available.\n")

        text_area.config(state='disabled')
        ttk.Button(list_frame, text="⬅ Back", style="Back.TButton", command=self.create_admin_menu).pack(pady=10)

    def search_cases_form(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        form_frame = ttk.LabelFrame(content_frame, text="Search Cases", padding=20)
        form_frame.pack(pady=20, fill="x")

        ttk.Label(form_frame, text="Search by Case Code or Type:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        search_entry = ttk.Entry(form_frame, width=30)
        search_entry.grid(row=0, column=1, padx=10, pady=10)

        text_area = scrolledtext.ScrolledText(form_frame, width=80, height=20, wrap=tk.WORD, font=("Times New Roman", 12))
        text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        def search():
            search_term = search_entry.get().strip()
            if not search_term:
                messagebox.showerror("Error", "Search term cannot be empty.", parent=self.root)
                return

            text_area.config(state='normal')
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f"Search results for '{search_term}':\n\n")

            cases = os.listdir(MAIN_DIR)
            found = False
            for case in cases:
                case_directory = os.path.join(MAIN_DIR, case)
                if os.path.isdir(case_directory):
                    case_info_path = os.path.join(case_directory, "case_info.txt")
                    if os.path.exists(case_info_path):
                        with open(case_info_path, 'r') as file:
                            case_info = file.read()
                            if search_term.lower() in case.lower() or search_term.lower() in case_info.lower():
                                text_area.insert(tk.END, f"- {case}\n")
                                found = True
            if not found:
                if search_term.lower().startswith("case"):
                    text_area.insert(tk.END, f"No case exists with code '{search_term}'.\n")
                else:
                    text_area.insert(tk.END, "No cases found.\n")

            text_area.config(state='disabled')

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="🔍 Search", style="Action.TButton", command=search).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⬅ Back", style="Back.TButton", command=self.create_admin_menu).pack(side="left", padx=5)

    def view_case_details_form(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        form_frame = ttk.LabelFrame(content_frame, text="View Case Details", padding=20)
        form_frame.pack(pady=20, fill="x")

        ttk.Label(form_frame, text="Case Code:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        case_code_entry = ttk.Entry(form_frame, width=30)
        case_code_entry.grid(row=0, column=1, padx=10, pady=10)

        # Reduced the height of the ScrolledText to ensure buttons are visible
        text_area = scrolledtext.ScrolledText(form_frame, width=80, height=20, wrap=tk.WORD, font=("Times New Roman", 12))
        text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        def view():
            case_code = case_code_entry.get().strip()
            if not case_code:
                messagebox.showerror("Error", "Case code cannot be empty.", parent=self.root)
                return

            case_directory = os.path.join(MAIN_DIR, case_code)
            text_area.config(state='normal')
            text_area.delete(1.0, tk.END)

            if os.path.exists(case_directory):
                try:
                    with open(os.path.join(case_directory, "case_info.txt"), 'r') as file:
                        case_info = file.read()
                        text_area.insert(tk.END, f"Case details for '{case_code}':\n\n")
                        text_area.insert(tk.END, case_info + "\n")

                    files = os.listdir(case_directory)
                    evidence_files = [f for f in files if f != "case_info.txt" and f != "version_control.txt"]
                    if evidence_files:
                        text_area.insert(tk.END, f"\nEvidence files for case '{case_code}':\n")
                        for file in evidence_files:
                            text_area.insert(tk.END, f"- {file}\n")
                    else:
                        text_area.insert(tk.END, f"\nNo evidence files found for case '{case_code}'.\n")

                    version_file = os.path.join(case_directory, "version_control.txt")
                    if os.path.exists(version_file):
                        with open(version_file, 'r') as file:
                            text_area.insert(tk.END, "\nVersion Control History:\n")
                            text_area.insert(tk.END, file.read())
                except FileNotFoundError:
                    text_area.insert(tk.END, f"Case details file for '{case_code}' not found.\n")
            else:
                text_area.insert(tk.END, f"Case '{case_code}' does not exist.\n")

            text_area.config(state='disabled')

        # --- Start of Button Frame Block ---
        # Create a button frame to hold the action buttons below the text area
        button_frame = ttk.Frame(form_frame)
        # Grid the button frame to ensure it appears below the text area
        # Reduced pady to ensure visibility within the window
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        # Add the "Search" button as requested to retrieve case details
        # This button uses the "Action.TButton" style (green background) for consistency
        # The command links to the view() function to display the case details in the text area
        ttk.Button(button_frame, text="🔍 Search", style="Action.TButton", command=view).pack(side="left", padx=5)

        # Retain the "View" button, which also calls the view() function
        ttk.Button(button_frame, text="📄 View", style="Action.TButton", command=view).pack(side="left", padx=5)

        # Retain the "Back" button to return to the committee menu
        # Uses "Back.TButton" style (red background) for visual distinction
        ttk.Button(button_frame, text="⬅ Back", style="Back.TButton", command=self.create_committee_menu).pack(side="left", padx=5)
        # --- End of Button Frame Block ---

    def delete_case_form(self):
        self.clear_screen()
        self.add_header_footer()

        content_frame = ttk.Frame(self.root, style="Content.TFrame", padding=20)
        content_frame.pack(pady=50, padx=50, fill="both", expand=True)

        form_frame = ttk.LabelFrame(content_frame, text="Delete Case", padding=20)
        form_frame.pack(pady=20, fill="x")

        ttk.Label(form_frame, text="Case Code:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        case_code_entry = ttk.Entry(form_frame, width=30)
        case_code_entry.grid(row=0, column=1, padx=10, pady=10)

        def delete():
            case_code = case_code_entry.get().strip()
            if not case_code:
                messagebox.showerror("Error", "Case code cannot be empty.", parent=self.root)
                return

            case_directory = os.path.join(MAIN_DIR, case_code)
            if os.path.exists(case_directory):
                if messagebox.askyesno("Confirm", f"Are you sure you want to delete case '{case_code}'?", parent=self.root):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_path = os.path.join(BACKUP_DIR, f"{case_code}_{timestamp}")
                    shutil.copytree(case_directory, backup_path)
                    shutil.rmtree(case_directory)
                    messagebox.showinfo("Success", f"Case '{case_code}' deleted successfully. Backup created at {backup_path}.", parent=self.root)
                    self.create_committee_menu()
                else:
                    messagebox.showinfo("Info", "Deletion cancelled.", parent=self.root)
            else:
                messagebox.showerror("Error", f"Case '{case_code}' does not exist.", parent=self.root)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="🗑 Delete", style="Action.TButton", command=delete).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⬅ Back", style="Back.TButton", command=self.create_committee_menu).pack(side="left", padx=5)

if __name__ == "__main__":
    try:
        root = ThemedTk(theme="arc")  # Use modern 'arc' theme
        app = JudiciarySystemGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error running GUI: {e}")