FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose necessary ports
EXPOSE 5005 5055 8000

# Run entrypoint script
CMD ["entrypoint.sh"]
