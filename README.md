# Academic Shared Review Platform
# 📋 Overview
The Academic Shared Review Platform is a web application designed to facilitate collaborative peer review and feedback sharing for academic papers. Built with a Flask backend and modern web technologies, this platform helps researchers and academics share, review, and improve scholarly work through a structured review process.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/76344012-9abd-4412-a93e-b8f222002c98" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5f1fa206-ab80-4a1e-a5c9-ae228a0ee375" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c6367885-cef9-4ee5-815e-007c76b082f7" />
![Uploading image.png…]()





 # ✨ Key Features
Paper Submission & Management: Upload and organize academic papers

Structured Review System: Provide detailed feedback through organized review forms

User Profiles: Customizable profiles with picture support

Admin Dashboard: Administrative controls for platform management

Secure File Handling: Protected upload and storage system

# 🛠️ Technology Stack
Backend: Python/Flask

Frontend: HTML (66.5%), CSS (15.9%), JavaScript (0.8%)

Database: SQLite (with migration support)

Deployment: Heroku-ready (Procfile configuration)

# 🚀 Quick Start
Prerequisites
Python 3.8+

pip package manager

Installation
Clone the repository:

bash
git clone https://github.com/Seanscript-dev/Academic-Shared-Review-Platform.git
cd Academic-Shared-Review-Platform
Install dependencies:

bash
pip install -r requirements.txt
Initialize the database:

bash
python migrate_db.py
Create an admin account:

bash
python create_admin.py
(Optional) Migrate profile pictures if needed:

bash
python migrate_profile_pictures.py
Run the application:

bash
python wsgi.py
Access the platform at http://localhost:5000

# 📁 Project Structure
text
Academic-Shared-Review-Platform/
├── app/                    # Main application module
├── uploads/               # File upload directory
├── .dist/                 # Distribution files
├── .vscode/               # VS Code configuration
├── __pycache__/           # Python cache files
├── instance/              # Instance-specific files
├── Procfile              # Heroku deployment configuration
├── requirements.txt      # Python dependencies
├── TODO.md               # Development roadmap
├── create_admin.py       # Admin user creation script
├── migrate_db.py         # Database migration script
├── migrate_profile_pictures.py  # Profile picture migration
├── test_admin_global.py  # Admin functionality tests
├── test_db.py            # Database tests
└── wsgi.py               # WSGI entry point
🔧 Configuration
Environment variables for sensitive configuration

SQLite database with migration support

Configurable upload paths and file size limits

# 🧪 Testing
Run the included test scripts:

bash
python test_db.py
python test_admin_global.py
🌐 Deployment
The application is configured for Heroku deployment with:

Pre-configured Procfile

WSGI application entry point

Production-ready settings

# 🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add some AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

# 📝 Development Notes
Check TODO.md for planned features and improvements

Regular database migrations may be required for updates

Profile pictures are handled separately via migration scripts

# 📄 License
This project is currently without a specified license. Please contact the repository owner for usage permissions.

# 📧 Contact
Repository Maintainer: Seanscript-dev

GitHub: @Seanscript-dev

Last Updated: January 2026 | Version: Initial Release
