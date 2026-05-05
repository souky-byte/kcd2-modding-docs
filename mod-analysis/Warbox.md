# Warbox

- **GitHub**: https://github.com/vawser/Warbox
- **Language**: C# (.NET 7)
- **Stars**: ~30+
- **Last Updated**: Active (2025)
- **Purpose**: Standalone modding tool for editing KCD2 XML configuration tables

## Description
Warbox is a desktop application for searching, editing, and packaging KCD2's XML-based game data tables and localization files. Based on DSMapStudio architecture.

## Key Features
- **Table Editor**: Search/edit all configuration table data (perks, buffs, items)
- **Text Editor**: Search/edit text localization files
- **Save/Package Workflow**: Edit -> Save -> Package as .pak
- **PTF (Patch) System**: Save only modified entries as patches

## Modding Workflow
1. Create project pointing to game Data directory
2. Edit tables in the visual editor
3. Save as PTF (Patch) - only changed entries
4. Package patched files into .pak
5. Auto-generates mod.manifest if missing

## PAK Packaging Convention
```
YourMod/
├── mod.manifest
├── Data/
│   └── modname.pak          # Table modifications
├── Localization/
│   └── English_xml.pak      # Localization modifications
└── Data/Levels/
    └── trosecko/
        └── modname.pak      # Level-specific modifications
```

## Key Patterns
- **PTF (Patch Table Format)**: Only store differences from base game
- **Source vs PTF**: Full file vs patch-only saving
- **Automatic Manifest**: Creates mod.manifest if missing
- **Vulkan UI**: Requires Vulkan 1.3 for rendering
