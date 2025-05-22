import yaml

class SecurityLayer:
    def __init__(self):
        with open("config/permissions.yaml") as f:
            self.rules = yaml.safe_load(f)
    
    def validate(self, user: str, command: str) -> bool:
        user_role = self._get_user_role(user)
        allowed_actions = self.rules['roles'][user_role]['actions']
        
        if "*" in allowed_actions:
            return True
            
        return any(
            action in command.lower()
            for action in allowed_actions
        )
