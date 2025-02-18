
FROM python:3.9-slim AS base



# Set the working directory
WORKDIR /app
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install required Python dependencies
RUN pip install --no-cache-dir flask selenium webdriver-manager pyyaml werkzeug openai

# Copy application files
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
