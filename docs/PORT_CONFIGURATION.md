# Port Configuration Guide

## Overview

The ChiPT Q&A System uses **alternate ports** for its Milvus instance to avoid conflicts with existing Milvus installations.

## Port Mapping

### ChiPT Milvus Instance (via Docker Compose)

| Service | Host Port | Container Port | Standard Port | Purpose |
|---------|-----------|----------------|---------------|---------|
| Milvus gRPC | **19531** | 19530 | 19530 | Vector database access |
| Milvus Health | **9092** | 9091 | 9091 | Health check endpoint |
| MinIO API | **9002** | 9000 | 9000 | Object storage API |
| MinIO Console | **9003** | 9001 | 9001 | MinIO web interface |
| Etcd | 2379 | 2379 | 2379 | Metadata storage (internal) |

### Q&A System Services

| Service | Port | Notes |
|---------|------|-------|
| Main Q&A System | 8000 or 8909 | User-facing web application |
| AI Service | 8901 | Answer generation service |
| Cache Service | 8902 | Semantic search service |
| OpenAI API | 14345 | Custom OpenAI-compatible endpoint |

## Why Alternate Ports?

The alternate port configuration (19531 instead of 19530) allows you to:
- ✅ Run ChiPT's Milvus alongside your existing Milvus v2.6.1 instance
- ✅ Avoid port conflicts
- ✅ Keep separate data stores for different applications
- ✅ Test without affecting production Milvus

## Configuration Options

### Option 1: Use ChiPT's Separate Milvus Instance (Default)

The cache service is pre-configured to use port **19531**:

```python
# cache_service/main.py
MILVUS_HOST = "localhost"
MILVUS_PORT = "19531"  # ChiPT's Milvus instance
```

Start it with:
```bash
cd cache_service
docker-compose up -d
python main.py
```

### Option 2: Use Your Existing Milvus Instance

If you want to use your existing Milvus on port 19530, edit `cache_service/main.py`:

```python
# cache_service/main.py
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"  # Your existing Milvus
```

Then skip the docker-compose step:
```bash
cd cache_service
# Don't run docker-compose
python main.py  # Will connect to your existing Milvus
```

### Option 3: Custom Port Configuration

You can use any available port. Update both files:

**1. Update cache service:**
```python
# cache_service/main.py
MILVUS_HOST = "localhost"
MILVUS_PORT = "12345"  # Your custom port
```

**2. Update docker-compose:**
```yaml
# cache_service/docker-compose.yml
standalone:
  ports:
    - "12345:19530"  # Your custom port mapping
```

## Checking Port Availability

Before starting services, verify ports are available:

```bash
# Check if port 19531 is available
netstat -an | grep 19531

# Check if port 19530 is in use (your existing Milvus)
netstat -an | grep 19530

# Check all ChiPT ports
netstat -an | grep -E '19531|9092|9002|9003'
```

## Accessing Services

### Milvus (ChiPT Instance)
```bash
# Connect using pymilvus
from pymilvus import connections
connections.connect("default", host="localhost", port="19531")
```

### MinIO Console (ChiPT Instance)
- URL: http://localhost:9003
- Username: minioadmin
- Password: minioadmin

### MinIO API (ChiPT Instance)
- Endpoint: http://localhost:9002

## Troubleshooting

### Port Already in Use

```bash
# Find what's using a port
lsof -i :19531

# Or on Linux
netstat -tuln | grep 19531
```

### Can't Connect to Milvus

```bash
# Verify ChiPT Milvus is running
docker ps | grep chipt-milvus

# Check logs
cd cache_service
docker-compose logs -f chipt-milvus-standalone

# Verify port mapping
docker port chipt-milvus-standalone
# Should show: 19530/tcp -> 0.0.0.0:19531
```

### Wrong Port Configuration

If you get connection errors, verify:

1. **Cache service configuration:**
   ```bash
   grep MILVUS_PORT cache_service/main.py
   # Should show: MILVUS_PORT = "19531"
   ```

2. **Docker port mapping:**
   ```bash
   grep -A2 "ports:" cache_service/docker-compose.yml | grep 19531
   # Should show: - "19531:19530"
   ```

3. **Both should match:**
   - Cache service connects to: `localhost:19531`
   - Docker exposes: `19531` → container's `19530`

## Quick Reference

| Scenario | MILVUS_PORT in main.py | Docker Compose | Notes |
|----------|------------------------|----------------|-------|
| Separate ChiPT Milvus | 19531 | Use docker-compose | ✅ Default, recommended |
| Existing Milvus | 19530 | Skip docker-compose | Use your existing instance |
| Custom port | Your choice | Update port mapping | Advanced users |
