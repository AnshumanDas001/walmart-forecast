# 🚀 Deploy to Vercel + Railway/Render

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Production

1. **Update API Base URL**
   ```bash
   cd walmart-forecast-frontend
   ```

2. **Create Environment File**
   Create `.env.production` in the frontend directory:
   ```env
   REACT_APP_API_BASE_URL=https://your-backend-url.railway.app/api
   ```

3. **Update API Service**
   Edit `src/services/api.js`:
   ```javascript
   const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';
   ```

### Step 2: Deploy to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd walmart-forecast-frontend
   vercel --prod
   ```

4. **Follow the prompts**:
   - Set up and deploy: `Y`
   - Which scope: Select your account
   - Link to existing project: `N`
   - Project name: `walmart-forecast-frontend`
   - Directory: `./` (current directory)
   - Override settings: `N`

### Step 3: Configure Environment Variables in Vercel

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add:
   - `REACT_APP_API_BASE_URL`: `https://your-backend-url.railway.app/api`

## Backend Deployment (Railway)

### Step 1: Prepare Backend

1. **Create `Procfile`** in the backend directory:
   ```
   web: python app.py
   ```

2. **Update `app.py`** for production:
   ```python
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       app.run(debug=False, host='0.0.0.0', port=port)
   ```

3. **Create `runtime.txt`** in backend directory:
   ```
   python-3.11.0
   ```

### Step 2: Deploy to Railway

1. **Sign up** at [railway.app](https://railway.app)

2. **Connect GitHub**:
   - Push your code to GitHub
   - Connect Railway to your GitHub repo

3. **Deploy**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Set root directory to `backend`

4. **Configure Environment Variables**:
   - Go to Variables tab
   - Add any required environment variables

5. **Get your backend URL** from Railway dashboard

### Step 3: Update Frontend API URL

1. Go back to Vercel dashboard
2. Update `REACT_APP_API_BASE_URL` with your Railway URL
3. Redeploy frontend

## Alternative: Render Deployment

### Backend on Render

1. **Sign up** at [render.com](https://render.com)

2. **Create Web Service**:
   - Connect GitHub repo
   - Set root directory to `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python app.py`

3. **Configure Environment**:
   - Add environment variables if needed
   - Set Python version to 3.11

## 🎯 Final Steps

1. **Test your deployment**:
   - Frontend: `https://your-app.vercel.app`
   - Backend: `https://your-backend.railway.app/api/health`

2. **Update CORS** in backend if needed:
   ```python
   CORS(app, origins=['https://your-app.vercel.app'])
   ```

3. **Monitor logs** in both platforms

## 💰 Cost Estimation

- **Vercel**: Free tier (100GB bandwidth/month)
- **Railway**: Free tier ($5 credit/month)
- **Render**: Free tier (750 hours/month)

Total: **$0-5/month** for small to medium usage! 