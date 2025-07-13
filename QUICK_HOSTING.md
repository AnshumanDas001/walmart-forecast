# 🚀 Quick Hosting Guide

## 🎯 Recommended: Vercel + Railway (Free)

### Frontend (Vercel)
- **URL**: https://vercel.com
- **Cost**: Free (100GB bandwidth/month)
- **Setup**: Connect GitHub repo, set root to `walmart-forecast-frontend`

### Backend (Railway)
- **URL**: https://railway.app
- **Cost**: Free ($5 credit/month)
- **Setup**: Connect GitHub repo, set root to `backend`

### Total Cost: $0-5/month

---

## 🎯 Alternative: Netlify + Render (Free)

### Frontend (Netlify)
- **URL**: https://netlify.com
- **Cost**: Free
- **Setup**: Connect GitHub repo, build command: `npm run build`

### Backend (Render)
- **URL**: https://render.com
- **Cost**: Free (750 hours/month)
- **Setup**: Connect GitHub repo, set root to `backend`

### Total Cost: $0/month

---

## 🎯 Advanced: AWS (Paid)

### Frontend: S3 + CloudFront
- **Cost**: $1-5/month
- **Setup**: Upload build files to S3, create CloudFront distribution

### Backend: EC2
- **Cost**: $10-20/month
- **Setup**: Launch Ubuntu instance, install dependencies

### Total Cost: $11-25/month

---

## 🚀 Quick Start (Vercel + Railway)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/walmart-forecast.git
git push -u origin main
```

### Step 2: Deploy Backend
1. Go to https://railway.app
2. Sign up and create new project
3. Connect your GitHub repo
4. Set root directory to `backend`
5. Get your backend URL

### Step 3: Deploy Frontend
1. Go to https://vercel.com
2. Sign up and import your GitHub repo
3. Set root directory to `walmart-forecast-frontend`
4. Add environment variable:
   - `REACT_APP_API_BASE_URL` = `https://your-backend-url.railway.app/api`

### Step 4: Test
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.railway.app/api/health`

---

## 📁 Files Ready for Deployment

✅ **Backend**:
- `backend/Procfile` - Railway deployment
- `backend/runtime.txt` - Python version
- `backend/app.py` - Production ready

✅ **Frontend**:
- `walmart-forecast-frontend/src/services/api.js` - Environment variables
- `walmart-forecast-frontend/package.json` - Build scripts

✅ **Documentation**:
- `HOSTING_GUIDE.md` - Complete guide
- `deployment/vercel-deployment.md` - Detailed steps
- `deploy.sh` - Automated helper script

---

## 🎉 Your App Will Be Live At:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-backend.railway.app`

## 💡 Pro Tips:
1. **Start with Vercel + Railway** - easiest and cheapest
2. **Use environment variables** for API URLs
3. **Test locally first** before deploying
4. **Monitor your usage** to stay within free tiers
5. **Set up custom domain** later if needed

Ready to deploy? Run `./deploy.sh` for step-by-step guidance! 🚀 