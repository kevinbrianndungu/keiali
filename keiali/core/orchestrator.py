from typing import Dict, Any
from agents.deepseek import DeepSeekV3
from interfaces.voice import VoiceInterface
from controllers.iot import IoTController
from security import SecurityLayer

class Orchestrator:
    def __init__(self):
        self.agents = {
            'ai': DeepSeekV3(),
            'voice': VoiceInterface(),
            'iot': IoTController()
        }
        self.security = SecurityLayer()

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Validate request
        if not self.security.validate(request['user'], request['command']):
            return {"error": "Permission denied"}
        
        # Route and execute
        try:
            if request['type'] == 'voice':
                return self._handle_voice(request)
            elif request['type'] == 'api':
                return self._handle_api(request)
        except Exception as e:
            self.security.audit_log(f"Error: {str(e)}")
            return {"error": str(e)}

    def _handle_voice(self, request):
        text = self.agents['voice'].transcribe(request['audio'])
        response = self.agents['ai'].process(text)
        return self.agents['voice'].speak(response)
