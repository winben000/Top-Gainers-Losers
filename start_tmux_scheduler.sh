#!/bin/bash

# Crypto Daily Report Scheduler - TMux Startup Script
# This script starts the crypto scheduler in a tmux session

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Crypto Scheduler - TMux Setup${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if tmux is installed
check_tmux() {
    if ! command -v tmux &> /dev/null; then
        print_error "tmux is not installed. Please install it first:"
        echo "  Ubuntu/Debian: sudo apt-get install tmux"
        echo "  CentOS/RHEL: sudo yum install tmux"
        echo "  macOS: brew install tmux"
        exit 1
    fi
    print_status "tmux is installed"
}

# Check if Python dependencies are available
check_python_deps() {
    if ! python3 -c "import schedule, requests" 2>/dev/null; then
        print_error "Python dependencies are missing. Please install them:"
        echo "  pip3 install -r requirements.txt"
        exit 1
    fi
    print_status "Python dependencies are available"
}

# Check if config file exists
check_config() {
    if [ ! -f "config.py" ]; then
        print_error "config.py not found. Please make sure you're in the correct directory."
        exit 1
    fi
    print_status "Configuration file found"
}

# Main function
main() {
    print_header
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    print_status "Checking prerequisites..."
    check_tmux
    check_python_deps
    check_config
    
    print_status "Starting crypto scheduler in tmux..."
    
    # Start the scheduler
    if python3 tmux_scheduler.py start; then
        print_status "✅ Scheduler started successfully!"
        echo ""
        echo "📱 Session name: crypto_scheduler"
        echo "🔗 To attach to the session: python3 tmux_scheduler.py attach"
        echo "📊 To check status: python3 tmux_scheduler.py status"
        echo "⏹️  To stop: python3 tmux_scheduler.py stop"
        echo "🔄 To restart: python3 tmux_scheduler.py restart"
        echo "🔍 To monitor: python3 tmux_scheduler.py monitor"
        echo ""
        print_status "The scheduler will run daily at 7:00 AM and send reports to Telegram"
    else
        print_error "Failed to start scheduler"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "attach")
        python3 tmux_scheduler.py attach
        ;;
    "stop")
        python3 tmux_scheduler.py stop
        ;;
    "restart")
        python3 tmux_scheduler.py restart
        ;;
    "status")
        python3 tmux_scheduler.py status
        ;;
    "monitor")
        python3 tmux_scheduler.py monitor
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)  - Start the scheduler"
        echo "  attach     - Attach to running session"
        echo "  stop       - Stop the scheduler"
        echo "  restart    - Restart the scheduler"
        echo "  status     - Check session status"
        echo "  monitor    - Monitor and auto-restart"
        echo "  help       - Show this help"
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 