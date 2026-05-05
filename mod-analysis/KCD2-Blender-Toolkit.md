# KCD2-Blender-Toolkit

- **GitHub**: https://github.com/Caseter/KCD2-Blender-Toolkit
- **Language**: Python (Blender addon)
- **Stars**: ~10+
- **Last Updated**: Active (2025)
- **Purpose**: Blender addon for importing/exporting KCD2 3D assets

## Description
A Blender addon that enables importing KCD2 game assets (models, textures, materials) and exporting custom assets for use in KCD2 mods. Based on the original KCD1 toolkit by Lune, modified for KCD2.

## File Structure
```
KCD2-Blender-Toolkit/
├── io_KCD2_Blender_Toolkit/
│   ├── __init__.py          # Addon registration, settings
│   ├── importers.py         # Asset import logic
│   ├── ui.py                # Blender UI panels
│   ├── dependency.py        # Dependency management
│   └── handlers/
│       ├── material_handler.py  # Material/texture handling
│       └── pak_handler.py      # PAK file reading
├── Tutorials/
│   └── Weapon Creation.md   # Tutorial for creating weapons
└── .vscode/settings.json
```

## Key Patterns

### Blender Addon Registration
```python
bl_info = {
    "name": "KCD2 Blender Toolkit",
    "author": "Created by Lune - Modified by Caseter",
    "version": (0, 2, 10),
    "blender": (4, 3, 0),
    "location": "File > Import",
    "description": "A toolkit for working with KCD2 Assets",
    "category": "Import-Export",
}
```

### Addon Settings (Preferences)
```python
class AddonSettings(AddonPreferences):
    filepath: StringProperty(
        name="KCD2 Data Directory",
        description="The folder of the .paks",
        subtype='FILE_PATH')
    texturesoutput: StringProperty(
        name="Textures Path (for conversion)",
        subtype='FILE_PATH')
    enable_update_check: BoolProperty(
        name="Enable Update Check", default=True)
```

## Modding Techniques
1. **Blender Python API**: Custom importers/exporters for game formats
2. **PAK File Reading**: Extracts assets from game .pak files
3. **Material Conversion**: Converts game materials to Blender materials
4. **CryExport Integration**: Exports in CryEngine-compatible format
5. **GitHub Update Checking**: Auto-checks for new versions
