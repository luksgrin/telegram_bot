# Helper to wrap execution when running through slurm
# so that I get notified when it's over

# Load the environmental variables needed for this to work:
# - TELEGRAM_CHAT_ID
# - TELEGRAM_BOT_API_KEY
source .env

# Function to send a message to Telegram
send_telegram_message() {
    local message=$1
    curl -H 'Content-Type: application/json' \
         -d "{\"chat_id\":$TELEGRAM_CHAT_ID, \"text\":\"$message\"}" \
         -X POST \
         "https://api.telegram.org/bot$TELEGRAM_BOT_API_KEY/sendMessage" \
         > /dev/null 2>&1
}

# Function to execute a command and handle success/failure
run_with_notification() {
    # Trap signals for failure or job interruption
    trap handle_failure ERR TERM

    # Execute the command directly
    $@  # This runs the command with all passed arguments
    COMMAND_EXIT_CODE=$?  # Capture the exit code

    # Handle success/failure based on the exit code
    if [ $COMMAND_EXIT_CODE -eq 0 ]; then
        handle_success
    else
        handle_failure
    fi
}

# Function to handle job failure
handle_failure() {
    send_telegram_message "Your job in garnatxa has failed or was interrupted."
    exit 1
}

# Function to handle job success
handle_success() {
    send_telegram_message "Your job in garnatxa has completed successfully."
}

