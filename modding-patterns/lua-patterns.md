# KCD2 Lua Scripting Patterns

Extracted from comprehensive modding patterns analysis. Focused on Lua scripting for KCD2 (CryEngine 5).

---

## 1. Bootstrap / Entry Point

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

---

## 2. Module Pattern (Object-Oriented Lua)

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

---

## 3. Console Command Registration

### Method 1: Direct Registration (LootBeacon style)
```lua
self:registerCommand("modname_command",
    "YourMod.Module:doSomething()",
    "Help text for the command")
```

### Method 2: Command Builder with Arguments (kcd2-cheat style)
```lua
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

---

## 4. Script Loading

```lua
Script.ReloadScript("path/to/script.lua")  -- Reload a script
Script.UnloadScript("path/to/script.lua")  -- Unload first, then reload
Script.ReloadScripts()                      -- Reload all scripts
Script.LoadScript("path/to/script.lua")     -- Load (returns 1 on success)
```

Source: kcd_coding_guide, kcd2-cheat

---

## 5. Timer Pattern

```lua
Script.SetTimer(milliseconds, function()
    -- code to execute after delay
end)
```

Source: KCD2Tools/LootBeacon

---

## 6. Event System

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

## 7. Key Binding & Input

### Lua Action Registration
```lua
Cheat:registerAction("1", "press", function() Cheat:proxy("cheat_phys_sprint") end)
Cheat:registerAction("3", "hold", function() Cheat:proxy("cheat_remove_buff_immortal") end)
```

Source: kcd2-cheat

### Config-Based Keybinds (mod.cfg)
```
-- Lua-style config with space-before-equals
loot_beacon_set_detection_radius =15.0
loot_beacon_set_highlight_duration =5.0
```

Source: KCD2Tools/LootBeacon

---

## 8. Entity & Game API

### Player Access
```lua
player = System.GetEntityByName("dude")  -- Get player entity
player:GetPos()                          -- Get position {x,y,z}
player:GetWorldPos()                     -- Get world position
player:SetWorldPos(pos)                  -- Set position
player:SetColliderMode(mode)             -- Set collision mode
player.class                             -- Returns "Player"
```

### Entity Queries
```lua
System.GetEntitiesInSphere(center, radius)                    -- All entities in sphere
System.GetEntitiesInSphereByClass(center, radius, class)      -- By class
System.GetEntitiesByClass("Player")                           -- All of class
System.GetEntityByName("name")                                -- By name
```

### Soul System (Player Stats)
```lua
player.soul:GetStatLevel("strength")     -- Get stat level
player.soul:SetState("health", 100)      -- Set state value
player.soul:GetState("health")           -- Get state value
player.soul:AddXP("skillname", xp)       -- Add experience
```

### Inventory System
```lua
player.inventory:CreateItem(guid, count, quality)
player.inventory:DeleteItemOfClass(guid, count)
player.inventory:GetCountOfClass(guid)
player.inventory:GetInventoryTable()
```

### Database Access
```lua
Database.LoadTable("buff")                        -- Load table into memory
Database.GetTableInfo("buff").LineCount           -- Get row count
Database.GetTableLine("buff", 0)                  -- Get row by index
```

Source: kcd2-cheat, kcd_coding_guide

---

## 9. Physics / Raycasting

```lua
local from = player:GetPos()
from.z = from.z + 1.615
local dir = System.GetViewCameraDir()
local hitData = {}
local hitCount = Physics.RayWorldIntersection(from, dir, 10, ent_all, player.id, nil, hitData)
```

Source: kcd_coding_guide

---

## 10. UI Patterns

### Game UI Notifications
```lua
Game.SendInfoText("Hello world", false, nil, 5)      -- Info text for 5s
Game.ShowItemsTransfer(itemGuid, amount)               -- Item transfer popup
System.LogAlways("Message")                            -- Console log
```

### ImGui (via KCD2ModLoader)
Dear ImGui integrated into Lua via `rom.gui` namespace for custom mod UI.

Source: kcd_coding_guide, kcd2-cheat, KCD2ModLoader

---

## 11. Persistence & Storage

### kcd2db (LuaDB)
```lua
local db = DB.Create("MyMod")
db.Set("key", value)           -- Local (per-save)
db.Get("key")
db.SetG("key", value)          -- Global (cross-save)
db.GetG("key")
```

Source: kcd2db

---

## 12. Error Handling & Logging

```lua
local success = Script.LoadScript(path)
if success ~= 1 then
    System.LogAlways("$4[ModName] Failed to load: " .. path)
    return false
end

System.LogAlways("Message")           -- Always visible
System.Log("$4[Mod] Error text")      -- Color-coded ($4=red)
```

---

## 13. Build & Distribution

### Version Placeholders
```lua
Cheat.version = "__VERSION__"  -- Replaced during build
```

### Multi-Mod Repository Pattern
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

See also: [PATTERNS.md](PATTERNS.md) for the complete patterns reference including C++ ASI mods, XML data modification, and PAK file system.
