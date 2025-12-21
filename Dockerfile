# -----------------------------------------
# Base image: lightweight Python
# -----------------------------------------
FROM python:3.10-slim

# -----------------------------------------
# Set working directory inside container
# -----------------------------------------
WORKDIR /app

# -----------------------------------------
# Copy dependency list and install packages
# -----------------------------------------
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------
# Copy application code & data
# -----------------------------------------
COPY app.py .
COPY data ./data

# -----------------------------------------
# Expose Streamlit default port
# -----------------------------------------
EXPOSE 8501

# -----------------------------------------
# Start Streamlit app
# -----------------------------------------
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]