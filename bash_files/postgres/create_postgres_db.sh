#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Print messages with colors
echo -e "Enter your username"
read username
echo -e "Enter your password"
read password
echo -e "Enter your database"
read database

# Check if all fields are provided
if [ "$username" != "" -a "$password" != "" -a "$database" != "" ]; then
    # Run psql commands with sudo
    sudo -u postgres psql << EOF
    create database $database;
    create user $username with encrypted password '$password';
    grant all privileges on database $database to $username;

    GRANT ALL ON ALL TABLES IN SCHEMA public to $username;
    GRANT ALL ON ALL SEQUENCES IN SCHEMA public to $username;
    GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to $username;
EOF
    message="Database ${RED}$database${NC} created successfully with user ${RED}$username${NC}, and password: ${RED}$password${NC}."
    echo -e "${GREEN}$message${NC}"
else
    errormessage="One or more fields are missing."
    echo -e "${YELLOW}$errormessage${NC}"
fi
