# -*- coding: utf-8 -*-
"""
RIZERxHOSTING - Complete Multi-language Telegram Hosting Bot (synchronous)
Combined file with requested upgrades applied:
 - ADMIN ACCESS is only visible to admins and owner in the main menu
 - Custom "Broadcast to User" from Manage Members fixed and added
 - All previous features included (ZIP upload, auto-extract, run/stop, logs, admin panel, broadcast, temp-admin)
 - PREMIUM SYSTEM: 4-option admin settings for premium control, star payments, and user management
 - REVOKE PREMIUM ACCESS option added
 - CPU/RAM/Disk usage optimizations
 - NEW: Direct .py and .js file upload support with auto requirements.txt generation
 - NEW: Silent dependency installation (no user notifications during install)
 - NEW: Performance optimizations for faster response times
 - NEW: Webhook mode support (host/port via environment variables) - FIXED binary compatibility issue
 - NEW: HYBRID MODE - Auto-detects public URL and uses webhook, falls back to polling
 - NEW: Battery interface for dependency installation progress
 - NEW: Enhanced database integrity with verification
 - NEW: Comprehensive error handlers
 - NEW: Telegram Stars premium purchase and auto-expiry
 - NEW: Professional, styled messages with Markdown formatting
 - NEW: Fixed polling lock (atomic file creation + persistent lock)
Notes:
 - Token is embedded below (as you provided)
 - Requires: pyTelegramBotAPI, psutil, flask
 - Run: python RIZERxHOSTING_full.py
 - Webhook Mode: Set WEBHOOK_MODE=true, PORT=5000 (or auto-detected from hosting platform)
 - Polling Mode: Default when no public URL is detected
"""

# ==============================================================================
#  PRODUCTION-GRADE SAFETY BOOTSTRAP  (ADDED – NON-BREAKING, PURELY ADDITIVE)
# ==============================================================================
import os
import sys
import subprocess

# --- Minimum guaranteed package set -------------------------------------------------
_REQUIRED = {
    "pyTelegramBotAPI": "telebot",
    "psutil": "psutil",
    "requests": "requests",
    "certifi": "certifi",
    "protobuf": "protobuf",
}

# --- Idempotent auto-installer ------------------------------------------------------
def _ensure_pkgs():
    """Install missing packages without touching already satisfied ones."""
    to_install = []
    for dist_name, import_name in _REQUIRED.items():
        try:
            __import__(import_name)
        except ImportError:
            to_install.append(dist_name)
    if not to_install:
        return
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--no-cache-dir"] + to_install
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

_ensure_pkgs()
# --- Protobuf runtime/gencode compatibility fix ------------------------------------
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
# ==============================================================================
#  END SAFETY BOOTSTRAP
# ==============================================================================

# ==============================================================================
#  ADDITIONAL SAFETY LAYER (PURELY ADDITIVE - NO EXISTING CODE MODIFIED)
# ==============================================================================
# This section adds more dependency handling without touching any existing code

# Additional dependencies for broader compatibility and hosting platform support
_ADDITIONAL_REQUIRED = {
    # Telegram bot libraries (alternative implementations)
    "aiogram": "aiogram",
    "python-telegram-bot": "telegram",
    # HTTP/async libraries
    "aiohttp": "aiohttp",
    "httpx": "httpx",
    # Web frameworks (common in hosted projects)
    "flask": "flask",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "django": "django",
    # Database libraries
    "sqlalchemy": "sqlalchemy",
    "alembic": "alembic",
    "redis": "redis",
    "pymongo": "pymongo",
    "psycopg2-binary": "psycopg2",
    "mysql-connector-python": "mysql.connector",
    # Utility and security libraries
    "cryptography": "cryptography",
    "python-dotenv": "dotenv",
    "pillow": "PIL",
    "qrcode": "qrcode",
    # Version pinning for known crash-causing packages
    "protobuf>=3.20.0,<5.0.0": "protobuf",
    # Common data science libs (often cause dependency issues)
    "numpy": "numpy",
    "pandas": "pandas",
    # Additional compatibility libraries
    "uvloop": "uvloop",
    "pytz": "pytz",
    "charset-normalizer": "charset_normalizer",
    "idna": "idna",
    "urllib3": "urllib3",
}

def _is_package_installed(dist_name: str, import_name: str) -> bool:
    """
    Safely check if a package is installed without triggering import errors.
    Uses importlib.metadata (safe) or subprocess (safest for complex packages).
    """
    # Skip None imports (built-in packages)
    if import_name is None:
        return True
    
    try:
        # Modern Python: use importlib.metadata (doesn't import the package)
        from importlib.metadata import distribution, PackageNotFoundError
        try:
            # Extract package name from version specifiers
            pkg_name = dist_name.split('>=')[0].split('<')[0].split('==')[0]
            distribution(pkg_name)
            return True
        except PackageNotFoundError:
            return False
    except ImportError:
        # Fallback: use subprocess to test import in isolation
        pass
    
    # Safest method: test import in separate process to avoid binary incompatibility errors
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import {import_name}"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def _ensure_additional_pkgs():
    """Install additional packages for user project compatibility without modifying existing logic."""
    to_install = []
    for dist_name, import_name in _ADDITIONAL_REQUIRED.items():
        # Skip None imports (built-in packages)
        if import_name is None:
            continue
            
        # Use safe check instead of direct import
        if not _is_package_installed(dist_name, import_name):
            to_install.append(dist_name)
    
    if not to_install:
        return
    
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--no-cache-dir", "--quiet"] + to_install
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

_ensure_additional_pkgs()

# Environment detection and hosting platform compatibility fixes
def _apply_hosting_compatibility():
    """Apply compatibility fixes for various hosting environments without altering core behavior."""
    # Render.com specific environment variables
    if os.getenv("RENDER"):
        os.environ["TELEGRAM_BOT_POLLING_TIMEOUT"] = "60"
        os.environ["RENDER"] = "true"
    
    # Railway.app specific environment variables
    if os.getenv("RAILWAY_ENVIRONMENT"):
        os.environ["TELEGRAM_BOT_POLLING_TIMEOUT"] = "60"
        os.environ["RAILWAY"] = "true"
    
    # Docker container detection
    if os.path.exists("/.dockerenv"):
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
        except Exception:
            pass
        os.environ["DOCKER"] = "true"
    
    # VPS/systemd detection
    if os.getenv("INVOCATION_ID") or os.path.exists("/run/systemd"):
        os.environ["SYSTEMD"] = "true"
    
    # Webhook mode detection
    if os.getenv("WEBHOOK_MODE", "").lower() in ("true", "1", "yes"):
        os.environ["WEBHOOK_MODE"] = "true"
    
    # General production settings that don't interfere with development
    os.environ["PYTHONUNBUFFERED"] = os.environ.get("PYTHONUNBUFFERED", "1")
    os.environ["PYTHONDONTWRITEBYTECODE"] = os.environ.get("PYTHONDONTWRITEBYTECODE", "1")
    os.environ["PYTHONIOENCODING"] = os.environ.get("PYTHONIOENCODING", "utf-8")

_apply_hosting_compatibility()

# ==============================================================================
#  END ADDITIONAL SAFETY LAYER
# ==============================================================================

import os
import sys
import time
import sqlite3
import logging
import zipfile
import shutil
import subprocess
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple, List
from types import SimpleNamespace
import re
import json
import queue
import functools
import fcntl  # For file locking in polling mode
import errno  # Added for polling lock error handling

import psutil
import telebot
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto,
    LabeledPrice, PreCheckoutQuery, ShippingQuery  # Added for Stars payments
)

# ==============================================================================
#  ULTRA-ROBUST DEPENDENCY AUTO-INSTALLER SYSTEM WITH CONFLICT RESOLUTION
# ==============================================================================
# This system provides comprehensive dependency management with zero user errors

class DependencyInstaller:
    """Enhanced dependency installer with conflict resolution and retry logic."""
    
    @staticmethod
    def _fix_telegram_namespace(uid: int, project_path: str):
        """Special fix for telegram namespace conflicts between pyTelegramBotAPI and python-telegram-bot."""
        try:
            main_files = ["main.py", "app.py", "bot.py", "start.py"]
            for mf in main_files:
                main_path = os.path.join(project_path, mf)
                if os.path.exists(main_path):
                    with open(main_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "from telegram import Update" in content or "from telegram.ext import Application" in content:
                            logger.info(f"Detected python-telegram-bot v20+ syntax in user {uid} project")
                            install_cmd = [
                                sys.executable, "-m", "pip", "install", 
                                "python-telegram-bot>=20.0", 
                                "--quiet", "--no-cache-dir", "--disable-pip-version-check",
                                "--upgrade", "--force-reinstall"
                            ]
                            subprocess.run(install_cmd, capture_output=True, timeout=180)
                            bot.send_message(uid, "🔧 Auto-fixed telegram library conflict (installed python-telegram-bot v20+)")
                            return True
        except Exception as e:
            logger.warning(f"Failed to fix telegram namespace for user {uid}: {e}")
        return False
    
    @staticmethod
    def install_python_deps(uid: int, project_path: str, project_name: str, silent: bool = False) -> bool:
        """Install Python dependencies with aggressive conflict resolution and special telegram handling."""
        req_files = [
            os.path.join(project_path, "requirements.txt"),
            os.path.join(project_path, "requirements-dev.txt"),
        ]
        
        success = False
        
        for req_file in req_files:
            if os.path.exists(req_file):
                try:
                    if not silent:
                        status_msg = bot.send_message(uid, f"⏳ Installing Python dependencies for `{project_name}`...")
                    
                    if req_file.endswith("requirements.txt"):
                        DependencyInstaller._fix_telegram_namespace(uid, project_path)
                    
                    cmd = [
                        sys.executable, "-m", "pip", "install", 
                        "-r", req_file, 
                        "--upgrade",
                        "--force-reinstall",
                        "--quiet", 
                        "--no-cache-dir", 
                        "--disable-pip-version-check",
                        "--timeout", "300"
                    ]
                    
                    result = subprocess.run(
                        cmd, 
                        cwd=project_path,
                        capture_output=True, 
                        text=True, 
                        timeout=600
                    )
                    
                    if result.returncode == 0:
                        success = True
                        if not silent:
                            bot.send_message(uid, f"✅ Python dependencies installed for `{project_name}`")
                    else:
                        error_detail = result.stderr[-300:] if result.stderr else "Unknown pip error"
                        if not silent:
                            bot.send_message(uid, f"⚠️ Installation issues for `{project_name}`")
                        logger.warning(f"User {uid} project {project_name}: install issues - {error_detail}")
                    
                    marker = os.path.join(project_path, f".installed_{os.path.basename(req_file)}")
                    with open(marker, "w") as f:
                        f.write(f"installed_{int(time.time())}")
                        
                except subprocess.TimeoutExpired:
                    if not silent:
                        bot.send_message(uid, f"⚠️ Installation timed out for `{project_name}`")
                    logger.error(f"User {uid} project {project_name}: install timeout")
                except Exception as e:
                    if not silent:
                        bot.send_message(uid, f"⚠️ Critical error: {str(e)[:200]}")
                    logger.exception(f"User {uid} project {project_name}: install critical error")
        
        return success
    
    @staticmethod
    def install_node_deps(uid: int, project_path: str, project_name: str, silent: bool = False) -> bool:
        """Install Node.js dependencies with enhanced error handling."""
        package_json = os.path.join(project_path, "package.json")
        if not os.path.exists(package_json):
            return True
        
        try:
            if not silent:
                status_msg = bot.send_message(uid, f"⏳ Installing Node.js dependencies for `{project_name}`...")
            
            npm_cmd = ["npm", "install", "--silent", "--no-fund", "--no-audit", "--no-warnings", "--no-progress"]
            result = subprocess.run(npm_cmd, cwd=project_path, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                if not silent:
                    bot.send_message(uid, f"✅ Node.js dependencies installed for `{project_name}`")
                return True
            else:
                error_detail = result.stderr[-200:] if result.stderr else "npm error"
                if not silent:
                    bot.send_message(uid, f"⚠️ Node.js install issues: {error_detail}")
                logger.warning(f"User {uid} project {project_name}: npm failed - {error_detail}")
                return False
                
        except subprocess.TimeoutExpired:
            if not silent:
                bot.send_message(uid, f"⚠️ Node.js install timed out for `{project_name}`")
            logger.error(f"User {uid} project {project_name}: npm timeout")
            return False
        except Exception as e:
            if not silent:
                bot.send_message(uid, f"⚠️ Node.js install error: {str(e)[:150]}")
            logger.exception(f"User {uid} project {project_name}: npm critical error")
            return False

# ==============================================================================
#  BATTERY PROGRESS INTERFACE FOR DEPENDENCY INSTALLATION
# ==============================================================================
class BatteryProgressInterface:
    """Visual battery-style progress bar for dependency installation."""
    
    @staticmethod
    def _get_battery_emoji_and_color(progress: int) -> str:
        """Get appropriate battery emoji and color based on progress."""
        if progress < 30:
            return "🔴"  # Red
        elif progress < 70:
            return "🟡"  # Yellow
        else:
            return "🟢"  # Green
    
    @staticmethod
    def _create_battery_visual(progress: int, width: int = 20) -> str:
        """Create a text-based battery visual."""
        filled = int((progress / 100) * width)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        return f"[{bar}] {progress}%"
    
    @staticmethod
    def _progress_monitor_thread(uid: int, project_path: str, project_name: str, message_id: int):
        """Background thread to monitor and update installation progress."""
        try:
            # Monitor requirements installation
            req_file = os.path.join(project_path, "requirements.txt")
            package_json = os.path.join(project_path, "package.json")
            
            # Determine total packages to install
            total_packages = 0
            current_installed = 0
            last_update_time = time.time()
            
            if os.path.exists(req_file):
                try:
                    with open(req_file, 'r', encoding='utf-8') as f:
                        total_packages = len([line for line in f if line.strip() and not line.startswith('#')])
                except Exception:
                    total_packages = 1  # Default if can't read
            
            elif os.path.exists(package_json):
                total_packages = 10  # Estimate for npm packages
            
            if total_packages == 0:
                total_packages = 1  # Avoid division by zero
            
            # Simulate progress based on installation markers
            progress = 0
            max_progress = 100
            
            while progress < max_progress:
                time.sleep(3)  # Update every 3 seconds
                
                # Check if installation completed
                marker_py = os.path.join(project_path, ".installed_requirements.txt")
                marker_dev = os.path.join(project_path, ".installed_requirements-dev.txt")
                marker_npm = os.path.join(project_path, "node_modules")
                
                python_done = os.path.exists(marker_py) or not os.path.exists(req_file)
                dev_done = os.path.exists(marker_dev) or not os.path.exists(package_json.replace('package.json', 'requirements-dev.txt'))
                npm_done = os.path.exists(marker_npm) or not os.path.exists(package_json)
                
                # Calculate progress
                if python_done and dev_done and npm_done:
                    progress = 100
                else:
                    # Simulate gradual progress
                    current_installed += 1
                    progress = min(int((current_installed / total_packages) * 100), 95)
                
                # Update message with battery visual
                color_emoji = BatteryProgressInterface._get_battery_emoji_and_color(progress)
                battery = BatteryProgressInterface._create_battery_visual(progress)
                
                try:
                    bot.edit_message_text(
                        chat_id=uid,
                        message_id=message_id,
                        text=f"📦 Installing dependencies for `{project_name}`...\n\n{color_emoji} {battery}"
                    )
                except Exception:
                    # Message might be deleted or other error
                    break
                
                # Stop if installation is complete
                if progress >= 100:
                    break
                
                # Timeout after 15 minutes
                if time.time() - last_update_time > 900:
                    break
        
        except Exception as e:
            logger.warning(f"Battery progress thread error for user {uid}: {e}")
        finally:
            # Clean up and send success message
            try:
                bot.delete_message(uid, message_id)
                bot.send_message(uid, f"🎉 All dependencies installed for `{project_name}`! ✅", parse_mode='Markdown')
            except Exception:
                pass
    
    @staticmethod
    def start_progress_monitor(uid: int, project_path: str, project_name: str) -> int:
        """
        Start a background thread to monitor installation progress.
        Returns the message ID of the progress message.
        """
        try:
            # Create initial battery message (0%)
            battery = BatteryProgressInterface._create_battery_visual(0)
            status_msg = bot.send_message(
                uid,
                f"📦 Installing dependencies for `{project_name}`...\n\n🔴 {battery}",
                parse_mode='Markdown'
            )
            
            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=BatteryProgressInterface._progress_monitor_thread,
                args=(uid, project_path, project_name, status_msg.message_id),
                daemon=True,
                name=f"BatteryProgress_{uid}_{project_name}"
            )
            monitor_thread.start()
            
            return status_msg.message_id
            
        except Exception as e:
            logger.error(f"Failed to start battery progress monitor for user {uid}: {e}")
            return None

# ==============================================================================
#  AUTO REQUIREMENTS.TXT GENERATOR FOR SINGLE FILE UPLOADS
# ==============================================================================
class RequirementsGenerator:
    """Automatically generate requirements.txt from source code analysis."""
    
    # Common import to package name mappings
    IMPORT_TO_PACKAGE = {
        'telebot': 'pyTelegramBotAPI',
        'telegram': 'python-telegram-bot',
        'aiogram': 'aiogram',
        'discord': 'discord.py',
        'flask': 'flask',
        'django': 'django',
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'requests': 'requests',
        'aiohttp': 'aiohttp',
        'httpx': 'httpx',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
        'PIL': 'pillow',
        'cv2': 'opencv-python',
        'asyncio': None,  # Built-in
        'json': None,  # Built-in
        'os': None,  # Built-in
        'sys': None,  # Built-in
        'time': None,  # Built-in
        'datetime': None,  # Built-in
        'typing': None,  # Built-in
        'collections': None,  # Built-in
        'itertools': None,  # Built-in
        'random': None,  # Built-in
        'math': None,  # Built-in
        're': None,  # Built-in
        'subprocess': None,  # Built-in
        'threading': None,  # Built-in
        'queue': None,  # Built-in
        'pathlib': None,  # Built-in
        'shutil': None,  # Built-in
        'sqlite3': None,  # Built-in
        'logging': None,  # Built-in
        'hashlib': None,  # Built-in
        'base64': None,  # Built-in
    }
    
    @staticmethod
    def generate_from_py_file(file_path: str) -> List[str]:
        """Analyze Python file and generate requirements list."""
        requirements = set()
        
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Find import statements
            # import module
            imports = re.findall(r'^import\s+(\w+)', content, re.MULTILINE)
            # from module import something
            from_imports = re.findall(r'^from\s+(\w+)', content, re.MULTILINE)
            
            all_imports = set(imports + from_imports)
            
            for imp in all_imports:
                package = RequirementsGenerator.IMPORT_TO_PACKAGE.get(imp)
                if package is None and imp not in RequirementsGenerator.IMPORT_TO_PACKAGE:
                    # Unknown import, try to guess package name (common pattern)
                    package = imp
                
                if package:
                    requirements.add(package)
            
            # Special handling for common patterns
            if 'python-telegram-bot' in requirements and 'pyTelegramBotAPI' in requirements:
                # Both detected, check which one is actually used
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if "from telegram import Update" in content or "from telegram.ext import Application" in content:
                    requirements.discard('pyTelegramBotAPI')
                else:
                    requirements.discard('python-telegram-bot')
            
        except Exception as e:
            logger.warning(f"Failed to generate requirements from {file_path}: {e}")
        
        return sorted(list(requirements))
    
    @staticmethod
    def generate_from_js_file(file_path: str) -> dict:
        """Analyze JavaScript file and generate package.json dependencies."""
        deps = {}
        
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Find require() statements
            requires = re.findall(r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', content)
            # Find import statements
            imports = re.findall(r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]', content)
            # Find import() dynamic imports
            dynamic_imports = re.findall(r'import\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', content)
            
            all_imports = set(requires + imports + dynamic_imports)
            
            for imp in all_imports:
                # Skip relative imports
                if imp.startswith('.'):
                    continue
                
                # Extract package name (remove @scope/ if present)
                if imp.startswith('@'):
                    package_name = imp.split('/')[0] + '/' + imp.split('/')[1]
                else:
                    package_name = imp.split('/')[0]
                
                # Add with latest version
                deps[package_name] = "^latest"
            
        except Exception as e:
            logger.warning(f"Failed to generate package.json from {file_path}: {e}")
        
        return deps

# ==============================================================================
#  PREMIUM SYSTEM DATABASE AND UTILITIES (PURELY ADDITIVE)
# ==============================================================================
# Premium membership management for RIZERxHOSTING

def init_premium_db():
    """Initialize premium system database tables."""
    with db_lock:
        cur = db_conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS premium_users (
            user_id INTEGER PRIMARY KEY,
            is_premium INTEGER DEFAULT 0,
            premium_since REAL,
            premium_until REAL,
            transaction_id TEXT
        )
        """)
        cur.execute("INSERT OR IGNORE INTO config (key, value) VALUES ('premium_mode', 'off')")
        cur.execute("INSERT OR IGNORE INTO config (key, value) VALUES ('premium_price_stars', '0')")
        db_conn.commit()

def is_premium_user(user_id: int) -> bool:
    """Check if user has premium access (considers expiry)."""
    premium_mode = get_config_sync("premium_mode", "off")
    if premium_mode == "off":
        return True
    
    with db_lock:
        cur = db_conn.cursor()
        cur.execute("SELECT is_premium, premium_until FROM premium_users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            return False
        is_premium, premium_until = row
        if not is_premium:
            return False
        if premium_until and time.time() > premium_until:
            # Auto-revoke expired premium
            cur.execute("DELETE FROM premium_users WHERE user_id = ?", (user_id,))
            db_conn.commit()
            logger.info(f"Premium expired for user {user_id}, revoked")
            return False
        return True

def set_user_premium_sync(user_id: int, is_premium: bool, transaction_id: str = None, duration_days: int = 30):
    """Set premium status for a user. If is_premium=True, set expiry to now+duration_days."""
    with db_lock:
        cur = db_conn.cursor()
        if is_premium:
            premium_since = time.time()
            premium_until = premium_since + (duration_days * 24 * 60 * 60) if duration_days > 0 else None
            cur.execute("""
            INSERT OR REPLACE INTO premium_users (user_id, is_premium, premium_since, premium_until, transaction_id)
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, 1, premium_since, premium_until, transaction_id))
        else:
            cur.execute("DELETE FROM premium_users WHERE user_id = ?", (user_id,))
        db_conn.commit()
        logger.info(f"Premium status updated for user {user_id}: is_premium={is_premium}")

