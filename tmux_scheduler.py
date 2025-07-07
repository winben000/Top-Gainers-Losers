#!/usr/bin/env python3
"""
TMux-based Crypto Daily Report Scheduler
Runs the crypto tracker in a tmux session for persistent operation on servers
"""

import subprocess
import sys
import os
import time
import signal
import logging
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from top50gainers_losers import send_telegram_message
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tmux_scheduler.log'),
        logging.StreamHandler()
    ]
)

class TmuxScheduler:
    def __init__(self, session_name="crypto_scheduler"):
        self.session_name = session_name
        self.script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_scheduler.py")
        
    def send_telegram_notification(self, message):
        """Send notification to Telegram"""
        try:
            asyncio.run(send_telegram_message(message))
            logging.info("Telegram notification sent")
        except Exception as e:
            logging.error(f"Failed to send Telegram notification: {e}")
    
    def tmux_command(self, command):
        """Execute tmux command and return result"""
        try:
            result = subprocess.run(
                f"tmux {command}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logging.error("Tmux command timed out")
            return False, "", "Command timed out"
        except Exception as e:
            logging.error(f"Tmux command failed: {e}")
            return False, "", str(e)
    
    def session_exists(self):
        """Check if tmux session exists"""
        success, stdout, stderr = self.tmux_command(f"has-session -t {self.session_name}")
        return success
    
    def create_session(self):
        """Create new tmux session"""
        logging.info(f"Creating tmux session: {self.session_name}")
        
        # Create session and run the scheduler
        command = f"new-session -d -s {self.session_name} -c {os.getcwd()}"
        success, stdout, stderr = self.tmux_command(command)
        
        if not success:
            logging.error(f"Failed to create tmux session: {stderr}")
            return False
        
        # Send the startup command to the session
        startup_cmd = f"send-keys -t {self.session_name} 'python3 {self.script_path}' Enter"
        success, stdout, stderr = self.tmux_command(startup_cmd)
        
        if not success:
            logging.error(f"Failed to start scheduler in tmux: {stderr}")
            return False
        
        logging.info("Tmux session created and scheduler started")
        return True
    
    def attach_session(self):
        """Attach to existing tmux session"""
        logging.info(f"Attaching to tmux session: {self.session_name}")
        os.system(f"tmux attach-session -t {self.session_name}")
    
    def kill_session(self):
        """Kill tmux session"""
        logging.info(f"Killing tmux session: {self.session_name}")
        success, stdout, stderr = self.tmux_command(f"kill-session -t {self.session_name}")
        
        if success:
            logging.info("Tmux session killed successfully")
            self.send_telegram_notification(
                f"🛑 <b>Crypto Scheduler Stopped</b>\n\n"
                f"📅 Stopped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"⚠️ Daily reports will no longer be sent automatically"
            )
        else:
            logging.error(f"Failed to kill tmux session: {stderr}")
        
        return success
    
    def restart_session(self):
        """Restart tmux session"""
        logging.info("Restarting tmux session")
        self.kill_session()
        time.sleep(2)
        return self.create_session()
    
    def get_session_status(self):
        """Get status of tmux session"""
        if not self.session_exists():
            return "not_running"
        
        # Check if the session has any panes
        success, stdout, stderr = self.tmux_command(f"list-panes -t {self.session_name}")
        if not success or not stdout.strip():
            return "empty"
        
        return "running"
    
    def monitor_session(self):
        """Monitor the tmux session and restart if needed"""
        logging.info("Starting session monitor...")
        
        while True:
            try:
                status = self.get_session_status()
                
                if status == "not_running":
                    logging.warning("Session not running, creating new session...")
                    self.send_telegram_notification(
                        f"⚠️ <b>Crypto Scheduler Restart</b>\n\n"
                        f"📅 Session was down, restarting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"🔄 Creating new tmux session..."
                    )
                    self.create_session()
                
                elif status == "empty":
                    logging.warning("Session exists but is empty, restarting...")
                    self.restart_session()
                
                time.sleep(300)  # Check every 5 minutes
                
            except KeyboardInterrupt:
                logging.info("Monitor interrupted by user")
                break
            except Exception as e:
                logging.error(f"Monitor error: {e}")
                time.sleep(60)  # Wait before retrying

def main():
    """Main function"""
    scheduler = TmuxScheduler()
    
    if len(sys.argv) < 2:
        print("🚀 Crypto Daily Report Scheduler - TMux Manager")
        print("")
        print("Usage:")
        print("  python3 tmux_scheduler.py start     - Start the scheduler in tmux")
        print("  python3 tmux_scheduler.py attach    - Attach to running session")
        print("  python3 tmux_scheduler.py stop      - Stop the scheduler")
        print("  python3 tmux_scheduler.py restart   - Restart the scheduler")
        print("  python3 tmux_scheduler.py status    - Check session status")
        print("  python3 tmux_scheduler.py monitor   - Monitor and auto-restart")
        print("")
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        if scheduler.session_exists():
            print("⚠️  Session already exists. Use 'restart' to restart or 'attach' to connect.")
        else:
            if scheduler.create_session():
                print("✅ Scheduler started successfully in tmux session")
                print(f"📱 Session name: {scheduler.session_name}")
                print("🔗 Use 'attach' to connect to the session")
                print("📊 Use 'status' to check if it's running")
            else:
                print("❌ Failed to start scheduler")
                sys.exit(1)
    
    elif command == "attach":
        if scheduler.session_exists():
            scheduler.attach_session()
        else:
            print("❌ No running session found. Use 'start' to create one.")
            sys.exit(1)
    
    elif command == "stop":
        if scheduler.session_exists():
            scheduler.kill_session()
            print("✅ Scheduler stopped")
        else:
            print("ℹ️  No running session found")
    
    elif command == "restart":
        scheduler.restart_session()
        print("✅ Scheduler restarted")
    
    elif command == "status":
        status = scheduler.get_session_status()
        print(f"📊 Session status: {status}")
        if status == "running":
            print("✅ Scheduler is running")
        elif status == "empty":
            print("⚠️  Session exists but is empty")
        else:
            print("❌ Session is not running")
    
    elif command == "monitor":
        print("🔍 Starting session monitor...")
        print("📱 Will auto-restart if session goes down")
        print("⏹️  Press Ctrl+C to stop monitoring")
        scheduler.monitor_session()
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main() 