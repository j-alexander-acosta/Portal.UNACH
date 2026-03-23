FROM python:3.11-slim

WORKDIR /app

# Install dependencies before code to leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose internal web port
EXPOSE 5000

# Start command
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
