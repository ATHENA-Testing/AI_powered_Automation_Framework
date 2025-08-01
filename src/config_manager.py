"""
Configuration Manager for Python Automation Framework
Handles loading and managing configuration settings from config.ini
"""

import configparser
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class ConfigManager:
    """Manages configuration settings for the automation framework"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager
        
        Args:
            config_path: Path to the configuration file. If None, uses default path.
        """
        self.config = configparser.ConfigParser()
        
        if config_path is None:
            # Default to config.ini in the project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config.ini"
        
        self.config_path = Path(config_path)
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from the config file"""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            self.config.read(self.config_path)
            logging.info(f"Configuration loaded from {self.config_path}")
            
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            raise
    
    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """
        Get a configuration value
        
        Args:
            section: Configuration section name
            key: Configuration key name
            fallback: Default value if key not found
            
        Returns:
            Configuration value as string
        """
        try:
            return self.config.get(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            logging.warning(f"Configuration key not found: {section}.{key}, using fallback: {fallback}")
            return fallback
    
    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Get a configuration value as integer"""
        try:
            return self.config.getint(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            logging.warning(f"Configuration key not found or invalid: {section}.{key}, using fallback: {fallback}")
            return fallback
    
    def get_boolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get a configuration value as boolean"""
        try:
            return self.config.getboolean(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            logging.warning(f"Configuration key not found or invalid: {section}.{key}, using fallback: {fallback}")
            return fallback
    
    def get_float(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get a configuration value as float"""
        try:
            return self.config.getfloat(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            logging.warning(f"Configuration key not found or invalid: {section}.{key}, using fallback: {fallback}")
            return fallback
    
    def get_section(self, section: str) -> Dict[str, str]:
        """
        Get all key-value pairs from a section
        
        Args:
            section: Section name
            
        Returns:
            Dictionary of key-value pairs
        """
        try:
            return dict(self.config[section])
        except KeyError:
            logging.warning(f"Configuration section not found: {section}")
            return {}
    
    def set(self, section: str, key: str, value: str) -> None:
        """
        Set a configuration value
        
        Args:
            section: Configuration section name
            key: Configuration key name
            value: Value to set
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, key, str(value))
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            logging.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")
            raise

# Global configuration instance
config = ConfigManager()

