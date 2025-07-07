# TMux-based Crypto Daily Report Scheduler

This guide explains how to use the new tmux-based scheduler instead of cron for running the crypto daily report automatically on a server.

## Why TMux Instead of Cron?

- **Persistent**: Continues running even if you disconnect from the server
- **Auto-restart**: Automatically restarts if the process crashes
- **Easy monitoring**: Can attach/detach to see what's happening
- **No system dependencies**: Doesn't require cron setup or root access
- **Better logging**: All output is captured in the tmux session

## Prerequisites

1. **Install tmux** (if not already installed):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tmux
   
   # CentOS/RHEL
   sudo yum install tmux
   
   # macOS
   brew install tmux
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure your settings** in `config.py` (Telegram bot token, etc.)

## Quick Start

### 1. Start the Scheduler
```bash
./start_tmux_scheduler.sh
```

This will:
- Check all prerequisites
- Create a tmux session named `crypto_scheduler`
- Start the daily scheduler inside the session
- Send a startup notification to Telegram

### 2. Check Status
```bash
./start_tmux_scheduler.sh status
```

### 3. Attach to Session (to see what's happening)
```bash
./start_tmux_scheduler.sh attach
```

To detach from the session: Press `Ctrl+B` then `D`

## Available Commands

| Command | Description |
|---------|-------------|
| `./start_tmux_scheduler.sh` | Start the scheduler |
| `./start_tmux_scheduler.sh attach` | Connect to running session |
| `./start_tmux_scheduler.sh stop` | Stop the scheduler |
| `./start_tmux_scheduler.sh restart` | Restart the scheduler |
| `./start_tmux_scheduler.sh status` | Check if it's running |
| `./start_tmux_scheduler.sh monitor` | Monitor and auto-restart |
| `./start_tmux_scheduler.sh help` | Show help |

## Advanced Usage

### Direct Python Commands
You can also use the Python script directly:

```bash
python3 tmux_scheduler.py start     # Start scheduler
python3 tmux_scheduler.py attach    # Attach to session
python3 tmux_scheduler.py stop      # Stop scheduler
python3 tmux_scheduler.py restart   # Restart scheduler
python3 tmux_scheduler.py status    # Check status
python3 tmux_scheduler.py monitor   # Monitor and auto-restart
```

### Manual TMux Commands
If you prefer to use tmux directly:

```bash
# List all tmux sessions
tmux list-sessions

# Attach to the crypto scheduler session
tmux attach-session -t crypto_scheduler

# Kill the session
tmux kill-session -t crypto_scheduler
```

## Monitoring and Auto-Restart

The scheduler includes a monitoring mode that will automatically restart the session if it goes down:

```bash
./start_tmux_scheduler.sh monitor
```

This will:
- Check the session status every 5 minutes
- Automatically restart if the session is down
- Send Telegram notifications when restarting
- Continue monitoring until you stop it (Ctrl+C)

## Logs and Debugging

### Log Files
- `tmux_scheduler.log` - TMux scheduler operations
- `daily_scheduler.log` - Daily scheduler operations
- `crypto_tracker.log` - Crypto data collection logs

### Viewing Logs
```bash
# View tmux scheduler logs
tail -f tmux_scheduler.log

# View daily scheduler logs
tail -f daily_scheduler.log

# View crypto tracker logs
tail -f crypto_tracker.log
```

### Attaching to Session for Debugging
```bash
./start_tmux_scheduler.sh attach
```

This will show you the live output of the scheduler, including any error messages.

## Server Deployment

### 1. Upload Files
Upload all the files to your server in the `Top Gainers & Losers` directory.

### 2. Install Dependencies
```bash
cd "Top Gainers & Losers"
pip3 install -r requirements.txt
```

### 3. Configure Settings
Edit `config.py` with your Telegram bot token and other settings.

### 4. Start the Scheduler
```bash
./start_tmux_scheduler.sh
```

### 5. Verify It's Running
```bash
./start_tmux_scheduler.sh status
```

### 6. Optional: Set Up Monitoring
For production servers, you might want to run the monitor in a separate tmux session:

```bash
# Create a monitoring session
tmux new-session -d -s crypto_monitor -c "$(pwd)"
tmux send-keys -t crypto_monitor 'python3 tmux_scheduler.py monitor' Enter
```

## Troubleshooting

### Session Won't Start
1. Check if tmux is installed: `which tmux`
2. Check Python dependencies: `python3 -c "import schedule, requests"`
3. Check config file exists: `ls config.py`
4. Check logs: `tail tmux_scheduler.log`

### Session Keeps Dying
1. Check the daily scheduler logs: `tail daily_scheduler.log`
2. Verify your Telegram bot token in `config.py`
3. Check network connectivity
4. Run the monitor to auto-restart: `./start_tmux_scheduler.sh monitor`

### Can't Attach to Session
1. Check if session exists: `tmux list-sessions`
2. If it doesn't exist, start it: `./start_tmux_scheduler.sh start`
3. If it exists but is empty, restart it: `./start_tmux_scheduler.sh restart`

### Telegram Notifications Not Working
1. Check your bot token in `config.py`
2. Verify the bot is active
3. Check if you've started a chat with the bot
4. Test with: `python3 test_telegram.py`

## Migration from Cron

If you were previously using cron, you can remove the cron job:

```bash
# View current cron jobs
crontab -l

# Remove all cron jobs (be careful!)
crontab -r

# Or edit cron jobs to remove the crypto scheduler
crontab -e
```

## Benefits Over Cron

| Feature | Cron | TMux |
|---------|------|------|
| Persistence | ❌ Stops on disconnect | ✅ Continues running |
| Auto-restart | ❌ Manual restart needed | ✅ Automatic restart |
| Easy monitoring | ❌ Hard to see output | ✅ Easy to attach/detach |
| Logging | ❌ Limited | ✅ Full output capture |
| Setup complexity | ❌ Requires root/cron | ✅ No special permissions |
| Debugging | ❌ Difficult | ✅ Easy to see live output |

## Security Notes

- The tmux session runs under your user account
- No root access required
- Session persists only while the server is running
- Consider using `screen` instead of `tmux` on some systems if tmux is not available

## Support

If you encounter issues:
1. Check the log files first
2. Try restarting the scheduler
3. Verify your configuration
4. Test the Telegram bot separately
5. Check server connectivity and dependencies 