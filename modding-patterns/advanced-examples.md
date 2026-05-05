# KCD2 Advanced Code Examples

Real code excerpts from production KCD2 mods, demonstrating advanced patterns.

---

## 1. DLL Proxy Loading (KCD2ModLoader)

C++ ASI mods use DLL proxying to hook into the game process:

```cpp
BOOL APIENTRY DllMain(HMODULE hmod, DWORD reason, PVOID)
{
    if (reason == DLL_PROCESS_ATTACH)
    {
        dll_proxy::init();  // Forward d3d12 calls to real DLL
        rom::init("KCD2ModLoader", "WHGame.dll", "rom");
        // Initialize logger, hooking, renderer...
        kcd2_init();        // Resolve game addresses
        g_hooking->enable();
        asi_loader::init(hmod);  // Load other ASI mods
    }
}
```

Source: KCD2ModLoader

---

## 2. gEnv Resolution via Signature Scanning (kcd2db)

Finding game environment pointers through pattern scanning — version-agnostic:

```cpp
std::optional<uintptr_t> find_env_addr() {
    lm_module_t module;
    while (!LM_FindModule("WHGame.DLL", &module)) {
        std::this_thread::yield();
    }
    // Step 1: Find "exec autoexec.cfg" string anchor
    uintptr_t string_addr = LM_SigScan(string_pattern.c_str(), module.base, module.size);
    // Step 2: Find LEA instruction referencing the string
    // Step 3: Check version context (V1.4+ vs V1.2/V1.3)
    // Step 4: Calculate gEnv base from pConsole offset (0xA8)
    return console_ptr_addr - 0xA8;
}
```

Source: kcd2db

---

## 3. VTable Hooking (kcd2db)

Hooking game functions via virtual table replacement:

```cpp
bool __thiscall Hooked_CompleteInit(IGame* pThis) {
    LuaDB* luaDB = gLuaDB.load(std::memory_order_acquire);
    luaDB->RegisterLuaAPI();
    return OriginalCompleteInit(pThis);
}

// Hook via vtable replacement
void** vTable = *reinterpret_cast<void***>(pGame);
VirtualProtect(&vTable[4], sizeof(void*), PAGE_EXECUTE_READWRITE, &old);
OriginalCompleteInit = std::bit_cast<CompleteInitFunc>(vTable[4]);
InterlockedCompareExchangePointer(&vTable[4], &Hooked_CompleteInit, OriginalCompleteInit);
```

Source: kcd2db

---

## 4. Modular Bootstrap with Error Handling (KCD2Tools/LootBeacon)

Production-grade Lua mod initialization:

```lua
-- Systems/loot_beacon.lua - Game loads this automatically
LootBeacon = {}

function LootBeacon_LoadModules()
    local modPath = "Scripts/LootBeacon"
    local moduleFiles = {
        "/core.lua", "/logger.lua", "/config.lua",
        "/entity_detector.lua", "/highlighter.lua",
        "/command_registry.lua", "/event_handler.lua", "/ui_manager.lua"
    }
    for _, file in ipairs(moduleFiles) do
        local success = Script.LoadScript(modPath .. file)
        if success ~= 1 then
            System.LogAlways("$4[LootBeacon] Failed to load: " .. file)
            return false
        end
    end
    return true
end

if LootBeacon_LoadModules() then
    LootBeacon.Core:initialize()
end
```

Source: KCD2Tools/LootBeacon

---

## 5. Cheat Module Bootstrap (kcd2-cheat)

Version placeholder, module loading, key binding registration:

```lua
Cheat = {}
Cheat.version = "__VERSION__"

function Cheat:loadFile(file)
    System.LogAlways("Loading file [" .. tostring(file) .. "] ...")
    Script.ReloadScript(file)
end

function Cheat:onInit()
    System.LogAlways("Cheat:OnInit")
    Cheat:loadFile("scripts/cheat/cheat_util.lua")
    Cheat:loadFile("scripts/cheat/cheat_args.lua")
    -- ... load all modules in order
    Cheat:loadFile("scripts/cheat/cheat_core_actions.lua")
    
    -- Register default key bindings
    Cheat:registerAction("1", "press", function() Cheat:proxy("cheat_phys_sprint") end)
    Cheat:registerAction("3", "press", function() Cheat:proxy("cheat_add_buff_immortal") end)
    Cheat:registerAction("3", "hold", function() Cheat:proxy("cheat_remove_buff_immortal") end)
end
```

Source: kcd2-cheat

---

## 6. Advanced Command Registration (kcd2-cheat)

Commands with argument parsing, help text, and examples:

```lua
Cheat:createCommand("cheat_find_buffs", {
    any = function(args, name, showHelp) 
        return Cheat:argsGetOptional(args, name, nil, showHelp, "Matches fields partially.") 
    end,
    exact = function(args, name, showHelp) 
        return Cheat:argsGetOptional(args, name, nil, showHelp, "Matches fields exactly.") 
    end,
}, "Displays buffs matching the given query.",
    "Show all", "cheat_find_buffs",
    "Search for 'heal'", "cheat_find_buffs any:heal")
```

Source: kcd2-cheat

---

## 7. SQLite Persistence API (kcd2db)

Full persistence example with local and global storage:

```lua
local myDB = DB.Create("MyAwesomeMod")

-- Local storage (per-save)
myDB.Set("player_health", 85.6)
myDB:Set("has_dragon_sword", true)
local health = myDB.Get("player_health")

-- Global storage (cross-save)
myDB.SetG("settings", {volume = 0.8, fullscreen = true})
local settings = myDB.GetG("settings")

-- Supports complex objects (tables, nested structures, Unicode)
myDB.Set("test", {a=1, b="hello", c={d=2, e="world"}})
```

Source: kcd2db

---

## 8. Entity Script Pattern (kcd2-mod-docs)

Game entity script with Properties and lifecycle callbacks:

```lua
UsableItem = {
    Properties = {
        soclasses_SmartObjectClass = "",
        object_Model = "",
        Physics = {
            bPhysicalize = true,
            bRigidBody = true,
            bPushableByPlayers = false,
        },
    },
    Editor = { Icon = "animobject.bmp" },
}

function UsableItem:OnPropertyChange() self:Reset() end
function UsableItem:OnReset() self.nUserId = 0; self:Reset() end
function UsableItem:OnSpawn() self:Reset() end
function UsableItem:LoadModel()
    if self.Properties.object_Model ~= "" then
        self:LoadObject(0, self.Properties.object_Model)
    end
end
```

Source: kcd2-mod-docs (extracted game scripts)

---

## 9. TCP Socket Communication (kcd2lua)

VS Code extension communicating with running game:

```bash
# Install ASI loader as dinput8.dll in game bin directory
# Copy vscodelua.asi to same directory
# Linux: add WINEDLLOVERRIDES="dinput8,n,b" to launch options
# Install VS Code extension from marketplace
# Write Lua in VS Code, execute with Ctrl+Enter
```

Source: kcd2lua

---

## 10. Blender Addon Registration (KCD2-Blender-Toolkit)

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

Source: KCD2-Blender-Toolkit
