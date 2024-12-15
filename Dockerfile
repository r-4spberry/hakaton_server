# Base image
FROM python:3.10

# Install dependencies
RUN apt-get update && apt-get install -y git && \
    apt-get clean

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add the auto-update script
COPY auto_update.sh /app/auto_update.sh
RUN chmod +x /app/auto_update.sh

# Start the app with the auto-update script
CMD ["/bin/bash", "/app/auto_update.sh"]
