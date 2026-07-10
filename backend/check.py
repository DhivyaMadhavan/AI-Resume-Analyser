from app.services.personal_service import extract_personal_details

text = """
John Doe

Email: john.doe@gmail.com
Phone: +91 9876543210

LinkedIn:
https://linkedin.com/in/johndoe

GitHub:
https://github.com/johndoe
"""

print(extract_personal_details(text))