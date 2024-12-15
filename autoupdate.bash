#!/bin/bash

# Variables
REPO_DIR=/app  # Path to your app inside the container
BRANCH=main    # Git branch to monitor

echo "Starting auto-update script..."

cd $REPO_DIR || exit 1

# Infinite loop to check for updates
while true; do
    echo "Checking for updates..."

    # Fetch the latest changes
    git fetch origin $BRANCH

    # Compare local and remote branches
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/$BRANCH)

    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "Updates detected! Pulling changes..."
        git pull origin $BRANCH

        echo "Reloading the application..."
        # Gracefully restart the app (adjust command as needed)
        pkill -f "python app.py"  # Stop the app
        python app.py &           # Restart the app
    else
        echo "No updates found. Sleeping..."
    fi

    sleep 30  # Check for updates every 30 seconds
done
