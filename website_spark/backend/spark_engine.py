from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, ArrayType
import re

# Define cleaning function outside of class to avoid serialization issues
def clean_text(text):
    """Clean text by removing special characters and converting to lowercase"""
    if text is None:
        return ""
    # Remove special characters and digits
    cleaned = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    cleaned = cleaned.lower()
    # Remove extra whitespaces
    cleaned = ' '.join(cleaned.split())
    return cleaned

# Define skills extraction function outside of class
def extract_skills(text):
    """Extract skills from text using keyword matching"""
    if text is None:
        return []
    
    # Common technical skills keywords (this is a simplified list)
    skills_keywords = [
        'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css', 'react', 'angular', 
        'vue', 'node', 'express', 'django', 'flask', 'spring', 'hibernate', 'mongodb', 
        'postgresql', 'mysql', 'oracle', 'aws', 'azure', 'docker', 'kubernetes', 
        'jenkins', 'git', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'matplotlib', 
        'scikit-learn', 'opencv', 'nlp', 'machine learning', 'deep learning', 
        'data science', 'artificial intelligence', 'ai', 'ml', 'devops', 'ci/cd', 
        'agile', 'scrum', 'jira', 'linux', 'unix', 'bash', 'shell', 'api', 'rest', 
        'graphql', 'microservices', 'cloud', 'serverless', 'lambda', 'ec2', 's3', 
        'rds', 'redshift', 'snowflake', 'tableau', 'power bi', 'excel', 'spark', 
        'hadoop', 'kafka', 'rabbitmq', 'redis', 'elasticsearch', 'solr', 'nginx', 
        'apache', 'tomcat', 'jenkins', 'ansible', 'terraform', 'puppet', 'chef'
    ]
    
    # Normalize text for comparison
    normalized_text = text.lower()
    found_skills = []
    
    for skill in skills_keywords:
        if skill in normalized_text:
            found_skills.append(skill.title())
            
    return list(set(found_skills))  # Remove duplicates

class SparkTextProcessor:
    def __init__(self):
        """Initialize Spark session"""
        self.spark = SparkSession.builder \
            .appName("ResumeParser") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.ui.enabled", "true") \
            .config("spark.ui.port", "4040") \
            .getOrCreate()
        
        # Define UDFs for text cleaning
        self.clean_text_udf = udf(clean_text, StringType())
        self.extract_skills_udf = udf(extract_skills, ArrayType(StringType()))
    
    def process_texts(self, resume_text, job_description_text):
        """Process texts using Spark ML pipeline"""
        try:
            # Create DataFrame with texts
            data = [(1, resume_text), (2, job_description_text)]
            df = self.spark.createDataFrame(data, ["id", "text"])
            
            # Clean text
            df_cleaned = df.withColumn("cleaned_text", self.clean_text_udf(col("text")))
            
            # Tokenize
            tokenizer = Tokenizer(inputCol="cleaned_text", outputCol="words")
            df_tokenized = tokenizer.transform(df_cleaned)
            
            # Remove stop words
            remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
            df_filtered = remover.transform(df_tokenized)
            
            # Apply HashingTF
            hashing_tf = HashingTF(inputCol="filtered_words", outputCol="raw_features", numFeatures=10000)
            df_featurized = hashing_tf.transform(df_filtered)
            
            # Apply IDF
            idf = IDF(inputCol="raw_features", outputCol="features")
            idf_model = idf.fit(df_featurized)
            df_tfidf = idf_model.transform(df_featurized)
            
            # Persist DataFrame to ensure it shows in Storage tab
            df_tfidf.persist()
                    
            # Collect results
            result_rows = df_tfidf.collect()
                    
            # Count rows to trigger computation and storage
            row_count = df_tfidf.count()
            
            # Extract skills from original texts using the standalone function
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_description_text)
            
            # Calculate matching skills
            matching_skills = list(set(resume_skills) & set(job_skills))
            
            # Calculate missing skills
            missing_skills = list(set(job_skills) - set(resume_skills))
            
            # Calculate similarity score (simplified approach)
            # In a production environment, you would use the TF-IDF vectors to calculate cosine similarity
            # For this demo, we'll use a simple ratio
            total_job_skills = len(job_skills)
            matching_skills_count = len(matching_skills)
            
            if total_job_skills > 0:
                score = int((matching_skills_count / total_job_skills) * 100)
            else:
                score = 0
            
            return {
                "score": score,
                "resume_skills": resume_skills,
                "job_skills": job_skills,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills,
                "summary": "This AI-powered system analyzes your resume and compares it with the job description to highlight your strengths, identify missing skills, and estimate your overall job compatibility."
            }
        except Exception as e:
            # If Spark processing fails, fall back to a simpler approach
            return self._fallback_processing(resume_text, job_description_text)
    
    def _fallback_processing(self, resume_text, job_description_text):
        """Fallback processing if Spark fails"""
        # Extract skills from original texts
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description_text)
        
        # Calculate matching skills
        matching_skills = list(set(resume_skills) & set(job_skills))
        
        # Calculate missing skills
        missing_skills = list(set(job_skills) - set(resume_skills))
        
        # Calculate similarity score
        total_job_skills = len(job_skills)
        matching_skills_count = len(matching_skills)
        
        if total_job_skills > 0:
            score = int((matching_skills_count / total_job_skills) * 100)
        else:
            score = 0
        
        return {
            "score": score,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "summary": "This AI-powered system analyzes your resume and compares it with the job description to highlight your strengths, identify missing skills, and estimate your overall job compatibility."
        }
    
    def stop_spark(self):
        """Stop Spark session"""
        self.spark.stop()