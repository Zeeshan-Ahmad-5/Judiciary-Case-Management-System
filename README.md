# Judiciary Case Management System

## Overview
The Judiciary Case Management System is a Python-based application designed to streamline and secure the management of judicial cases and evidence. The system allows administrators to create and manage case directories, upload evidence files, update case statuses, and enable committee members (judges) to view case details and evidence. It improves transparency, accountability, and efficiency within judicial processes.

## Features
- **User Authentication:** Role-based access for Admin and Committee members.
- **Case Management:** Create new cases with detailed information and store them in structured directories.
- **Evidence Uploading:** Securely upload PDF evidence files linked to specific cases.
- **Case Status Update:** Change case status between "Active" and "Solved".
- **Version Control:** Track all changes made to case files with timestamps for accountability.
- **Search & List Cases:** Search cases by code or type and list all existing cases with their current status.
- **Role-Specific Menus:** Separate interfaces and permissions for admins and committee members.

## Technologies Used
- Python 3.x
- Standard libraries: `os`, `shutil`, `datetime`, `re`
- (Optional) Tkinter for GUI version (included in `GUI.py`)

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/judiciary-case-management.git
   cd judiciary-case-management
