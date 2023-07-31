login_schema = {
  "type": "object",
  "properties": {
    "username": { "type": "string", "minLength": 4, "maxLength": 20 },
    "password": { "type": "string", "minLength": 6, "maxLength": 80 }
  },
  "required": ["username", "password"]
}

register_schema = {
    "type": "object",
    "properties": {
    "name": { "type": "string" },
    "email": {   "type": "string", 
                "pattern": "^\\S+@\\S+\\.\\S+$",
                "format": "email",
                "minLength": 6,
                "maxLength": 127
            },
    "avatar": { "type": "string" },
    "username": { "type": "string", "minLength": 4, "maxLength": 20 },
    "password": { "type": "string", "minLength": 6, "maxLength": 80 },
    "birthdate": { "type": "string", "format": "date" }
    },
    "required": ["name", "email", "username", "password", "birthdate"]
}