# 🚀 Selgo Marketplace - Quick Start Guide

## Prerequisites
- **Docker Desktop** installed and running
- **8GB+ RAM** available
- **20GB+ free disk space**

## 1-Minute Setup

### Option A: Using the Startup Script (Recommended)
```bash
# Make script executable (Linux/Mac)
chmod +x start-selgo.sh

# Start everything
./start-selgo.sh

# Or start with specific options
./start-selgo.sh infrastructure  # Just database and Redis
./start-selgo.sh core           # Core services only
./start-selgo.sh logs           # With visible logs
```

### Option B: Using Docker Compose Directly
```bash
# Start all services
docker-compose up -d

# Start with logs visible
docker-compose up
```

## 🌐 Access Your Platform

Once running, access these URLs:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main Selgo website |
| **Auth API** | http://localhost:8001 | User authentication |
| **Property API** | http://localhost:8004 | Real estate listings |
| **Car API** | http://localhost:8005 | Vehicle marketplace |
| **Motorcycle API** | http://localhost:8003 | Motorcycle listings |
| **Boat API** | http://localhost:8000 | Marine marketplace |
| **Job API** | http://localhost:8002 | Job board |
| **Chat API** | http://localhost:8007 | Messaging system |
| **PgAdmin** | http://localhost:5050 | Database admin |

### PgAdmin Login
- **Email**: admin@selgo.com
- **Password**: admin

## 🛠️ Common Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f [service-name]

# Stop everything
docker-compose down

# Restart a service
docker-compose restart [service-name]

# Rebuild after code changes
docker-compose up --build -d
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 3000
lsof -i :3000

# Kill the process or change port in docker-compose.yml
```

### Services Won't Start
```bash
# Check Docker Desktop is running
docker info

# View service logs
docker-compose logs [service-name]

# Clean restart
docker-compose down && docker-compose up -d
```

### Out of Memory
- Increase Docker Desktop memory allocation
- Go to Docker Desktop → Settings → Resources → Memory
- Allocate at least 8GB

## 📊 What's Running?

### ✅ Enhanced Services (Active)
- **Auth Service** - User management with ratings & notifications
- **Property Service** - Real estate with advanced search
- **Car Service** - Vehicle marketplace with inspections
- **Motorcycle Service** - Motorcycle marketplace
- **Boat Service** - Marine marketplace with marina info
- **Job Service** - Job board with company reviews
- **Chat Service** - Real-time messaging

### 🚧 Available but Commented Out
- Square Service (General marketplace)
- Travel Service (Vacation rentals)
- Electronics Service (Gadgets)
- Commercial Service (Commercial vehicles)

To enable these services, uncomment them in `docker-compose.yml`

## 🎯 Next Steps

1. **Explore the Frontend**: Visit http://localhost:3000
2. **Test APIs**: Use the service endpoints
3. **Add Test Data**: Create sample listings
4. **Customize**: Modify services as needed
5. **Deploy**: Prepare for production

## 📞 Need Help?

1. Check `DOCKER_SETUP.md` for detailed instructions
2. View logs: `docker-compose logs [service-name]`
3. Check service health: `docker-compose ps`
4. Restart services: `docker-compose restart`

Happy coding! 🎉