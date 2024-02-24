FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the files
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the app
CMD ["gunicorn","-k", "uvicorn.workers.UvicornWorker","app:app", "--bind", "0.0.0.0:8000", "--workers=4"]
