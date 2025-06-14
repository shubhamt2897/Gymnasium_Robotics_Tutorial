#!/bin/bash

echo "Checking MuJoCo installation and version..."
echo "-------------------------------------------"

# Check if MuJoCo is installed via pip
echo -n "Checking for MuJoCo Python package: "
if python3 -c "import mujoco" &> /dev/null; then
    mujoco_version=$(python3 -c "import mujoco; print(mujoco.__version__)" 2>/dev/null)
    echo "✅ MuJoCo Python package found (version $mujoco_version)"
else
    echo "❌ MuJoCo Python package not found"
fi

# Check for alternative mujoco-py package
echo -n "Checking for mujoco-py package: "
if python3 -c "import mujoco_py" &> /dev/null; then
    mujoco_py_version=$(python3 -c "import mujoco_py; print(mujoco_py.__version__)" 2>/dev/null)
    echo "✅ mujoco-py package found (version $mujoco_py_version)"
else
    echo "❌ mujoco-py package not found"
fi

# Check for gymnasium's MuJoCo
echo -n "Checking for gymnasium's MuJoCo integration: "
if python3 -c "import gymnasium.envs.mujoco" &> /dev/null; then
    gymnasium_version=$(python3 -c "import gymnasium; print(gymnasium.__version__)" 2>/dev/null)
    echo "✅ gymnasium MuJoCo integration found (gymnasium version $gymnasium_version)"
else
    echo "❌ gymnasium MuJoCo integration not found"
fi

# Check for system-wide MuJoCo installation
echo -n "Checking for system-wide MuJoCo installation: "

# Common MuJoCo installation locations
mujoco_locations=(
    "$HOME/.mujoco"
    "/usr/local/mujoco"
    "/opt/mujoco"
    "$HOME/.local/mujoco"
)

found_mujoco=false

for location in "${mujoco_locations[@]}"; do
    if [ -d "$location" ]; then
        echo "✅ Found MuJoCo directory at: $location"
        echo "Installed versions:"
        for version_dir in "$location"/*; do
            if [ -d "$version_dir" ]; then
                base_name=$(basename "$version_dir")
                echo "  - $base_name"
            fi
        done
        found_mujoco=true
    fi
done

# Check for MuJoCo in environment variables
echo -n "Checking for MuJoCo in environment variables: "
if [[ -n "$MUJOCO_PY_MUJOCO_PATH" ]]; then
    echo "✅ MUJOCO_PY_MUJOCO_PATH is set to: $MUJOCO_PY_MUJOCO_PATH"
    found_mujoco=true
elif [[ -n "$MUJOCO_PATH" ]]; then
    echo "✅ MUJOCO_PATH is set to: $MUJOCO_PATH"
    found_mujoco=true
else
    echo "❌ No MuJoCo environment variables found"
fi

if [ "$found_mujoco" = false ]; then
    echo "❌ No system-wide MuJoCo installation detected"
fi

# Check MuJoCo rendering capabilities
echo -n "Checking MuJoCo rendering capabilities: "
if python3 -c "
import sys
try:
    import mujoco
    try:
        # Try to initialize the OpenGL renderer
        mujoco.MjrContext(mujoco.MjModel.from_xml_string('<mujoco/>'))
        print('OpenGL rendering should work')
        sys.exit(0)
    except Exception as e:
        print(f'OpenGL rendering might have issues: {e}')
        sys.exit(1)
except ImportError:
    try:
        import mujoco_py
        try:
            # Try to initialize a simple model with rendering
            from mujoco_py import load_model_from_xml, MjSim
            model = load_model_from_xml('<mujoco/>')
            sim = MjSim(model)
            print('mujoco_py rendering should work')
            sys.exit(0)
        except Exception as e:
            print(f'mujoco_py rendering might have issues: {e}')
            sys.exit(1)
    except ImportError:
        print('Neither mujoco nor mujoco_py packages found')
        sys.exit(1)
" &> /dev/null; then
    echo "✅ MuJoCo rendering seems to be working"
else
    echo "❌ MuJoCo rendering might have issues"
fi

echo "-------------------------------------------"
echo "Summary:"
if python3 -c "import mujoco" &> /dev/null || python3 -c "import mujoco_py" &> /dev/null; then
    echo "MuJoCo is installed via Python packages."
    if [ "$found_mujoco" = true ]; then
        echo "System-wide MuJoCo installation also detected."
    fi
    echo "You should be able to use gymnasium-robotics with your current setup."
else
    echo "MuJoCo Python packages not found."
    if [ "$found_mujoco" = true ]; then
        echo "System-wide MuJoCo installation detected, but Python bindings might be missing."
        echo "Consider installing MuJoCo Python packages with: pip install mujoco"
    else
        echo "No MuJoCo installation detected."
        echo "Install MuJoCo with: pip install mujoco"
    fi
fi