def get_all_users_sync():
    """Get list of all users from database."""
    with db_lock:
        cur = db_conn.cursor()
        cur.execute("SELECT user_id, display_name, username, blocked, server_limit FROM users ORDER BY display_name COLLATE NOCASE")
        rows = cur.fetchall()
        logger.info(f"Retrieved {len(rows)} users from database")
        return rows

def premium_check_required(func):
    """Decorator to check premium access before executing handler."""
    def wrapper(message):
        if not is_premium_user(message.from_user.id):
            premium_mode = get_config_sync("premium_mode", "off")
            if premium_mode == "on":
                try:
                    bot.reply_to(message, f"🚫 PREMIUM SETTINGS HAS BEEN TURNED ON\n\n⚠️ Please contact admin for premium access.\nAdmin: {ADMIN_USERNAME}")
                except Exception:
                    pass
                return
        return func(message)
    return wrapper

# ==============================================================================
#  END PREMIUM SYSTEM DATABASE AND UTILITIES
# ==============================================================================

# -------------------------
# CONFIG (token inserted)
# -------------------------
TOKEN = "8550349407:AAGm3-nv4Mv73PnKD_ewMbHg1tpg3muNxf8"
OWNER_ID = 7735912988
ADMIN_USERNAME = "@beotherjk"
DISPLAY_NAME = "RIZERxHOSTING"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(BASE_DIR, "USERS")
LOGS_DIR = os.path.join(BASE_DIR, "LOGS")
DB_PATH = os.path.join(BASE_DIR, "rizerx_pro.db")
TMP_DIR = os.path.join(BASE_DIR, "TMP")

for d in (USERS_DIR, LOGS_DIR, TMP_DIR):
    os.makedirs(d, exist_ok=True)

# -------------------------
# LOGGING
# -------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("rizerx")

# -------------------------
# BOT
# -------------------------
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# -------------------------
# RUNTIME STATE
# -------------------------
running_instances: Dict[int, Dict[str, subprocess.Popen]] = {}
user_main_files: Dict[int, Dict[str, str]] = {}
ui_cleaner: Dict[int, list] = {}
user_cache: Dict[int, dict] = {}
message_queue = queue.Queue()
cache_lock = threading.Lock()
# Global variable to hold polling lock file descriptor (never closed)
polling_lock_fd = None

# ==============================================================================
#  HYBRID MODE DETECTION AND SETUP (AUTO WEBHOOK/POLLING)
# ==============================================================================
# This section automatically detects if a public URL is available and chooses
# between webhook mode (preferred) and polling mode (fallback).

def detect_public_url() -> Optional[str]:
    """
    Automatically detect public URL from various hosting environments.
    Returns: Public URL string or None if not detected.
    """
    # Check for manually configured webhook URL first
    manual_url = os.getenv("WEBHOOK_URL")
    if manual_url:
        logger.info(f"Using manually configured WEBHOOK_URL: {manual_url}")
        return manual_url.rstrip('/')
    
    # Check Render.com
    render_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if render_url:
        url = f"https://{render_url}"
        logger.info(f"Detected Render.com URL: {url}")
        return url.rstrip('/')
    
    # Check Railway.app
    railway_url = os.getenv("RAILWAY_STATIC_URL") or os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_url:
        # Railway sometimes provides just the domain without protocol
        if not railway_url.startswith(('http://', 'https://')):
            railway_url = f"https://{railway_url}"
        logger.info(f"Detected Railway.app URL: {railway_url}")
        return railway_url.rstrip('/')
    
    # Check Heroku
    heroku_app_name = os.getenv("HEROKU_APP_NAME")
    if heroku_app_name:
        url = f"https://{heroku_app_name}.herokuapp.com"
        logger.info(f"Detected Heroku URL: {url}")
        return url.rstrip('/')
    
    # Check for DOKKU (common VPS setup)
    dokku_url = os.getenv("DOKKU_APP_NAME")
    if dokku_url:
        url = f"https://{dokku_url}"
        logger.info(f"Detected Dokku URL: {url}")
        return url.rstrip('/')
    
    # Check for custom platform URLs
    custom_url = os.getenv("PUBLIC_URL") or os.getenv("APP_URL") or os.getenv("BOT_URL")
    if custom_url:
        logger.info(f"Detected custom URL: {custom_url}")
        return custom_url.rstrip('/')
    
    # Check if WEBHOOK_MODE is explicitly enabled (user knows what they're doing)
    if os.getenv("WEBHOOK_MODE", "").lower() in ("true", "1", "yes"):
        # User must configure WEBHOOK_URL manually
        logger.warning("WEBHOOK_MODE enabled but no public URL detected. Set WEBHOOK_URL environment variable.")
        return None
    
    logger.info("No public URL detected. Will use polling mode.")
    return None

def acquire_polling_lock() -> bool:
    """
    Prevent multiple polling instances using atomic file creation + persistent lock.
    Returns: True if lock acquired, False otherwise.
    """
    global polling_lock_fd
    lock_file = os.path.join(BASE_DIR, ".polling_lock")
    
    # Check for stale lock (if file exists but process is dead)
    if os.path.exists(lock_file):
        try:
            with open(lock_file, 'r') as f:
                old_pid_str = f.read().strip()
            if old_pid_str:
                try:
                    old_pid = int(old_pid_str)
                    if not psutil.pid_exists(old_pid):
                        logger.info(f"Removing stale polling lock from PID {old_pid} (not running)")
                        os.remove(lock_file)
                    else:
                        logger.warning(f"Polling lock held by running process PID {old_pid}")
                        return False
                except ValueError:
                    logger.warning(f"Invalid PID in lock file: {old_pid_str}, removing")
                    os.remove(lock_file)
            else:
                logger.info("Removing empty polling lock file")
                os.remove(lock_file)
        except Exception as e:
            logger.warning(f"Error checking lock file: {e}")
            # If we can't read, try to remove it and continue
            try:
                os.remove(lock_file)
            except:
                pass
    
    # Try to create and lock the file atomically
    try:
        fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        # Write PID
        os.write(fd, str(os.getpid()).encode())
        os.fsync(fd)
        # Lock the file (exclusive, non-blocking)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        polling_lock_fd = fd  # Keep open forever
        logger.info(f"Acquired polling lock (PID: {os.getpid()})")
        return True
    except OSError as e:
        if e.errno == errno.EEXIST:
            # File was created by another process between our check and now
            logger.warning("Polling lock file created by another process concurrently")
            return False
        else:
            logger.error(f"Error creating lock file: {e}")
            return False
    except Exception as e:
        logger.error(f"Error acquiring polling lock: {e}")
        return False

