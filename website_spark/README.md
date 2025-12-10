# Resume Parser & Job Match Application

This is a Flask-based web application that parses resumes and job descriptions, extracts skills, and calculates a match percentage between them using Apache Spark for text processing.

## Project Structure

```
website_spark/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── spark_engine.py     # Spark text processing engine
│   └── file_reader.py      # File reading utilities
├── frontend/
│   ├── index.html          # Upload page
│   ├── result.html         # Results display page
│   └── loading.html        # Loading page
└── requirements.txt        # Python dependencies
```

## Prerequisites

1. Python 3.8 or higher
2. Java 8 or higher (required for PySpark)
3. pip (Python package installer)

## Installation

1. Clone or download this repository

2. Navigate to the project directory:
   ```
   cd website_spark
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask backend server:
   ```
   cd backend
   python app.py
   ```

2. The backend server will start on `http://127.0.0.1:5000` and automatically serve the frontend files

3. Open your browser and go to `http://localhost:5000` to access the application

4. To access the Spark UI (for monitoring Spark jobs), click the "Open Spark UI" button on the results page

## How It Works

1. Users upload a resume (PDF or DOCX) and a job description (PDF or DOCX)
2. The Flask backend receives the files and extracts text content
3. Apache Spark processes the text:
   - Cleans and normalizes text
   - Tokenizes words
   - Removes stop words
   - Applies TF-IDF transformation
   - Extracts skills using keyword matching
   - Calculates match percentage
4. Results are sent back to the frontend and displayed

## API Endpoints

- `POST /analyze` - Analyze resume and job description files
- `GET /health` - Health check endpoint
- `GET /spark-ui` - Check Spark UI availability
- `GET /spark-ui-proxy/*` - Proxy requests to Spark UI
- `GET /ngrok-url` - Get ngrok URL (for remote access)

## Features

- PDF and DOCX file support
- Text cleaning and normalization
- Stop word removal
- TF-IDF vectorization
- Skill extraction
- Match percentage calculation
- Responsive and attractive UI

## Technologies Used

- **Backend**: Flask, PySpark, PyPDF2, python-docx
- **Frontend**: HTML, CSS, JavaScript
- **Text Processing**: Apache Spark MLlib