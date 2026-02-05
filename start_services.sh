#!/bin/bash

# Startup script for Q&A System
# Starts all three services in separate terminal windows

echo "=========================================="
echo "Q&A System - Service Startup"
echo "=========================================="
echo ""

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker first."
    exit 1
fi

# Start Milvus
echo "1. Starting Milvus (Vector Database)..."
cd cache_service
if [ ! -f "docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found in cache_service/"
    exit 1
fi

docker compose up -d
echo "   Waiting for Milvus to be ready..."
sleep 10

# Check Milvus health
if docker ps | grep -q "milvus-standalone.*healthy"; then
    echo "   ✓ Milvus is running"
else
    echo "   ⚠ Milvus may not be fully ready yet. Check with: docker-compose logs"
fi

cd ..
echo ""

# Instructions for starting other services
echo "2. Start Cache Service (Terminal 1):"
echo "   cd cache_service && python main.py"
echo ""

echo "3. Start AI Service (Terminal 2):"
echo "   cd ai_service && python main.py"
echo ""

echo "4. Start Main Q&A System (Terminal 3):"
echo "   cd project && uvicorn main:app --reload --host 0.0.0.0 --port 10000"
echo ""

echo "=========================================="
echo "Service Ports:"
echo "  - Main Q&A:      http://localhost:8000"
echo "  - AI Service:    http://localhost:8901"
echo "  - Cache Service: http://localhost:8902"
echo "  - Milvus:        localhost:19530"
echo "=========================================="
echo ""
echo "To stop Milvus: cd cache_service && docker compose down"
echo ""

