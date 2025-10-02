#!/usr/bin/env python3
"""
Stable server runner for Resume Analyzer
Run this instead of app.py directly
"""

import os
import sys
from app import app

def main():
    print("🚀 Starting Resume Analyzer Server (Stable Mode)...")
    print("📁 Upload folder:", app.config['UPLOAD_FOLDER'])
    print("🌐 Server will run on: http://localhost:5000")
    print("✅ Health check: http://localhost:5000/health")
    print("")
    print("🔧 Server running in PRODUCTION mode (no auto-reload)")
    print("💡 To stop server: Press Ctrl+C")
    print("-" * 50)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run without debug mode
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)