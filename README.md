# 📄 Distributed Resume Parser & Job Match Engine

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.4.1-E25A1C?style=flat&logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end NLP and distributed text matching pipeline that ingests unstructured resumes and job specifications, performs distributed tokenization and TF-IDF feature weighting using **Apache Spark MLlib**, and delivers deterministic match analytics via a lightweight **Flask REST API**.

---

## 🎥 Live Demonstration & Video Walkthrough

### 📺 Watch Full Walkthrough on YouTube
[![Watch Resume Parser Demo](https://img.youtube.com/vi/l0cNkLBdFlo/maxresdefault.jpg)](https://www.youtube.com/watch?v=l0cNkLBdFlo)

> 👆 **Click the image banner above** to watch the full project walkthrough on YouTube.  
> 📹 You can also inspect or download the local demonstration clip directly from this repository: [`full_spark_video.mp4`](full_spark_video.mp4).

---

## ⚡ System Pipeline & Architecture

```text
[ Candidate Resume (PDF/DOCX) ] ──┐
                                  ├──> [ File Readers (PyPDF2 / docx) ]
[ Job Description (PDF/DOCX)  ] ──┘                 │
                                                    ▼
                                       [ Apache Spark Processing Engine ]
                                       ├── Text Normalization & Cleaning
                                       ├── Tokenization & Stop-word Filtering
                                       ├── TF-IDF Vector Space Model
                                       └── Cosine Similarity & Skill Extraction
                                                    │
                                                    ▼
                                          [ Flask REST Service Layer ]
                                                    │
                                                    ▼
                                       [ Interactive Web Interface ]
                                 (Match %, Skill Breakdown & Spark Web UI)
