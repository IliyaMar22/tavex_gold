# Tavex Gold Simulation - Deployment Guide

## Overview

This project consists of:
- **Backend**: FastAPI Python server with GoldAPI integration
- **Frontend**: Next.js React application with Tailwind CSS
- **Deployment**: Vercel for both frontend and backend

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **GoldAPI Key**: Already provided (`goldapi-q738vsmgfbokhe-io`)

## Deployment Steps

### 1. Backend Deployment (API)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy Backend**:
   ```bash
   cd backend
   vercel --prod
   ```

3. **Set Environment Variables**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add: `GOLDAPI_KEY` = `goldapi-q738vsmgfbokhe-io`

4. **Note the API URL**: You'll get a URL like `https://tavex-gold-simulation-api.vercel.app`

### 2. Frontend Deployment

1. **Deploy Frontend**:
   ```bash
   cd frontend
   vercel --prod
   ```

2. **Set Environment Variables**:
   - Add: `API_BASE_URL` = `https://tavex-gold-simulation-api.vercel.app`

3. **Note the Frontend URL**: You'll get a URL like `https://tavex-gold-simulation.vercel.app`

### 3. Alternative: Deploy Both Together

1. **From Root Directory**:
   ```bash
   vercel --prod
   ```

2. **Configure in Vercel Dashboard**:
   - Set build command for frontend
   - Set build command for backend
   - Configure environment variables

## Local Development

### Backend (Port 8000)
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend (Port 3000)
```bash
cd frontend
npm install
npm run dev
```

### Full Stack
```bash
# Terminal 1 - Backend
cd backend && python main.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

## Environment Variables

### Backend
- `GOLDAPI_KEY`: Your GoldAPI.io API key
- `API_BASE_URL`: Backend URL (for CORS)

### Frontend
- `API_BASE_URL`: Backend API URL
- `NEXT_PUBLIC_API_URL`: Public API URL (if needed)

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `GET /gold/current` - Current gold price
- `GET /gold/historical` - Historical gold data
- `POST /simulate` - Run Monte Carlo simulation

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Check `API_BASE_URL` in frontend
   - Verify CORS middleware in backend

2. **GoldAPI Errors**:
   - Check API key validity
   - Verify network connectivity
   - Check rate limits

3. **Build Failures**:
   - Check Python/Node.js versions
   - Verify all dependencies installed
   - Check for syntax errors

### Debug Mode

1. **Backend Debug**:
   ```bash
   cd backend
   python -c "import requests; print(requests.get('https://www.goldapi.io/api/XAU/EUR', headers={'x-access-token': 'goldapi-q738vsmgfbokhe-io'}).text)"
   ```

2. **Frontend Debug**:
   - Check browser console
   - Verify API calls in Network tab
   - Check environment variables

## Production Considerations

1. **Rate Limiting**: Implement rate limiting for API calls
2. **Caching**: Add Redis for simulation result caching
3. **Monitoring**: Add logging and error tracking
4. **Security**: Implement API authentication if needed
5. **Performance**: Optimize simulation algorithms for large datasets

## Scaling

1. **Database**: Add PostgreSQL for persistent data storage
2. **Queue**: Use Celery for background simulation processing
3. **CDN**: Use Vercel's CDN for static assets
4. **Load Balancing**: Multiple backend instances

## Monitoring

1. **Vercel Analytics**: Built-in performance monitoring
2. **Error Tracking**: Sentry integration
3. **Uptime Monitoring**: UptimeRobot or similar
4. **API Monitoring**: Vercel Functions monitoring

## Cost Optimization

1. **Vercel Pro**: For production workloads
2. **API Caching**: Reduce GoldAPI calls
3. **Simulation Caching**: Cache common simulation results
4. **CDN**: Use Vercel's global CDN

## Security

1. **API Keys**: Store in Vercel environment variables
2. **CORS**: Configure appropriate origins
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Validate all inputs
5. **HTTPS**: Always use HTTPS in production
