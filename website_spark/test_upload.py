import requests

# Test the /analyze endpoint with our test files
url = "http://127.0.0.1:5000/analyze"

# Open the test files
with open("test_resume.pdf", "rb") as resume_file, open("test_jd.pdf", "rb") as jd_file:
    files = {
        "resume": ("test_resume.pdf", resume_file, "application/pdf"),
        "job": ("test_jd.pdf", jd_file, "application/pdf")
    }
    
    try:
        response = requests.post(url, files=files)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", str(e))