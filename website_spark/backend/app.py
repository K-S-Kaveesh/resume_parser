from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import tempfile
import requests
from urllib.parse import urljoin
from pyngrok import ngrok
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from file_reader import read_file
from spark_engine import SparkTextProcessor

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Global Spark processor
processor = None
ngrok_tunnel = None
spark_ui_url = None

# Ngrok authentication (set this with your actual auth token)
ngrok.set_auth_token("34BoIGsnT0ul4IRC9WV8afzvJlF_6WRCnWp8V5rJnsheZP6Sr")

def initialize_spark():
    """Initialize Spark processor globally"""
    global processor, spark_ui_url
    if processor is None:
        processor = SparkTextProcessor()
        # Get Spark UI URL
        spark_ui_url = processor.spark.sparkContext.uiWebUrl
        print(f"Spark UI URL: {spark_ui_url}")  # Debug info
        
        # Ensure the URL is properly formatted
        if spark_ui_url:
            # Remove any trailing slashes
            spark_ui_url = spark_ui_url.rstrip('/')
            print(f"Formatted Spark UI URL: {spark_ui_url}")
    return processor

def start_ngrok():
    """Start ngrok tunnel for the application"""
    global ngrok_tunnel
    try:
        # Create ngrok tunnel for port 5000 (Flask app)
        ngrok_tunnel = ngrok.connect(5000)
        print(f"Ngrok tunnel started: {ngrok_tunnel.public_url}")
        return ngrok_tunnel
    except Exception as e:
        print(f"Failed to start ngrok tunnel: {e}")
        print("Ngrok integration disabled. To enable, sign up at https://dashboard.ngrok.com/signup and set your auth token.")
        return None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze resume and job description"""
    # Check if both files are present
    if 'resume' not in request.files or 'job' not in request.files:
        return jsonify({'error': 'Both resume and job description files are required'}), 400
    
    resume_file = request.files['resume']
    job_file = request.files['job']
    
    # Check if files are selected
    if resume_file.filename == '' or job_file.filename == '':
        return jsonify({'error': 'Please select both files'}), 400
    
    # Check if file types are allowed
    if not (allowed_file(resume_file.filename) and allowed_file(job_file.filename)):
        return jsonify({'error': 'Only PDF and DOCX files are allowed'}), 400
    
    try:
        # Read file contents
        resume_text = read_file(resume_file, resume_file.filename)
        job_text = read_file(job_file, job_file.filename)
        
        # Initialize Spark processor
        spark_processor = initialize_spark()
        
        # Process texts with Spark
        result = spark_processor.process_texts(resume_text, job_text)
        return jsonify(result)
            
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

@app.route('/spark-ui')
def spark_ui():
    """Endpoint to check if Spark UI is available"""
    try:
        # Initialize Spark if not already done
        initialize_spark()
        global spark_ui_url
        return jsonify({'status': 'Spark initialized', 'ui_available': True, 'spark_ui_url': spark_ui_url})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/spark-status')
def spark_status():
    """Endpoint to check Spark status"""
    global processor, spark_ui_url
    if processor is not None and spark_ui_url:
        return jsonify({'status': 'ready', 'spark_ui_url': spark_ui_url})
    else:
        return jsonify({'status': 'not_initialized'})

@app.route('/ngrok-url')
def get_ngrok_url():
    """Endpoint to get the ngrok URL"""
    global ngrok_tunnel
    if ngrok_tunnel:
        return jsonify({'ngrok_url': ngrok_tunnel.public_url})
    else:
        # Try to start ngrok if not already started
        tunnel = start_ngrok()
        if tunnel:
            return jsonify({'ngrok_url': tunnel.public_url})
        else:
            # Return local URL if ngrok is not available
            return jsonify({'ngrok_url': 'http://127.0.0.1:5000', 'message': 'Ngrok not available, using local URL'})

# Proxy endpoint for Spark UI
@app.route('/spark-ui-proxy/', defaults={'path': ''}, methods=['GET'])
@app.route('/spark-ui-proxy/<path:path>', methods=['GET'])
def spark_ui_proxy(path=''):
    """Proxy requests to Spark UI"""
    global spark_ui_url
    print(f"Spark UI Proxy called with path: '{path}'")  # Debug info
    
    if not spark_ui_url:
        # Try to initialize Spark to get the UI URL
        try:
            initialize_spark()
        except Exception as e:
            print(f"Failed to initialize Spark: {str(e)}")  # Debug info
            return jsonify({'error': 'Failed to initialize Spark: ' + str(e)}), 500
    
    if not spark_ui_url:
        print("Spark UI URL not available")  # Debug info
        return jsonify({'error': 'Spark UI URL not available'}), 500
    
    # Handle the case where path is empty (root request)
    if path == '':
        # Redirect to the Spark UI root
        spark_url = spark_ui_url
    else:
        # Construct the full Spark UI URL with the requested path
        base_url = spark_ui_url.rstrip('/')
        full_path = path.lstrip('/')
        spark_url = f"{base_url}/{full_path}"
    
    print(f"Proxying to Spark UI URL: {spark_url}")  # Debug info
    
    try:
        # Forward the request to Spark UI
        resp = requests.get(spark_url, stream=True, timeout=30)
        return resp.content, resp.status_code, dict(resp.headers)
    except Exception as e:
        print(f"Failed to connect to Spark UI: {str(e)}")  # Debug info
        return jsonify({'error': 'Failed to connect to Spark UI: ' + str(e)}), 500

# Serve frontend static files
@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Serve static files from frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    if os.path.exists(os.path.join(frontend_dir, path)):
        return send_from_directory(frontend_dir, path)
    # If file not found, return index.html for SPA routing
    return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':
    # Initialize Spark when the app starts
    initialize_spark()
    
    # Start ngrok tunnel (disabled for now due to conflict)
    # start_ngrok()
    
    app.run(host='127.0.0.1', port=5000, debug=True)