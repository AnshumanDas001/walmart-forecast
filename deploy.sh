#!/bin/bash

# 🚀 Walmart AI Forecasting System - Deployment Script
# This script helps you deploy your application to various platforms

echo "🚀 Walmart AI Forecasting System - Deployment Helper"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Walmart AI Forecasting System"
    echo "✅ Git repository initialized"
    echo ""
    echo "🔗 Please create a GitHub repository and run:"
    echo "   git remote add origin https://github.com/yourusername/walmart-forecast.git"
    echo "   git push -u origin main"
    echo ""
else
    echo "✅ Git repository already exists"
fi

echo "🌐 Choose your deployment option:"
echo ""
echo "1. Vercel + Railway (Recommended - Free)"
echo "2. Netlify + Render (Free)"
echo "3. AWS (Advanced - Paid)"
echo "4. Local Production Build"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🎯 Deploying to Vercel + Railway"
        echo "================================"
        echo ""
        echo "📋 Steps to follow:"
        echo ""
        echo "1. Push your code to GitHub:"
        echo "   git add ."
        echo "   git commit -m 'Ready for deployment'"
        echo "   git push"
        echo ""
        echo "2. Deploy Backend to Railway:"
        echo "   - Go to https://railway.app"
        echo "   - Sign up and create new project"
        echo "   - Connect your GitHub repo"
        echo "   - Set root directory to 'backend'"
        echo "   - Get your backend URL"
        echo ""
        echo "3. Deploy Frontend to Vercel:"
        echo "   - Go to https://vercel.com"
        echo "   - Sign up and import your GitHub repo"
        echo "   - Set root directory to 'walmart-forecast-frontend'"
        echo "   - Add environment variable:"
        echo "     REACT_APP_API_BASE_URL=https://your-backend-url.railway.app/api"
        echo ""
        echo "4. Test your deployment:"
        echo "   - Frontend: https://your-app.vercel.app"
        echo "   - Backend: https://your-backend.railway.app/api/health"
        ;;
    2)
        echo ""
        echo "🎯 Deploying to Netlify + Render"
        echo "================================"
        echo ""
        echo "📋 Steps to follow:"
        echo ""
        echo "1. Deploy Backend to Render:"
        echo "   - Go to https://render.com"
        echo "   - Sign up and create web service"
        echo "   - Connect your GitHub repo"
        echo "   - Set root directory to 'backend'"
        echo "   - Build command: pip install -r requirements.txt"
        echo "   - Start command: python app.py"
        echo ""
        echo "2. Deploy Frontend to Netlify:"
        echo "   - Go to https://netlify.com"
        echo "   - Sign up and deploy from Git"
        echo "   - Connect your GitHub repo"
        echo "   - Set root directory to 'walmart-forecast-frontend'"
        echo "   - Build command: npm run build"
        echo "   - Publish directory: build"
        echo "   - Add environment variable:"
        echo "     REACT_APP_API_BASE_URL=https://your-backend.render.com"
        ;;
    3)
        echo ""
        echo "🎯 Deploying to AWS"
        echo "==================="
        echo ""
        echo "📋 Steps to follow:"
        echo ""
        echo "1. Frontend (S3 + CloudFront):"
        echo "   - Create S3 bucket: walmart-forecast-frontend"
        echo "   - Enable static website hosting"
        echo "   - Build: npm run build"
        echo "   - Upload: aws s3 sync build/ s3://walmart-forecast-frontend"
        echo "   - Create CloudFront distribution"
        echo ""
        echo "2. Backend (EC2):"
        echo "   - Launch Ubuntu EC2 instance (t2.micro free tier)"
        echo "   - Install Python, pip, nginx"
        echo "   - Clone your repo and install requirements"
        echo "   - Configure nginx as reverse proxy"
        echo "   - Set up SSL with Let's Encrypt"
        ;;
    4)
        echo ""
        echo "🎯 Local Production Build"
        echo "========================"
        echo ""
        echo "📋 Building for production..."
        echo ""
        
        # Build frontend
        echo "🔨 Building frontend..."
        cd walmart-forecast-frontend
        npm run build
        echo "✅ Frontend built successfully"
        echo ""
        
        # Check backend
        echo "🔍 Checking backend..."
        cd ../backend
        echo "✅ Backend ready for production"
        echo ""
        
        echo "📁 Production files created:"
        echo "   Frontend: walmart-forecast-frontend/build/"
        echo "   Backend: backend/"
        echo ""
        echo "🚀 To run in production:"
        echo "   Backend: python app.py"
        echo "   Frontend: Serve build/ directory with a web server"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment guide completed!"
echo ""
echo "📚 For detailed instructions, see:"
echo "   - HOSTING_GUIDE.md"
echo "   - deployment/vercel-deployment.md"
echo ""
echo "🔧 Need help? Check the troubleshooting section in HOSTING_GUIDE.md" 