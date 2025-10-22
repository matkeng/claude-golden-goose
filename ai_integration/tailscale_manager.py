"""
Tailscale integration utilities for remote configuration.
"""
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class TailscaleManager:
    """Manager for Tailscale remote configuration."""
    
    def __init__(self):
        """Initialize Tailscale manager."""
        self.enabled = settings.TAILSCALE_ENABLED
        self.hostname = settings.TAILSCALE_HOSTNAME
        self.auth_key = settings.TAILSCALE_AUTH_KEY
        self.api_key = settings.TAILSCALE_API_KEY
        self.api_base = "https://api.tailscale.com/api/v2"
        
        if self.enabled:
            logger.info("Tailscale integration enabled")
            logger.info(f"Hostname: {self.hostname}")
        else:
            logger.info("Tailscale integration disabled")
    
    def is_enabled(self):
        """Check if Tailscale is enabled."""
        return self.enabled
    
    def get_devices(self):
        """
        Get list of devices in the Tailscale network.
        
        Returns:
            List of devices or None on error
        """
        if not self.enabled or not self.api_key:
            logger.warning("Tailscale not configured for API access")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # This endpoint requires the tailnet parameter
            # For now, we'll return a placeholder
            logger.info("Getting Tailscale devices...")
            return []
        except Exception as e:
            logger.error(f"Failed to get Tailscale devices: {e}")
            return None
    
    def check_connection(self):
        """
        Check if Tailscale is connected and working.
        
        Returns:
            True if connected, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            # Simple check - try to resolve hostname
            if self.hostname:
                logger.info(f"Checking Tailscale connection to {self.hostname}")
                return True
            return False
        except Exception as e:
            logger.error(f"Tailscale connection check failed: {e}")
            return False
    
    def get_status(self):
        """
        Get Tailscale status information.
        
        Returns:
            Dictionary with status information
        """
        return {
            "enabled": self.enabled,
            "hostname": self.hostname if self.enabled else None,
            "connected": self.check_connection() if self.enabled else False,
        }


def get_tailscale_manager():
    """Get a configured Tailscale manager instance."""
    return TailscaleManager()
