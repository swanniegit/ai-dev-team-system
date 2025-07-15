import os
import sys
import subprocess

REQUIRED_ENV_VARS = [
    "DATABASE_URL", "MONGODB_URL", "REDIS_URL", "SECRET_KEY", "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES", "SLACK_WEBHOOK_URL", "GITHUB_WEBHOOK_SECRET",
    "API_BASE_URL", "ANTHROPIC_API_KEY"
]

OPTIONAL_ENV_VARS = [
    "GITHUB_TOKEN", "GITHUB_REPO", "GITLAB_WEBHOOK_TOKEN"
]

def check_env():
    print("Checking required environment variables...")
    missing = []
    for var in REQUIRED_ENV_VARS:
        if not os.getenv(var):
            print(f"❌ {var} is missing!")
            missing.append(var)
        else:
            print(f"✅ {var} is set.")
    if missing:
        print("\nPlease set the missing environment variables in your .env file.")
        sys.exit(1)
    print("All required environment variables are set.\n")

def check_docker_services():
    print("Checking Docker Compose services...")
    try:
        result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
        print(result.stdout)
        if "Exit" in result.stdout or "Restarting" in result.stdout:
            print("❌ Some services are not running correctly. Check logs with `docker-compose logs <service>`." )
        else:
            print("✅ All services appear to be running.")
    except Exception as e:
        print(f"Error running docker-compose: {e}")

if __name__ == "__main__":
    check_env()
    check_docker_services() 