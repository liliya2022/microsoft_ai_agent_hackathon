import json
import os
from datetime import datetime
from typing import Dict, Any

class AgentLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self._ensure_log_dir()
        self.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"session_{self.current_session}.json")
        self.conversation = []

    def _ensure_log_dir(self):
        """Create logs directory if it doesn't exist."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def log_interaction(self, user_input: str, agent_response: Dict[str, Any], timestamp: str = None):
        """Log a single interaction between user and agent."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        interaction = {
            "timestamp": timestamp,
            "user_input": user_input,
            "agent_response": agent_response,
            "emergency_flag": agent_response.get("emergency", False)
        }
        
        self.conversation.append(interaction)
        self._save_to_file()

    def _save_to_file(self):
        """Save the current conversation to a JSON file."""
        log_data = {
            "session_id": self.current_session,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "conversation": self.conversation
        }
        
        with open(self.log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        return {
            "session_id": self.current_session,
            "total_interactions": len(self.conversation),
            "emergency_flags": sum(1 for i in self.conversation if i["emergency_flag"]),
            "start_time": self.conversation[0]["timestamp"] if self.conversation else None,
            "end_time": datetime.now().isoformat()
        }

    def export_session(self, format: str = "json") -> str:
        """Export the current session in the specified format."""
        if format.lower() == "json":
            return json.dumps(self.get_session_summary(), indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}") 