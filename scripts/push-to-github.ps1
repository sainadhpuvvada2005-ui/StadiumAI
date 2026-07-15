#!/usr/bin/env pwsh
# GitHub Push Script for StadiumAI
# This script automates pushing your StadiumAI project to GitHub

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$Repository = "StadiumAI",
    
    [Parameter(Mandatory=$false)]
    [string]$AuthMethod = "https"
)

Write-Host "╔════════════════════════════════════════════════════════╗"
Write-Host "║        StadiumAI - GitHub Push Script                ║"
Write-Host "╚════════════════════════════════════════════════════════╝"

# Verify we're in the right directory
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: Not in a git repository directory" -ForegroundColor Red
    Write-Host "Please navigate to the StadiumAI project directory first"
    exit 1
}

Write-Host "✓ Git repository detected" -ForegroundColor Green
Write-Host ""

# Step 1: Configure git user
Write-Host "📝 Configuring git user..." -ForegroundColor Cyan
git config user.name "StadiumAI Developer"
git config user.email "admin@stadiumai.example"
Write-Host "✓ Git configured" -ForegroundColor Green
Write-Host ""

# Step 2: Check status
Write-Host "📊 Checking git status..." -ForegroundColor Cyan
git status
Write-Host ""

# Step 3: Add files
Write-Host "📦 Adding files to git..." -ForegroundColor Cyan
git add .
Write-Host "✓ Files staged" -ForegroundColor Green
Write-Host ""

# Step 4: Commit
Write-Host "💾 Creating commit..." -ForegroundColor Cyan
$commitMessage = "Initial commit: StadiumAI - AI-powered smart stadium operations platform for FIFA World Cup 2026"
git commit -m $commitMessage
Write-Host "✓ Changes committed" -ForegroundColor Green
Write-Host ""

# Step 5: Set up remote
Write-Host "🔗 Setting up GitHub remote..." -ForegroundColor Cyan
$remoteUrl = if ($AuthMethod -eq "ssh") {
    "git@github.com:$GitHubUsername/$Repository.git"
} else {
    "https://github.com/$GitHubUsername/$Repository.git"
}

Write-Host "Remote URL: $remoteUrl" -ForegroundColor Yellow
git remote add origin $remoteUrl -ErrorAction SilentlyContinue
Write-Host "✓ Remote configured" -ForegroundColor Green
Write-Host ""

# Step 6: Set main branch
Write-Host "🌳 Setting main branch..." -ForegroundColor Cyan
git branch -M main
Write-Host "✓ Branch set to main" -ForegroundColor Green
Write-Host ""

# Step 7: Push to GitHub
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "This will prompt for authentication if needed" -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════╗"
    Write-Host "║           ✓ Successfully pushed to GitHub!            ║"
    Write-Host "╚════════════════════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "📍 Repository URL:" -ForegroundColor Green
    Write-Host "   https://github.com/$GitHubUsername/$Repository"
    Write-Host ""
    Write-Host "🔗 Next steps:" -ForegroundColor Cyan
    Write-Host "   1. Visit your repository on GitHub"
    Write-Host "   2. Go to Settings → Make sure 'Public' is selected"
    Write-Host "   3. Add topics for discoverability"
    Write-Host "   4. Enable GitHub Pages (optional)"
} else {
    Write-Host ""
    Write-Host "❌ Error during push. Please check your credentials." -ForegroundColor Red
    Write-Host "For HTTPS: Use a Personal Access Token as password" -ForegroundColor Yellow
    Write-Host "For SSH: Ensure SSH keys are configured" -ForegroundColor Yellow
}
