# 🚂 Railway Deployment Guide

## Quick Deploy to Railway

### Step 1: Prepare Your Repository

1. **Push to GitHub** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Spotify MCP Server"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app/)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**

### Step 3: Set Environment Variables

In Railway dashboard, go to your project → **Variables** tab and add:

```
SPOTIFY_CLIENT_ID=c9838c5e918344d6b17e69052d2bbc26
SPOTIFY_CLIENT_SECRET=0815bfd33c504a39b63f6bffd3086ddf
SPOTIFY_REDIRECT_URI=https://httpbin.org/get
PORT=8000
```

### Step 4: Deploy

Railway will automatically:
- ✅ Detect Python and install dependencies from `requirements.txt`
- ✅ Use the `Procfile` to start the server
- ✅ Assign a public URL like `https://your-app-name.railway.app`

### Step 5: Test Your Deployment

Once deployed, visit these URLs:

- **🏠 Home**: `https://your-app-name.railway.app/`
- **🎧 Dashboard**: `https://your-app-name.railway.app/dashboard`
- **🏆 Top Songs API**: `https://your-app-name.railway.app/top-songs`
- **🕒 Recent Songs API**: `https://your-app-name.railway.app/recent-songs`
- **❤️ Health Check**: `https://your-app-name.railway.app/health`

## 🎯 What You'll Get

### Beautiful Web Dashboard
- **Spotify-themed UI** with green gradients
- **Your top 10 songs** with artist, album, duration, popularity
- **Recently played tracks** with timestamps
- **Responsive design** that works on mobile
- **Auto-refresh** functionality

### API Endpoints
- **REST API** for all Spotify data
- **JSON responses** for easy integration
- **CORS enabled** for web apps
- **Error handling** with meaningful messages

### Features
- **Automatic token refresh** (uses your stored authentication)
- **Fallback to sample data** if authentication fails
- **Health monitoring** for Railway
- **Logging** for debugging

## 🔧 Troubleshooting

### If Authentication Fails
The app will show sample data instead of failing completely.

### If Deployment Fails
1. Check Railway logs in the dashboard
2. Ensure all environment variables are set
3. Make sure `requirements.txt` is in the root directory

### To Update
Just push to your GitHub repo - Railway will auto-deploy!

## 🚀 Ready to Deploy!

Your Spotify MCP Server is now ready for Railway deployment with:
- ✅ Web dashboard
- ✅ API endpoints  
- ✅ Authentication handling
- ✅ Beautiful UI
- ✅ Error handling
- ✅ Auto-deployment
