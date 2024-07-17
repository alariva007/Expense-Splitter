CS3300-SemesterProject
Group Project CS3300 Intro to Software Engineering

How to run our software on a Windows device

1. Download the software Package
• Download and Extract the software package into an easily accesible folder.

2. Open the Command Prompt
• type cmd into the windows search field then press Enter.

3. Verify Python is Installed, Otherwise Install Python
• type: py --version
• If the command does not return: Python 3.12.2, then install python at https://www.python.org/downloads/release/python-3122/

4. Navigate to Project Directory containing the Software Package
• Use the cd command to enter the directory where the downloaded/extracted Django project is located.
• For example: cd path\directory\another_directory\TheSoftwarePackage

5. Create a Virtual Environment
• Created a virtual environment with the following command (replace “env” with whatever you would like to name your environment):
• py -m venv env

6. Move the Entire Software Package into the Virtual Environment Folder
• Using Windows file exploer, copy the entire software package into the virtual environment's newly created folder.
• Select the Replace All option for any/all duplicate files.

7. Activate the Virtual Environment
• Activate the virtual environment with the following command on the command line:
• env\Scripts\activate.bat

8. Install Django
• If Django is not already installed in your virtual environment, install the Django framework with the command:
• py -m pip install Django

9. Run the Django Development Server
• Navigate to the folder in your virtual environment containing the application: manage.py
• Start the Django development server with the command:  py manage.py runserver

10. In Your Web-Browser, Go to the Provided URL
• The command prompt will return a locally hosted web-url like http://localhost:8000/ or something very similar.