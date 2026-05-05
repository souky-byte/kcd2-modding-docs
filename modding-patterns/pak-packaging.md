# KCD2 PAK File Packaging

PAK files are the standard distribution format for KCD2 mods. They are renamed ZIP archives loaded by the game engine.

---

## PAK = Renamed ZIP

```bash
# Manual creation
cd YourMod/Data && zip -r ../Data/modname.pak .
cd YourMod/Localization/English_xml && zip -r ../../English_xml.pak .
```

Source: kcd_coding_guide, KCD2-PAK

---

## PAK Packaging Rules

Based on KCD2-PAK (ModFolder.cs) analysis:

| Source Path | PAK Destination | Description |
|------------|----------------|-------------|
| `Data/` (excluding Levels/) | `Data/{modid}.pak` | Scripts, tables, configs |
| `Localization/{lang}/` | `Localization/{lang}.pak` | Per-language text |
| `Data/Levels/{levelname}/` | `Data/Levels/{levelname}/{modid}.pak` | Level-specific mods |

### Mod Folder Structure
```
YourMod/
├── mod.manifest                    # REQUIRED: mod identity
├── mod.cfg                         # Optional: user configuration
├── Data/
│   ├── Scripts/
│   │   ├── Systems/your_mod.lua    # Auto-loaded bootstrap
│   │   └── YourMod/                # Module scripts
│   │       ├── core.lua
│   │       ├── config.lua
│   │       └── ...
│   ├── Libs/
│   │   ├── Tables/rpg/*.xml        # Game data overrides
│   │   ├── Particles/*.xml         # Custom particle effects
│   │   └── config/*.xml            # Configuration files
│   └── Levels/{levelname}/         # Level-specific modifications
├── Localization/
│   ├── English_xml/*.xml           # English text
│   ├── German_xml/*.xml            # German text
│   └── ...                         # Other languages
```

---

## PAK Loading Order

1. Game's own .pak files
2. Mod .pak files from `Mods/` directory (alphabetical by `mod_order.txt`)
3. Loose files from `Data/` (editor mode only)

Source: kcd_coding_guide

---

## File Replacement via PAK

Any game file can be overridden by including it in your mod's .pak with the same relative path. The game resolves files by checking mod PAKs first, then falling back to base game PAKs.

Source: KCD2ModLoader (rom.game_data.on_cryfile_open)

---

## PAK File Format Details (KCD2-PAK)

```csharp
// KCD2-PAK implementation notes:
// - Uses System.IO.Compression (ZIP format)
// - Custom PakArchive/PakArchiveEntry classes
// - DOS timestamp encoding for compatibility
// - UTF-8 and ASCII encoding support
```

Source: KCD2-PAK

---

## Packaging Convention (Warbox)

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

Source: Warbox

---

## Tools for PAK Creation

| Tool | Method |
|------|--------|
| **KCD2-PAK** | Drag-and-drop or right-click context menu |
| **kcd-toolkit** | KCD PAK Builder — directory to PAK |
| **Warbox** | Save -> Package workflow |
| **ModForge** | Export as .pak from visual editor |
| **Manual** | `zip -r modname.pak .` |

---

## Best Practices

- Always include `mod.manifest` with valid `<modid>`
- Use the `<modid>` as the PAK filename
- Separate localization into per-language PAKs
- Level-specific mods go in `Data/Levels/{level}/{modid}.pak`
- Test with multiple mods to verify load order compatibility
- Use `mod_order.txt` in `Mods/` directory for explicit load priority
