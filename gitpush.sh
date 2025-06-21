#!/bin/bash

# Ask for commit message
echo "🔧 Enter commit message:"
read msg

# Exit if no message is given
if [ -z "$msg" ]; then
  echo "❌ Commit message cannot be empty."
  exit 1
fi

# Add, commit, and push
git add .
git commit -m "$msg"
git push origin main

echo "✅ Push complete!"

