# kcd_coding_guide

- **GitHub**: https://github.com/benjaminfoo/kcd_coding_guide
- **Language**: Documentation (Markdown) + Lua examples
- **Stars**: ~9
- **Last Updated**: 2020 (KCD1, still applicable)
- **Purpose**: Unofficial Lua coding guide for KCD engine

## Description
An unofficial but comprehensive guide to Lua scripting in the CryEngine-based KCD engine. While written for KCD1, most patterns apply to KCD2 as the engine is the same fork.

## Key Lua API Reference (from guide)

### Basic Commands
```lua
System.LogAlways("Hello World!")
System.ClearConsole()
System.GetEntityByName("dude")
System.GetEntitiesByClass("Player")
System.GetEntitiesInSphereByClass(center, radius, EntityClass)
```

### Entity Operations
```lua
player:GetWorldPos()           -- {x=0, y=0, z=0}
player:SetWorldPos(pos)
player:GetPos()
System.GetViewCameraDir()      -- Camera direction vector
```

### Raycasting
```lua
local from = player:GetPos()
from.z = from.z + 1.615
local dir = System.GetViewCameraDir()
local hitData = {}
local hitCount = Physics.RayWorldIntersection(from, dir, 10, ent_all, player.id, nil, hitData)
```

### UI
```lua
Game.SendInfoText("text", false, nil, seconds)
Game.ShowItemsTransfer(itemGuid, amount)
```

### Script Management
```lua
Script.ReloadScript("path.lua")
Script.UnloadScript("path.lua")
Script.ReloadScripts()
```

### Console Lua Execution
```
-- In-game console, prefix with #:
#System.LogAlways("Hello")
#player:SetColliderMode(2)
```

### Key Binding
```
bind keyname action value
bind mouse4 cl_fov 70
```

### Dev Mode
```
KingdomCome.exe -devmode
```
