# MaMuJoCo Tutorial

A comprehensive tutorial and toolkit for working with MuJoCo physics simulator via the Gymnasium interface.

## 📋 Overview

This repository contains scripts, examples, and tutorials for using MuJoCo physics simulator with Gymnasium (formerly OpenAI Gym) for reinforcement learning and robotics simulation.

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- MuJoCo Python package
- Gymnasium with MuJoCo integration

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/MaMuJoCo_Tutorial.git
   cd MaMuJoCo_Tutorial
   ```

2. Install the required packages:
   ```bash
   pip install gymnasium mujoco
   ```

3. Check your MuJoCo installation:
   ```bash
   ./scripts/check_mujoco_version.sh
   ```

4. If you have rendering issues, run:
   ```bash
   ./scripts/fix_mujoco_rendering.sh
   ```

## 📁 Repository Structure

```
MaMuJoCo_Tutorial/
├── src/               # Source code for MuJoCo utilities and custom environments
├── scripts/           # Utility scripts for setup and diagnostics
├── tests/             # Unit tests
├── docs/              # Documentation and tutorials
├── LICENSE            # License file
└── README.md          # Project documentation
```

## 🎮 Usage

As you learn and experiment with MuJoCo, you can add your own examples and implementations to this repository.

## 📚 Documentation

Detailed documentation is available in the `docs` directory, covering:

- MuJoCo setup and configuration
- Working with Gymnasium environments
- Creating custom environments
- Troubleshooting common issues

## 🛠️ Troubleshooting

If you encounter rendering issues:

1. Check your graphics drivers and OpenGL support.
2. Try different rendering backends by setting environment variables:
   ```bash
   export MUJOCO_GL=glfw    # Default hardware accelerated rendering
   export MUJOCO_GL=egl     # Headless rendering with GPU acceleration
   export MUJOCO_GL=osmesa  # Software rendering (slow but most compatible)
   ```
3. Run the diagnostic script:
   ```bash
   python tests/test_mujoco_rendering.py
   ```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
