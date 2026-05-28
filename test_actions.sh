#!/bin/bash
# Test GitHub Actions workflows locally using act

set -e

echo "================================"
echo "GitHub Actions Local Tester"
echo "================================"
echo ""

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "❌ act is not installed"
    echo ""
    echo "Install act:"
    echo "  macOS:   brew install act"
    echo "  Windows: choco install act-cli"
    echo "  Linux:   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash"
    exit 1
fi

echo "✅ act is installed"
echo ""

# Menu
echo "Select what to test:"
echo "1. Run all workflows"
echo "2. Test job only"
echo "3. Build Linux"
echo "4. Build Windows"
echo "5. Build macOS"
echo "6. Run specific workflow file"
echo ""

read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo "Running all workflows..."
        act
        ;;
    2)
        echo "Running test job..."
        act -j test
        ;;
    3)
        echo "Running Linux build..."
        act -j build-linux
        ;;
    4)
        echo "Running Windows build..."
        act -j build-windows -P windows-latest=ghcr.io/catthehacker/windows:full-latest
        ;;
    5)
        echo "Running macOS build..."
        act -j build-macos
        ;;
    6)
        read -p "Enter workflow filename (.github/workflows/...): " workflow
        echo "Running $workflow..."
        act -W "$workflow"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Test complete!"
