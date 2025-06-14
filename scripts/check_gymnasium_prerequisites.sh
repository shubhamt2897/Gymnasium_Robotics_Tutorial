#!/bin/bash

echo "Checking prerequisites for gymnasium-robotics installation..."
echo "-------------------------------------------------------"

# Check Python version
echo -n "Checking Python version: "
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version | cut -d' ' -f2)
    echo "Python $python_version found"
    python_major=$(echo $python_version | cut -d. -f1)
    python_minor=$(echo $python_version | cut -d. -f2)
    
    if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 7 ]); then
        echo "❌ Warning: gymnasium-robotics requires Python 3.7+ (found $python_version)"
    else
        echo "✅ Python version requirement met ($python_version >= 3.7)"
    fi
else
    echo "❌ Python 3 not found"
fi

# Check pip installation
echo -n "Checking pip installation: "
if command -v pip3 &> /dev/null; then
    pip_version=$(pip3 --version | awk '{print $2}')
    echo "✅ pip $pip_version found"
else
    echo "❌ pip3 not found. Please install pip"
fi

# Check for essential build tools
echo -n "Checking for build tools: "
if command -v gcc &> /dev/null; then
    gcc_version=$(gcc --version | head -n 1 | awk '{print $3}')
    echo "✅ gcc $gcc_version found"
else
    echo "❌ gcc not found. You may need to install build-essential"
fi

# Check for Python development headers
echo -n "Checking for Python development headers: "
if dpkg -l | grep -q "python3-dev\|python-dev"; then
    echo "✅ Python development headers found"
else
    echo "❌ Python development headers might be missing (python3-dev)"
fi

# Check for gymnasium installation
echo -n "Checking for gymnasium: "
if python3 -c "import gymnasium" &> /dev/null; then
    gymnasium_version=$(python3 -c "import gymnasium; print(gymnasium.__version__)" 2>/dev/null)
    echo "✅ gymnasium $gymnasium_version found"
else
    echo "❌ gymnasium not found. You should install it first: pip install gymnasium"
fi

# Check for MuJoCo dependencies
echo -n "Checking for MuJoCo dependencies: "
missing_deps=()

# Check for OpenGL
if ! dpkg -l | grep -q "libgl1-mesa\|nvidia-glx"; then
    missing_deps+=("libgl1-mesa-dev or nvidia drivers")
fi

# Check for X11 libs
if ! dpkg -l | grep -q "libx11-dev"; then
    missing_deps+=("libx11-dev")
fi

# Check for other common MuJoCo dependencies
deps=("libglew-dev" "libosmesa6-dev" "patchelf" "libglfw3-dev")
for dep in "${deps[@]}"; do
    if ! dpkg -l | grep -q "$dep"; then
        missing_deps+=("$dep")
    fi
done

if [ ${#missing_deps[@]} -eq 0 ]; then
    echo "✅ MuJoCo dependencies seem to be installed"
else
    echo "❌ Some MuJoCo dependencies might be missing:"
    for dep in "${missing_deps[@]}"; do
        echo "  - $dep"
    done
    echo ""
    echo "You might need to install them with:"
    echo "sudo apt-get install libgl1-mesa-dev libglew-dev libosmesa6-dev patchelf libglfw3-dev libx11-dev"
fi

# Check for Numpy and other scientific libraries
echo -n "Checking for NumPy and other scientific libraries: "
libs=("numpy" "scipy")
missing_libs=()

for lib in "${libs[@]}"; do
    if ! python3 -c "import $lib" &> /dev/null; then
        missing_libs+=("$lib")
    fi
done

if [ ${#missing_libs[@]} -eq 0 ]; then
    echo "✅ Scientific libraries found"
else
    echo "❌ Some scientific libraries might be missing:"
    for lib in "${missing_libs[@]}"; do
        echo "  - $lib"
    done
    echo ""
    echo "You might need to install them with: pip install numpy scipy"
fi

echo "-------------------------------------------------------"
echo "Recommendation:"
echo "If any prerequisites are missing, install them first."
echo "Then install gymnasium-robotics with: pip install gymnasium-robotics"
echo ""
echo "For a full environment setup, you might want to use:"
echo "pip install gymnasium-robotics[all]"
echo "-------------------------------------------------------"

# Make installation suggestion based on results
if python3 -c "import gymnasium" &> /dev/null; then
    echo "You can proceed with:"
    echo "pip install gymnasium-robotics"
else
    echo "First install gymnasium:"
    echo "pip install gymnasium"
    echo "Then install gymnasium-robotics:"
    echo "pip install gymnasium-robotics"
fi
