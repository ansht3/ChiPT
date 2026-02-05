#!/bin/bash

# Script to start Q&A System services in separate tmux sessions
# To view the sessions:
# Ctrl-b then d to detach from a session
# tmux attach -t ai_service
# tmux attach -t cache_service
# tmux attach -t project_service

# Session names
SESSION_AI="ai_service"
SESSION_CACHE="cache_service"
SESSION_PROJECT="project_service"

# Directories (Absolute paths)
BASE_DIR="/.gavea/store/chipt/chipt_v2/ChiPT"
DIR_AI="$BASE_DIR/ai_service"
DIR_CACHE="$BASE_DIR/cache_service"
DIR_PROJECT="$BASE_DIR/project"

# Virtual Environment Path (Relative to each service directory)
VENV_PATH="chipt-venv/bin/activate"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "Error: tmux is not installed."
    exit 1
fi

echo "Starting Tmux sessions..."

# Start AI Service
tmux has-session -t $SESSION_AI 2>/dev/null
if [ $? != 0 ]; then
    tmux new-session -d -s $SESSION_AI -n "server"
    tmux send-keys -t $SESSION_AI "cd $DIR_AI" C-m
    tmux send-keys -t $SESSION_AI "source $VENV_PATH" C-m
    tmux send-keys -t $SESSION_AI "python main.py" C-m
    echo "Started $SESSION_AI"
else
    echo "Session $SESSION_AI already exists."
fi

# Start Cache Service
tmux has-session -t $SESSION_CACHE 2>/dev/null
if [ $? != 0 ]; then
    tmux new-session -d -s $SESSION_CACHE -n "server"
    tmux send-keys -t $SESSION_CACHE "cd $DIR_CACHE" C-m
    tmux send-keys -t $SESSION_CACHE "source $VENV_PATH" C-m
    tmux send-keys -t $SESSION_CACHE "python main.py" C-m
    echo "Started $SESSION_CACHE"
else
    echo "Session $SESSION_CACHE already exists."
fi

# Start Project Service (Main App)
tmux has-session -t $SESSION_PROJECT 2>/dev/null
if [ $? != 0 ]; then
    tmux new-session -d -s $SESSION_PROJECT -n "server"
    tmux send-keys -t $SESSION_PROJECT "cd $DIR_PROJECT" C-m
    tmux send-keys -t $SESSION_PROJECT "source $VENV_PATH" C-m
    tmux send-keys -t $SESSION_PROJECT "uvicorn main:app --host 0.0.0.0 --port 9189" C-m
    echo "Started $SESSION_PROJECT"
else
    echo "Session $SESSION_PROJECT already exists."
fi

echo ""
echo "All sessions started (if they didn't exist)."
echo "Use 'tmux attach -t <session_name>' to view a session."
echo "Sessions: $SESSION_AI, $SESSION_CACHE, $SESSION_PROJECT"
