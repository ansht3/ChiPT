#!/bin/bash
# Setup script to verify and create necessary directories

echo "Setting up Q&A System..."

# Check if we're in the project directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the project directory."
    exit 1
fi

# Create templates directory if it doesn't exist
if [ ! -d "templates" ]; then
    echo "Creating templates directory..."
    mkdir -p templates
fi

# Create static directory if it doesn't exist
if [ ! -d "static" ]; then
    echo "Creating static directory..."
    mkdir -p static
fi

# Check for required files
echo ""
echo "Checking for required files..."
MISSING=0

if [ ! -f "templates/index.html" ]; then
    echo "✗ templates/index.html is missing"
    MISSING=1
else
    echo "✓ templates/index.html"
fi

if [ ! -f "static/app.js" ]; then
    echo "✗ static/app.js is missing"
    MISSING=1
else
    echo "✓ static/app.js"
fi

FILES=("main.py" "database.py" "auth.py" "schemas.py" "services.py" "requirements.txt")
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "✗ $file is missing"
        MISSING=1
    else
        echo "✓ $file"
    fi
done

echo ""
if [ $MISSING -eq 1 ]; then
    echo "Some files are missing. Please copy all files from the project directory."
    exit 1
fi

echo "All files present!"
echo ""
echo "Directory structure:"
find . -type f -not -path '*/\.*' -not -name '*.db' | sort

echo ""
echo "Ready to run! Use: uvicorn main:app --reload --port 8000"
