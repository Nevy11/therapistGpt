#!/bin/bash

# URL to check for internet connection
URL="https://www.google.com"

# Function to check internet connection
check_connection() {
    ping -c 1 8.8.8.8 > /dev/null 2>&1
    return $?
}

download_tensorflow(){
    
    echo "Downloading Tensorflow"
    pip install tensorflow
}

pause_tensor_flow_download(){
    echo "pausing tensorflow..."
    
}

# Function to install packages with periodic pauses
install_with_check() {
    PACKAGE=$1
    echo "Starting installation of $PACKAGE with periodic connection checks..."

    # Loop to control the download and check connection
    while true; do
        # Run the pip install command with a timeout
        timeout 5s pip install "$PACKAGE" --no-cache-dir
        
        # Check if the previous command completed successfully
        if [ $? -eq 0 ]; then
            echo "$PACKAGE installed successfully."
            break
        fi
        
        # Check for internet connection after each timeout
        if check_connection; then
            echo "Internet is connected. Continuing $PACKAGE installation..."
        else
            echo "Internet disconnected. Waiting to resume $PACKAGE installation..."
            # Wait until the internet is reconnected
            until check_connection; do
                sleep 3
            done
        fi
    done
}

# Start the installation with periodic checks
install_with_check "tensorflow"
install_with_check "torch"
