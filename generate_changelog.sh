#!/bin/bash

# Fetch recent commits
git log --pretty=format:"- \`%h\`: %s" -n 10 > /tmp/changelog_entries.txt

# Create the changelog content
cat > CHANGELOG.md << 'EOF'
# Changelog

## Features

EOF

# Append the commit entries
cat /tmp/changelog_entries.txt >> CHANGELOG.md

echo "Changelog generated successfully!"
