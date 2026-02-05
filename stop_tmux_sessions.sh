#!/bin/bash

# Script to stop Q&A System services tmux sessions

# Session names
SESSION_AI="ai_service"
SESSION_CACHE="cache_service"
SESSION_PROJECT="project_service"

echo "Stopping Tmux sessions..."

# Stop AI Service
tmux has-session -t $SESSION_AI 2>/dev/null
if [ $? == 0 ]; then
    tmux kill-session -t $SESSION_AI
    echo "Stopped $SESSION_AI"
else
    echo "Session $SESSION_AI not found."
fi

# Stop Cache Service
tmux has-session -t $SESSION_CACHE 2>/dev/null
if [ $? == 0 ]; then
    tmux kill-session -t $SESSION_CACHE
    echo "Stopped $SESSION_CACHE"
else
    echo "Session $SESSION_CACHE not found."
fi

# Stop Project Service
tmux has-session -t $SESSION_PROJECT 2>/dev/null
if [ $? == 0 ]; then
    tmux kill-session -t $SESSION_PROJECT
    echo "Stopped $SESSION_PROJECT"
else
    echo "Session $SESSION_PROJECT not found."
fi

echo ""
echo "All listed sessions stopped."
