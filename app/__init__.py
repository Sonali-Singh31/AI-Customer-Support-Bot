# app/__init__.py

# This allows you to import the agent directly from the 'app' package
# Example: from app import SupportAgent
from .agent import SupportAgent
from .database import init_db, save_message, get_history