# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 (required for Cloud Run)
EXPOSE 8080

# Run the app with Gunicorn (better for production)
CMD ["python3", "linkedin_scraper_app.py"]
