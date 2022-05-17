#!/usr/bin/env bash
# requires: Nodejs/NPM, PowerShell
# Permission to run PS scripts (for this session only):
# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# exit if cmdlet gives error
$ErrorActionPreference = "Stop"

# Check to see if root CA file exists, download if not
If (!(Test-Path ".\root-CA.crt")) {
    "`nDownloading AWS IoT Root CA certificate from AWS..."
    Invoke-WebRequest -Uri https://www.amazontrust.com/repository/AmazonRootCA1.pem -OutFile root-CA.crt
}

# install AWS Device SDK for NodeJS if not already installed
node -e "require('aws-iot-device-sdk')"
If (!($?)) {
    "`nInstalling AWS SDK..."
    npm install aws-iot-device-sdk
}

"`nRunning pub/sub sample application..."
node .\fighter.js --host-name a3fnw75gmb7w4v-ats.iot.us-west-2.amazonaws.com --private-key .\fighter.private.key --client-certificate .\fighter.cert.pem --ca-certificate .\root-CA.crt --client-id=sdk-nodejs-e2bf114c-43e1-4ef1-9d56-caa89094006b
