# ModForge

- **GitHub**: https://github.com/Destuur/ModForge
- **Language**: C# (WPF + Blazor/MudBlazor)
- **Stars**: ~10+
- **Last Updated**: Active (2025)
- **Purpose**: Desktop modding tool for editing KCD2 XML game data

## Description
A WPF application with Blazor/MudBlazor frontend for reading, editing, and exporting KCD2 XML-based game files (perks, buffs, localizations) into playable mods.

## Key Features
- Import/edit/create Perks, Buffs, Debuffs, Localizations
- Drag-and-drop mod installation
- Automatic mod folder structure generation with mod.manifest
- Export mods as .pak files
- Mod loadout configuration per save file

## Modding Patterns
1. **XML Schema Understanding**: Reads game's XML structure for perks/buffs
2. **Automatic Manifest Generation**: Creates proper mod.manifest
3. **PAK Export**: Packages mods for game consumption
4. **Project Management**: Saves mod projects for iterative editing

## Workflow
1. Create new mod -> generates folder structure + manifest
2. Edit elements (perks, buffs, etc.) in visual editor
3. Export as .pak file
4. Add to mod_order.txt or use mod manager
