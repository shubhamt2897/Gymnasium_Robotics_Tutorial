# MuJoCo and Gymnasium Setup Guide

This document provides a comprehensive guide to setting up MuJoCo and Gymnasium for robotics simulation.

## Installation

### 1. Basic Installation

```bash
pip install gymnasium mujoco
```

### 2. Full Installation with Additional Features

```bash
pip install gymnasium[all] mujoco
```

### 3. For Robotics-specific Environments

```bash
pip install gymnasium-robotics
```

## System Dependencies

MuJoCo requires several system libraries for proper operation:

```bash
sudo apt-get update && sudo apt-get install -y \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    patchelf \
    libglfw3 \
    libglfw3-dev \
    libx11-dev \
    libxcursor-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxi-dev
```

## Rendering Backends

MuJoCo supports multiple rendering backends which can be configured via the `MUJOCO_GL` environment variable:

- **GLFW**: Hardware-accelerated rendering (default)
  ```bash
  export MUJOCO_GL=glfw
  ```

- **EGL**: Headless rendering with GPU acceleration
  ```bash
  export MUJOCO_GL=egl
  ```

- **OSMesa**: Software rendering (slow but most compatible)
  ```bash
  export MUJOCO_GL=osmesa
  ```

Add the preferred option to your `~/.bashrc` file for persistence.

## Troubleshooting

### Common Issues

1. **Segmentation Fault on Rendering**
   
   This often occurs due to incompatible OpenGL drivers or configurations.
   
   Solution: Try different rendering backends:
   ```bash
   export MUJOCO_GL=osmesa
   ```

2. **Library Not Found Error**

   If you see errors about missing libraries, ensure all dependencies are installed:
   ```bash
   sudo apt-get install -y libgl1-mesa-dev libglew-dev libosmesa6-dev
   ```

3. **Black Rendering Window**

   This can happen due to incompatible graphics drivers.
   
   Solution: Update your graphics drivers or try a different rendering backend.

### Debugging Tools

Use our diagnostic scripts in the `scripts/` directory:

```bash
./scripts/check_mujoco_version.sh
./scripts/fix_mujoco_rendering.sh
```

## Verifying Installation

Run the test script to verify your MuJoCo installation:

```bash
python tests/test_mujoco_rendering.py
```

You should see a rendering window with a MuJoCo environment if everything is working correctly.
