#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Print messages with colors
echo -e "Enter your Database"
read database


# Check if all fields are provided
if [ "$database" != "" ]; then
    # Run psql commands with sudo
    sudo -u postgres psql << EOF
    drop database $database;
EOF
    message="Database ${RED}$database${NC} removed successfully."
    echo -e "${GREEN}$message${NC}"
else
    errormessage="One or more fields are missing."
    echo -e "${YELLOW}$errormessage${NC}"
fi
