# 🐳 Docker Desktop Instructions for Selgo Marketplace

## Step-by-Step Setup for Docker Desktop

### 1. Install Docker Desktop
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
2. Install and start Docker Desktop
3. Ensure Docker Desktop is running (check system tray/menu bar)

### 2. Clone the Repository
```bash
git clone https://github.com/mhxfa007-beep/main.git
cd main
```

### 3. Start the Platform

#### Option A: Quick Start (Recommended)
```bash
# Make the script executable (Mac/Linux)
chmod +x start-selgo.sh

# Start everything
./start-selgo.sh
```

#### Option B: Manual Docker Compose
```bash
# Start all services in background
docker-compose up -d

# Or start with logs visible
docker-compose up
```

### 4. Access Your Services

Once all containers are running (takes 2-3 minutes), open these URLs:

| Service | URL | Login |
|---------|-----|-------|
| **Main Website** | http://localhost:3000 | - |
| **Database Admin** | http://localhost:5050 | admin@selgo.com / admin |

### 5. API Endpoints Available

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| Auth | 8001 | http://localhost:8001 | User authentication |
| Property | 8004 | http://localhost:8004 | Real estate listings |
| Car | 8005 | http://localhost:8005 | Vehicle marketplace |
| Motorcycle | 8003 | http://localhost:8003 | Motorcycle listings |
| Boat | 8000 | http://localhost:8000 | Marine marketplace |
| Job | 8002 | http://localhost:8002 | Job board |
| Chat | 8007 | http://localhost:8007 | Messaging system |

## 🛠️ Docker Desktop Management

### Using Docker Desktop GUI
1. Open Docker Desktop application
2. Go to "Containers" tab
3. You'll see all Selgo services listed
4. Use Start/Stop/Restart buttons as needed

### Using Command Line
```bash
# Check status
docker-compose ps

# Stop all services
docker-compose down

# Restart all services
docker-compose up -d

# View logs
docker-compose logs -f [service-name]

# Example: View auth service logs
docker-compose logs -f auth-service
```

## 🔧 Common Issues & Solutions

### Issue: Port Already in Use
**Error**: "Port 3000 is already allocated"

**Solution**:
```bash
# Find what's using the port
lsof -i :3000

# Kill the process or change port in docker-compose.yml
```

### Issue: Docker Not Running
**Error**: "Cannot connect to the Docker daemon"

**Solution**:
1. Start Docker Desktop application
2. Wait for it to fully start (green icon)
3. Try the command again

### Issue: Out of Memory
**Error**: Services crash or don't start

**Solution**:
1. Open Docker Desktop
2. Go to Settings → Resources → Memory
3. Increase to at least 8GB
4. Click "Apply & Restart"

### Issue: Services Won't Start
**Solution**:
```bash
# Clean restart
docker-compose down
docker system prune -f
docker-compose up -d
```

## 📊 Resource Requirements

### Minimum Requirements
- **RAM**: 8GB (4GB for Docker Desktop + 4GB for services)
- **Disk**: 20GB free space
- **CPU**: 2+ cores

### Recommended
- **RAM**: 16GB
- **Disk**: 50GB free space
- **CPU**: 4+ cores

## 🎯 What's Running?

### Active Services (Enhanced with Finn.no features)
- ✅ **Auth Service** - User management, ratings, notifications
- ✅ **Property Service** - Real estate with advanced search
- ✅ **Car Service** - Vehicle marketplace with inspections
- ✅ **Motorcycle Service** - Motorcycle marketplace
- ✅ **Boat Service** - Marine marketplace with marina info
- ✅ **Job Service** - Job board with company reviews
- ✅ **Chat Service** - Real-time messaging with WebSocket
- ✅ **Frontend** - Next.js with updated Selgo branding

### Infrastructure Services
- ✅ **PostgreSQL** - Database with PostGIS for location features
- ✅ **Redis** - Caching and session management
- ✅ **PgAdmin** - Database administration interface

### Services Available but Commented Out
- 🚧 **Square Service** - General marketplace items
- 🚧 **Travel Service** - Travel and vacation rentals
- 🚧 **Electronics Service** - Electronics and gadgets
- 🚧 **Commercial Service** - Commercial vehicles

To enable these, uncomment them in `docker-compose.yml`

## 🚀 Quick Commands Reference

```bash
# Start everything
./start-selgo.sh

# Start only database and Redis
./start-selgo.sh infrastructure

# Start core services only
./start-selgo.sh core

# View service status
./start-selgo.sh status

# Stop everything
./start-selgo.sh stop

# Show all URLs
./start-selgo.sh urls

# Get help
./start-selgo.sh help
```

## 📱 Testing the Platform

1. **Visit Frontend**: http://localhost:3000
2. **Test API**: http://localhost:8001/docs (FastAPI documentation)
3. **Check Database**: http://localhost:5050 (PgAdmin)
4. **View Logs**: `docker-compose logs -f auth-service`

## 🔒 Security Notes

### Development Setup (Current)
- Default passwords (change for production!)
- All ports exposed locally
- Debug mode enabled

### For Production
- Change all default passwords
- Use environment files
- Enable SSL/TLS
- Configure firewall rules
- Set up monitoring

## 📞 Getting Help

1. **Check logs**: `docker-compose logs [service-name]`
2. **View status**: `docker-compose ps`
3. **Restart service**: `docker-compose restart [service-name]`
4. **Clean restart**: `docker-compose down && docker-compose up -d`

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ All containers show "Up" status in `docker-compose ps`
- ✅ Frontend loads at http://localhost:3000
- ✅ API docs load at http://localhost:8001/docs
- ✅ PgAdmin loads at http://localhost:5050
- ✅ No error messages in logs

Happy coding with Selgo! 🚀