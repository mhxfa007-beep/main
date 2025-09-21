#!/bin/bash

# Selgo Marketplace Startup Script
# This script helps you easily start the Selgo platform with different configurations

set -e

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
    echo -e "${BLUE}   Selgo Marketplace Platform   ${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop first."
        exit 1
    fi
    print_status "Docker is running ✓"
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "docker-compose is not installed or not in PATH"
        exit 1
    fi
    print_status "docker-compose is available ✓"
}

# Function to create .env file if it doesn't exist
setup_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from .env.example..."
        cp .env.example .env
        print_status ".env file created. You may want to customize it."
    else
        print_status ".env file exists ✓"
    fi
}

# Function to start all services
start_all() {
    print_status "Starting all enhanced Selgo services..."
    docker-compose up -d
    print_status "All services started! 🚀"
    show_urls
}

# Function to start only infrastructure
start_infrastructure() {
    print_status "Starting infrastructure services (Database, Redis, PgAdmin)..."
    docker-compose up -d postgres redis pgadmin
    print_status "Infrastructure services started! 🗄️"
}

# Function to start core services
start_core() {
    print_status "Starting core services (Auth, Frontend, Database, Redis)..."
    docker-compose up -d postgres redis auth-service frontend
    print_status "Core services started! 🔐"
}

# Function to start with logs
start_with_logs() {
    print_status "Starting all services with logs visible..."
    docker-compose up
}

# Function to show service URLs
show_urls() {
    echo ""
    print_header
    echo -e "${GREEN}🌐 Service URLs:${NC}"
    echo "  Frontend:           http://localhost:3000"
    echo "  Auth Service:       http://localhost:8001"
    echo "  Property Service:   http://localhost:8004"
    echo "  Car Service:        http://localhost:8005"
    echo "  Motorcycle Service: http://localhost:8003"
    echo "  Boat Service:       http://localhost:8000"
    echo "  Job Service:        http://localhost:8002"
    echo "  Chat Service:       http://localhost:8007"
    echo ""
    echo -e "${GREEN}🛠️  Admin Tools:${NC}"
    echo "  PgAdmin:            http://localhost:5050"
    echo "  Redis:              localhost:6379"
    echo ""
    echo -e "${GREEN}📊 Management Commands:${NC}"
    echo "  View status:        docker-compose ps"
    echo "  View logs:          docker-compose logs -f [service-name]"
    echo "  Stop services:      docker-compose down"
    echo "  Restart service:    docker-compose restart [service-name]"
    echo ""
}

# Function to show service status
show_status() {
    print_status "Current service status:"
    docker-compose ps
}

# Function to stop all services
stop_services() {
    print_status "Stopping all services..."
    docker-compose down
    print_status "All services stopped! 🛑"
}

# Function to restart services
restart_services() {
    print_status "Restarting all services..."
    docker-compose restart
    print_status "All services restarted! 🔄"
}

# Function to rebuild and start
rebuild_and_start() {
    print_status "Rebuilding and starting all services..."
    docker-compose up --build -d
    print_status "Services rebuilt and started! 🔨"
    show_urls
}

# Function to show help
show_help() {
    echo "Selgo Marketplace Startup Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start, up           Start all enhanced services (default)"
    echo "  infrastructure      Start only infrastructure (DB, Redis, PgAdmin)"
    echo "  core               Start core services (Auth, Frontend, DB, Redis)"
    echo "  logs               Start all services with logs visible"
    echo "  status             Show current service status"
    echo "  stop, down         Stop all services"
    echo "  restart            Restart all services"
    echo "  rebuild            Rebuild and start all services"
    echo "  urls               Show service URLs"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                 # Start all services"
    echo "  $0 infrastructure  # Start only database and Redis"
    echo "  $0 logs           # Start with logs visible"
    echo "  $0 status         # Check service status"
    echo ""
}

# Main script logic
main() {
    print_header
    
    # Check prerequisites
    check_docker
    check_docker_compose
    setup_env
    
    # Handle command line arguments
    case "${1:-start}" in
        "start"|"up"|"")
            start_all
            ;;
        "infrastructure"|"infra")
            start_infrastructure
            ;;
        "core")
            start_core
            ;;
        "logs")
            start_with_logs
            ;;
        "status")
            show_status
            ;;
        "stop"|"down")
            stop_services
            ;;
        "restart")
            restart_services
            ;;
        "rebuild")
            rebuild_and_start
            ;;
        "urls")
            show_urls
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"