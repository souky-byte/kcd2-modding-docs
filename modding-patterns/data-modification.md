# KCD2 XML Data Modification Patterns

KCD2 uses XML tables for game data (buffs, items, perks, keybinds, etc.). Mods can override or extend these tables.

---

## Game Data Table Format

```xml
<?xml version="1.0" encoding="us-ascii"?>
<database xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    name="tablename" xsi:noNamespaceSchemaLocation="../database.xsd">
    <table_name version="1">
        <row field1="value1" field2="value2" />
    </table_name>
</database>
```

Source: kcd2-cheat (buff__cheat.xml)

---

## Common XML Data Types

| Data Type | Path | Description |
|-----------|------|-------------|
| Buffs | `Libs/Tables/rpg/buff*.xml` | Status effects, perks |
| Items | `Libs/Tables/item/*.xml` | Item definitions |
| Keybinds | `Libs/config/defaultProfile.xml`, `keybindSuperactions.xml` | Input bindings |
| Particles | `Libs/Particles/*.xml` | Visual effects |
| Localization | `Localization/{lang}/*.xml` | Text strings |

Source: kcd2-cheat, KCD2Tools, kcd2-mod-docs

---

## Keybinding Superactions XML

```xml
<!-- Define keybind slots -->
<action consoleCMD="1" name="cheat_action slot:1 type:press" 
    onPress="1" onRelease="0" onHold="0" keyboard="_keybinds_ref_"/>
<action consoleCMD="1" name="cheat_action slot:1 type:hold" 
    onPress="0" onRelease="0" onHold="1" 
    holdTriggerDelay="0.5" holdRepeatDelay="0.25" keyboard="_keybinds_ref_"/>
```

Source: kcd2-cheat

---

## PTF (Patch Table Format)

Save only differences from base game data, not full file overrides. This is the preferred method for table modifications.

Source: Warbox

---

## XML Merging System

KCD2ModLoader provides runtime XML merging for files not fully supported by PTF (e.g., InventoryPreset). The system:

1. Intercepts file open calls via `rom.game_data.on_cryfile_open`
2. Loads the original file content
3. Applies patches from all active mods
4. Returns merged content to the game engine

```cpp
// Global XML context -> filename -> modifications buffer
ankerl::unordered_dense::map<std::string, 
    ankerl::unordered_dense::map<std::string, std::vector<std::string>>> 
    g_xml_context_to_xml_filename_to_modifications;

void apply_xml_patches(std::string &originalFileContent, 
                       const std::vector<std::string> &patchFileContents, 
                       bool is_inventory_preset);
```

Source: KCD2ModLoader

---

## Table Patching (Data Table Overrides)

KCD2ModLoader supports runtime table patching:

```cpp
// Table name -> line -> patch info
std::map<std::string, std::map<std::string, std::vector<table_patch_info_t>>> 
    g_table_name_to_added_line_to_info;
std::map<std::string, std::map<std::string, std::vector<table_patch_info_t>>> 
    g_table_name_to_modified_line_to_info;
```

Source: KCD2ModLoader

---

## Particle Effects XML

Custom particle definitions in `Libs/Particles/` for visual effects (highlighting, markers, etc.).

Source: KCD2Tools/LootBeacon

---

## Best Practices for Data Modification

1. **Use PTF when possible** — only store changed entries, not full files
2. **Match the exact XML schema** — the game validates table structure
3. **Include `<database>` root element** with proper namespace and schema reference
4. **Test compatibility** with other mods that modify the same tables
5. **Use tools** like ModForge or Warbox for visual editing and validation
