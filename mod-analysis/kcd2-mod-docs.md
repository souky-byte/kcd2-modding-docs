# kcd2-mod-docs

- **GitHub**: https://github.com/muyuanjin/kcd2-mod-docs
- **Language**: Lua (game scripts) + HTML (scriptbind docs)
- **Stars**: ~4
- **Last Updated**: Mar 2025
- **Purpose**: Official mod documentation and extracted game scripts

## Description
Mirror of official KCD2 modding documentation including extracted game scripts from Scripts.pak, Lua scriptbind documentation, DLL exports, and community links.

## Key Resources
1. **Scripts/**: Extracted game Lua scripts (V1.2.2) - critical reference
2. **script_bind/**: Official Lua Scriptbind HTML documentation
3. **DLL/**: Game DLL exports for reverse engineering
4. **CONSOLE.md**: Console command documentation
5. **LINKS.md**: Community resource links

## Important Game Script Patterns (from extracted scripts)

### Entity Script Pattern (UsableItem.lua)
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

### Entity Lifecycle Callbacks
- `OnPropertyChange()` - Editor property changes
- `OnReset()` - Editor/game reset
- `OnSpawn()` - Entity spawned
- `OnDestroy()` - Entity destroyed
- `OnUpdate(frameTime)` - Per-frame update
