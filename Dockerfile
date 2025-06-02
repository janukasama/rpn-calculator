# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Use start.sh as the entrypoint
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]