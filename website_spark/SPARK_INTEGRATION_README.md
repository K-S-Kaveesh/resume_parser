# Spark Web UI Integration Guide

## What Was Implemented

This integration connects the frontend with the backend and enables the Spark Web UI button to display the working of the Spark web UI when clicked.

## Changes Made

### Backend Changes (app.py)

1. Added a global variable `spark_ui_url` to store the Spark UI URL
2. Modified the `initialize_spark()` function to capture the Spark UI URL when initializing the Spark session
3. Updated the `/spark-ui` endpoint to return the actual Spark UI URL

### Frontend Changes (result.html)

1. Added a new function `getSparkUiUrl()` to fetch the Spark UI URL from the backend
2. Modified the `connectToNgrok()` function to fetch both the ngrok URL and Spark UI URL simultaneously
3. Updated the button click handler to open the Spark UI in a new tab when clicked

## How to Test the Integration

1. Start the backend server:
   ```
   cd backend
   python app.py
   ```

2. Start the frontend server:
   ```
   cd frontend
   python -m http.server 8000
   ```

3. Open your browser and navigate to http://localhost:8000

4. Upload a resume and job description file

5. On the results page, click the "Connect & Open Spark UI" button

6. The first click will connect to the backend and fetch the URLs

7. The second click will open the Spark Web UI in a new tab

## Spark UI Access

The Spark Web UI should be accessible at a URL similar to:
http://LAPTOP-PS68ODPE:4041

This URL is dynamically fetched from the Spark session and may vary depending on your system.