FROM python:3.11-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install flask werkzeug

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]