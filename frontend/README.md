# Agentic Agile System - Frontend Dashboard

A modern React TypeScript dashboard for the Agentic Agile System, providing a comprehensive interface for monitoring and managing autonomous agents, issues, wellness metrics, and system events.

## Features

- **Dashboard Overview**: Real-time metrics and charts showing system health
- **Agent Management**: Monitor and control autonomous agents
- **Issue Tracking**: View and manage project issues with filtering and search
- **Wellness Monitoring**: Team health check-ins and wellness trends
- **Event System**: Real-time event monitoring and system communications
- **Settings**: Comprehensive system configuration options

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Recharts** for data visualization
- **Heroicons** for icons
- **React Hot Toast** for notifications

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Development

### Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── hooks/         # Custom React hooks
├── utils/         # Utility functions
├── types/         # TypeScript type definitions
├── App.tsx        # Main app component
├── main.tsx       # Entry point
└── index.css      # Global styles
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors

## API Integration

The frontend is configured to proxy API requests to the backend at `http://localhost:8000`. The proxy is configured in `vite.config.ts`.

## Styling

The project uses Tailwind CSS with custom color schemes and components. Custom styles are defined in `src/index.css`.

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Test your changes thoroughly
4. Update documentation as needed

## License

This project is part of the Agentic Agile System and follows the same license terms. 