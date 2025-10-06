#!/bin/bash

# Tavex Gold Simulation Deployment Script
# This script deploys both backend and frontend to Vercel

set -e

echo "🚀 Starting Tavex Gold Simulation Deployment"
echo "============================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if user is logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "❌ Not logged in to Vercel. Please login first:"
    vercel login
fi

echo ""
echo "📦 Deploying Backend API..."
echo "============================"

cd backend

# Deploy backend
echo "Deploying backend to Vercel..."
vercel --prod --yes

# Get the deployment URL
BACKEND_URL=$(vercel ls | grep "tavex-gold-simulation" | head -1 | awk '{print $2}')
echo "✅ Backend deployed to: https://$BACKEND_URL"

cd ..

echo ""
echo "🎨 Deploying Frontend..."
echo "========================"

cd frontend

# Set the API base URL
export API_BASE_URL="https://$BACKEND_URL"

# Deploy frontend
echo "Deploying frontend to Vercel..."
vercel --prod --yes

# Get the frontend URL
FRONTEND_URL=$(vercel ls | grep "tavex-gold-simulation" | tail -1 | awk '{print $2}')
echo "✅ Frontend deployed to: https://$FRONTEND_URL"

cd ..

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo "Backend API:  https://$BACKEND_URL"
echo "Frontend:     https://$FRONTEND_URL"
echo ""
echo "📋 Next Steps:"
echo "1. Set environment variables in Vercel dashboard"
echo "2. Test the API endpoints"
echo "3. Test the frontend application"
echo "4. Monitor for any errors"
echo ""
echo "🔧 Environment Variables to Set:"
echo "Backend:"
echo "  - GOLDAPI_KEY: goldapi-q738vsmgfbokhe-io"
echo ""
echo "Frontend:"
echo "  - API_BASE_URL: https://$BACKEND_URL"
echo ""
echo "Happy simulating! 🏆"
