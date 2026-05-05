# kcd2lua

- **GitHub**: https://github.com/yobson1/kcd2lua
- **Language**: C++ + TypeScript (VS Code extension)
- **Stars**: ~10+
- **Last Updated**: Active (2025)
- **Purpose**: VS Code extension for live Lua execution in KCD2

## Description
Provides a VS Code extension + ASI DLL that communicate via TCP socket, allowing developers to write and execute Lua code directly in the running game from VS Code. Supports Linux/Wine.

## File Structure
```
kcd2lua/
├── cpp/                    # C++ ASI DLL
│   ├── CMakeLists.txt
│   ├── build.sh
│   └── src/               # DLL source
└── vscode_extension/       # VS Code extension
    ├── package.json
    ├── src/                # TypeScript source
    └── README.md
```

## Key Patterns
- **TCP Socket Communication**: ASI DLL listens on localhost, VS Code connects
- **Ultimate ASI Loader**: Loaded as vscodelua.asi via dinput8.dll proxy
- **Cross-Platform**: Works on Linux via Wine with WINEDLLOVERRIDES
- **Live Code Execution**: Send Lua snippets to running game
- **Version Matching**: ASI and extension major versions must match

## Usage Pattern
```bash
# Install ASI loader as dinput8.dll in game bin directory
# Copy vscodelua.asi to same directory
# Linux: add WINEDLLOVERRIDES="dinput8,n,b" to launch options
# Install VS Code extension from marketplace
# Write Lua in VS Code, execute with Ctrl+Enter
```
