# ACME HR Attrition Analytics

A data-driven HR analytics application designed to identify, explain, and visualize
drivers of voluntary employee attrition using Python, Streamlit, and Docker.

---

## Project Overview

ACME Corp is experiencing elevated voluntary attrition, particularly among younger
and mid-level employees. This application helps HR and leadership teams:

- Identify key attrition drivers
- Understand feature interactions
- Explore attrition risk patterns visually
- Review executive-ready insights and recommendations

---

## Project Structure

hr-attrition-app/

    App.py                         # Streamlit application
    requirements.txt               # Python dependencies
    Dockerfile                     # Docker configuration
    README.md                      # Project documentation

    data/
    employee_attrition.csv
    ttrition_scored.csv
    attrition_pairwise_patterns.csv

    01_attrition_pattern_discovery.ipynb
    venv/                          # Local virtual environment (not used in Docker)


## Local Development Setup (Virtual Environment)

### Prerequisites
- min Python 3.9 or 3.10
- pip

### Create and activate virtual environment

Mac / Linux:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

### Run Streamlit app locally
streamlit run app.py

Automatically should open default browser and run. If not Open in browser:
http://localhost:8501

---

## Docker Setup (Recommended for Demo / Production)

### Install Docker

Mac:
Download Docker Desktop from https://www.docker.com/products/docker-desktop

Windows:
Install Docker Desktop for Windows and enable WSL 2

Verify installation:
docker --version

---

### Build Docker Image

Navigate to project directory:
cd hr-attrition-app

Build image:
docker build -t acme-attrition-app .

---

### Run Docker Container

docker run -p 8501:8501 acme-attrition-app

Open browser:
http://localhost:8501

---

## Application Features

### Tab 1 – Attrition Driver Explorer
- Select any HR feature (Job Satisfaction, Overtime, Distance, etc.)
- View attrition rate distribution
- See top-risk feature combinations

### Tab 2 – Heatmap Laboratory
- Select any two features
- Explore pairwise attrition interactions via heatmaps

### Tab 3 – Executive Summary
- Top attrition drivers
- High-risk employee profiles
- Actionable recommendations for ACME

---

## What ACME Can Take Steps to Reduce Attrition

- Improve work-life balance and reduce overtime exposure
- Address role stagnation through internal mobility programs
- Strengthen managerial effectiveness
- Offer commute flexibility and compensation reviews

---

## Tech Stack

- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Streamlit
- Docker

---

## Notes

- Docker runs independently of local virtual environments
- The venv directory is ignored during Docker build
- Relative paths ensure compatibility across local and Docker runs

---

## Author
Shekhar S.
shekhar.sj07@gmail.com
