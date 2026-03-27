#!/usr/bin/env python3
"""
Validate configuration file
"""
import os
import sys

def validate_config():
    """Validate configuration settings"""
    print("Validating configuration...")
    
    if not os.path.exists("config.py"):
        print("⚠️  config.py not found, using default settings")
        return True
    
    try:
        import config
        print("✅ Configuration loaded successfully")
        
        # Validate Redis config
        if not hasattr(config, "REDIS_HOST") or not hasattr(config, "REDIS_PORT"):
            print("❌ Missing Redis configuration")
            return False
        
        print("✅ Redis configuration valid")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    success = validate_config()
    sys.exit(0 if success else 1)
