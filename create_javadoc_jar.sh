#!/bin/bash

# Script to download Processing Javadoc and create a JAR file
# This creates a proper javadoc JAR that VS Code can use

set -e

JAVADOC_URL="https://processing.github.io/processing4-javadocs"
TEMP_DIR="temp_javadoc"
OUTPUT_JAR="core-4.4.8-javadoc.jar"

echo "Creating temporary directory..."
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

echo "Downloading Processing Javadoc..."
echo "This may take a few minutes..."

# Download the entire javadoc site using wget
# -r: recursive
# -np: no parent (don't go up to parent directory)
# -k: convert links for local viewing
# -p: download all page requisites (images, css, etc)
# -nH: no host directory
# --cut-dirs=1: remove the first directory level
wget -r -np -k -p -nH --cut-dirs=1 \
     -e robots=off \
     --reject "index.html?*" \
     "$JAVADOC_URL/" || {
    echo "Error: wget failed. Trying with curl and a simpler approach..."
    echo "Please install wget: brew install wget"
    exit 1
}

echo "Creating JAR file..."
cd ..

# Create the JAR file with all the downloaded content
jar cf "$OUTPUT_JAR" -C "$TEMP_DIR" .

echo "Cleaning up..."
rm -rf "$TEMP_DIR"

echo "Done! Created $OUTPUT_JAR"
echo "File location: $(pwd)/$OUTPUT_JAR"
