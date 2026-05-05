# kcd2-cheat

- **GitHub**: https://github.com/pryans/kcd2-cheat
- **Language**: Lua
- **Stars**: ~10+
- **Last Updated**: Active (2025)
- **Purpose**: Comprehensive cheat/trainer mod for KCD2

## Description
A feature-rich cheat mod that provides console commands for player stats, items, buffs, skills, teleportation, weather control, NPC manipulation, and more. Uses KCD2's native Lua scripting system with PAK-based distribution.

## File Structure
```
kcd2-cheat/
├── mods/
│   ├── cheat/                     # Main cheat mod
│   │   ├── data/
│   │   │   ├── scripts/
│   │   │   │   ├── mods/cheat.lua           # Entry point / bootstrap
│   │   │   │   └── cheat/
│   │   │   │       ├── cheat_util.lua        # Utility functions
│   │   │   │       ├── cheat_args.lua        # Argument parsing
│   │   │   │       ├── cheat_core_player.lua # Player stats/commands
│   │   │   │       ├── cheat_core_items.lua  # Item management
│   │   │   │       ├── cheat_core_buffs.lua  # Buff system
│   │   │   │       ├── cheat_core_skills.lua # Skill manipulation
│   │   │   │       ├── cheat_core_actions.lua# Key binding system
│   │   │   │       └── ... (20+ modules)
│   │   │   └── libs/tables/rpg/buff__cheat.xml  # Custom buff definitions
│   │   └── release.properties
│   ├── cheat-keys/                # Key binding extension
│   │   └── data/libs/config/      # XML keybind configs
│   ├── cheat-autoexec/            # Autoexec extension
│   └── cheat-quest/               # Quest cheat extension
├── docs/                          # API documentation (stubs, CSVs)
├── mods.sh                        # Build script
└── .github/workflows/release.yml  # CI/CD
```

## Key Code Patterns

### Bootstrap / Entry Point Pattern
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

### Console Command Registration Pattern
```lua
function Cheat:createCommand(name, argDefinitions, description, example1, example1cmd, ...)
    -- Registers System.ExecuteCommand-compatible commands
    -- with argument parsing, help text, and examples
end

Cheat:createCommand("cheat_find_buffs", {
    any = function(args, name, showHelp) 
        return Cheat:argsGetOptional(args, name, nil, showHelp, "Matches fields partially.") 
    end,
    exact = function(args, name, showHelp) 
        return Cheat:argsGetOptional(args, name, nil, showHelp, "Matches fields exactly.") 
    end,
}, "Displays buffs matching the given query.",
    "Show all buffs", "cheat_find_buffs",
    "Shows buffs with 'heal' in names", "cheat_find_buffs any:heal")
```

### Player Soul API Pattern (Scriptbinds)
```lua
-- Get/Set player stats
player.soul:GetStatLevel("strength")
player.soul:SetState("health", amount)
player.soul:GetState("health")

-- Inventory manipulation
player.inventory:CreateItem(itemGuid, count, quality)
player.inventory:DeleteItemOfClass(itemGuid, count)
player.inventory:GetCountOfClass(itemGuid)
player.inventory:GetInventoryTable()

-- Money (special item GUID)
Cheat.g_money_id = "5ef63059-322e-4e1b-abe8-926e100c770e"
player.inventory:CreateItem(Cheat.g_money_id, 1, amount * 10)
Game.ShowItemsTransfer(Cheat.g_money_id, amount)
```

### Database Access Pattern
```lua
function Cheat:loadDatabase(databaseName)
    Database.LoadTable(databaseName)
    local lineCount = Database.GetTableInfo(databaseName).LineCount
    local database = {}
    for n = 0, lineCount - 1 do
        table.insert(database, Database.GetTableLine(databaseName, n))
    end
    return database
end
```

### Key Binding / Action System
```lua
-- XML keybind definition (cheat_keybindSuperactions.xml)
<action consoleCMD="1" name="cheat_action slot:1 type:press" 
    onPress="1" onRelease="0" onHold="0" keyboard="_keybinds_ref_"/>

-- Lua action registration
Cheat.g_action_callbacks = {}
function Cheat:registerAction(slot, type, funcPointer)
    local key = slot .. ":" .. type
    if not Cheat.g_action_callbacks[key] then
        Cheat.g_action_callbacks[key] = {}
    end
    table.insert(Cheat.g_action_callbacks[key], funcPointer)
end

function Cheat:publishAction(slot, type)
    local key = slot .. ":" .. type
    for _, funcPointer in ipairs(Cheat.g_action_callbacks[key]) do
        pcall(funcPointer)
    end
end
```

### Collider/Noclip Mode
```lua
function Cheat:setClipMode(mode)
    -- 0 normal, 1 no collision/no gravity, 2 no collision/gravity/ground
    player:SetColliderMode(mode)
end
```

### XML Data Modification (Buff Definition)
```xml
<database xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" name="barbora"
    xsi:noNamespaceSchemaLocation="../database.xsd">
    <buffs version="1">
        <buff buff_class_id="1" buff_exclusivity_id="1" 
              buff_id="a218b534-..." buff_name="cheat_invisibility"
              buff_params="con=-100,evi=-100,lpv=-100" duration="-1"
              implementation="Cpp:Constant" is_persistent="true" />
    </buffs>
</database>
```

## Modding Techniques
1. **PAK Distribution**: Scripts packaged as .pak (renamed .zip)
2. **Script.ReloadScript()**: Module loading system
3. **Console Commands**: System.ExecuteCommand() for game commands
4. **Database API**: Database.LoadTable/GetTableLine for game data
5. **XML Overrides**: Custom buff/item definitions in Libs/Tables/
6. **Key Binding XML**: Superactions XML for input handling
7. **Build Automation**: Shell script + GitHub Actions for releases
