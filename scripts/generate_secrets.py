#!/usr/bin/env python3
"""
Generate secure secrets for the Agentic Agile System

This script generates cryptographically secure secrets for production deployment.
Run this script and update your environment variables with the generated values.
"""

import secrets
import string
import os
from pathlib import Path

def generate_secret_key(length: int = 32) -> str:
    """Generate a cryptographically secure secret key"""
    return secrets.token_urlsafe(length)

def generate_password(length: int = 16) -> str:
    """Generate a secure password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_webhook_secret(length: int = 40) -> str:
    """Generate a webhook secret"""
    return secrets.token_hex(length)

def main():
    """Generate all secrets and display them"""
    print("🔐 Agentic Agile System - Security Keys Generator")
    print("=" * 60)
    print()
    
    # Generate secrets
    jwt_secret = generate_secret_key(64)  # Extra long for JWT
    database_password = generate_password(20)
    github_webhook_secret = generate_webhook_secret(20)
    gitlab_webhook_secret = generate_webhook_secret(20)
    api_key = generate_secret_key(32)
    
    print("🔑 Generated Secrets (store these securely!):")
    print("-" * 50)
    print(f"SECRET_KEY={jwt_secret}")
    print(f"DATABASE_PASSWORD={database_password}")
    print(f"GITHUB_WEBHOOK_SECRET={github_webhook_secret}")
    print(f"GITLAB_WEBHOOK_TOKEN={gitlab_webhook_secret}")
    print(f"API_ENCRYPTION_KEY={api_key}")
    print()
    
    # Generate .env file
    env_content = f"""# Agentic Agile System - Production Secrets
# Generated on: {os.getcwd()}
# 
# CRITICAL: Keep these secrets secure and never commit to version control!

# JWT Secret Key (keep this secret!)
SECRET_KEY={jwt_secret}

# Database Password
DATABASE_PASSWORD={database_password}

# Webhook Secrets
GITHUB_WEBHOOK_SECRET={github_webhook_secret}
GITLAB_WEBHOOK_TOKEN={gitlab_webhook_secret}

# API Encryption
API_ENCRYPTION_KEY={api_key}

# Instructions:
# 1. Copy these values to your production environment
# 2. Update your DATABASE_URL with the generated password
# 3. Configure your webhook endpoints with the generated secrets
# 4. Delete this file after copying the secrets
"""
    
    # Write to .env.secrets file
    secrets_file = Path(".env.secrets")
    with open(secrets_file, "w") as f:
        f.write(env_content)
    
    print(f"💾 Secrets also saved to: {secrets_file.absolute()}")
    print()
    print("⚠️  SECURITY WARNINGS:")
    print("   1. Copy these secrets to your secure environment")
    print("   2. Delete the .env.secrets file after copying")
    print("   3. Never commit these secrets to version control")
    print("   4. Rotate these secrets regularly")
    print()
    print("🚀 Next steps:")
    print("   1. Update your production environment variables")
    print("   2. Restart your services")
    print("   3. Test authentication and webhooks")

if __name__ == "__main__":
    main()