# Port Conflict Troubleshooting

## Error: "address already in use"

If you see this error:
```
ERROR: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8901): address already in use
```

## Solution 1: Find and Stop the Process Using the Port

### Check what's using the port:

```bash
# On Linux
lsof -i :8901

# Or
netstat -tuln | grep 8901

# Or
ss -tuln | grep 8901
```

### Kill the process:

```bash
# Find the PID (Process ID)
lsof -i :8901
# Shows something like: python 12345 user ...

# Kill it
kill 12345

# Or force kill if needed
kill -9 12345
```

### Or use fuser:

```bash
# Find and kill in one command
fuser -k 8901/tcp
```

## Solution 2: Use a Different Port

Both services now support custom ports via command-line argument:

### AI Service (default: 8901)

```bash
# Use default port 8901
python main.py

# Use custom port
python main.py 8911
```

### Cache Service (default: 8902)

```bash
# Use default port 8902
python main.py

# Use custom port
python main.py 8912
```

### Update Main Q&A System

If you change the service ports, update the main Q&A system's configuration:

**Edit `project/services.py`:**

```python
# Change these URLs to match your custom ports
CACHE_API_URL = "http://localhost:8912/search"  # Changed from 8902
AI_API_URL = "http://localhost:8911/generate"   # Changed from 8901
```

## Solution 3: Check for Duplicate Processes

You might have accidentally started the service twice:

```bash
# Check for running Python processes
ps aux | grep python

# Kill all Python processes (careful!)
pkill python

# Or be more specific
ps aux | grep "main.py" | grep -v grep
```

## Common Port Conflicts

| Service | Default Port | Alternative Port | Check Command |
|---------|--------------|------------------|---------------|
| AI Service | 8901 | 8911 | `lsof -i :8901` |
| Cache Service | 8902 | 8912 | `lsof -i :8902` |
| Main Q&A | 8000/8909 | 8000/8909 | `lsof -i :8000` |
| Milvus (ChiPT) | 19531 | - | `lsof -i :19531` |

## Quick Check All Ports

```bash
# Check all service ports at once
for port in 8901 8902 8000 8909 19531; do
    echo "Port $port:"
    lsof -i :$port 2>/dev/null || echo "  Available"
done
```

## Recommended Port Setup

If you have port conflicts, use these alternate ports:

```bash
# Terminal 1: Cache Service
cd cache_service
python main.py 8912

# Terminal 2: AI Service  
cd ai_service
python main.py 8911

# Terminal 3: Main Q&A
cd project
# Edit services.py to use ports 8912 and 8911
uvicorn main:app --reload --port 8000
```

Then update `project/services.py`:
```python
CACHE_API_URL = "http://localhost:8912/search"
AI_API_URL = "http://localhost:8911/generate"
```

## Prevention

To avoid port conflicts in the future:

1. **Always check before starting:**
   ```bash
   lsof -i :8901 && echo "Port in use!" || python main.py
   ```

2. **Use screen/tmux for persistent sessions:**
   ```bash
   screen -S ai_service
   python main.py
   # Ctrl+A, D to detach
   ```

3. **Create a startup script:**
   ```bash
   #!/bin/bash
   # Check and kill old processes
   fuser -k 8901/tcp 2>/dev/null
   fuser -k 8902/tcp 2>/dev/null
   
   # Start services
   cd ai_service && python main.py &
   cd cache_service && python main.py &
   ```

## Docker Alternative

If port management becomes too complex, consider containerizing the services:

```dockerfile
# ai_service/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD ["python", "main.py"]
```

Then use docker-compose to manage ports easily.
