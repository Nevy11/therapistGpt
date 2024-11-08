#!/bin/bash

# URL to check for internet connection
URL="https://www.google.com"

# Function to check internet connection
check_connection() {
    ping -c 1 8.8.8.8 > /dev/null 2>&1
    return $?
}

# Function to install packages with periodic pauses
install_with_pause_resume() {
    PACKAGE=$1
    echo "Starting installation of $PACKAGE with periodic pauses..."

    # Start the pip install command as a background job
    pip install "$PACKAGE" --no-cache-dir &
    JOB_ID=$!

    # Loop to control the pause and resume of the download
    while kill -0 $JOB_ID 2>/dev/null; do
        # Allow the job to run for 5 seconds
        sleep 5
        echo "Pausing $PACKAGE installation to check connection..."

        # Pause the job
        kill -STOP $JOB_ID

        # Check for internet connection
        if check_connection; then
            echo "Internet is connected. Resuming $PACKAGE installation..."
            # Resume the job
            kill -CONT $JOB_ID
        else
            echo "Internet disconnected. Waiting to resume $PACKAGE installation..."
            # Wait until the internet is reconnected
            until check_connection; do
                sleep 3
            done
            echo "Internet reconnected. Resuming $PACKAGE installation..."
            kill -CONT $JOB_ID
        fi
    done

    # Wait for the job to complete
    wait $JOB_ID
    echo "$PACKAGE installation completed."
}

# Start the installation with periodic pauses and connection checks
install_with_pause_resume "tensorflow"
install_with_pause_resume "torch"
