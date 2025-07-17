# Deployment Guide

## Architecture

The application is now split into two containers:

- **Backend**: FastAPI server that interfaces with Ollama/Llama
- **Frontend**: Streamlit UI that communicates with the backend API

## Prerequisites

1. **Ollama**: Must be running on the host machine
   ```bash
   # Install and start Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama serve
   
   # Pull the required model
   ollama pull llama3.2:3b
   ```

## Deployment Options

### Option 1: Docker Compose (Recommended)

```bash
# Build and start both containers
docker-compose up --build

# Access the application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Separate Container Builds

```bash
# Build backend
docker build -f Dockerfile.backend -t yes-and-backend .

# Build frontend  
docker build -f Dockerfile.frontend -t yes-and-frontend .

# Run backend
docker run -p 8000:8000 \
  -e OLLAMA_HOST=host.docker.internal:11434 \
  -v $(pwd)/logs:/app/logs \
  yes-and-backend

# Run frontend
docker run -p 8501:8501 \
  -e API_BASE_URL=http://localhost:8000 \
  yes-and-frontend
```

### Option 3: Development Mode

```bash
# Terminal 1: Start backend
cd /infra/yes-and
pip install -r requirements-backend.txt
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
pip install -r requirements-frontend.txt
streamlit run src/frontend/humor_cohost_ui.py
```

## Environment Variables

### Backend
- `MODEL_NAME`: Ollama model to use (default: llama3.2:3b)
- `OLLAMA_HOST`: Ollama server address (default: localhost:11434)
- `HOST`: API host (default: 0.0.0.0)
- `PORT`: API port (default: 8000)
- `LOG_LEVEL`: Logging level (default: info)
- `TEMPERATURE`: Model temperature (default: 0.9)
- `TOP_P`: Model top_p (default: 0.9)
- `MAX_TOKENS`: Max tokens to generate (default: 150)

### Frontend
- `API_BASE_URL`: Backend API URL (default: http://localhost:8000)

## Health Checks

- Backend: `curl http://localhost:8000/health`
- Frontend: `curl http://localhost:8501/_stcore/health`

## Troubleshooting

1. **Ollama Connection Issues**: Ensure Ollama is running and accessible
2. **Model Not Found**: Pull the required model with `ollama pull llama3.2:3b`
3. **Port Conflicts**: Change ports in docker-compose.yml if needed
4. **API Connection**: Check that backend is healthy before starting frontend