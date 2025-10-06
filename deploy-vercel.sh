#!/bin/bash

# Tavex Gold Simulation - Vercel Deployment Script
# This script deploys the frontend to Vercel

set -e

echo "🚀 Deploying Tavex Gold Simulation to Vercel"
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
echo "🎨 Deploying Frontend..."
echo "========================"

cd frontend

# Deploy frontend
echo "Deploying frontend to Vercel..."
vercel --prod --yes

# Get the deployment URL
FRONTEND_URL=$(vercel ls | grep "tavex-gold-simulation" | head -1 | awk '{print $2}')
echo "✅ Frontend deployed to: https://$FRONTEND_URL"

cd ..

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo "Frontend: https://$FRONTEND_URL"
echo ""
echo "📋 Next Steps:"
echo "1. Test the application in your browser"
echo "2. The app will use GoldAPI.io for real-time gold prices"
echo "3. All simulations run client-side with realistic historical data"
echo ""
echo "🔧 Features:"
echo "- Real-time gold price data from GoldAPI.io"
echo "- Monte Carlo simulation with 10,000+ runs"
echo "- Historical data based on gold market research"
echo "- Interactive charts and visualizations"
echo "- Responsive design with Tailwind CSS"
echo ""
echo "Happy simulating! 🏆"
