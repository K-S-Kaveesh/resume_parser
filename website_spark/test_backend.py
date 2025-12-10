import requests
import json

# Test data
test_resume = "I am a software engineer with experience in Python, Java, and JavaScript. I have worked with Flask, Django, and React frameworks. I'm familiar with AWS and Docker."
test_jd = "We are looking for a software engineer with Python and Java experience. The candidate should know Flask and Django frameworks. AWS experience is required. Knowledge of Docker is preferred."

# Test the /analyze endpoint
url = "http://127.0.0.1:5000/analyze"

# Since we can't easily test file uploads without actual files, let's test the health endpoint first
health_url = "http://127.0.0.1:5000/health"
try:
    response = requests.get(health_url)
    print("Health check response:", response.json())
except Exception as e:
    print("Error checking health:", str(e))