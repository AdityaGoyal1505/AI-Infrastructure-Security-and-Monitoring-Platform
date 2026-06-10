import json


config = {}

config["api_key"] = input("Workspace API Key: ")

log_path = input("Log file path: ")

service_name = input("Service name: ")

config["logs"] = [
    {
        "path": log_path,
        "service": service_name
    }
]

with open("config.json","w") as f:
    json.dump(config,f,indent=4)

print("config.json generated")