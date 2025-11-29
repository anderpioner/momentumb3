# Deployment Guide for Streamlit Cloud

Since Git is not installed or configured on your system, you will need to perform these steps manually.

## 1. Install Git (if not installed)
Download and install Git from [git-scm.com](https://git-scm.com/downloads).

## 2. Initialize Repository
Open your terminal (PowerShell or Command Prompt) in the `stock_ranker` folder and run:

```bash
cd C:\Users\ander\.gemini\antigravity\scratch\stock_ranker
git init
git add .
git commit -m "Initial commit"
```

## 3. Push to GitHub
1.  Create a new repository on [GitHub](https://github.com/new).
2.  Follow the instructions to push an existing repository:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## 4. Deploy on Streamlit Cloud
1.  Go to [Streamlit Community Cloud](https://share.streamlit.io/).
2.  Click "New app".
3.  Select your GitHub repository.
4.  Set the **Main file path** to `app.py`.
5.  Click **Deploy**.

## Files to Include
Ensure these files are in your repository (I have already created them):
- `app.py`
- `stock_ranker.py`
- `requirements.txt`
- `.gitignore`
