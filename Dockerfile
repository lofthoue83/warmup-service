FROM python:3.11-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script
COPY warmup.py .

# Copy cron job file
COPY crontab /etc/cron.d/warmup-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/warmup-cron

# Apply cron job
RUN crontab /etc/cron.d/warmup-cron

# Create log file
RUN touch /var/log/cron.log

# Run the warmup once on startup, then start cron
CMD python /app/warmup.py && echo "Initial warmup completed. Starting cron..." && cron && tail -f /var/log/cron.log