#!/bin/bash

# Crypto Scheduler Service Setup
# Choose between tmux and systemd for running the scheduler

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    echo -e "${BLUE}  Crypto Scheduler Setup${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_usage() {
    echo "Usage: $0 [tmux|systemd|help]"
    echo ""
    echo "Options:"
    echo "  tmux     - Set up tmux-based scheduler (recommended)"
    echo "  systemd  - Set up systemd service (requires root)"
    echo "  help     - Show this help message"
    echo ""
    echo "TMux (Recommended):"
    echo "  - No root access required"
    echo "  - Easy to monitor and debug"
    echo "  - Works on any system with tmux"
    echo ""
    echo "Systemd:"
    echo "  - Requires root access"
    echo "  - Automatic startup on boot"
    echo "  - Better for production servers"
}

setup_tmux() {
    print_status "Setting up tmux-based scheduler..."
    
    # Check if tmux is installed
    if ! command -v tmux &> /dev/null; then
        print_error "tmux is not installed. Please install it first:"
        echo "  Ubuntu/Debian: sudo apt-get install tmux"
        echo "  CentOS/RHEL: sudo yum install tmux"
        echo "  macOS: brew install tmux"
        exit 1
    fi
    
    # Make scripts executable
    chmod +x start_tmux_scheduler.sh
    
    print_status "TMux setup complete!"
    echo ""
    echo "To start the scheduler:"
    echo "  ./start_tmux_scheduler.sh"
    echo ""
    echo "To check status:"
    echo "  ./start_tmux_scheduler.sh status"
    echo ""
    echo "To attach to session:"
    echo "  ./start_tmux_scheduler.sh attach"
}

setup_systemd() {
    print_status "Setting up systemd service..."
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        print_error "Systemd setup requires root access. Please run with sudo."
        exit 1
    fi
    
    # Get current user and directory
    CURRENT_USER=$(logname || who am i | awk '{print $1}')
    CURRENT_DIR=$(pwd)
    
    print_warning "Current user: $CURRENT_USER"
    print_warning "Current directory: $CURRENT_DIR"
    echo ""
    
    # Ask for confirmation
    read -p "Do you want to continue with these settings? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Setup cancelled."
        exit 0
    fi
    
    # Create systemd service file
    SERVICE_FILE="/etc/systemd/system/crypto-scheduler.service"
    
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Crypto Daily Report Scheduler
After=network.target
Wants=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
ExecStart=/usr/bin/python3 $CURRENT_DIR/daily_scheduler.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable crypto-scheduler.service
    
    print_status "Systemd service created and enabled!"
    echo ""
    echo "Service commands:"
    echo "  sudo systemctl start crypto-scheduler    # Start the service"
    echo "  sudo systemctl stop crypto-scheduler     # Stop the service"
    echo "  sudo systemctl restart crypto-scheduler  # Restart the service"
    echo "  sudo systemctl status crypto-scheduler   # Check status"
    echo "  sudo journalctl -u crypto-scheduler -f   # View logs"
    echo ""
    echo "The service will start automatically on boot."
}

main() {
    print_header
    
    if [ $# -eq 0 ]; then
        echo "Please choose a setup method:"
        echo ""
        echo "1) TMux (Recommended - No root access required)"
        echo "2) Systemd (Requires root access)"
        echo ""
        read -p "Enter your choice (1 or 2): " choice
        
        case $choice in
            1) setup_tmux ;;
            2) setup_systemd ;;
            *) print_error "Invalid choice"; exit 1 ;;
        esac
    else
        case "$1" in
            "tmux") setup_tmux ;;
            "systemd") setup_systemd ;;
            "help"|"-h"|"--help") print_usage ;;
            *) print_error "Unknown option: $1"; print_usage; exit 1 ;;
        esac
    fi
}

main "$@" 