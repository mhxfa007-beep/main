# Selgo Marketplace - Docker Setup Guide

This guide will help you run the complete Selgo marketplace platform using Docker Desktop.

## 🚀 Quick Start

### Prerequisites

1. **Docker Desktop** - Download and install from [docker.com](https://www.docker.com/products/docker-desktop/)
2. **Git** - For cloning the repository
3. **At least 8GB RAM** - Recommended for running all services
4. **20GB free disk space** - For Docker images and volumes

### 1. Clone and Navigate to Repository

```bash
git clone https://github.com/mhxfa007-beep/main.git
cd main
```

### 2. Start the Complete Platform

```bash
# Start all enhanced services (recommended)
docker-compose up -d

# Or start with logs visible
docker-compose up
```

### 3. Access the Platform

Once all containers are running, you can access:

- **Frontend**: http://localhost:3000
- **Auth Service**: http://localhost:8001
- **Property Service**: http://localhost:8004
- **Car Service**: http://localhost:8005
- **Motorcycle Service**: http://localhost:8003
- **Boat Service**: http://localhost:8000
- **Job Service**: http://localhost:8002
- **Chat Service**: http://localhost:8007
- **PgAdmin**: http://localhost:5050 (admin@selgo.com / admin)
- **Redis**: localhost:6379

## 📋 Service Status

### ✅ Enhanced Services (Active)
These services have been enhanced with comprehensive Finn.no-inspired features:

- **Auth Service** (Port 8001) - User management, ratings, notifications
- **Property Service** (Port 8004) - Real estate with advanced search
- **Car Service** (Port 8005) - Vehicle marketplace with inspections
- **Motorcycle Service** (Port 8003) - Motorcycle marketplace
- **Boat Service** (Port 8000) - Marine marketplace with marina info
- **Job Service** (Port 8002) - Job board with company reviews
- **Chat Service** (Port 8007) - Real-time messaging with WebSocket

### 🚧 Services Not Yet Enhanced (Commented Out)
These services exist but are not yet enhanced. Uncomment in docker-compose.yml when ready:

- **Square Service** (Port 8006) - General marketplace items
- **Travel Service** (Port 8008) - Travel and vacation rentals
- **Electronics Service** (Port 8009) - Electronics and gadgets
- **Commercial Service** (Port 8010) - Commercial vehicles

## 🛠️ Docker Commands

### Basic Operations

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f [service-name]

# Restart a specific service
docker-compose restart [service-name]

# Rebuild and start (after code changes)
docker-compose up --build -d
```

### Development Commands

```bash
# Start only infrastructure (database, redis)
docker-compose up -d postgres redis pgadmin

# Start specific services
docker-compose up -d auth-service property-service frontend

# View service status
docker-compose ps

# Execute commands in containers
docker-compose exec postgres psql -U postgres
docker-compose exec redis redis-cli
```

### Troubleshooting Commands

```bash
# View container logs
docker-compose logs [service-name]

# Check container health
docker-compose ps

# Remove all containers and volumes (CAUTION: This deletes data)
docker-compose down -v

# Clean up Docker system
docker system prune -a
```

## 🗄️ Database Setup

### Automatic Database Initialization

The PostgreSQL container automatically creates all required databases using the `init-db.sql` script:

- `selgo_auth` - User authentication and profiles
- `selgo_property` - Real estate listings
- `selgo_car` - Vehicle listings
- `selgo_motorcycle` - Motorcycle listings
- `selgo_boat` - Marine vessel listings
- `selgo_job` - Job postings and applications
- `selgo_chat` - Messaging and conversations

### Manual Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres

# Connect to specific database
docker-compose exec postgres psql -U postgres -d selgo_property

# Access via PgAdmin
# URL: http://localhost:5050
# Email: admin@selgo.com
# Password: admin
```

## 🔧 Configuration

### Environment Variables

Key environment variables are set in the docker-compose.yml file:

```yaml
# Database Configuration
DB_USER=postgres
DB_PASSWORD=12345
DB_HOST=postgres
DB_PORT=5432

# Security (Change in production!)
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# Service URLs
AUTH_SERVICE_URL=http://auth-service:8001
REDIS_URL=redis://redis:6379
```

### Production Considerations

For production deployment:

1. **Change default passwords** in environment variables
2. **Use environment files** (.env) instead of hardcoded values
3. **Enable SSL/TLS** with proper certificates
4. **Configure backup strategies** for PostgreSQL
5. **Set up monitoring** and logging
6. **Use Docker secrets** for sensitive data

## 📊 Service Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Auth Service  │    │  Property Svc   │
│   (Next.js)     │    │   (FastAPI)     │    │   (FastAPI)     │
│   Port: 3000    │    │   Port: 8001    │    │   Port: 8004    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Car Service   │    │  Motorcycle Svc │    │   Boat Service  │
│   (FastAPI)     │    │   (FastAPI)     │    │   (FastAPI)     │
│   Port: 8005    │    │   Port: 8003    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Job Service   │    │  Chat Service   │    │     Redis       │
│   (FastAPI)     │    │   (FastAPI)     │    │   (Cache)       │
│   Port: 8002    │    │   Port: 8007    │    │   Port: 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   (PostGIS)     │
                    │   Port: 5432    │
                    └─────────────────┘
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :3000
   # Kill the process or change port in docker-compose.yml
   ```

2. **Database Connection Issues**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps postgres
   # View PostgreSQL logs
   docker-compose logs postgres
   ```

3. **Out of Memory**
   ```bash
   # Increase Docker Desktop memory allocation
   # Docker Desktop → Settings → Resources → Memory
   ```

4. **Build Failures**
   ```bash
   # Clean build cache
   docker-compose build --no-cache
   # Remove old images
   docker image prune -a
   ```

### Health Checks

All services include health checks. Check service health:

```bash
# View service health status
docker-compose ps

# Check specific service health
docker inspect selgo-auth-service | grep Health -A 10
```

### Log Analysis

```bash
# View all logs
docker-compose logs

# Follow logs for specific service
docker-compose logs -f auth-service

# View last 100 lines
docker-compose logs --tail=100 property-service
```

## 🔄 Development Workflow

### Making Changes

1. **Code Changes**: Edit files in your local directory
2. **Auto-reload**: Services automatically reload on file changes
3. **Database Changes**: Restart services if schema changes
4. **New Dependencies**: Rebuild containers with `--build` flag

### Adding New Services

1. Uncomment the service in `docker-compose.yml`
2. Ensure the service has proper Dockerfile
3. Add database initialization if needed
4. Update environment variables
5. Start the service: `docker-compose up -d [service-name]`

## 📈 Monitoring

### Service Monitoring

```bash
# View resource usage
docker stats

# Monitor specific containers
docker stats selgo-auth-service selgo-postgres

# View container processes
docker-compose top
```

### Database Monitoring

Access PgAdmin at http://localhost:5050 to:
- Monitor database performance
- View query statistics
- Manage database connections
- Backup and restore data

## 🔒 Security Notes

### Development vs Production

**Development (Current Setup):**
- Default passwords
- Debug mode enabled
- All ports exposed
- No SSL/TLS

**Production Requirements:**
- Strong passwords and secrets
- Environment-based configuration
- Reverse proxy (Nginx)
- SSL/TLS certificates
- Network security
- Regular backups

### Immediate Security Steps

1. Change default passwords in docker-compose.yml
2. Use environment files for sensitive data
3. Limit exposed ports
4. Enable container security scanning

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs [service-name]`
3. Verify all containers are healthy: `docker-compose ps`
4. Check Docker Desktop resources and settings

## 🎯 Next Steps

1. **Start the platform**: `docker-compose up -d`
2. **Access frontend**: http://localhost:3000
3. **Explore services**: Use the API endpoints
4. **Add data**: Create test listings and users
5. **Customize**: Modify services as needed
6. **Deploy**: Prepare for production deployment

Happy coding! 🚀