#!/bin/bash

# Variables
REPO_DIR=/app            # Path to your app inside the container
BRANCH=main              # Git branch to monitor
APP_COMMAND="python app.py"  # Command to start the app

echo "Starting auto-update script..."

cd $REPO_DIR || exit 1

# Start the application for the first time
echo "Starting the application for the first time..."
$APP_COMMAND &  # Start the app in the background
APP_PID=$!      # Save the app's PID

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
        # Stop the current app process
        kill $APP_PID
        wait $APP_PID 2>/dev/null

        # Restart the application
        $APP_COMMAND &
        APP_PID=$!  # Update the app's PID
        echo "Application reloaded successfully."
    else
        echo "No updates found. Sleeping..."
    fi

    sleep 30  # Check for updates every 30 seconds
done
