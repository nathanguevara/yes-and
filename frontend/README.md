# Yes-And Frontend

Modern React TypeScript frontend for the Yes-And comedy AI chatbot.

## Features

- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Full type safety and excellent developer experience
- **Tailwind CSS**: Utility-first CSS framework for rapid styling
- **Zustand**: Lightweight state management
- **React Query**: Data fetching and caching
- **Vite**: Fast development server and build tool
- **Docker Support**: Production-ready containerization

## Development

### Prerequisites
- Node.js 20+ 
- npm or yarn

### Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Type checking
npm run type-check

# Linting
npm run lint
```

### Environment Configuration

Create a `.env` file in the frontend directory:
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_DEV_MODE=true
```

For production deployment, update the API URL:
```bash
VITE_API_BASE_URL=http://192.168.50.2:31102
```

## Docker Deployment

### Production Build
```bash
# Build from project root
docker build -f Dockerfile.frontend -t yes-and-frontend .

# Run container
docker run -p 80:80 yes-and-frontend
```

### Development Container
```bash
# Build development image
docker build -f Dockerfile.dev -t yes-and-frontend:dev .

# Run with hot reload
docker run -p 5173:5173 -v $(pwd):/app yes-and-frontend:dev
```

## Architecture

### Component Structure
```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Base UI components (Button, Input, etc.)
│   ├── ChatInterface.tsx
│   ├── ChatMessage.tsx
│   ├── HumorStyleSelector.tsx
│   └── Sidebar.tsx
├── pages/              # Page components
├── services/           # API client and external services
├── stores/             # Zustand state management
├── types/              # TypeScript type definitions
└── styles/             # Global styles and Tailwind config
```

### State Management

The app uses Zustand for state management:
- **Chat Store**: Manages conversation history and UI state
- **Settings Store**: User preferences and configuration

### API Integration

The frontend communicates with the FastAPI backend via:
- REST API calls for generating responses and submitting feedback
- TypeScript interfaces for type-safe API communication
- Automatic error handling and loading states

## Configuration Files

- **package.json**: Dependencies and scripts
- **tsconfig.json**: TypeScript configuration
- **tailwind.config.js**: Tailwind CSS configuration
- **vite.config.ts**: Vite build configuration
- **nginx.conf**: Production nginx configuration

## Deployment

The frontend is designed for production deployment with:
- **Nginx**: Serves static assets and handles SPA routing
- **Docker**: Multi-stage build for optimized production images
- **CI/CD**: Automated builds via GitHub Actions

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run preview`: Preview production build locally
- `npm run lint`: Run ESLint
- `npm run type-check`: Run TypeScript type checking

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Contributing

1. Follow the existing code style
2. Add type definitions for new features
3. Update tests when adding functionality
4. Ensure production build works correctly