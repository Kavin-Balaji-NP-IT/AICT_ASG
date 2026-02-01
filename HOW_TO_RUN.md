# How to Run ChangiLink AI

**Quick start guide to get the system running in 3 simple steps!**

## Super Quick Start

1. **Install packages:**
   ```bash
   pip install flask numpy pandas requests
   ```

2. **Run the system:**
   ```bash
   python integrated_launcher.py
   ```

3. **Open your browser** - The dashboard will open automatically!

---

## Step-by-Step Instructions

### Step 1: Check Python
Make sure Python is installed:
```bash
python --version
```
*Need Python 3.7 or higher*

### Step 2: Install Required Packages
Copy and paste this command:
```bash
pip install flask numpy pandas requests
```

### Step 3: Launch the System

**Choose one method:**

**Method A - Direct Python (All platforms):**
```bash
python integrated_launcher.py
```

**Method B - Windows:**
```bash
start_changilink_ai.bat
```

**Method C - Linux/Mac:**
```bash
chmod +x start_changilink_ai.sh
./start_changilink_ai.sh
```

### Step 4: Access the Systems

The system will automatically open your browser. If not, visit:

- **Main Dashboard**: Opens automatically
- **Route Planning**: http://localhost:5000
- **Logical Inference**: http://localhost:5001
- **Crowding Risk**: http://localhost:5002

## How to Stop

Press `Ctrl+C` in the terminal where the system is running.

---

## Troubleshooting

**Problem: "Module not found"**
```bash
pip install flask numpy pandas requests
```

**Problem: "Port already in use"**
- Close any other programs using ports 5000, 5001, 5002
- Or restart your computer

**Problem: Python not found**
- Install Python from https://python.org
- Make sure to check "Add to PATH" during installation

**Problem: Permission denied (Linux/Mac)**
```bash
chmod +x start_changilink_ai.sh
```

---

## What You'll See

When everything works correctly, you'll see:
```
ChangiLink AI - Integrated Transportation Intelligence System
All dependencies satisfied!
Starting Route Planning...
   Route Planning started on http://localhost:5000
Starting Logical Inference...
   Logical Inference started on http://localhost:5001
Starting Crowding Risk...
   Crowding Risk started on http://localhost:5002
ChangiLink AI is ready!
```

**That's it! The system is now running and ready to use.**

---

## Still Having Issues?

1. Make sure you're in the correct folder (where `integrated_launcher.py` is located)
2. Try running individual systems:
   ```bash
   cd Route_Planning
   python web_app.py
   ```
3. Check the main README.md for detailed troubleshooting

**Happy exploring!**