# KCD2 Modding Patterns Summary

Compiled from analysis of 15+ actively maintained KCD2 modding repositories on GitHub.

## Table of Contents
1. [Mod Distribution & Packaging](#1-mod-distribution--packaging)
2. [Mod Manifest Format](#2-mod-manifest-format)
3. [Lua Scripting Patterns](#3-lua-scripting-patterns)
4. [C++ ASI Mod Patterns](#4-c-asi-mod-patterns)
5. [XML Data Modification](#5-xml-data-modification)
6. [PAK File System](#6-pak-file-system)
7. [Key Binding & Input](#7-key-binding--input)
8. [UI Patterns](#8-ui-patterns)
9. [Entity & Game API](#9-entity--game-api)
10. [Persistence & Storage](#10-persistence--storage)
11. [Build & Distribution](#11-build--distribution)
12. [Best Practices](#12-best-practices)

---

## 1. Mod Distribution & Packaging

### Mod Folder Structure
```
YourMod/
├── mod.manifest                    # REQUIRED: mod identity
├── mod.cfg                         # Optional: user configuration
├── Data/
│   ├── Scripts/
│   │   ├── Systems/your_mod.lua    # Auto-loaded bootstrap (by game engine)
│   │   └── YourMod/                # Module scripts
│   │       ├── core.lua
│   │       ├── config.lua
│   │       └── ...
│   ├── Libs/
│   │   ├── Tables/rpg/*.xml        # Game data overrides (buffs, items, etc.)
│   │   ├── Particles/*.xml         # Custom particle effects
│   │   └── config/*.xml            # Configuration files (keybinds, etc.)
│   └── Levels/{levelname}/         # Level-specific modifications
├── Localization/
│   ├── English_xml/*.xml           # English text
│   ├── German_xml/*.xml            # German text
│   └── ...                         # Other languages
```

### PAK Packaging Rules
PAK files are renamed ZIP archives. The game loads them from the Mods/ directory.
- `Data/{modid}.pak` - All Data/ contents except Levels/
- `Localization/{lang}.pak` - Localization files per language
- `Data/Levels/{level}/{modid}.pak` - Level-specific modifications

Source: KCD2-PAK (ModFolder.cs), Warbox

---

## 2. Mod Manifest Format

Every KCD2 mod requires a `mod.manifest` XML file:

```xml
<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
    <info>
        <name>Mod Display Name</name>
        <modid>unique_mod_identifier</modid>
        <description>Brief description of the mod</description>
        <author>AuthorName</author>
        <version>1.0.0</version>
        <created_on>2025-01-15</created_on>
        <modifies_level>false</modifies_level>
    </info>
</kcd_mod>
```

Key fields:
- `<modid>`: Used for PAK filename and mod_order.txt reference
- `<modifies_level>`: Set to `true` if mod changes level geometry/objects
- `<version>`: Semantic versioning recommended

Source: KCD2Tools (PizzleYanked, LootBeacon), KCD2-PAK (ModFolder.cs)

---

## 3. Lua Scripting Patterns

### 3.1 Bootstrap / Entry Point
The game engine auto-loads scripts from `Data/Scripts/Systems/` directory.

```lua
-- Data/Scripts/Systems/your_mod.lua
YourMod = {}

function YourMod_LoadModules()
    local modPath = "Scripts/YourMod"
    local modules = {"/core.lua", "/config.lua", "/feature.lua"}
    for _, file in ipairs(modules) do
        if Script.LoadScript(modPath .. file) ~= 1 then
            System.LogAlways("$4[YourMod] Failed: " .. file)
            return false
        end
    end
    return true
end

if YourMod_LoadModules() then
    YourMod.Core:initialize()
end
```

Source: KCD2Tools/LootBeacon

### 3.2 Module Pattern (Object-Oriented Lua)
```lua
YourMod.ModuleName = {
    initialized = false,
    config = {}
}

function YourMod.ModuleName:initialize()
    if self.initialized then return end
    -- initialization logic
    self.initialized = true
end

return YourMod.ModuleName
```

Source: KCD2Tools/LootBeacon (all modules)

### 3.3 Console Command Registration
```lua
-- Method 1: Direct registration (LootBeacon style)
self:registerCommand("modname_command",
    "YourMod.Module:doSomething()",
    "Help text for the command")

-- Method 2: Command builder with arguments (kcd2-cheat style)
Cheat:createCommand("cheat_find_buffs", {
    any = function(args, name, showHelp)
        return Cheat:argsGetOptional(args, name, nil, showHelp, "Partial match")
    end,
    exact = function(args, name, showHelp)
        return Cheat:argsGetOptional(args, name, nil, showHelp, "Exact match")
    end,
}, "Searches buffs by name",
    "Show all", "cheat_find_buffs",
    "Search for 'heal'", "cheat_find_buffs any:heal")
```

Source: KCD2Tools/LootBeacon, kcd2-cheat

### 3.4 Script Loading
```lua
Script.ReloadScript("path/to/script.lua")  -- Reload a script
Script.UnloadScript("path/to/script.lua")  -- Unload first, then reload
Script.ReloadScripts()                      -- Reload all scripts
Script.LoadScript("path/to/script.lua")     -- Load (returns 1 on success)
```

Source: kcd_coding_guide, kcd2-cheat

### 3.5 Timer Pattern
```lua
Script.SetTimer(milliseconds, function()
    -- code to execute after delay
end)
```

Source: KCD2Tools/LootBeacon

### 3.6 Event System
```lua
-- Register for system events
UIAction.RegisterEventSystemListener(self, "System", "OnSystemStarted", "onSystemStarted")
UIAction.RegisterEventSystemListener(self, "System", "OnGamePause", "onGamePause")
UIAction.RegisterEventSystemListener(self, "System", "OnGameResume", "onGameResume")

-- Unregister
UIAction.UnregisterEventSystemListener(self, "OnSystemStarted")
```

Source: KCD2Tools/LootBeacon

---

## 4. C++ ASI Mod Patterns

### 4.1 DLL Proxy Loading
```cpp
BOOL APIENTRY DllMain(HMODULE hmod, DWORD reason, PVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        dll_proxy::init();  // Forward calls to real DLL
        // Initialize hooks, renderer, etc.
    }
}
```

Source: KCD2ModLoader

### 4.2 ASI Loader Chain
Mods are loaded as .asi files via Ultimate ASI Loader (dinput8.dll or d3d12.dll proxy).

Source: kcd2db, kcd2lua, KCD2ModLoader

### 4.3 gEnv Resolution (Game Environment)
```cpp
// Find gEnv by scanning for "exec autoexec.cfg" string anchor
// Then trace back to pConsole pointer, subtract offset 0xA8
// Handles V1.2/V1.3 and V1.4+ different instruction layouts
```

Source: kcd2db

### 4.4 VTable Hooking
```cpp
void** vTable = *reinterpret_cast<void***>(pGame);
VirtualProtect(&vTable[INDEX], sizeof(void*), PAGE_EXECUTE_READWRITE, &old);
OriginalFunc = std::bit_cast<FuncPtr>(vTable[INDEX]);
InterlockedCompareExchangePointer(&vTable[INDEX], &HookedFunc, OriginalFunc);
```

Source: kcd2db

### 4.5 DetourModKit Framework
Used by TPVToggle for hooking game functions (camera, input, UI).

Source: KCD2Tools/TPVToggle

---

## 5. XML Data Modification

### 5.1 Game Data Table Format
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

### 5.2 Common XML Data Types
- **Buffs**: `Libs/Tables/rpg/buff*.xml` - Status effects, perks
- **Items**: `Libs/Tables/item/*.xml` - Item definitions
- **Keybinds**: `Libs/config/defaultProfile.xml`, `keybindSuperactions.xml`
- **Particles**: `Libs/Particles/*.xml` - Visual effects
- **Localization**: `Localization/{lang}/*.xml` - Text strings

Source: kcd2-cheat, KCD2Tools, kcd2-mod-docs

### 5.3 PTF (Patch Table Format)
Save only differences from base game data, not full file overrides.

Source: Warbox

### 5.4 XML Merging System
KCD2ModLoader provides runtime XML merging for files not fully supported by PTF (e.g., InventoryPreset).

Source: KCD2ModLoader

---

## 6. PAK File System

### 6.1 PAK = Renamed ZIP
```bash
# Manual creation
cd YourMod/Data && zip -r ../Data/modname.pak .
cd YourMod/Localization/English_xml && zip -r ../../English_xml.pak .
```

Source: kcd_coding_guide, KCD2-PAK

### 6.2 PAK Loading Order
1. Game's own .pak files
2. Mod .pak files from Mods/ directory (alphabetical by mod_order.txt)
3. Loose files from Data/ (editor mode only)

Source: kcd_coding_guide

### 6.3 File Replacement via PAK
Any game file can be overridden by including it in your mod's .pak with the same relative path.

Source: KCD2ModLoader (rom.game_data.on_cryfile_open)

---

## 7. Key Binding & Input

### 7.1 Superactions XML
```xml
<!-- Define keybind slots -->
<action consoleCMD="1" name="cheat_action slot:1 type:press" 
    onPress="1" onRelease="0" onHold="0" keyboard="_keybinds_ref_"/>
<action consoleCMD="1" name="cheat_action slot:1 type:hold" 
    onPress="0" onRelease="0" onHold="1" 
    holdTriggerDelay="0.5" holdRepeatDelay="0.25" keyboard="_keybinds_ref_"/>
```

Source: kcd2-cheat

### 7.2 Config-Based Keybinds (mod.cfg)
```
-- Lua-style config with space-before-equals
loot_beacon_set_detection_radius =15.0
loot_beacon_set_highlight_duration =5.0
```

Source: KCD2Tools/LootBeacon

### 7.3 Lua Action Registration
```lua
Cheat:registerAction("1", "press", function() Cheat:proxy("cheat_phys_sprint") end)
Cheat:registerAction("3", "hold", function() Cheat:proxy("cheat_remove_buff_immortal") end)
```

Source: kcd2-cheat

---

## 8. UI Patterns

### 8.1 ImGui (KCD2ModLoader)
Dear ImGui integrated into Lua via `rom.gui` namespace for custom mod UI.

Source: KCD2ModLoader

### 8.2 Game UI Notifications
```lua
Game.SendInfoText("Hello world", false, nil, 5)      -- Info text for 5s
Game.ShowItemsTransfer(itemGuid, amount)               -- Item transfer popup
System.LogAlways("Message")                            -- Console log
```

Source: kcd_coding_guide, kcd2-cheat

### 8.3 Particle Effects
Custom particle XML in `Libs/Particles/` for visual effects (highlighting, markers).

Source: KCD2Tools/LootBeacon

---

## 9. Entity & Game API

### 9.1 Player Access
```lua
player = System.GetEntityByName("dude")  -- Get player entity
player:GetPos()                          -- Get position {x,y,z}
player:GetWorldPos()                     -- Get world position
player:SetWorldPos(pos)                  -- Set position
player:SetColliderMode(mode)             -- Set collision mode
player.class                             -- Returns "Player"
```

Source: kcd_coding_guide, kcd2-cheat

### 9.2 Entity Queries
```lua
System.GetEntitiesInSphere(center, radius)           -- All entities in sphere
System.GetEntitiesInSphereByClass(center, radius, class)  -- By class
System.GetEntitiesByClass("Player")                  -- All of class
System.GetEntityByName("name")                       -- By name
```

Source: KCD2Tools/LootBeacon, kcd_coding_guide

### 9.3 Soul System (Player Stats)
```lua
player.soul:GetStatLevel("strength")     -- Get stat level
player.soul:SetState("health", 100)      -- Set state value
player.soul:GetState("health")           -- Get state value
player.soul:AddXP("skillname", xp)       -- Add experience
```

Source: kcd2-cheat

### 9.4 Inventory System
```lua
player.inventory:CreateItem(guid, count, quality)
player.inventory:DeleteItemOfClass(guid, count)
player.inventory:GetCountOfClass(guid)
player.inventory:GetInventoryTable()
```

Source: kcd2-cheat

### 9.5 Database Access
```lua
Database.LoadTable("buff")                        -- Load table into memory
Database.GetTableInfo("buff").LineCount           -- Get row count
Database.GetTableLine("buff", 0)                  -- Get row by index
```

Source: kcd2-cheat

### 9.6 Physics / Raycasting
```lua
local from = player:GetPos()
from.z = from.z + 1.615
local dir = System.GetViewCameraDir()
local hitData = {}
local hitCount = Physics.RayWorldIntersection(from, dir, 10, ent_all, player.id, nil, hitData)
```

Source: kcd_coding_guide

---

## 10. Persistence & Storage

### 10.1 kcd2db (LuaDB)
```lua
local db = DB.Create("MyMod")
db.Set("key", value)           -- Local (per-save)
db.Get("key")
db.SetG("key", value)          -- Global (cross-save)
db.GetG("key")
```

Source: kcd2db

### 10.2 mod.cfg (Configuration)
User-editable configuration file using cvar-style syntax.

Source: KCD2Tools/LootBeacon

---

## 11. Build & Distribution

### 11.1 GitHub Actions Release Pipeline
```yaml
# kcd2-cheat uses mods.sh + GitHub Actions for automated builds
# Bumps version in release.properties, creates .pak, uploads release
```

Source: kcd2-cheat

### 11.2 Version Placeholders
```lua
Cheat.version = "__VERSION__"  -- Replaced during build
```

Source: kcd2-cheat

### 11.3 Multi-Mod Repository Pattern
```
repo/
├── mods/
│   ├── mod-core/release.properties
│   ├── mod-extension1/release.properties
│   └── mod-extension2/release.properties
├── mods.sh              # Build all mods
└── .github/workflows/   # CI/CD
```

Source: kcd2-cheat

---

## 12. Best Practices

### 12.1 Mod Architecture
- Use modular file structure with clear separation of concerns
- Bootstrap in Systems/ directory, modules in separate directory
- Load modules in dependency order
- Initialize subsystems sequentially with error handling

### 12.2 Error Handling
```lua
local success = Script.LoadScript(path)
if success ~= 1 then
    System.LogAlways("$4[ModName] Failed to load: " .. path)
    return false
end
```

### 12.3 Logging
```lua
System.LogAlways("Message")           -- Always visible
System.Log("$4[Mod] Error text")      -- Color-coded ($4=red)
```

### 12.4 Configuration
- Use mod.cfg for user-configurable settings
- Use console commands for runtime configuration
- Provide sensible defaults

### 12.5 Compatibility
- Use pattern scanning for version-agnostic C++ mods
- Provide fallback behavior when APIs unavailable
- Test with multiple game versions

### 12.6 Distribution
- Always include mod.manifest
- Package as .pak (renamed .zip)
- Include localization for user-facing text
- Use mod_order.txt for load priority

---

## Repositories Analyzed

| # | Repository | Language | Type |
|---|-----------|----------|------|
| 1 | xiaoxiao921/KCD2ModLoader | C++ | Lua mod loader framework |
| 2 | tkhquang/KCD2Tools | Lua + C++ | Mod collection + scriptbind docs |
| 3 | KCD2ModManager/KCD2-Mod-Manager | C# | Mod manager (MVVM) |
| 4 | muyuanjin/kcd2-mod-docs | Lua/HTML | Official docs mirror |
| 5 | muyuanjin/kcd2db | C++ | SQLite Lua persistence |
| 6 | yobson1/kcd2lua | C++ + TS | VS Code Lua dev tools |
| 7 | pryans/kcd2-cheat | Lua | Comprehensive cheat mod |
| 8 | Destuur/ModForge | C# | XML editor (WPF/Blazor) |
| 9 | vawser/Warbox | C# | Table/localization editor |
| 10 | 7H3LaughingMan/KCD2-PAK | C# | PAK file creator |
| 11 | SDxBacon/kcd2-mod-dualdialog-tool | C# | Dual-language subtitles |
| 12 | altire-dev/kcd-toolkit | C# | Modding toolkit suite |
| 13 | Caseter/KCD2-Substance-Painter-DDS-Exporter | - | Texture pipeline |
| 14 | Caseter/KCD2-Blender-Toolkit | - | 3D asset pipeline |
| 15 | benjaminfoo/kcd_coding_guide | Docs | KCD Lua coding guide |
