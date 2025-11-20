#!/bin/bash

# ==========================================
# SETUP & CONFIGURATION
# ==========================================

# 1. Check for arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <TOTAL_ITEMS> <SESSIONS>"
    echo "Example: $0 20000 4"
    exit 1
fi

TOTAL_ITEMS=$1
SESSIONS=$2
REPO_URL="https://github.com/Chanveasna-ENG/synthetic-data-generation-for-computer-vision.git"
DIR_NAME="synthetic-data-generation-for-computer-vision"
VENV_NAME="bot"

# Ensure we are running as root for apt installs
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root (sudo)"
  exit
fi

echo "--- 🚀 Starting Setup ---"

# 2. Install System Dependencies
echo "--- 📦 Installing System Dependencies ---"
apt-get update -qq
# Installing python3-venv (standard name on Debian/Ubuntu) and tmux
apt-get install -y python3-venv python3-pip git tmux

# 3. Clone Repository
if [ ! -d "$DIR_NAME" ]; then
    echo "--- ⬇️ Cloning Repository ---"
    git clone "$REPO_URL"
else
    echo "--- 📂 Repository already exists, skipping clone ---"
fi

# Enter the directory
cd "$DIR_NAME"

# 4. Setup Python Environment
if [ ! -d "$VENV_NAME" ]; then
    echo "--- 🐍 Creating Virtual Environment ($VENV_NAME) ---"
    python3 -m venv "$VENV_NAME"
fi

echo "--- 🔌 Activating Environment & Installing Requirements ---"
source "$VENV_NAME/bin/activate"
pip install -r requirements.txt

# ==========================================
# CALCULATION & EXECUTION
# ==========================================

echo "--- 🧮 Calculating Batches ---"

# Integer division for batch size
BATCH_SIZE=$(( TOTAL_ITEMS / SESSIONS ))
REMAINDER=$(( TOTAL_ITEMS % SESSIONS ))

echo "Total Items: $TOTAL_ITEMS"
echo "Sessions:    $SESSIONS"
echo "Batch Size:  $BATCH_SIZE"

# Loop to create tmux sessions
for (( i=0; i<SESSIONS; i++ )); do
    
    # Calculate Start
    START=$(( i * BATCH_SIZE ))
    
    # Calculate End
    # If it's the last session, add the remainder to ensure we reach the exact total
    if [ $((i + 1)) -eq $SESSIONS ]; then
        END=$(( START + BATCH_SIZE + REMAINDER ))
    else
        END=$(( START + BATCH_SIZE ))
    fi

    SESSION_ID="worker_$i"
    
    # 1. Kill existing session with same name (cleanup)
    tmux kill-session -t "$SESSION_ID" 2>/dev/null || true

    # 2. Create new detached tmux session
    tmux new-session -d -s "$SESSION_ID"

    # 3. Send commands to the tmux session
    # Command A: Activate the virtual environment
    # We use $(pwd) to ensure absolute path inside tmux
    tmux send-keys -t "$SESSION_ID" "cd $(pwd)" C-m
    tmux send-keys -t "$SESSION_ID" "source $VENV_NAME/bin/activate" C-m
    
    # Command B: Run the python script
    CMD="python3 main.py $START $END 1"
    tmux send-keys -t "$SESSION_ID" "$CMD" C-m

    echo "✅ Started Tmux Session: $SESSION_ID | Range: $START -> $END"

done

echo "--- 🎉 All sessions started! ---"
echo "Type 'tmux list-sessions' to view them."
echo "Type 'tmux attach -t worker_0' to view the first worker."
