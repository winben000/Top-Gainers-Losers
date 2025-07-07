#!/bin/bash

# Setup cron job for Daily Crypto Report Scheduler
echo "Setting up cron job for Daily Crypto Report Scheduler..."

# Get the current directory
CURRENT_DIR=$(pwd)

# Create the cron job entry (runs daily at 7:00 AM)
CRON_JOB="0 7 * * * cd $CURRENT_DIR && python3 daily_scheduler.py >> daily_cron.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Daily cron job added successfully!"
echo "📅 Daily report will run at 7:00 AM every day"
echo "📝 Logs will be saved to daily_cron.log"
echo ""
echo "To view current cron jobs: crontab -l"
echo "To remove cron job: crontab -r"
echo "To edit cron jobs: crontab -e" 