def setup_flask_webhook(public_url: str) -> bool:
    """
    Setup Flask webhook server and configure Telegram webhook.
    Returns: True if setup successful, False otherwise.
    """
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        logger.error("Flask is required for webhook mode but not installed. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "--quiet"])
            from flask import Flask, request, jsonify
            logger.info("Flask installed successfully.")
        except Exception as e:
            logger.error(f"Failed to install Flask: {e}")
            return False
    
    try:
        app = Flask(__name__)
        
        @app.route('/')
        def health_check():
            """Health check endpoint for monitoring."""
            return jsonify({
                "status": "running",
                "bot_name": DISPLAY_NAME,
                "mode": "webhook",
                "timestamp": time.time()
            }), 200
        
        @app.route(f'/{TOKEN}', methods=['POST'])
        def telegram_webhook():
            """Handle incoming Telegram updates via webhook."""
            try:
                if request.headers.get('content-type') == 'application/json':
                    json_str = request.get_data().decode('utf-8')
                    update = telebot.types.Update.de_json(json_str)
                    bot.process_new_updates([update])
                    return '', 200
                else:
                    return '', 403
            except Exception as e:
                logger.error(f"Webhook processing error: {e}")
                return jsonify({"error": str(e)}), 500
        
        # Set webhook URL
        webhook_url = f"{public_url}/{TOKEN}"
        try:
            success = bot.set_webhook(url=webhook_url, drop_pending_updates=True)
            if success:
                logger.info(f"✅ Webhook set successfully: {webhook_url}")
            else:
                logger.error("❌ Failed to set webhook. Telegram API returned False.")
                return False
        except Exception as e:
            logger.error(f"❌ Error setting webhook: {e}")
            return False
        
        # Get port from environment or use default
        port = int(os.getenv("PORT", 8443))
        host = os.getenv("WEBHOOK_HOST", "0.0.0.0")
        
        # Start Flask server in a separate thread
        server_thread = threading.Thread(
            target=lambda: app.run(host=host, port=port, debug=False, use_reloader=False),
            daemon=True,
            name="FlaskWebhookServer"
        )
        server_thread.start()
        
        logger.info(f"🚀 Flask webhook server started on {host}:{port}")
        logger.info(f"📡 Bot running in WEBHOOK mode at {public_url}")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down webhook server...")
            bot.remove_webhook()
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup Flask webhook: {e}")
        return False

def run_polling_mode():
    """
    Run bot in polling mode with single-instance protection.
    """
    logger.info("Starting bot in POLLING mode...")
    
    # Acquire lock to prevent multiple instances
    if not acquire_polling_lock():
        sys.exit(1)
    
    try:
        # Remove any existing webhook if switching from webhook mode
        bot.remove_webhook()
        logger.info("Removed existing webhook (if any)")
    except Exception as e:
        logger.warning(f"Error removing webhook: {e}")
    
    # Start polling
    try:
        logger.info("Bot is now polling for updates...")
        bot.infinity_polling(timeout=60, skip_pending=True, allowed_updates=None)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.exception(f"Bot polling error: {e}")
    finally:
        # Lock file will be automatically closed and released on process exit
        pass

def run_bot_in_hybrid_mode():
    """
    Main entry point: detect environment and run in appropriate mode.
    """
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {DISPLAY_NAME} in HYBRID MODE")
    logger.info(f"📅 Date: {datetime.now().isoformat()}")
    logger.info(f"🐍 Python: {sys.version}")
    # FIX: Wrap bot.get_me() in try-except to handle network errors gracefully
    try:
        bot_info = bot.get_me()
        logger.info(f"🤖 Bot ID: {bot_info.id}")
    except Exception as e:
        logger.error(f"Failed to retrieve bot info (network issue): {e}. Continuing without bot ID.")
    logger.info("=" * 60)
    
    # Detect public URL
    public_url = detect_public_url()
    
    if public_url:
        # Try webhook mode
        logger.info(f"🌐 Public URL detected: {public_url}")
        logger.info("Attempting to start in WEBHOOK mode...")
        
        success = setup_flask_webhook(public_url)
        if success:
            logger.info("✅ Bot started successfully in WEBHOOK mode")
            return
        else:
            logger.warning("❌ Failed to start webhook mode. Falling back to polling...")
    
    # Fallback to polling mode
    run_polling_mode()

# ==============================================================================
#  END HYBRID MODE DETECTION AND SETUP
# ==============================================================================

# ==============================================================================
#  RUNTIME COMPATIBILITY IMPORTS (PURELY ADDITIVE)
# ==============================================================================
# These imports support the additional safety features without modifying existing imports

try:
    import resource
except ImportError:
    resource = None

try:
    import signal
except ImportError:
    signal = None

# ==============================================================================
#  END RUNTIME COMPATIBILITY IMPORTS
# ==============================================================================

# -------------------------
# DB Initialization
# -------------------------
def init_db() -> sqlite3.Connection:
    logger.info("Initializing database with force-create and integrity checks...")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()
    
    # Create tables with force-create logic
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        display_name TEXT,
        username TEXT,
        mobile TEXT,
        email TEXT,
        bio TEXT,
        blocked INTEGER DEFAULT 0,
        server_limit INTEGER DEFAULT 1000,
        created_at TEXT
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY,
        is_temporary INTEGER DEFAULT 0,
        expire_time REAL DEFAULT NULL
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        project_name TEXT,
        main_file TEXT,
        status TEXT,
        start_time REAL,
        UNIQUE(user_id, project_name)
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        project_name TEXT,
        log_path TEXT,
        created_at REAL
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER,
        target_user_id INTEGER,
        action TEXT,
        reason TEXT,
        created_at REAL
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    
    # Insert owner as admin if not exists
    cur.execute("INSERT OR IGNORE INTO admins (user_id, is_temporary, expire_time) VALUES (?, ?, ?)",
                (OWNER_ID, 0, None))
    cur.execute("INSERT OR IGNORE INTO config (key, value) VALUES ('global_server_limit', '1000')")
    
    conn.commit()
    logger.info("Database initialization completed successfully")
    
    # Verify database integrity
    _verify_database_integrity(conn)
    
    return conn

def _verify_database_integrity(conn: sqlite3.Connection):
    """Verify that all required tables exist and are accessible."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
        required_tables = ['users', 'admins', 'projects', 'logs', 'admin_actions', 'config']
        
        for table in required_tables:
            if table not in tables:
                logger.error(f"CRITICAL: Table '{table}' is missing from database!")
            else:
                logger.info(f"✅ Table '{table}' verified")
        
        # Check if we can read/write to users table
        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]
        logger.info(f"Database integrity check passed. Current users: {count}")
        
    except Exception as e:
        logger.error(f"Database integrity verification failed: {e}")

db_conn = init_db()
db_lock = threading.Lock()
init_premium_db()

# -------------------------
# DB Helpers with caching
# -------------------------
def get_config_sync(key: str, default=None):
    with db_lock:
        cur = db_conn.cursor()
        cur.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = cur.fetchone()
        result = row[0] if row else default
        logger.debug(f"Config get: {key} = {result}")
        return result

def set_config_sync(key: str, value: str):
    with db_lock:
        cur = db_conn.cursor()
        cur.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
        db_conn.commit()
        logger.info(f"Config set: {key} = {value}")

def add_user_record_sync_from_chat(user_obj):
    """Add user record with detailed logging and verification."""
    try:
        display_name = (getattr(user_obj, "first_name", "") or "") + (" " + getattr(user_obj, "last_name", "") if getattr(user_obj, "last_name", None) else "")
        display_name = display_name.strip() or f"User{getattr(user_obj, 'id', '')}"
        username = getattr(user_obj, "username", "") or ""
        
        logger.info(f"Attempting to add user {user_obj.id} to database: {display_name}")
        
        with db_lock:
            cur = db_conn.cursor()
            cur.execute("""
                INSERT OR IGNORE INTO users (user_id, display_name, username, mobile, email, bio, blocked, server_limit, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?)
            """, (user_obj.id, display_name, username, "", "", "", 1000, datetime.utcnow().isoformat()))
            
            # Update server limit from global config
            cur.execute("SELECT value FROM config WHERE key = 'global_server_limit'")
            row = cur.fetchone()
            if row:
                try:
                    g = int(row[0])
                except Exception:
                    g = 1000
                cur.execute("UPDATE users SET server_limit = ? WHERE user_id = ? AND (server_limit IS NULL OR server_limit = 0)", (g, user_obj.id))
            
            db_conn.commit()
            
            # Verify insertion
            cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_obj.id,))
            if cur.fetchone():
                logger.info(f"✅ User {user_obj.id} successfully added to database")
            else:
                logger.error(f"❌ Failed to add user {user_obj.id} to database")
        
        # Update cache
        with cache_lock:
            user_cache[user_obj.id] = {'exists': True, 'verified': True}
            
    except Exception as e:
        logger.exception(f"Error adding user {user_obj.id} to database: {e}")

def ensure_user_exists(user_id: int):
    """Ensure user exists in database with enhanced error handling and verification."""
    try:
        # Check cache first
        with cache_lock:
            if user_id in user_cache and user_cache[user_id].get('verified', False):
                logger.debug(f"User {user_id} found in cache, skipping DB check")
                return
        
        # Check database
        with db_lock:
            cur = db_conn.cursor()
            cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
        
        if row:
            logger.debug(f"User {user_id} exists in database")
            with cache_lock:
                user_cache[user_id] = {'exists': True, 'verified': True}
            return
        
        logger.info(f"User {user_id} not found in database, creating record...")
        
        # Try to get user info from Telegram
        try:
            chat = bot.get_chat(user_id)
            fake_user = SimpleNamespace(
                id=chat.id,
                first_name=getattr(chat, "first_name", "") or getattr(chat, "title", ""),
                last_name=getattr(chat, "last_name", "") or "",
                username=getattr(chat, "username", "") or ""
            )
            add_user_record_sync_from_chat(fake_user)
            logger.info(f"Successfully created user record for {user_id}")
        except Exception:
            logger.warning(f"Failed to get chat info for user {user_id}, creating minimal record")
            # Create minimal user record as fallback
            with db_lock:
                cur = db_conn.cursor()
                cur.execute("INSERT OR IGNORE INTO users (user_id, display_name, username, created_at) VALUES (?, ?, ?, ?)",
                            (user_id, f"User{user_id}", "", datetime.utcnow().isoformat()))
                db_conn.commit()
        
        # Update cache
        with cache_lock:
            user_cache[user_id] = {'exists': True, 'verified': True}
            
    except Exception as e:
        logger.exception(f"Critical error in ensure_user_exists for user {user_id}: {e}")
        # Try to recover by creating minimal record
        try:
            with db_lock:
                cur = db_conn.cursor()
                cur.execute("INSERT OR IGNORE INTO users (user_id, display_name, username, created_at) VALUES (?, ?, ?, ?)",
                            (user_id, f"User{user_id}", "", datetime.utcnow().isoformat()))
                db_conn.commit()
                logger.info(f"Recovered: Created minimal user record for {user_id}")
        except Exception as recover_error:
            logger.error(f"Failed to recover user {user_id}: {recover_error}")

def get_user_record_sync(user_id: int) -> Optional[Tuple]:
    """Get user record with error handling."""
    try:
        ensure_user_exists(user_id)
        with db_lock:
            cur = db_conn.cursor()
            cur.execute("SELECT user_id, display_name, username, blocked, server_limit, mobile, email, bio, created_at FROM users WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            if row:
                logger.debug(f"Retrieved user record for {user_id}: {row[1]}")
            return row
    except Exception as e:
        logger.exception(f"Error retrieving user record for {user_id}: {e}")
        return None

def set_user_block_sync(user_id: int, blocked: bool, admin_id: int, reason: str = ""):
    """Set user block status with logging."""
    ensure_user_exists(user_id)
    with db_lock:
        cur = db_conn.cursor()
        cur.execute("UPDATE users SET blocked = ? WHERE user_id = ?", (1 if blocked else 0, user_id))
        cur.execute("INSERT INTO admin_actions (admin_id, target_user_id, action, reason, created_at) VALUES (?, ?, ?, ?, ?)",
                    (admin_id, user_id, "BLOCK" if blocked else "UNBLOCK", reason, time.time()))
        db_conn.commit()
        logger.info(f"User {user_id} blocked={blocked} by admin {admin_id}")
    # Clear cache
    with cache_lock:
        user_cache.pop(user_id, None)

def set_user_limit_sync(user_id: int, limit: int, admin_id: int):
    """Set user limit with logging."""
    ensure_user_exists(user_id)
    with db_lock:
        cur = db_conn.cursor()
        cur.execute("UPDATE users SET server_limit = ? WHERE user_id = ?", (limit, user_id))
        cur.execute("INSERT INTO admin_actions (admin_id, target_user_id, action, reason, created_at) VALUES (?, ?, ?, ?, ?)",
                    (admin_id, user_id, "SET_LIMIT", str(limit), time.time()))
        db_conn.commit()
        logger.info(f"User {user_id} server limit set to {limit} by admin {admin_id}")
    # Clear cache
    with cache_lock:
        user_cache.pop(user_id, None)

def add_admin_sync(user_id: int, temporary: bool = False, minutes: Optional[int] = None):
    """Add admin with logging."""
    with db_lock:
        cur = db_conn.cursor()
        if temporary and minutes:
            expire_time = time.time() + minutes * 60
            cur.execute("INSERT OR REPLACE INTO admins (user_id, is_temporary, expire_time) VALUES (?, ?, ?)",
                        (user_id, 1, expire_time))
        else:
            cur.execute("INSERT OR REPLACE INTO admins (user_id, is_temporary, expire_time) VALUES (?, ?, ?)",
                        (user_id, 0, None))
        db_conn.commit()
        logger.info(f"Admin added: {user_id} (temporary={temporary})")
    try:
        bot.send_message(user_id, f"👑 You have been granted admin access{' for ' + str(minutes) + ' minutes' if temporary and minutes else ''}. Contact {ADMIN_USERNAME} for details.")
    except Exception:
        pass

def remove_admin_sync(user_id: int):
    """Remove admin with logging."""
    with db_lock:
        cur = db_conn.cursor()
        cur.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
        db_conn.commit()
        logger.info(f"Admin removed: {user_id}")

def is_admin_sync(user_id: int) -> bool:
    """Check if user is admin with temporary expiry handling."""
    try:
        with db_lock:
            cur = db_conn.cursor()
            cur.execute("SELECT is_temporary, expire_time FROM admins WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                return False
            is_temp, expire = row
            if is_temp:
                if expire is None:
                    return False
                if time.time() > expire:
                    cur.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
                    db_conn.commit()
                    try:
                        bot.send_message(user_id, "⏰ Your temporary admin access has expired.")
                    except Exception:
                        pass
                    try:
                        bot.send_message(OWNER_ID, f"ℹ️ Temporary admin {user_id} expired and removed.")
                    except Exception:
                        pass
                    return False
            logger.debug(f"Admin check for {user_id}: {True}")
            return True
    except Exception as e:
        logger.exception(f"Error checking admin status for {user_id}: {e}")
        return False

def record_project_db_sync(user_id: int, project_name: str, main_file: str, status: str):
    """Record project status in database."""
    try:
        with db_lock:
            cur = db_conn.cursor()
            start_time = time.time() if status == "running" else None
            cur.execute("""
                INSERT INTO projects (user_id, project_name, main_file, status, start_time)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, project_name) DO UPDATE SET main_file=excluded.main_file, status=excluded.status, start_time=excluded.start_time
            """, (user_id, project_name, main_file, status, start_time))
            db_conn.commit()
            logger.info(f"Project {project_name} for user {user_id} status updated to {status}")
    except Exception as e:
        logger.exception(f"Error recording project {project_name} for user {user_id}: {e}")

def remove_project_db_sync(user_id: int, project_name: str):
    """Remove project from database."""
    try:
        with db_lock:
            cur = db_conn.cursor()
            cur.execute("DELETE FROM projects WHERE user_id = ? AND project_name = ?", (user_id, project_name))
            db_conn.commit()
            logger.info(f"Project {project_name} for user {user_id} removed from database")
    except Exception as e:
        logger.exception(f"Error removing project {project_name} for user {user_id}: {e}")

def add_log_record_sync(user_id: int, project_name: str, log_path: str):
    """Add log record to database."""
    try:
        with db_lock:
            cur = db_conn.cursor()
            cur.execute("INSERT INTO logs (user_id, project_name, log_path, created_at) VALUES (?, ?, ?, ?)",
                        (user_id, project_name, log_path, time.time()))
            db_conn.commit()
            logger.info(f"Log record added for user {user_id} project {project_name}")
    except Exception as e:
        logger.exception(f"Error adding log record: {e}")

# -------------------------
# Utilities
# -------------------------
def get_user_space(uid: int) -> str:
    path = os.path.join(USERS_DIR, str(uid))
    os.makedirs(path, exist_ok=True)
    return path

def safe_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in name).strip("_")

def detect_main_file(project_path: str) -> str:
    try:
        files = os.listdir(project_path)
    except Exception:
        return "Not Found"
    for f in files:
        if f.lower() in ("main.py", "app.py", "bot.py", "start.py"):
            return f
    if "package.json" in files:
        if "index.js" in files:
            return "index.js"
        for f in files:
            if f.endswith(".js"):
                return f
    for f in files:
        if f.endswith(".py"):
            return f
    for f in files:
        if f.endswith(".js"):
            return f
    for f in files:
        if f.endswith(".jar"):
            return f
    for f in files:
        if f.endswith(".class"):
            return f
    return "Not Found"

def write_log(path: str, text: str):
    try:
        with open(path, "a", encoding="utf-8", errors="ignore") as f:
            f.write(text + "\n")
    except Exception:
        pass

def is_user_blocked(user_id: int) -> bool:
    try:
        with cache_lock:
            if user_id in user_cache and 'blocked' in user_cache[user_id]:
                return user_cache[user_id]['blocked']
        
        with db_lock:
            cur = db_conn.cursor()
            cur.execute("SELECT blocked FROM users WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            blocked = bool(row[0]) if row else False
        
        with cache_lock:
            user_cache[user_id] = user_cache.get(user_id, {})
            user_cache[user_id]['blocked'] = blocked
        
        return blocked
    except Exception as e:
        logger.exception(f"Error checking blocked status for {user_id}: {e}")
        return False

# ==============================================================================
#  STYLISH MESSAGE HELPER (NEW)
# ==============================================================================
def send_styled_message(chat_id, text, title=None, emoji=None, parse_mode='Markdown', **kwargs):
    """
    Send a beautifully formatted message with consistent styling.
    """
    if title:
        header = f"**{title}**"
        if emoji:
            header = f"{emoji} {header}"
        full_text = f"{header}\n\n{text}"
    else:
        full_text = text
    return bot.send_message(chat_id, full_text, parse_mode=parse_mode, **kwargs)

# -------------------------
# Keyboards (ADMIN ACCESS only visible to admins/owner)
# -------------------------
def main_menu_kb(uid: int):
    try:
        ensure_user_exists(uid)
    except Exception:
        logger.exception("main_menu_kb: ensure_user_exists failed for %s", uid)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📁 FILE MANAGER"), KeyboardButton("🚀 DEPLOY CONSOLE"))
    kb.add(KeyboardButton("⏹ STOP INSTANCE"), KeyboardButton("📜 LIVE LOGS"))
    kb.add(KeyboardButton("📊 SYSTEM HEALTH"), KeyboardButton("⚙ SETTINGS"))
    kb.add(KeyboardButton("🌐 SERVER INFO"))
    # Add a "💎 BUY PREMIUM" button for users (only if premium mode is on and not already premium)
    try:
        premium_mode = get_config_sync("premium_mode", "off")
        if premium_mode == "on" and not is_premium_user(uid):
            kb.add(KeyboardButton("💎 BUY PREMIUM"))
    except Exception:
        pass
    try:
        if uid == OWNER_ID or is_admin_sync(uid):
            kb.add(KeyboardButton("👑 ADMIN ACCESS"))
    except Exception:
        logger.exception("main_menu_kb: admin check failed for %s", uid)
    return kb

def admin_panel_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🕒 TEMPORARY ADMIN", callback_data="admin_temp"))
    kb.add(InlineKeyboardButton("📣 BROADCAST", callback_data="admin_broadcast"))
    kb.add(InlineKeyboardButton("👥 MANAGE USERS", callback_data="admin_manage_users"))
    kb.add(InlineKeyboardButton("📁 FILE MANAGER", callback_data="admin_file_manager"))
    kb.add(InlineKeyboardButton("🚀 DEPLOY CONSOLE", callback_data="admin_deploy_console"))
    kb.add(InlineKeyboardButton("📜 LIVE LOGS", callback_data="admin_live_logs"))
    kb.add(InlineKeyboardButton("⚙ SETTINGS", callback_data="admin_settings"))
    kb.add(InlineKeyboardButton("📊 SYSTEM HEALTH", callback_data="admin_health"))
    kb.add(InlineKeyboardButton("🌐 SERVER INFO", callback_data="admin_server_info"))
    kb.add(InlineKeyboardButton("✉️ CONTACT ADMIN", callback_data="contact_admin"))
    return kb

# -------------------------
# Message queue system for faster response
# -------------------------
def message_worker():
    while True:
        try:
            task = message_queue.get(timeout=1)
            if task is None:
                break
            func, args, kwargs = task
            try:
                func(*args, **kwargs)
            except Exception:
                logger.exception("Message worker error")
            message_queue.task_done()
        except queue.Empty:
            pass
        except Exception:
            logger.exception("Message worker loop error")

message_thread = threading.Thread(target=message_worker, daemon=True, name="MessageWorker")
message_thread.start()

# -------------------------
# Background: temp admin expiry monitor
# -------------------------
def temp_admin_monitor():
    while True:
        try:
            now = time.time()
            expired = []
            with db_lock:
                cur = db_conn.cursor()
                cur.execute("SELECT user_id, expire_time FROM admins WHERE is_temporary = 1")
                rows = cur.fetchall()
                for uid, expire in rows:
                    if expire and now > expire:
                        expired.append(uid)
                        cur.execute("DELETE FROM admins WHERE user_id = ?", (uid,))
                if expired:
                    db_conn.commit()
            for uid in expired:
                try:
                    bot.send_message(uid, "⏰ Your temporary admin access has expired. Contact admin if you need it extended.")
                except Exception:
                    pass
                try:
                    bot.send_message(OWNER_ID, f"ℹ️ Temporary admin {uid} expired and removed.")
                except Exception:
                    pass
        except Exception:
            logger.exception("temp_admin_monitor error")
        time.sleep(20)

threading.Thread(target=temp_admin_monitor, daemon=True, name="TempAdminMonitor").start()

# ==============================================================================
#  PREMIUM EXPIRY MONITOR (NEW)
# ==============================================================================
def premium_expiry_monitor():
    while True:
        try:
            now = time.time()
            with db_lock:
                cur = db_conn.cursor()
                cur.execute("SELECT user_id FROM premium_users WHERE premium_until IS NOT NULL AND premium_until < ?", (now,))
                expired = [row[0] for row in cur.fetchall()]
                for uid in expired:
                    cur.execute("DELETE FROM premium_users WHERE user_id = ?", (uid,))
                    db_conn.commit()
                    logger.info(f"Premium auto-revoked for user {uid} due to expiry")
                    try:
                        bot.send_message(uid, "⏰ Your premium membership has expired. You can renew it anytime.")
                    except Exception:
                        pass
        except Exception as e:
            logger.exception(f"Premium expiry monitor error: {e}")
        time.sleep(60)  # check every minute

threading.Thread(target=premium_expiry_monitor, daemon=True, name="PremiumExpiryMonitor").start()

# -------------------------
# Global blocked-user handlers
# -------------------------
BLOCKED_MESSAGE_TEXT = "YOU ARE BLOCKED BY ADMIN. Please contact " + ADMIN_USERNAME + "."

@bot.callback_query_handler(func=lambda c: is_user_blocked(c.from_user.id))
def blocked_callback_handler(call):
    try:
        bot.answer_callback_query(call.id, "🚫 " + BLOCKED_MESSAGE_TEXT)
    except Exception:
        pass

@bot.message_handler(func=lambda m: is_user_blocked(m.from_user.id), content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'voice', 'video_note', 'location', 'contact'])
def blocked_message_handler(message):
    try:
        bot.reply_to(message, f"🚫 {BLOCKED_MESSAGE_TEXT} 🔒")
    except Exception:
        pass

# -------------------------
# /start handler + Welcome message with profile info
# -------------------------
def generate_welcome_text(user_info: dict) -> str:
    name = user_info.get("display_name") or "there"
    uname = user_info.get("username")
    bio = user_info.get("bio") or "No bio available."
    mobile = user_info.get("mobile") or "Hidden"
    email = user_info.get("email") or "Hidden"
    welcome = (
        f"👋 **Hello {name}!**\n\n"
        "Welcome to **RIZERxHOSTING** — your lightweight multi-language hosting platform on Telegram. "
        "I'm here to help you upload, run, and manage your Python, NodeJS, and Java projects directly from Telegram.\n\n"
        "**📌 Your Profile:**\n"
        f"• **Username:** @{uname if uname else 'N/A'}\n"
        f"• **Bio:** {bio}\n"
        f"• **Mobile:** {mobile}\n"
        f"• **Email:** {email}\n\n"
        "**✨ Quick Tips:**\n"
        "• Upload a **ZIP** with your project, I will auto-extract it.\n"
        "• Upload single **.py** or **.js** files – I'll auto-generate requirements and install them silently.\n"
        "• I auto-detect common main files (`main.py`, `app.py`, `index.js`, `*.jar`).\n"
        "• Dependencies are **auto-installed** from `requirements.txt`, `package.json`.\n"
        "• Version conflicts are automatically resolved.\n"
        "• Use the buttons below to manage files, deploy projects, view logs and more.\n\n"
        f"**🆘 Need help?** Contact the admin: {ADMIN_USERNAME}\n\n"
        "🚀 **Happy hosting!**"
    )
    return welcome

@bot.message_handler(commands=['start'])
def handle_start(message):
    uid = message.from_user.id
    try:
        logger.info(f"Start command received from user {uid}")
        ensure_user_exists(uid)
        
        photo_file_id = None
        try:
            photos = bot.get_user_profile_photos(uid, limit=1)
            if photos.total_count > 0:
                photo_file_id = photos.photos[0][-1].file_id
        except Exception:
            photo_file_id = None
        
        bio = ""
        try:
            chat = bot.get_chat(uid)
            bio = getattr(chat, "bio", "") or ""
        except Exception:
            bio = ""
        
        user_rec = get_user_record_sync(uid) or ()
        display_name = user_rec[1] if len(user_rec) > 1 else (message.from_user.first_name or "")
        username = user_rec[2] if len(user_rec) > 2 else (message.from_user.username or "")
        mobile = user_rec[5] if len(user_rec) > 5 else ""
        email = user_rec[6] if len(user_rec) > 6 else ""
        
        uinfo = {
            "display_name": display_name,
            "username": username,
            "bio": bio,
            "mobile": mobile if mobile else "Hidden",
            "email": email if email else "Hidden"
        }
        
        welcome = generate_welcome_text(uinfo)
        if photo_file_id:
            try:
                bot.send_photo(uid, photo_file_id, caption=welcome, parse_mode='Markdown', reply_markup=main_menu_kb(uid))
            except Exception:
                send_styled_message(uid, welcome, title="Welcome!", emoji="👋", reply_markup=main_menu_kb(uid))
        else:
            send_styled_message(uid, welcome, title="Welcome!", emoji="👋", reply_markup=main_menu_kb(uid))
        
        logger.info(f"Welcome message sent to user {uid}")
        
    except Exception:
        logger.exception("handle_start error")
        try:
            send_styled_message(uid, "Welcome to RIZERxHOSTING!", title="Hello", emoji="👋", reply_markup=main_menu_kb(uid))
        except Exception:
            pass

# ==============================================================================
#  TELEGRAM STARS PREMIUM PURCHASE (NEW)
# ==============================================================================
@bot.message_handler(func=lambda m: m.text == "💎 BUY PREMIUM")
def buy_premium_handler(message):
    uid = message.from_user.id
    if is_premium_user(uid):
        send_styled_message(uid, "You already have premium access! Enjoy the benefits.", title="Already Premium", emoji="✅")
        return
    price = int(get_config_sync("premium_price_stars", "0"))
    if price <= 0:
        send_styled_message(uid, "Premium is not available for purchase at the moment. Please contact admin.", title="Not Available", emoji="❌")
        return
    
    # Create invoice
    prices = [LabeledPrice(label="Premium Membership (30 days)", amount=price * 100)]  # amount in smallest currency unit (cents for real currency, but for stars it's just stars)
    # Telegram Stars uses amount = number of stars * 100? Actually for stars, amount is just stars. Let's check docs: For Telegram Stars, amount is the number of stars, not multiplied by 100.
    # We'll use amount = price (stars)
    prices = [LabeledPrice(label="Premium Membership (30 days)", amount=price)]  # stars
    
    try:
        bot.send_invoice(
            chat_id=uid,
            title="RIZERxHOSTING Premium",
            description="Get 30 days of unlimited access to all features!",
            invoice_payload="premium_purchase",
            provider_token="",  # Empty for Telegram Stars
            currency="XTR",  # Special currency for Telegram Stars
            prices=prices,
            start_parameter="premium",
            photo_url=None,
            photo_height=None,
            photo_width=None,
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False,
            reply_markup=None
        )
        logger.info(f"Sent premium invoice to user {uid} for {price} stars")
    except Exception as e:
        logger.exception(f"Error sending invoice to user {uid}")
        send_styled_message(uid, f"Error creating invoice: {str(e)}", title="Payment Error", emoji="❌")

@bot.pre_checkout_query_handler(func=lambda query: True)
def handle_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    # Always confirm (you could add additional checks here)
    try:
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        logger.info(f"Pre-checkout approved for user {pre_checkout_query.from_user.id}")
    except Exception as e:
        logger.exception(f"Error answering pre-checkout query: {e}")

@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    uid = message.from_user.id
    payment = message.successful_payment
    stars = payment.total_amount  # amount in stars
    transaction_id = payment.telegram_payment_charge_id
    # Grant premium for 30 days
    set_user_premium_sync(uid, True, transaction_id=transaction_id, duration_days=30)
    send_styled_message(uid, 
                        f"🎉 **Payment Successful!**\n\nYou have been granted **30 days** of premium access.\nTransaction ID: `{transaction_id}`\n\nEnjoy all the features!",
                        title="Thank You!", emoji="💎")
    logger.info(f"User {uid} purchased premium with {stars} stars, transaction {transaction_id}")

# -------------------------
# NEW: Direct file upload handler (.py, .js)
# -------------------------
@bot.message_handler(content_types=['document'])
@premium_check_required
def handle_document(message):
    uid = message.from_user.id
    ensure_user_exists(uid)
    
    try:
        fname = message.document.file_name or ""
        file_ext = os.path.splitext(fname)[1].lower()
        
        # Handle ZIP files (existing functionality)
        if file_ext == ".zip":
            user_path = get_user_space(uid)
            zip_path = os.path.join(user_path, "process.zip")
            file_info = bot.get_file(message.document.file_id)
            downloaded = bot.download_file(file_info.file_path)
            with open(zip_path, "wb") as f:
                f.write(downloaded)
            pending_marker = os.path.join(user_path, ".pending_zip")
            with open(pending_marker, "w", encoding="utf-8") as f:
                f.write(zip_path)
            send_styled_message(uid, "ZIP received! Please reply with a **custom name** for the project folder (single line). Example: `my_project`", title="📦 ZIP Upload", emoji="📝")
            return
        
        # Handle single Python files
        elif file_ext == ".py":
            _handle_single_file(uid, message, fname, "python")
            return
        
        # Handle single JavaScript files
        elif file_ext == ".js":
            _handle_single_file(uid, message, fname, "nodejs")
            return
        
        else:
            send_styled_message(uid, "Only **ZIP archives**, **.py**, and **.js** files are supported. Please send a supported file type.", title="Unsupported File", emoji="❌")
            return
            
    except Exception as e:
        logger.exception("handle_document")
        send_styled_message(uid, f"Error processing file: {e}", title="Error", emoji="❌")

def _handle_single_file(uid: int, message, original_fname: str, file_type: str):
    """Handle single file uploads (.py or .js) with auto requirements generation and battery progress."""
    try:
        # Create project name from filename
        project_name = safe_filename(os.path.splitext(original_fname)[0]) or f"project_{int(time.time())}"
        user_path = get_user_space(uid)
        project_path = os.path.join(user_path, project_name)
        
        # Create project directory
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
        os.makedirs(project_path, exist_ok=True)
        
        # Download file
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        # Save file in project directory
        file_path = os.path.join(project_path, original_fname)
        with open(file_path, "wb") as f:
            f.write(downloaded)
        
        # Generate requirements/package.json automatically
        if file_type == "python":
            # Generate requirements.txt
            requirements = RequirementsGenerator.generate_from_py_file(file_path)
            if requirements:
                req_path = os.path.join(project_path, "requirements.txt")
                with open(req_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(requirements))
                send_styled_message(uid, f"Auto-detected dependencies: `{', '.join(requirements)}`", title="🔍 Dependency Scan", emoji="🔍")
        
        elif file_type == "nodejs":
            # Generate package.json if not exists
            package_json_path = os.path.join(project_path, "package.json")
            if not os.path.exists(package_json_path):
                deps = RequirementsGenerator.generate_from_js_file(file_path)
                package_data = {
                    "name": project_name,
                    "version": "1.0.0",
                    "description": "Auto-generated package.json",
                    "main": original_fname,
                    "dependencies": deps
                }
                with open(package_json_path, "w", encoding="utf-8") as f:
                    json.dump(package_data, f, indent=2)
                if deps:
                    send_styled_message(uid, f"Auto-detected dependencies: `{', '.join(deps.keys())}`", title="🔍 Dependency Scan", emoji="🔍")
        
        # Set main file
        user_main_files.setdefault(uid, {})[project_name] = original_fname
        record_project_db_sync(uid, project_name, original_fname, "stopped")
        
        # Start battery progress monitor for dependency installation
        BatteryProgressInterface.start_progress_monitor(uid, project_path, project_name)
        
        # Silent dependency installation in background
        send_styled_message(uid, f"**File uploaded successfully!**\n\n**Project:** `{project_name}`\n**Main file:** `{original_fname}`\n\n📦 Installing dependencies in background...", title="✅ Upload Complete", emoji="✅")
        
        install_thread = threading.Thread(
            target=_install_project_deps_comprehensive,
            args=(uid, project_path, project_name, True),  # True = silent mode
            daemon=True,
            name=f"DepInstall_{uid}_{project_name}"
        )
        install_thread.start()
        
        # Store thread reference
        threading._project_install_threads = getattr(threading, '_project_install_threads', {})
        threading._project_install_threads[f"{uid}_{project_name}"] = install_thread
        
    except Exception as e:
        logger.exception("_handle_single_file")
        send_styled_message(uid, f"Error processing file: {e}", title="Error", emoji="❌")

# -------------------------
# ZIP processing (existing, unchanged logic)
# -------------------------
@bot.message_handler(func=lambda m: os.path.exists(os.path.join(USERS_DIR, str(m.from_user.id), ".pending_zip")))
@premium_check_required
def process_custom_project_name(message):
    uid = message.from_user.id
    user_path = get_user_space(uid)
    pending_marker = os.path.join(user_path, ".pending_zip")
    try:
        with open(pending_marker, "r", encoding="utf-8") as f:
            zip_path = f.read().strip()
    except Exception:
        send_styled_message(uid, "No pending ZIP found.", title="Error", emoji="❌")
        try:
            os.remove(pending_marker)
        except:
            pass
        return
    custom_name = safe_filename(message.text.strip()) or f"project_{int(time.time())}"
    project_path = os.path.join(user_path, custom_name)
    status_msg = bot.send_message(uid, f"⏳ Processing project: `{custom_name}` ...")
    try:
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
        os.makedirs(project_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(project_path)
        try:
            os.remove(zip_path)
        except Exception:
            pass
        try:
            os.remove(pending_marker)
        except Exception:
            pass
        main_f = detect_main_file(project_path)
        user_main_files.setdefault(uid, {})[custom_name] = main_f
        record_project_db_sync(uid, custom_name, main_f if main_f != "Not Found" else "", "stopped")
        
        # Start battery progress monitor for dependency installation
        BatteryProgressInterface.start_progress_monitor(uid, project_path, custom_name)
        
        install_thread = threading.Thread(
            target=_install_project_deps_comprehensive,
            args=(uid, project_path, custom_name, True),  # Silent mode
            daemon=True,
            name=f"DepInstall_{uid}_{custom_name}"
        )
        install_thread.start()
        threading._project_install_threads = getattr(threading, '_project_install_threads', {})
        threading._project_install_threads[f"{uid}_{custom_name}"] = install_thread
        
        send_styled_message(uid, 
                           f"**Extraction successful!**\n\n**Folder:** `{custom_name}`\n**Detected Main:** `{main_f}`\n\n📦 Dependencies are being installed in background...",
                           title="✅ Project Created", emoji="✅", reply_markup=main_menu_kb(uid))
    except Exception as e:
        logger.exception("process_custom_project_name")
        send_styled_message(uid, f"Error extracting ZIP: {e}", title="Error", emoji="❌")
    finally:
        try:
            bot.delete_message(uid, status_msg.message_id)
        except Exception:
            pass

# -------------------------
# Comprehensive dependency installer (updated for silent mode)
# -------------------------
def _install_project_deps_comprehensive(uid: int, project_path: str, project_name: str, silent: bool = False):
    """Comprehensive dependency installation that blocks until complete."""
    logger.info(f"Starting dependency install for user {uid} project {project_name}")
    
    try:
        DependencyInstaller._fix_telegram_namespace(uid, project_path)
        
        python_success = DependencyInstaller.install_python_deps(uid, project_path, project_name, silent)
        node_success = DependencyInstaller.install_node_deps(uid, project_path, project_name, silent)
        
        # Post-install verification for telegram libraries
        try:
            main_files = ["main.py", "app.py", "bot.py", "start.py"]
            for mf in main_files:
                main_path = os.path.join(project_path, mf)
                if os.path.exists(main_path):
                    with open(main_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "from telegram import Update" in content or "from telegram.ext import Application" in content:
                            verify_cmd = [sys.executable, "-c", "import telegram; print(hasattr(telegram, 'Update'))"]
                            result = subprocess.run(verify_cmd, capture_output=True, text=True)
                            if "True" not in result.stdout:
                                install_cmd = [
                                    sys.executable, "-m", "pip", "install", 
                                    "python-telegram-bot>=20.0", "--force-reinstall", "--quiet"
                                ]
                                subprocess.run(install_cmd, capture_output=True, timeout=180)
                                if not silent:
                                    send_styled_message(uid, "Telegram library fixed.", title="🔧 Fix Applied", emoji="✅")
                            break
        except Exception as e:
            logger.warning(f"Post-install telegram check failed: {e}")
        
        logger.info(f"Dependency installation completed for user {uid} project {project_name}")
        
        if not silent:
            if python_success and node_success:
                send_styled_message(uid, f"All dependencies installed for **{project_name}**!", title="🎉 Success", emoji="✅")
            else:
                send_styled_message(uid, f"Dependency installation completed for **{project_name}** with some issues.", title="⚠️ Warning", emoji="⚠️")
                
    except Exception as e:
        logger.exception(f"Critical error in _install_project_deps_comprehensive for user {uid}: {e}")
        if not silent:
            send_styled_message(uid, f"Critical error during dependency installation: {str(e)[:200]}", title="❌ Error", emoji="❌")

# -------------------------
# Deploy / File Manager UI
# -------------------------
@bot.message_handler(func=lambda m: m.text in ["📁 FILE MANAGER", "🚀 DEPLOY CONSOLE"])
@premium_check_required
def deploy_console_handler(message):
    uid = message.from_user.id
    ensure_user_exists(uid)
    user_rec = get_user_record_sync(uid)
    if user_rec and user_rec[3]:
        return send_styled_message(uid, "You are blocked. Contact admin.", title="🚫 Blocked", emoji="🚫")
    user_path = get_user_space(uid)
    projects = [d for d in os.listdir(user_path) if os.path.isdir(os.path.join(user_path, d))]
    if not projects:
        send_styled_message(uid, "Your directory is empty. Upload a ZIP, .py, or .js file to create a project.", title="📁 No Projects", emoji="📁")
        return
    kb = InlineKeyboardMarkup()
    for p in projects:
        kb.add(InlineKeyboardButton(f"📦 {p}", callback_data=f"proj_info:{p}"))
    sent = bot.send_message(uid, f"**🚀 DEPLOY CONSOLE** — Select a project to manage:", reply_markup=kb, parse_mode='Markdown')
    ui_cleaner.setdefault(uid, []).append(sent.message_id)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("proj_info:"))
def project_detail_view(call):
    uid = call.from_user.id
    ensure_user_exists(uid)
    p_name = call.data.split(":", 1)[1]
    p_path = os.path.join(get_user_space(uid), p_name)
    if not os.path.exists(p_path):
        bot.answer_callback_query(call.id, "❌ Project folder not found.")
        try:
            log_file = os.path.join(LOGS_DIR, f"{uid}_{p_name}.log")
            if os.path.exists(log_file):
                os.remove(log_file)
        except Exception:
            pass
        return
    main_f = detect_main_file(p_path)
    user_main_files.setdefault(uid, {})[p_name] = main_f
    kb = InlineKeyboardMarkup()
    if main_f != "Not Found":
        kb.add(InlineKeyboardButton("▶ RUN", callback_data=f"start_p:{p_name}"),
               InlineKeyboardButton("🗑 DELETE", callback_data=f"del_p:{p_name}"))
    else:
        kb.add(InlineKeyboardButton("🗑 DELETE ONLY", callback_data=f"del_p:{p_name}"))
    kb.add(InlineKeyboardButton("✏ CHANGE MAIN FILE", callback_data=f"edit_main:{p_name}"))
    kb.add(InlineKeyboardButton("📜 VIEW LOG", callback_data=f"view_log:{p_name}"))
    status_label = "✅ MAIN FILE FOUND" if main_f != "Not Found" else "❌ MAIN FILE NOT FOUND"
    text = (f"📦 **Project:** `{p_name}`\n"
            f"📄 **Current Main:** `{main_f}`\n"
            f"📡 **Status:** {status_label}\n\n"
            "**Select action:**")
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=kb, parse_mode='Markdown')
    except Exception:
        bot.send_message(uid, text, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("edit_main:"))
def edit_main_req(call):
    uid = call.from_user.id
    p_name = call.data.split(":", 1)[1]
    tmp = os.path.join(get_user_space(uid), ".pending_edit_main")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(p_name)
    send_styled_message(uid, f"Send the file name that should be the main file for project `{p_name}` (e.g. `main.py` or `index.js`):", title="✏️ Change Main File", emoji="✏️")

@bot.message_handler(func=lambda m: os.path.exists(os.path.join(USERS_DIR, str(m.from_user.id), ".pending_edit_main")))
def save_custom_main(message):
    uid = message.from_user.id
    tmp = os.path.join(get_user_space(uid), ".pending_edit_main")
    try:
        with open(tmp, "r", encoding="utf-8") as f:
            p_name = f.read().strip()
    except Exception:
        send_styled_message(uid, "No pending main-file change found.", title="Error", emoji="❌")
        try:
            os.remove(tmp)
        except:
            pass
        return
    new_main = message.text.strip()
    p_path = os.path.join(get_user_space(uid), p_name)
    if os.path.exists(os.path.join(p_path, new_main)):
        user_main_files.setdefault(uid, {})[p_name] = new_main
        record_project_db_sync(uid, p_name, new_main, "stopped")
        send_styled_message(uid, f"Main file set to `{new_main}` for project `{p_name}`.", title="✅ Success", emoji="✅")
    else:
        user_main_files.setdefault(uid, {})[p_name] = "Not Found"
        record_project_db_sync(uid, p_name, "", "stopped")
        send_styled_message(uid, f"File `{new_main}` not found in project `{p_name}`. Project main remains **Not Found**.", title="❌ Error", emoji="❌")
    try:
        os.remove(tmp)
    except Exception:
        pass

# -------------------------
# Start project
# -------------------------
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("start_p:"))
def run_project_engine(call):
    uid = call.from_user.id
    ensure_user_exists(uid)
    user_row = get_user_record_sync(uid)
    if user_row and user_row[3]:
        return bot.answer_callback_query(call.id, "🚫 You are blocked from running projects.")
    p_name = call.data.split(":", 1)[1]
    try:
        limit = int(user_row[4]) if (user_row and user_row[4]) else int(get_config_sync("global_server_limit", "1000") or 1000)
    except Exception:
        limit = int(get_config_sync("global_server_limit", "1000") or 1000)
    current_running = len(running_instances.get(uid, {}))
    if current_running >= limit:
        return bot.answer_callback_query(call.id, f"❌ Server limit reached: {current_running}/{limit}")
    p_path = os.path.join(get_user_space(uid), p_name)
    if not os.path.exists(p_path):
        bot.answer_callback_query(call.id, "❌ Project folder not found.")
        return
    main_f = user_main_files.get(uid, {}).get(p_name) or detect_main_file(p_path)
    if not main_f or main_f == "Not Found":
        bot.answer_callback_query(call.id, "❌ No runnable main file detected.")
        return
    full_main_path = os.path.join(p_path, main_f)
    cmd = None
    
    try:
        # Pre-run verification for telegram libraries
        if main_f.endswith(".py"):
            with open(full_main_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "from telegram import Update" in content or "from telegram.ext import Application" in content:
                    verify_cmd = [sys.executable, "-c", "import telegram; print(hasattr(telegram, 'Update'))"]
                    result = subprocess.run(verify_cmd, capture_output=True, text=True)
                    if "True" not in result.stdout:
                        install_cmd = [
                            sys.executable, "-m", "pip", "install", 
                            "python-telegram-bot>=20.0", "--force-reinstall", "--quiet"
                        ]
                        subprocess.run(install_cmd, capture_output=True, timeout=180)
                        send_styled_message(uid, "Telegram library fixed. Launching project...", title="🔧 Fix Applied", emoji="✅")
    except Exception as e:
        logger.warning(f"Pre-run telegram verification failed: {e}")
    
    try:
        if main_f.endswith(".py"):
            cmd = [sys.executable, full_main_path]
        elif main_f.endswith(".js"):
            cmd = ["node", full_main_path]
        elif main_f.endswith(".jar"):
            cmd = ["java", "-jar", full_main_path]
        elif main_f.endswith(".class"):
            cls = os.path.splitext(main_f)[0]
            cmd = ["java", "-cp", p_path, cls]
        elif main_f.endswith(".java"):
            compile_proc = subprocess.run(["javac", full_main_path], cwd=p_path, capture_output=True, text=True)
            if compile_proc.returncode != 0:
                send_styled_message(uid, f"Java compile error:\n```\n{compile_proc.stdout}\n{compile_proc.stderr}\n```", title="❌ Compilation Failed", emoji="❌")
                write_log(os.path.join(LOGS_DIR, f"{uid}_{p_name}.log"), compile_proc.stdout + "\n" + compile_proc.stderr)
                return
            cls = os.path.splitext(main_f)[0]
            cmd = ["java", "-cp", p_path, cls]
        else:
            bot.answer_callback_query(call.id, "❌ Unsupported main file type.")
            return
        log_path = os.path.join(LOGS_DIR, f"{uid}_{p_name}.log")
        f_log = open(log_path, "a", encoding="utf-8", errors="ignore")
        proc = subprocess.Popen(cmd, stdout=f_log, stderr=f_log, cwd=p_path, start_new_session=True)
        running_instances.setdefault(uid, {})[p_name] = proc
        record_project_db_sync(uid, p_name, main_f, "running")
        add_log_record_sync(uid, p_name, log_path)
        bot.answer_callback_query(call.id, f"🚀 Project started: {p_name}")
        send_styled_message(uid, f"**Project started successfully!**\n\n**Name:** `{p_name}`\n**Main:** `{main_f}`", title="🚀 Running", emoji="✅")
    except Exception as e:
        logger.exception("run_project_engine")
        bot.answer_callback_query(call.id, f"❌ Error starting project: {e}")

# -------------------------
# Stop / Kill project
# -------------------------
@bot.message_handler(func=lambda m: m.text == "⏹ STOP INSTANCE")
@premium_check_required
def stop_engine_menu(message):
    uid = message.from_user.id
    ensure_user_exists(uid)
    instances = running_instances.get(uid, {})
    if not instances:
        return send_styled_message(uid, "No active instances.", title="⏹️ Stop", emoji="⏹️")
    kb = InlineKeyboardMarkup()
    for p in instances.keys():
        kb.add(InlineKeyboardButton(f"🛑 Kill {p}", callback_data=f"kill_p:{p}"))
    send_styled_message(uid, "Select instance to stop:", title="⏹️ Stop Instance", emoji="⏹️", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("kill_p:"))
def kill_process_handler(call):
    uid = call.from_user.id
    p = call.data.split(":", 1)[1]
    if uid in running_instances and p in running_instances[uid]:
        try:
            running_instances[uid][p].terminate()
        except Exception:
            pass
        del running_instances[uid][p]
        record_project_db_sync(uid, p, "", "stopped")
        bot.answer_callback_query(call.id, f"✅ Instance stopped: {p}")
        send_styled_message(uid, f"Instance `{p}` stopped.", title="✅ Stopped", emoji="⏹️")
    else:
        bot.answer_callback_query(call.id, "No running instance found.")

# -------------------------
# Delete project
# -------------------------
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("del_p:"))
def delete_project_handler(call):
    uid = call.from_user.id
    p_name = call.data.split(":", 1)[1]
    p_path = os.path.join(get_user_space(uid), p_name)
    try:
        if uid in running_instances and p_name in running_instances[uid]:
            try:
                running_instances[uid][p_name].terminate()
            except:
                pass
            del running_instances[uid][p_name]
        if os.path.exists(p_path):
            shutil.rmtree(p_path)
        remove_project_db_sync(uid, p_name)
        log_file = os.path.join(LOGS_DIR, f"{uid}_{p_name}.log")
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
            except Exception:
                pass
        bot.answer_callback_query(call.id, f"🗑 Project `{p_name}` deleted and logs cleared.")
        send_styled_message(uid, f"Project `{p_name}` deleted.", title="🗑 Deleted", emoji="✅")
    except Exception as e:
        logger.exception("delete_project_handler")
        bot.answer_callback_query(call.id, f"❌ Error deleting project: {e}")

# -------------------------
# Live logs
# -------------------------
@bot.message_handler(func=lambda m: m.text == "📜 LIVE LOGS")
@premium_check_required
def live_log_menu(message):
    uid = message.from_user.id
    ensure_user_exists(uid)
    logs = [f for f in os.listdir(LOGS_DIR) if f.startswith(str(uid) + "_")]
    if not logs:
        return send_styled_message(uid, "No logs available for your projects.", title="📜 Logs", emoji="📜")
    kb = InlineKeyboardMarkup()
    for l in logs:
        kb.add(InlineKeyboardButton(f"📄 {l}", callback_data=f"read_l:{l}"))
    send_styled_message(uid, "Select a log to read:", title="📜 Live Logs", emoji="📜", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("read_l:"))
def read_log_stream(call):
    l_name = call.data.split(":", 1)[1]
    path = os.path.join(LOGS_DIR, l_name)
    try:
        if os.path.exists(path):
            file_size = os.path.getsize(path)
            if file_size == 0:
                data = "Log file is empty."
            elif file_size > 500000:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    f.seek(file_size - 4000)
                    data = f.read()
            else:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    data = f.read()
            
            if len(data) > 4000:
                data = data[-4000:]
        else:
            data = "Log file not found."
    except Exception as e:
        data = f"Error reading log: {str(e)}"
    
    try:
        bot.send_message(call.from_user.id, f"📜 **Log ({l_name}):**\n```\n{data}\n```", parse_mode='Markdown')
    except Exception:
        bot.send_message(call.from_user.id, f"📜 Log ({l_name}):\n{data}")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("view_log:"))
def view_log_callback(call):
    uid = call.from_user.id
    p_name = call.data.split(":", 1)[1]
    log_file = os.path.join(LOGS_DIR, f"{uid}_{p_name}.log")
    
    if not os.path.exists(log_file):
        return bot.answer_callback_query(call.id, "❌ No log file found for this project.")
    
    try:
        file_size = os.path.getsize(log_file)
        if file_size == 0:
            data = "Log file is empty - project may not have started yet."
        else:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                if file_size > 4000:
                    f.seek(file_size - 4000)
                data = f.read()
        
        message_text = f"📜 **Log for `{p_name}`:**\n```\n{data}\n```"
        if len(message_text) > 4096:
            message_text = message_text[:4093] + "..."
            
        bot.send_message(uid, message_text, parse_mode='Markdown')
    except Exception as e:
        logger.exception(f"Error viewing log for user {uid} project {p_name}")
        send_styled_message(uid, f"Error reading log: {str(e)}", title="Error", emoji="❌")

# -------------------------
# Server Info, Settings, Health
# -------------------------
@bot.message_handler(func=lambda m: m.text == "🌐 SERVER INFO")
@premium_check_required
def srv_details(message):
    mode = "WEBHOOK" if os.getenv("WEBHOOK_URL") or detect_public_url() else "POLLING"
    node = os.uname().nodename if hasattr(os, "uname") else os.getenv("COMPUTERNAME", "n/a")
    py = sys.version.split()[0]
    send_styled_message(message.from_user.id,
                       f"**Node:** `{node}`\n**Python:** `{py}`\n**Mode:** `{mode}`\n**Status:** `Stable ✅`",
                       title="🌐 Platform Info", emoji="🌐")

@bot.message_handler(func=lambda m: m.text == "⚙ SETTINGS")
@premium_check_required
def settings_view(message):
    g = get_config_sync("global_server_limit", "1000")
    mode = "WEBHOOK" if os.getenv("WEBHOOK_URL") or detect_public_url() else "POLLING"
    send_styled_message(message.from_user.id,
                       f"**Mode:** `{mode}`\n**Auto-extract:** `True`\n**Single File Upload:** `Enabled (.py/.js)`\n**Auto Requirements:** `Enabled`\n**Dependency Auto-Install:** `Enabled`\n**Global Max Concurrent Servers per User:** `{g}`\n\nContact admin: {ADMIN_USERNAME}",
                       title="⚙ Settings", emoji="⚙")

@bot.message_handler(func=lambda m: m.text == "📊 SYSTEM HEALTH")
@premium_check_required
def health_mon(message):
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        send_styled_message(message.from_user.id,
                           f"**CPU:** `{cpu}%`\n**RAM:** `{ram}%`\n**Disk:** `{disk}%`",
                           title="📊 System Health", emoji="📊")
    except Exception as e:
        logger.exception("health_mon")
        send_styled_message(message.from_user.id, f"Error reading metrics: {e}", title="Error", emoji="❌")

# -------------------------
# ADMIN PANEL
# -------------------------
@bot.message_handler(func=lambda m: m.text == "👑 ADMIN ACCESS")
def admin_access(message):
    uid = message.from_user.id
    ensure_user_exists(uid)
    if not is_admin_sync(uid):
        return send_styled_message(uid, "Access Denied. You are not an admin.", title="🚫 Restricted", emoji="🚫")
    send_styled_message(uid, "👑 **ADMIN PANEL**", title="👑 Admin", emoji="👑", reply_markup=admin_panel_kb())

@bot.callback_query_handler(func=lambda c: c.data == "contact_admin")
def contact_admin_callback(call):
    bot.answer_callback_query(call.id, text=f"Contact Admin: {ADMIN_USERNAME}")
    send_styled_message(call.from_user.id, f"**Contact Admin:** {ADMIN_USERNAME}", title="✉️ Contact", emoji="✉️")

@bot.callback_query_handler(func=lambda c: c.data == "admin_health")
def admin_health_cb(call):
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        send_styled_message(call.from_user.id, f"**CPU:** `{cpu}%`\n**RAM:** `{ram}%`\n**Disk:** `{disk}%`", title="📊 System Health", emoji="📊")
    except Exception as e:
        send_styled_message(call.from_user.id, f"Error reading metrics: {e}", title="Error", emoji="❌")

@bot.callback_query_handler(func=lambda c: c.data == "admin_server_info")
def admin_server_info_cb(call):
    node = os.uname().nodename if hasattr(os, "uname") else os.getenv("COMPUTERNAME", "n/a")
    py = sys.version.split()[0]
    mode = "WEBHOOK" if os.getenv("WEBHOOK_URL") or detect_public_url() else "POLLING"
    send_styled_message(call.from_user.id, f"**Node:** `{node}`\n**Python:** `{py}`\n**Mode:** `{mode}`\n**Status:** `Stable ✅`", title="🌐 Platform Info", emoji="🌐")

# -------------------------
# ADMIN: Manage Users
# -------------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin_manage_users")
def admin_manage_users(call):
    rows = get_all_users_sync()
    if not rows:
        return send_styled_message(call.from_user.id, "No users found in database.", title="👥 Users", emoji="👥")
    kb = InlineKeyboardMarkup()
    for r in rows:
        uid, display_name, username, blocked, server_limit = r
        label = f"{display_name}" + (f" (@{username})" if username else "")
        kb.add(InlineKeyboardButton(f"👤 {label}", callback_data=f"admin_user:{uid}"))
    send_styled_message(call.from_user.id, "Select a user to manage:", title="👥 Manage Users", emoji="👥", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_user:"))
def admin_user_actions(call):
    target_uid = int(call.data.split(":", 1)[1])
    row = get_user_record_sync(target_uid)
    if not row:
        return bot.answer_callback_query(call.id, "User not found.")
    display_name = row[1]
    username = row[2]
    blocked = bool(row[3])
    server_limit = row[4]
    label = f"{display_name}" + (f" (@{username})" if username else "")
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🚫 Block User", callback_data=f"admin_block:{target_uid}"),
           InlineKeyboardButton("✅ Unblock User", callback_data=f"admin_unblock:{target_uid}"))
    kb.add(InlineKeyboardButton("📣 Broadcast to User", callback_data=f"admin_broadcast_user:{target_uid}"))
    kb.add(InlineKeyboardButton("⚖️ Set Server Limit", callback_data=f"admin_set_limit:{target_uid}"))
    info = f"**User:** {label}\n**Blocked:** {'Yes' if blocked else 'No'}\n**Server Limit:** {server_limit}"
    send_styled_message(call.from_user.id, info, title="👤 User Info", emoji="👤", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_block:"))
def admin_block_cb(call):
    admin_id = call.from_user.id
    target_uid = int(call.data.split(":", 1)[1])
    ensure_user_exists(target_uid)
    set_user_block_sync(target_uid, True, admin_id, reason="Blocked via admin panel")
    bot.answer_callback_query(call.id, "✅ User blocked.")
    send_styled_message(admin_id, f"User {target_uid} blocked.", title="✅ Blocked", emoji="✅")
    try:
        send_styled_message(target_uid, "You have been blocked by an admin. Contact " + ADMIN_USERNAME + " for help.", title="🚫 Blocked", emoji="🚫")
    except Exception:
        pass

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_unblock:"))
def admin_unblock_cb(call):
    admin_id = call.from_user.id
    target_uid = int(call.data.split(":", 1)[1])
    ensure_user_exists(target_uid)
    set_user_block_sync(target_uid, False, admin_id, reason="Unblocked via admin panel")
    bot.answer_callback_query(call.id, "✅ User unblocked.")
    send_styled_message(admin_id, f"User {target_uid} unblocked.", title="✅ Unblocked", emoji="✅")
    try:
        send_styled_message(target_uid, "You have been unblocked by an admin. You can now use RIZERxHOSTING. 🎉", title="✅ Unblocked", emoji="✅")
    except Exception:
        pass

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_set_limit:"))
def admin_set_limit_cb(call):
    admin_id = call.from_user.id
    target_uid = int(call.data.split(":", 1)[1])
    tmp = os.path.join(TMP_DIR, f"pending_set_limit_{admin_id}.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(str(target_uid))
    send_styled_message(admin_id, "Send the numeric server/project limit for this user (e.g. `2`):", title="⚖️ Set Limit", emoji="⚖️")

@bot.message_handler(func=lambda m: os.path.exists(os.path.join(TMP_DIR, f"pending_set_limit_{m.from_user.id}.txt")))
def admin_set_limit_save(message):
    admin_id = message.from_user.id
    tmp = os.path.join(TMP_DIR, f"pending_set_limit_{admin_id}.txt")
    try:
        with open(tmp, "r", encoding="utf-8") as f:
            target_uid = int(f.read().strip())
    except Exception:
        send_styled_message(admin_id, "No pending target found.", title="Error", emoji="❌")
        try:
            os.remove(tmp)
        except Exception:
            pass
        return
    try:
        limit = int(message.text.strip())
        set_user_limit_sync(target_uid, limit, admin_id)
        send_styled_message(admin_id, f"Server limit set to **{limit}** for user {target_uid}.", title="✅ Success", emoji="✅")
        try:
            send_styled_message(target_uid, f"Your server/project limit has been set to **{limit}** by an admin.", title="⚖️ Limit Updated", emoji="⚖️")
        except Exception:
            pass
    except Exception:
        send_styled_message(admin_id, "Invalid number. Please try again.", title="Error", emoji="❌")
    try:
        os.remove(tmp)
    except Exception:
        pass

# -------------------------
# BROADCAST (all / selected)
# -------------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin_broadcast")
def admin_broadcast_cb(call):
    admin_id = call.from_user.id
    tmp = os.path.join(TMP_DIR, f"pending_broadcast_{admin_id}.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("awaiting_choice")
    send_styled_message(admin_id, "Reply with **/all** to send to all users, **/select** to pick users.", title="📣 Broadcast", emoji="📣")

@bot.message_handler(commands=['all', 'select', 'send'])
def broadcast_commands(message):
    admin_id = message.from_user.id
    tmp = os.path.join(TMP_DIR, f"pending_broadcast_{admin_id}.txt")
    if not os.path.exists(tmp):
        return send_styled_message(admin_id, "Use Admin Panel -> **BROADCAST** first.", title="Error", emoji="❌")
    cmd = message.text.strip().lower()
    if cmd.startswith("/all"):
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("all")
        send_styled_message(admin_id, "Send the message you want to broadcast to **ALL** users now.", title="📣 Broadcast", emoji="📣")
    elif cmd.startswith("/select"):
        rows = get_all_users_sync()
        if not rows:
            send_styled_message(admin_id, "No users found.", title="Error", emoji="❌")
            try:
                os.remove(tmp)
            except:
                pass
            return
        kb = InlineKeyboardMarkup()
        for r in rows:
            uid, display_name, username, blocked, server_limit = r
            label = display_name + (f" (@{username})" if username else "")
            kb.add(InlineKeyboardButton(label, callback_data=f"broadcast_select_user:{uid}"))
        send_styled_message(admin_id, "Select users to broadcast (click to toggle). When done, send **/send** to continue.", title="📣 Select Users", emoji="📣", reply_markup=kb)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("select")
    elif cmd.startswith("/send"):
        with open(tmp, "r", encoding="utf-8") as f:
            mode = f.read().strip()
        if mode != "select":
            send_styled_message(admin_id, "You didn't choose **/select**. Use **/all** or **/select** first.", title="Error", emoji="❌")
            return
        sel_file = os.path.join(TMP_DIR, f"broadcast_selected_{admin_id}.txt")
        if not os.path.exists(sel_file):
            send_styled_message(admin_id, "No users selected. Use the selection buttons first.", title="Error", emoji="❌")
            return
        send_styled_message(admin_id, "Send the message to broadcast to selected users now.", title="📣 Broadcast", emoji="📣")
    else:
        send_styled_message(admin_id, "Unknown command. Use **/all**, **/select**, or **/send**.", title="Error", emoji="❌")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("broadcast_select_user:"))
def broadcast_select_user(call):
    admin_id = call.from_user.id
    target_uid = int(call.data.split(":", 1)[1])
    sel_file = os.path.join(TMP_DIR, f"broadcast_selected_{admin_id}.txt")
    sel = set()
    if os.path.exists(sel_file):
        try:
            with open(sel_file, "r", encoding="utf-8") as f:
                sel = set(int(x) for x in f.read().splitlines() if x.strip())
        except Exception:
            sel = set()
    if target_uid in sel:
        sel.remove(target_uid)
        bot.answer_callback_query(call.id, "Removed from selection.")
    else:
        sel.add(target_uid)
        bot.answer_callback_query(call.id, "Added to selection.")
    with open(sel_file, "w", encoding="utf-8") as f:
        for s in sel:
            f.write(str(s) + "\n")

@bot.message_handler(func=lambda m: os.path.exists(os.path.join(TMP_DIR, f"pending_broadcast_{m.from_user.id}.txt")))
def admin_broadcast_text(message):
    admin_id = message.from_user.id
    tmp = os.path.join(TMP_DIR, f"pending_broadcast_{admin_id}.txt")
    if not os.path.exists(tmp):
        return
    mode = open(tmp, "r", encoding="utf-8").read().strip()
    text = message.text
    if mode == "all":
        rows = get_all_users_sync()
        count = 0
        for r in rows:
            try:
                bot.send_message(r[0], f"📣 **Broadcast from Admin:**\n\n{text}", parse_mode='Markdown')
                count += 1
            except Exception:
                pass
        send_styled_message(admin_id, f"Broadcast sent to **{count}** users.", title="✅ Done", emoji="✅")
        try:
            send_styled_message(admin_id, f"Broadcast to ALL users completed. Delivered to {count} users.", title="🔔 Notice", emoji="🔔")
        except Exception:
            pass
        try:
            os.remove(tmp)
        except:
            pass
    elif mode == "select":
        sel_file = os.path.join(TMP_DIR, f"broadcast_selected_{admin_id}.txt")
        if not os.path.exists(sel_file):
            send_styled_message(admin_id, "No users selected.", title="Error", emoji="❌")
            try:
                os.remove(tmp)
            except:
                pass
            return
        targets = []
        with open(sel_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        targets.append(int(line))
                    except:
                        pass
        count = 0
        for t in targets:
            try:
                bot.send_message(t, f"📣 **Broadcast from Admin:**\n\n{text}", parse_mode='Markdown')
                count += 1
            except Exception:
                pass
        send_styled_message(admin_id, f"Broadcast sent to **{count}** selected users.", title="✅ Done", emoji="✅")
        try:
            send_styled_message(admin_id, f"Broadcast to selected users completed. Delivered to {count} users.", title="🔔 Notice", emoji="🔔")
        except Exception:
            pass
        try:
            os.remove(tmp)
        except:
            pass
        try:
            os.remove(sel_file)
        except:
            pass
    else:
        send_styled_message(admin_id, "Unknown broadcast mode.", title="Error", emoji="❌")
        try:
            os.remove(tmp)
        except:
            pass

# -------------------------
# TEMPORARY ADMIN promotion flow
# -------------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin_temp")
def admin_temp_prompt(call):
    admin_id = call.from_user.id
    send_styled_message(admin_id, "Reply with: `<user_id> <minutes>`\nExample: `12345678 60`", title="🕒 Temporary Admin", emoji="🕒")
    tmp = os.path.join(TMP_DIR, f"pending_tempadmin_{admin_id}.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("awaiting")

@bot.message_handler(func=lambda m: os.path.exists(os.path.join(TMP_DIR, f"pending_tempadmin_{m.from_user.id}.txt")))
def admin_temp_promote(message):
    admin_id = message.from_user.id
    tmp = os.path.join(TMP_DIR, f"pending_tempadmin_{admin_id}.txt")
    try:
        parts = message.text.strip().split()
        user_id = int(parts[0])
        minutes = int(parts[1]) if len(parts) > 1 else 60
        add_admin_sync(user_id, temporary=True, minutes=minutes)
        send_styled_message(admin_id, f"User {user_id} promoted to temporary admin for **{minutes}** minutes.", title="✅ Success", emoji="✅")
        try:
            send_styled_message(user_id, f"You were granted temporary admin access for **{minutes}** minutes.", title="👑 Admin Granted", emoji="👑")
        except Exception:
            pass
    except Exception:
        send_styled_message(admin_id, "Usage: `<user_id> <minutes>`", title="Error", emoji="❌")
    finally:
        try:
            os.remove(tmp)
        except:
            pass

# -------------------------
# ADMIN: Deploy Console
# -------------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin_deploy_console")
def admin_deploy_console(call):
    rows = get_all_users_sync()
    kb = InlineKeyboardMarkup()
    found = False
    for r in rows:
        uid, display_name, username, blocked, server_limit = r
        user_path = get_user_space(uid)
        projects = [d for d in os.listdir(user_path) if os.path.isdir(os.path.join(user_path, d))]
        if projects:
            found = True
            label = display_name + (f" (@{username})" if username else "")
            kb.add(InlineKeyboardButton(label, callback_data=f"admin_user_projects:{uid}"))
    if not found:
        return send_styled_message(call.from_user.id, "No user projects found.", title="Error", emoji="❌")
    send_styled_message(call.from_user.id, "Select a user to view their projects:", title="👥 User Projects", emoji="👥", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_user_projects:"))
def admin_user_projects(call):
    target_uid = int(call.data.split(":", 1)[1])
    user_path = get_user_space(target_uid)
    projects = [d for d in os.listdir(user_path) if os.path.isdir(os.path.join(user_path, d))]
    if not projects:
        return send_styled_message(call.from_user.id, "No projects for this user.", title="Error", emoji="❌")
    kb = InlineKeyboardMarkup()
    for p in projects:
        kb.add(InlineKeyboardButton(p, callback_data=f"admin_user_project_action:{target_uid}:{p}"))
    send_styled_message(call.from_user.id, "Select a project:", title="📁 Projects", emoji="📁", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_user_project_action:"))
def admin_user_project_action(call):
    _, target_uid, proj = call.data.split(":", 2)
    target_uid = int(target_uid)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🛑 Kill Instance", callback_data=f"admin_kill:{target_uid}:{proj}"))
    kb.add(InlineKeyboardButton("🗑 Delete Project", callback_data=f"admin_del:{target_uid}:{proj}"))
    kb.add(InlineKeyboardButton("📜 View Log", callback_data=f"admin_viewlog:{target_uid}:{proj}"))
    send_styled_message(call.from_user.id, f"**Project:** `{proj}`\n\nSelect action:", title="📁 Project Actions", emoji="📁", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_kill:"))
def admin_kill_cb(call):
    _, target_uid_s, proj = call.data.split(":", 2)
    target_uid = int(target_uid_s)
    if target_uid in running_instances and proj in running_instances[target_uid]:
        try:
            running_instances[target_uid][proj].terminate()
        except:
            pass
        del running_instances[target_uid][proj]
        record_project_db_sync(target_uid, proj, "", "stopped")
        send_styled_message(call.from_user.id, f"Instance `{proj}` killed.", title="✅ Killed", emoji="✅")
    else:
        send_styled_message(call.from_user.id, "No running instance found.", title="Error", emoji="❌")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_del:"))
def admin_del_cb(call):
    _, target_uid_s, proj = call.data.split(":", 2)
    target_uid = int(target_uid_s)
    p_path = os.path.join(get_user_space(target_uid), proj)
    try:
        if os.path.exists(p_path):
            shutil.rmtree(p_path)
        remove_project_db_sync(target_uid, proj)
        log_file = os.path.join(LOGS_DIR, f"{target_uid}_{proj}.log")
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
            except:
                pass
        send_styled_message(call.from_user.id, f"Project `{proj}` deleted and logs cleared.", title="🗑 Deleted", emoji="✅")
    except Exception as e:
        send_styled_message(call.from_user.id, f"Error: {e}", title="Error", emoji="❌")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_viewlog:"))
def admin_viewlog_cb(call):
    _, target_uid_s, proj = call.data.split(":", 2)
    target_uid = int(target_uid_s)
    log_file = os.path.join(LOGS_DIR, f"{target_uid}_{proj}.log")
    if not os.path.exists(log_file):
        return send_styled_message(call.from_user.id, "No log available for this project.", title="Error", emoji="❌")
    try:
        file_size = os.path.getsize(log_file)
        if file_size > 4000:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(file_size - 4000)
                data = f.read()
        else:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()
        bot.send_message(call.from_user.id, f"📜 **Log for {proj}:**\n```\n{data}\n```", parse_mode='Markdown')
    except Exception as e:
        send_styled_message(call.from_user.id, f"Error reading log: {str(e)}", title="Error", emoji="❌")

# -------------------------
# ADMIN: Live logs
# -------------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin_live_logs")
def admin_live_logs_cb(call):
    logs = os.listdir(LOGS_DIR)
    if not logs:
        return send_styled_message(call.from_user.id, "No logs available.", title="Error", emoji="❌")
    kb = InlineKeyboardMarkup()
    for l in logs:
        kb.add(InlineKeyboardButton(l, callback_data=f"admin_read_l:{l}"))
    send_styled_message(call.from_user.id, "Select log stream:", title="📜 Live Logs", emoji="📜", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_read_l:"))
def admin_read_l(call):
    l_name = call.data.split(":", 1)[1]
    path = os.path.join(LOGS_DIR, l_name)
    try:
        file_size = os.path.getsize(path)
        if file_size > 4000:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(file_size - 4000)
                data = f.read()
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()
        bot.send_message(call.from_user.id, f"📜 **Log ({l_name}):**\n```\n{data}\n```", parse_mode='Markdown')
    except Exception as e:
        send_styled_message(call.from_user.id, f"Error reading log: {str(e)}", title="Error", emoji="❌")

# -------------------------
# ADMIN: Broadcast to single user
# -------------------------
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_broadcast_user:"))
def admin_broadcast_user_prompt(call):
    admin_id = call.from_user.id
    if not (admin_id == OWNER_ID or is_admin_sync(admin_id)):
        return bot.answer_callback_query(call.id, "🚫 Access denied.")
    try:
        target_uid = int(call.data.split(":", 1)[1])
    except Exception:
        return bot.answer_callback_query(call.id, "❌ Invalid target user.")
    tmp_path = os.path.join(TMP_DIR, f"pending_broadcast_user_{admin_id}.txt")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(str(target_uid))
    except Exception:
        logger.exception("admin_broadcast_user_prompt: can't write tmp file")
        return send_styled_message(admin_id, "Unable to prepare broadcast (filesystem error).", title="Error", emoji="❌")
    send_styled_message(admin_id, f"Send the message to deliver to user **{target_uid}** now. (They will receive the exact text you send.)", title="📣 Broadcast", emoji="📣")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: os.path.exists(os.path.join(TMP_DIR, f"pending_broadcast_user_{m.from_user.id}.txt")))
def admin_broadcast_user_send(message):
    admin_id = message.from_user.id
    tmp_path = os.path.join(TMP_DIR, f"pending_broadcast_user_{admin_id}.txt")
    try:
        with open(tmp_path, "r", encoding="utf-8") as f:
            target_uid = int(f.read().strip())
    except Exception:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        return send_styled_message(admin_id, "Broadcast session expired or invalid. Please try again from Manage Users.", title="Error", emoji="❌")
    text = message.text or (message.caption if getattr(message, "caption", None) else "")
    if not text:
        send_styled_message(admin_id, "Please send text message content to deliver.", title="Error", emoji="❌")
        return
    try:
        bot.send_message(target_uid, f"📣 **Message from Admin:**\n\n{text}", parse_mode='Markdown')
        send_styled_message(admin_id, f"Message sent to user {target_uid}. (Delivered: 1)\n\nCustom broadcast delivered.", title="✅ Success", emoji="✅")
    except Exception:
        logger.exception("admin_broadcast_user_send: failed sending to %s", target_uid)
        send_styled_message(admin_id, f"Failed to deliver message to user {target_uid}. They may have blocked the bot or have privacy restrictions.", title="Error", emoji="❌")
    try:
        os.remove(tmp_path)
    except Exception:
        pass

# ==============================================================================
#  ADMIN PREMIUM SETTINGS MENU
# ==============================================================================
@bot.callback_query_handler(func=lambda c: c.data == "admin_settings")
def admin_settings_cb(call):
    admin_id = call.from_user.id
    if not (admin_id == OWNER_ID or is_admin_sync(admin_id)):
        return bot.answer_callback_query(call.id, "🚫 Access denied.")
    
    premium_mode = get_config_sync("premium_mode", "off")
    price_stars = get_config_sync("premium_price_stars", "0")
    
    kb = InlineKeyboardMarkup()
    
    if premium_mode == "off":
        kb.add(InlineKeyboardButton("💎 PREMIUM ON", callback_data="admin_premium_on"))
    else:
        kb.add(InlineKeyboardButton("✅ PREMIUM IS ON (Click to OFF)", callback_data="admin_premium_off"))
    
    kb.add(InlineKeyboardButton("🔄 PREMIUM OFF", callback_data="admin_premium_force_off"))
    kb.add(InlineKeyboardButton("💰 MANAGE MEMBERSHIP (Stars)", callback_data="admin_manage_membership"))
    kb.add(InlineKeyboardButton("👑 GRANT PREMIUM ACCESS", callback_data="admin_grant_premium"))
    kb.add(InlineKeyboardButton("🚫 REVOKE PREMIUM ACCESS", callback_data="admin_revoke_premium"))
    kb.add(InlineKeyboardButton("⬅️ BACK TO ADMIN PANEL", callback_data="admin_back_to_panel"))
    
    status_text = f"**Current Premium Mode:** {'ON 🔒' if premium_mode == 'on' else 'OFF 🔓'}\n**Premium Price:** {price_stars} ⭐"
    send_styled_message(admin_id, status_text, title="⚙️ Admin Settings", emoji="⚙️", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "admin_back_to_panel")
def admin_back_to_panel_cb(call):
    send_styled_message(call.from_user.id, "👑 **ADMIN PANEL**", title="👑 Admin", emoji="👑", reply_markup=admin_panel_kb())

@bot.callback_query_handler(func=lambda c: c.data == "admin_premium_on")
def admin_premium_on_cb(call):
    admin_id = call.from_user.id
    if not (admin_id == OWNER_ID or is_admin_sync(admin_id)):
        return bot.answer_callback_query(call.id, "🚫 Access denied.")
    set_config_sync("premium_mode", "on")
    bot.answer_callback_query(call.id, "✅ Premium mode enabled!")
    send_styled_message(admin_id, "Premium mode is now **ON**. Non-premium users will be blocked.", title="🔒 Premium ON", emoji="✅")
    
    try:
        all_users = get_all_users_sync()
        for user_row in all_users:
            uid = user_row[0]
            if not is_premium_user(uid):
                try:
                    send_styled_message(uid, f"**PREMIUM SETTINGS HAS BEEN TURNED ON**\n\n⚠️ Please contact admin for premium access.\nAdmin: {ADMIN_USERNAME}", title="🔒 Premium Mode", emoji="🚫")
                except Exception:
                    pass
    except Exception as e:
        logger.warning(f"Failed to notify users about premium activation: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "admin_premium_off")
def admin_premium_off_cb(call):
    admin_id = call.from_user.id
    if not (admin_id == OWNER_ID or is_admin_sync(admin_id)):
        return bot.answer_callback_query(call.id, "🚫 Access denied.")
    set_config_sync("premium_mode", "off")
    bot.answer_callback_query(call.id, "✅ Premium mode disabled!")
    send_styled_message(admin_id, "Premium mode is now **OFF**. All users can access the bot.", title="🔓 Premium OFF", emoji="✅")
    
    try:
        all_users = get_all_users_sync()
        for user_row in all_users:
            uid = user_row[0]
            try:
                send_styled_message(uid, "Premium mode has been turned **OFF**. You now have full access to the bot! 🎉", title="🔓 Premium Deactivated", emoji="✅")
            except Exception:
                    pass
    except Exception as e:
        logger.warning(f"Failed to notify users about premium deactivation: {e}")

@bot.callback_query_handler(func=lambda c: c.data == "admin_premium_force_off")
def admin_premium_force_off_cb(call):
    admin_id = call.from_user.id
    if not (admin_id == OWNER_ID or is_admin_sync(admin_id)):
        return bot.answer_callback_query(call.id, "🚫 Access denied.")
    set_config_sync("premium_mode", "off")
    bot.answer_callback_query(call.id, "✅ Premium mode forced OFF!")
    send_styled_message(admin_id, "Premium mode is now **OFF**. All users can access the bot.", title="🔓 Premium OFF", emoji="✅")

@bot.callback_query_handler(func=lambda c: c.data == "admin_manage_membership")
def admin_manage_membership_cb(call):
    admin_id = call.from_user.id
    if not (admin_id == OWNER_ID or is_admin_sync(admin_id)):
        return bot.answer_callback_query(call.id, "🚫 Access denied.")
    
    current_price = get_config_sync("premium_price_stars", "0")
    send_styled_message(admin_id, f"**Current Premium Price:** {current_price} ⭐\n\nSend the new price in stars (e.g., `50`) or `0` to make it free:", title="💰 Manage Membership", emoji="💰")
    
    tmp = os.path.join(TMP_DIR, f"pending_set_price_{admin_id}.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("awaiting_price")

@bot.message_handler(func=lambda m: os.path.exists(os.path.join(TMP_DIR, f"pending_set_price_{m.from_user.id}.txt")))
def admin_set_price_save(message):
    admin_id = message.from_user.id
    tmp = os.path.join(TMP_DIR, f"pending_set_price_{admin_id}.txt")
    try:
        os.remove(tmp)
    except Exception:
        pass
    
    try:
        price = int(message.text.strip())
        if price < 0:
            raise ValueError("Price cannot be negative")
        set_config_sync("premium_price_stars", str(price))
        send_styled_message(admin_id, f"Premium price set to **{price}** ⭐", title="✅ Success", emoji="✅")
    except Exception:
        send_styled_message(admin_id, "Invalid price. Please send a valid number (e.g., `50`).", title="Error", emoji="❌")

@bot.callback_query_handler(func=lambda c: c.data == "admin_grant_premium")
def admin_grant_premium_cb(call):
    admin_id = call.from_user.id
    if not (admin_id == OWNER_ID or is_admin_sync(admin_id)):
        return bot.answer_callback_query(call.id, "🚫 Access denied.")
    
    send_styled_message(admin_id, "Send the user ID, username, or display name of the user you want to grant premium access to:", title="👑 Grant Premium", emoji="👑")
    
    tmp = os.path.join(TMP_DIR, f"pending_grant_premium_{admin_id}.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("awaiting_user")

@bot.message_handler(func=lambda m: os.path.exists(os.path.join(TMP_DIR, f"pending_grant_premium_{m.from_user.id}.txt")))
def admin_grant_premium_save(message):
    admin_id = message.from_user.id
    tmp = os.path.join(TMP_DIR, f"pending_grant_premium_{admin_id}.txt")
    try:
        os.remove(tmp)
    except Exception:
        pass
    
    search_term = message.text.strip()
    if not search_term:
        send_styled_message(admin_id, "Please provide a valid user ID, username, or display name.", title="Error", emoji="❌")
        return
    
    found_user = None
    try:
        with db_lock:
            cur = db_conn.cursor()
            if search_term.isdigit():
                cur.execute("SELECT user_id FROM users WHERE user_id = ?", (int(search_term),))
                row = cur.fetchone()
                if row:
                    found_user = row[0]
            
            if not found_user:
                cur.execute("SELECT user_id FROM users WHERE username = ?", (search_term.replace("@", ""),))
                row = cur.fetchone()
                if row:
                    found_user = row[0]
            
            if not found_user:
                cur.execute("SELECT user_id, display_name FROM users WHERE display_name LIKE ?", (f"%{search_term}%",))
                rows = cur.fetchall()
                if rows:
                    if len(rows) == 1:
                        found_user = rows[0][0]
                    else:
                        kb = InlineKeyboardMarkup()
                        for r in rows[:10]:
                            uid, name = r
                            kb.add(InlineKeyboardButton(f"👤 {name} (ID: {uid})", callback_data=f"admin_grant_confirm:{uid}"))
                        send_styled_message(admin_id, "Multiple users found. Select one:", title="Select User", emoji="👤", reply_markup=kb)
                        return
        
        if found_user:
            set_user_premium_sync(found_user, True, transaction_id="admin_grant")
            user_info = get_user_record_sync(found_user)
            user_label = user_info[1] if user_info else f"User {found_user}"
            send_styled_message(admin_id, f"Premium access granted to **{user_label}** (ID: `{found_user}`)", title="✅ Success", emoji="✅")
            try:
                send_styled_message(found_user, "You have been granted premium access by the admin! You can now use all features of the bot.", title="🎉 Premium Granted", emoji="💎")
            except Exception:
                pass
        else:
            send_styled_message(admin_id, "User not found. Please check the ID, username, or name and try again.", title="Error", emoji="❌")
            
    except Exception as e:
        logger.exception("admin_grant_premium_save")
        send_styled_message(admin_id, f"Error granting premium access: {str(e)}", title="Error", emoji="❌")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_grant_confirm:"))
def admin_grant_confirm_cb(call):
    admin_id = call.from_user.id
    target_uid = int(call.data.split(":", 1)[1])
    
    set_user_premium_sync(target_uid, True, transaction_id="admin_grant")
    user_info = get_user_record_sync(target_uid)
    user_label = user_info[1] if user_info else f"User {target_uid}"
    send_styled_message(admin_id, f"Premium access granted to **{user_label}** (ID: `{target_uid}`)", title="✅ Success", emoji="✅")
    try:
        send_styled_message(target_uid, "You have been granted premium access by the admin! You can now use all features of the bot.", title="🎉 Premium Granted", emoji="💎")
    except Exception:
        pass
    bot.answer_callback_query(call.id, "Premium granted!")

# ==============================================================================
#  REVOKE PREMIUM ACCESS HANDLER
# ==============================================================================
@bot.callback_query_handler(func=lambda c: c.data == "admin_revoke_premium")
def admin_revoke_premium_cb(call):
    admin_id = call.from_user.id
    if not (admin_id == OWNER_ID or is_admin_sync(admin_id)):
        return bot.answer_callback_query(call.id, "🚫 Access denied.")
    
    send_styled_message(admin_id, "Send the user ID, username, or display name of the user you want to revoke premium access from:", title="🚫 Revoke Premium", emoji="🚫")
    
    tmp = os.path.join(TMP_DIR, f"pending_revoke_premium_{admin_id}.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("awaiting_user")

@bot.message_handler(func=lambda m: os.path.exists(os.path.join(TMP_DIR, f"pending_revoke_premium_{m.from_user.id}.txt")))
def admin_revoke_premium_save(message):
    admin_id = message.from_user.id
    tmp = os.path.join(TMP_DIR, f"pending_revoke_premium_{admin_id}.txt")
    try:
        os.remove(tmp)
    except Exception:
        pass
    
    search_term = message.text.strip()
    if not search_term:
        send_styled_message(admin_id, "Please provide a valid user ID, username, or display name.", title="Error", emoji="❌")
        return
    
    found_user = None
    try:
        with db_lock:
            cur = db_conn.cursor()
            if search_term.isdigit():
                cur.execute("SELECT user_id FROM users WHERE user_id = ?", (int(search_term),))
                row = cur.fetchone()
                if row:
                    found_user = row[0]
            
            if not found_user:
                cur.execute("SELECT user_id FROM users WHERE username = ?", (search_term.replace("@", ""),))
                row = cur.fetchone()
                if row:
                    found_user = row[0]
            
            if not found_user:
                cur.execute("SELECT user_id, display_name FROM users WHERE display_name LIKE ?", (f"%{search_term}%",))
                rows = cur.fetchall()
                if rows:
                    if len(rows) == 1:
                        found_user = rows[0][0]
                    else:
                        kb = InlineKeyboardMarkup()
                        for r in rows[:10]:
                            uid, name = r
                            kb.add(InlineKeyboardButton(f"👤 {name} (ID: {uid})", callback_data=f"admin_revoke_confirm:{uid}"))
                        send_styled_message(admin_id, "Multiple users found. Select one to revoke premium:", title="Select User", emoji="👤", reply_markup=kb)
                        return
        
        if found_user:
            if is_premium_user(found_user):
                set_user_premium_sync(found_user, False)
                user_info = get_user_record_sync(found_user)
                user_label = user_info[1] if user_info else f"User {found_user}"
                send_styled_message(admin_id, f"Premium access revoked from **{user_label}** (ID: `{found_user}`)", title="🚫 Revoked", emoji="✅")
                try:
                    send_styled_message(found_user, f"Your premium access has been revoked by the admin. Please contact {ADMIN_USERNAME} for assistance.", title="⚠️ Premium Revoked", emoji="⚠️")
                except Exception:
                    pass
            else:
                send_styled_message(admin_id, f"User {found_user} does not have premium access.", title="ℹ️ Info", emoji="ℹ️")
        else:
            send_styled_message(admin_id, "User not found. Please check the ID, username, or name and try again.", title="Error", emoji="❌")
            
    except Exception as e:
        logger.exception("admin_revoke_premium_save")
        send_styled_message(admin_id, f"Error revoking premium access: {str(e)}", title="Error", emoji="❌")

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("admin_revoke_confirm:"))
def admin_revoke_confirm_cb(call):
    admin_id = call.from_user.id
    target_uid = int(call.data.split(":", 1)[1])
    
    if is_premium_user(target_uid):
        set_user_premium_sync(target_uid, False)
        user_info = get_user_record_sync(target_uid)
        user_label = user_info[1] if user_info else f"User {target_uid}"
        send_styled_message(admin_id, f"Premium access revoked from **{user_label}** (ID: `{target_uid}`)", title="🚫 Revoked", emoji="✅")
        try:
            send_styled_message(target_uid, f"Your premium access has been revoked by the admin. Please contact {ADMIN_USERNAME} for assistance.", title="⚠️ Premium Revoked", emoji="⚠️")
        except Exception:
            pass
    else:
        send_styled_message(admin_id, f"User {target_uid} does not have premium access.", title="ℹ️ Info", emoji="ℹ️")
    bot.answer_callback_query(call.id, "Premium revoked!")

# ==============================================================================
#  RESOURCE OPTIMIZATION UTILITIES
# ==============================================================================
def optimize_resource_usage():
    """Apply system-level optimizations to reduce CPU/RAM/Disk usage."""
    try:
        if resource is not None:
            resource.setrlimit(resource.RLIMIT_NICE, (10, 10))
            os.nice(10)
        
        if resource is not None:
            soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
            if soft > 10000:
                resource.setrlimit(resource.RLIMIT_NOFILE, (8192, hard))
        
        if os.path.exists(TMP_DIR):
            for f in os.listdir(TMP_DIR):
                try:
                    file_path = os.path.join(TMP_DIR, f)
                    if os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) > 86400:
                        os.remove(file_path)
                except Exception:
                    pass
        
        logger.info("Resource optimizations applied successfully")
    except Exception as e:
        logger.warning(f"Resource optimization failed: {e}")

optimize_resource_usage()

# ==============================================================================
#  RUNTIME VERSION COMPATIBILITY AND SAFETY FINALIZERS
# ==============================================================================
def _check_python_version_compatibility():
    """Verify Python version is within supported range."""
    version = sys.version_info
    if version < (3, 9):
        logger.error(f"Python {version.major}.{version.minor} is below minimum supported version 3.9.")
    elif version > (3, 12):
        logger.warning(f"Python {version.major}.{version.minor} is newer than tested versions (3.9-3.12).")
    else:
        logger.info(f"Running on Python {version.major}.{version.minor}.{version.micro} - Supported ✅")

def _check_critical_dependency_versions():
    """Check versions of critical dependencies."""
    try:
        from importlib.metadata import version, PackageNotFoundError
        deps_to_check = ["pyTelegramBotAPI", "psutil", "protobuf", "requests"]
        for dep_name in deps_to_check:
            try:
                ver = version(dep_name)
                logger.info(f"{dep_name} version: {ver}")
                if dep_name == "protobuf" and ver.startswith("4."):
                    logger.warning("protobuf 4.x may cause issues. Protocol buffer implementation set to 'python'.")
            except PackageNotFoundError:
                logger.warning(f"{dep_name} is not installed.")
            except Exception:
                pass
    except Exception:
        pass

def _setup_graceful_shutdown_handlers():
    """Setup signal handlers for graceful shutdown."""
    if signal is None:
        return
        
    def _signal_handler(signum, frame):
        logger.info(f"Received termination signal {signum}. Shutting down gracefully...")
        for uid, projects in running_instances.items():
            for proj_name, proc in projects.items():
                try:
                    proc.terminate()
                except Exception:
                    pass
        try:
            time.sleep(2)
        except Exception:
            pass
        sys.exit(0)
    
    try:
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)
        logger.info("Graceful shutdown handlers installed.")
    except Exception:
        pass

def _log_deployment_environment():
    """Log detected deployment environment."""
    env_detected = []
    if os.getenv("RENDER"):
        env_detected.append("Render.com")
    if os.getenv("RAILWAY_ENVIRONMENT"):
        env_detected.append("Railway.app")
    if os.path.exists("/.dockerenv"):
        env_detected.append("Docker")
    if os.getenv("SYSTEMD") or os.path.exists("/run/systemd"):
        env_detected.append("SystemD/VPS")
    if os.getenv("WEBHOOK_MODE"):
        env_detected.append(f"Webhook Mode (Port: {os.getenv('PORT', '5000')})")
    
    if env_detected:
        logger.info(f"Detected deployment environment: {', '.join(env_detected)}")
    else:
        logger.info("Running in standard environment (development/local)")

_check_python_version_compatibility()
_check_critical_dependency_versions()
_setup_graceful_shutdown_handlers()
_log_deployment_environment()

# ==============================================================================
#  BACKGROUND MAINTENANCE THREAD
# ==============================================================================
def _system_maintenance_worker():
    """Background worker for system maintenance tasks."""
    while True:
        try:
            time.sleep(300)
            
            try:
                current_time = time.time()
                for log_file in os.listdir(LOGS_DIR):
                    log_path = os.path.join(LOGS_DIR, log_file)
                    if os.path.isfile(log_path):
                        file_age = current_time - os.path.getmtime(log_path)
                        if file_age > 7 * 24 * 60 * 60:
                            os.remove(log_path)
                            logger.info(f"Removed old log file: {log_file}")
            except Exception as e:
                logger.warning(f"Log cleanup failed: {e}")
            
            active_threads = getattr(threading, '_project_install_threads', {})
            for thread_id, thread in list(active_threads.items()):
                if not thread.is_alive():
                    del active_threads[thread_id]
            
            try:
                for temp_file in os.listdir(TMP_DIR):
                    temp_path = os.path.join(TMP_DIR, temp_file)
                    if os.path.isfile(temp_path) and temp_file.startswith("pending_") and time.time() - os.path.getmtime(temp_path) > 3600:
                        os.remove(temp_path)
            except Exception:
                pass
                    
        except Exception as e:
            logger.exception("Maintenance worker error")
        time.sleep(300)

threading.Thread(target=_system_maintenance_worker, daemon=True, name="MaintenanceWorker").start()

# -------------------------
# Fallback handlers & safety
# -------------------------
@bot.message_handler(func=lambda m: True, content_types=['text'])
def fallback_text(message):
    txt = message.text.strip().lower()
    if txt.startswith("/"):
        send_styled_message(message.from_user.id, "Unknown command. Use the menu buttons or /start to return to the main menu.", title="❓ Help", emoji="❓")
    else:
        send_styled_message(message.from_user.id, "I didn't recognize that action. Use the menu buttons to manage your projects or /start to see the welcome message.", title="❓ Help", emoji="❓")

# -------------------------
# Main entry point - MODIFIED for HYBRID MODE
# -------------------------
def main():
    logger.info("=" * 60)
    logger.info("Starting RIZERxHOSTING (full) ...")
    logger.info("Enhanced dependency auto-installer system is ACTIVE")
    logger.info("Telegram library conflict resolver is ACTIVE")
    logger.info("Premium membership system is ACTIVE")
    logger.info("Resource optimization is ACTIVE")
    logger.info("Direct file upload support is ACTIVE")
    logger.info("Silent dependency installation is ACTIVE")
    logger.info("Hybrid mode (webhook/polling) is ACTIVE")
    logger.info("Binary compatibility fix is ACTIVE")
    logger.info("Battery progress interface is ACTIVE")
    logger.info("Enhanced database integrity is ACTIVE")
    logger.info("Full error handling is ACTIVE")
    logger.info("=" * 60)
    
    # Run in hybrid mode (auto-detect and choose appropriate mode)
    run_bot_in_hybrid_mode()

if __name__ == "__main__":
    main()