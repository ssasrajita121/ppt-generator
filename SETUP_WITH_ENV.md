# EduBridge PPT Generator - Setup Guide

## 📋 Quick Setup with .env File

### **Step 1: Install Dependencies**

```bash
pip install -r requirements_multi_ai.txt
npm install pptxgenjs
```

### **Step 2: Create .env File**

Create a file named `.env` in your project folder:

```
D:\snapskill\Projects\AI_slides\
├── edubridge_gemini_only.py
├── .env                          ← Create this file
├── requirements_multi_ai.txt
├── node_modules/
└── package.json
```

### **Step 3: Add Your API Key to .env**

Open `.env` and add:

```env
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Get your key from:** https://aistudio.google.com/apikey

### **Step 4: Run the App**

```bash
streamlit run edubridge_gemini_only.py
```

---

## ✅ Why .env File?

- ✅ **Secure** - API key not in code
- ✅ **Easy** - One file for all secrets
- ✅ **Git-friendly** - Add `.env` to `.gitignore`
- ✅ **Portable** - Works on any machine

---

## 🔒 Security Best Practices

### **Add .env to .gitignore**

Create `.gitignore` file:

```
.env
*.pyc
__pycache__/
node_modules/
.streamlit/secrets.toml
```

This prevents accidentally committing your API key to GitHub!

---

## 📁 Complete File Structure

```
D:\snapskill\Projects\AI_slides\
├── edubridge_gemini_only.py      # Main app
├── .env                           # Your API key (DON'T COMMIT!)
├── .env.example                   # Example template (safe to commit)
├── .gitignore                     # Ignore sensitive files
├── requirements_multi_ai.txt      # Python dependencies
├── packages.txt                   # System dependencies
├── node_modules/                  # Node.js packages
│   └── pptxgenjs/
└── package.json                   # npm config
```

---

## 🚀 Deployment Options

### **Option 1: Local Development (using .env)**

1. Create `.env` file with your key
2. Run: `streamlit run edubridge_gemini_only.py`
3. Works immediately! ✅

### **Option 2: Streamlit Cloud (using Secrets)**

1. Deploy to Streamlit Cloud
2. Settings → Secrets
3. Add:
   ```toml
   GOOGLE_API_KEY = "your-key-here"
   ```
4. No `.env` file needed on cloud ✅

---

## 🐛 Troubleshooting

### **"GOOGLE_API_KEY not found"**

**Solution:**
1. Check `.env` file exists in same folder as `.py` file
2. Check `.env` has the correct format (no quotes needed)
3. Restart the app

### **"Module 'dotenv' not found"**

**Solution:**
```bash
pip install python-dotenv
```

### **API key still not working**

**Check .env format:**
```env
# ✅ Correct
GOOGLE_API_KEY=AIzaSyXXXXXXXX

# ❌ Wrong (no quotes, no spaces around =)
GOOGLE_API_KEY = "AIzaSyXXXXXXXX"
```

---

## 💡 Example .env File

Copy this template:

```env
# EduBridge PPT Generator - API Configuration

# Google Gemini API Key
# Get from: https://aistudio.google.com/apikey
GOOGLE_API_KEY=your-actual-key-here

# Optional: Add other settings
# DEBUG_MODE=false
# MAX_SLIDES=10
```

---

## ✅ Verification

After setup, verify everything works:

```bash
# 1. Check .env exists
ls -la .env

# 2. Run the app
streamlit run edubridge_gemini_only.py

# 3. Generate a test presentation
# Topic: "Test Presentation"
# Slides: 3
```

If you see the download button → **Success!** 🎉

---

## 📞 Need Help?

Common issues:
- `.env` in wrong folder → Move to same folder as `.py` file
- Wrong API key → Get new one from Google AI Studio
- Missing dependencies → Run `pip install -r requirements_multi_ai.txt`

---

**You're all set! Start generating presentations!** 🚀
