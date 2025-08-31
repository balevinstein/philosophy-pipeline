#!/bin/bash
# Development installation script for Philosophy Pipeline

set -e

echo "🚀 Setting up Philosophy Pipeline development environment..."

# Check if Python 3.8+ is available
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ is required, but found $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install development dependencies
echo "📚 Installing development dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🔒 Installing pre-commit hooks..."
pre-commit install

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "To activate the environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
echo "To format code:"
echo "  black src/ tests/"
echo ""
echo "To lint code:"
echo "  flake8 src/ tests/"
echo ""
echo "To run the pipeline:"
echo "  philosophy-pipeline --help"
echo ""
echo "Happy coding! 🚀"
