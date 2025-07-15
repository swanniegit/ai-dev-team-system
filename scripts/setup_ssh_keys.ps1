# SSH Key Setup Script for GitHub
# This script helps you generate and configure SSH keys for GitHub

Write-Host "Setting up SSH keys for GitHub..." -ForegroundColor Green

# Check if SSH keys already exist
$sshDir = "$env:USERPROFILE\.ssh"
$idRsaPath = "$sshDir\id_rsa"
$idRsaPubPath = "$sshDir\id_rsa.pub"

if (Test-Path $idRsaPath) {
    Write-Host "SSH keys already exist at $idRsaPath" -ForegroundColor Yellow
    Write-Host "Public key:" -ForegroundColor Cyan
    Get-Content $idRsaPubPath
    Write-Host ""
    Write-Host "If you want to generate new keys, delete the existing ones first." -ForegroundColor Yellow
    exit 0
}

# Create .ssh directory if it doesn't exist
if (!(Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir -Force
    Write-Host "Created SSH directory: $sshDir" -ForegroundColor Green
}

# Generate SSH key pair
Write-Host "Generating SSH key pair..." -ForegroundColor Cyan
Write-Host "When prompted, you can press Enter to use the default file location." -ForegroundColor Yellow
Write-Host "For the passphrase, you can either create one or leave it empty (less secure)." -ForegroundColor Yellow

ssh-keygen -t rsa -b 4096 -C "$env:USERNAME@$(hostname)"

# Check if key generation was successful
if (Test-Path $idRsaPath) {
    Write-Host "SSH key pair generated successfully!" -ForegroundColor Green
    
    # Display the public key
    Write-Host ""
    Write-Host "Your public SSH key:" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Gray
    Get-Content $idRsaPubPath
    Write-Host "==========================================" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Copy the public key above (everything between the lines)" -ForegroundColor White
    Write-Host "2. Go to GitHub.com > Settings > SSH and GPG keys" -ForegroundColor White
    Write-Host "3. Click New SSH key" -ForegroundColor White
    Write-Host "4. Give it a title (e.g., Work Laptop)" -ForegroundColor White
    Write-Host "5. Paste the public key in the Key field" -ForegroundColor White
    Write-Host "6. Click Add SSH key" -ForegroundColor White
    Write-Host ""
    Write-Host "7. Test the connection with: ssh -T git@github.com" -ForegroundColor White
    Write-Host "8. Update your repository remote to use SSH:" -ForegroundColor White
    Write-Host "   git remote set-url origin git@github.com:swanniegit/ai-dev-team-system.git" -ForegroundColor White
    
} else {
    Write-Host "Failed to generate SSH keys" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "SSH key setup complete!" -ForegroundColor Green 