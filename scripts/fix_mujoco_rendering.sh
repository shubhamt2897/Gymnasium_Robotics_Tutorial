#!/bin/bash

echo "Installing MuJoCo rendering dependencies..."
echo "-------------------------------------------"

# Install rendering dependencies
sudo apt-get update && sudo apt-get install -y \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    libglfw3 \
    libglfw3-dev \
    libx11-dev \
    libxcursor-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxi-dev \
    mesa-utils

echo "Setting up EGL rendering if needed..."
# For headless servers or systems with rendering issues
if ! command -v glxinfo &> /dev/null || ! glxinfo | grep -q "direct rendering: Yes"; then
    echo "Setting up EGL rendering support..."
    # Install additional EGL support
    sudo apt-get install -y libegl1-mesa libegl1-mesa-dev
    
    # Create a script to set environment variables for headless rendering
    cat > "$HOME/.mujoco_egl_setup.sh" << 'EOF'
#!/bin/bash
# Environment variables for MuJoCo headless rendering
export MUJOCO_GL=egl
# For older mujoco-py
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so
EOF
    
    # Add to bashrc if not already there
    if ! grep -q "source.*mujoco_egl_setup.sh" "$HOME/.bashrc"; then
        echo "# MuJoCo headless rendering setup" >> "$HOME/.bashrc"
        echo "source $HOME/.mujoco_egl_setup.sh" >> "$HOME/.bashrc"
    fi
    
    echo "Added EGL rendering support. Please run 'source ~/.bashrc' after this script completes."
fi

echo "Testing MuJoCo rendering after installing dependencies..."
echo "-------------------------------------------------------"

# Create a temporary Python script to test rendering
cat > /tmp/test_mujoco_rendering.py << 'EOF'
import sys

try:
    import mujoco
    import numpy as np
    
    print("Testing MuJoCo rendering...")
    
    # Create a simple model
    xml = """
    <mujoco>
        <worldbody>
            <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
            <geom type="plane" size="1 1 0.1" rgba=".9 .9 .9 1"/>
            <body pos="0 0 1">
                <joint type="free"/>
                <geom type="sphere" size="0.1" rgba="1 0 0 1"/>
            </body>
        </worldbody>
    </mujoco>
    """
    
    # Load the model
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    
    # Initialize renderer
    renderer = mujoco.Renderer(model, height=480, width=640)
    
    # Step simulation and render
    mujoco.mj_step(model, data)
    renderer.update_scene(data)
    pixels = renderer.render()
    
    # Check if rendering produced valid pixels
    if np.any(pixels):
        print("✅ MuJoCo rendering is working correctly!")
        sys.exit(0)
    else:
        print("❌ Rendering produced empty image")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error testing MuJoCo rendering: {e}")
    sys.exit(1)
EOF

# Run the test script
echo "Running MuJoCo rendering test..."
python3 /tmp/test_mujoco_rendering.py

echo "-------------------------------------------"
echo "Next steps:"
echo "1. Run 'source ~/.bashrc' to apply environment changes"
echo "2. Try running a MuJoCo environment to verify rendering:"
echo "   python3 -c 'import gymnasium as gym; env = gym.make(\"HumanoidStandup-v4\", render_mode=\"human\"); env.reset(); for _ in range(100): env.step(env.action_space.sample()); env.render()'"
echo "-------------------------------------------"
echo "If you're still having rendering issues, you might need to:"
echo "1. Try different GL backends by setting environment variables:"
echo "   export MUJOCO_GL=glfw    # Default hardware accelerated rendering"
echo "   export MUJOCO_GL=egl     # Headless rendering with GPU acceleration"
echo "   export MUJOCO_GL=osmesa  # Software rendering (slow but most compatible)"
echo "2. Check your GPU drivers and OpenGL support:"
echo "   glxinfo | grep \"OpenGL\""
