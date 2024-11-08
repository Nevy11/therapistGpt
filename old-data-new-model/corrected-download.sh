#!/bin/bash

# URL to check for internet connection
URL="https://www.google.com"

# Main command to run
MAIN_SCRIPT="./mhd.sh"

# Function to check internet connection
check_connection() {
    # Use nc (netcat) to check if the port 443 (HTTPS) on google.com is reachable
    nc -zw1 google.com 443 > /dev/null 2>&1
    return $? # Returns 0 if connected, non-zero otherwise
}

echo "Checking internet connection..."

# Infinite loop to monitor internet and run the script
while true; do
    if check_connection; then
        echo "Internet is connected. Running script..."
        
        # Run the main script
        $MAIN_SCRIPT
        
        # Exit the loop if the script runs successfully
        if [ $? -eq 0 ]; then
            echo "Script completed successfully."
            break
        fi
    else
        echo "Internet disconnected. Retrying in 5 seconds..."
    fi

    # Wait for a few seconds before checking connection again
    sleep 5
done
