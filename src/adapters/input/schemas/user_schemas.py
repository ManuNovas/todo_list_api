REGISTER_BODY={
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128,
        },
        "email": {
            "type": "string",
            "format": "email",
            "minLength": 1,
            "maxLength": 128,
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLentgh": 32,
        },
    },
    "required": ["name", "email", "password"],
}
