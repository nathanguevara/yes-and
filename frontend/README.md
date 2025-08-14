# Yes-And Frontend

A modern React frontend for the Yes-And AI Comedy Cohost application.

## Features

- 🎭 **Interactive Chat Interface** - Real-time conversation with AI comedy cohost
- 🎨 **Multiple Humor Styles** - Choose from witty, sarcastic, observational, self-deprecating, and absurd styles
- ⭐ **Rating System** - Rate AI responses with emoji-based feedback
- 📊 **Performance Metrics** - View response times, humor scores, and enhancement status
- 📈 **Statistics Dashboard** - Track feedback stats and style performance
- 🎛️ **Advanced Controls** - Session management and settings customization
- 🔄 **Real-time Health Monitoring** - Backend connection status and health checks

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Query** for API state management
- **Zustand** for global state management
- **React Hook Form** for form handling
- **Lucide React** for icons

## Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Copy environment configuration
cp .env.example .env

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000

### Building for Production

```bash
# Build the application
npm run build

# Preview the build
npm run preview
```

## Project Structure

```
src/
├── components/          # React components
│   ├── ui/             # Reusable UI components
│   ├── ChatInterface.tsx
│   ├── ChatMessage.tsx
│   ├── ChatInput.tsx
│   ├── Sidebar.tsx
│   ├── Rating.tsx
│   └── HumorStyleSelector.tsx
├── pages/              # Page components
│   └── ChatPage.tsx
├── services/           # API client and services
│   └── api.ts
├── stores/             # Zustand stores
│   └── chat.ts
├── types/              # TypeScript type definitions
│   └── api.ts
├── styles/             # Global styles
│   └── index.css
└── App.tsx             # Main application component
```

## Configuration

### Environment Variables

- `VITE_API_BASE_URL`: Backend API base URL (default: http://localhost:8000)
- `VITE_DEV_MODE`: Enable development features (default: true)

### Customization

The application can be customized through:

- **Theme colors**: Edit `tailwind.config.js` comedy color palette
- **API endpoints**: Modify `src/services/api.ts`
- **Chat behavior**: Update `src/stores/chat.ts`
- **UI components**: Customize components in `src/components/ui/`

## API Integration

The frontend connects to the Yes-And backend API with these endpoints:

- `GET /health` - Health check
- `POST /generate` - Generate comedy responses
- `POST /feedback` - Submit user ratings
- `GET /feedback/stats` - Get feedback statistics
- `GET /model/info` - Get model information

See the main project README for complete API documentation.

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Code Style

- **ESLint** for code linting
- **TypeScript** for type safety
- **Prettier** for code formatting (recommended)

### State Management

- **Chat State**: Managed by Zustand store in `src/stores/chat.ts`
- **API State**: Managed by React Query for caching and synchronization
- **UI State**: Local component state for transient UI interactions

## Deployment

### Static Hosting

Build the application and deploy the `dist` folder to any static hosting service:

```bash
npm run build
# Deploy the dist/ folder
```

### Docker

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Environment Configuration

For production deployment, ensure:

1. Set `VITE_API_BASE_URL` to your production API URL
2. Configure CORS on the backend to allow your frontend domain
3. Set up proper error monitoring and analytics

## Features in Detail

### Chat Interface

- Real-time message streaming
- Typing indicators
- Message history persistence (optional)
- Error handling and retry logic

### Rating System

- 5-level emoji-based ratings
- Immediate feedback submission
- Rating statistics tracking
- Style-specific performance metrics

### Humor Styles

- **Witty**: Clever wordplay and smart observations
- **Sarcastic**: Dry humor with irony
- **Observational**: Funny takes on everyday situations  
- **Self-Deprecating**: Humble humor at one's own expense
- **Absurd**: Wildly imaginative and unexpected humor

### Performance Metrics

- Response generation time
- Humor quality scores
- Enhancement status (original vs enhanced responses)
- Real-time backend health monitoring

## Troubleshooting

### Common Issues

**Backend Connection Failed**
- Ensure the backend API is running on the configured port
- Check CORS configuration
- Verify the `VITE_API_BASE_URL` environment variable

**Build Errors**
- Clear node_modules and reinstall dependencies
- Check TypeScript configuration
- Ensure all imports use proper paths

**Performance Issues**
- Enable React Query DevTools in development
- Check browser network tab for slow API calls
- Monitor bundle size with `npm run build`

## Contributing

1. Follow the existing code style and patterns
2. Add TypeScript types for new features
3. Test changes with the backend API
4. Update documentation for new features

## License

MIT License - See the main project LICENSE file for details.