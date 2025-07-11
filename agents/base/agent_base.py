import time
import threading
import signal
import sys
import logging
from datetime import datetime
from typing import Dict, Any

class AgentBase:
    """Base class for all agents in the Agentic Agile System"""
    def __init__(self, api_client, config):
        self.api_client = api_client
        self.config = config
        self.running = False
        self.agent_id = None
        self.stats = {
            "heartbeats_sent": 0,
            "started_at": datetime.utcnow()
        }
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        """Start the agent"""
        self.logger.info(f"Starting {self.config.name} v{self.config.version}")
        try:
            # Check API health
            if not self.api_client.health_check():
                self.logger.error("API hub is not healthy. Cannot start agent.")
                return False
            # Register with API hub
            agent_data = self.api_client.register_agent()
            self.agent_id = agent_data["id"]
            self.logger.info(f"Successfully registered with API hub. Agent ID: {self.agent_id}")
            self.running = True
            # Start background threads
            self._start_heartbeat_thread()
            self.logger.info(f"{self.config.name} is now running. Press Ctrl+C to stop.")
            # Main loop
            self.run()
            return True
        except Exception as e:
            self.logger.error(f"Failed to start agent: {e}")
            return False

    def stop(self):
        """Stop the agent"""
        self.logger.info(f"Stopping {self.config.name}...")
        self.running = False
        # Send final heartbeat
        if self.agent_id:
            self.api_client.send_heartbeat(status="inactive", current_task="shutting_down")
        self.logger.info(f"{self.config.name} stopped.")

    def _signal_handler(self, signum, frame):
        self.logger.info(f"Received signal {signum}. Shutting down...")
        self.stop()
        sys.exit(0)

    def _start_heartbeat_thread(self):
        def heartbeat_loop():
            while self.running:
                try:
                    current_task = self.get_current_task()
                    success = self.api_client.send_heartbeat(
                        status="active",
                        current_task=current_task
                    )
                    if success:
                        self.stats["heartbeats_sent"] += 1
                    time.sleep(self.config.heartbeat_interval)
                except Exception as e:
                    self.logger.error(f"Heartbeat error: {e}")
                    time.sleep(10)
        thread = threading.Thread(target=heartbeat_loop, daemon=True)
        thread.start()
        self.logger.info("Heartbeat thread started")

    def get_current_task(self):
        """Override in subclass to report current task"""
        return "idle"

    def run(self):
        """Override in subclass for main agent loop"""
        while self.running:
            time.sleep(1)

    def get_stats(self) -> Dict[str, Any]:
        return {
            **self.stats,
            "uptime_seconds": (datetime.utcnow() - self.stats["started_at"]).total_seconds(),
            "agent_id": self.agent_id,
            "status": "running" if self.running else "stopped"
        } 