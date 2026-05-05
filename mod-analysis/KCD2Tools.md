# KCD2Tools (LootBeacon, TPVToggle, PizzleYanked)

- **GitHub**: https://github.com/tkhquang/KCD2Tools
- **Language**: Lua + C++
- **Stars**: ~2
- **Last Updated**: Active (Mar 2026)
- **Purpose**: Collection of KCD2 mods + Lua Scriptbind documentation

## Description
A modular collection of KCD2 mods demonstrating both Lua-based and C++ ASI-based modding approaches. Also hosts official Lua Scriptbind documentation from Warhorse Studios.

## File Structure
```
KCD2Tools/
├── README.md
├── docs/script_bind/           # Official WH Lua Scriptbind docs (HTML)
├── LootBeacon/                 # Lua mod - item highlighting
│   └── src/
│       ├── mod.manifest        # Mod manifest XML
│       ├── mod.cfg             # User configuration file
│       ├── Data/
│       │   ├── Scripts/
│       │   │   ├── Systems/loot_beacon.lua    # Bootstrap
│       │   │   └── LootBeacon/
│       │   │       ├── core.lua               # Core initialization
│       │   │       ├── logger.lua             # Logging module
│       │   │       ├── config.lua             # Configuration
│       │   │       ├── entity_detector.lua    # Entity scanning
│       │   │       ├── highlighter.lua        # Particle effects
│       │   │       ├── command_registry.lua   # Console commands
│       │   │       ├── event_handler.lua      # Game events
│       │   │       └── ui_manager.lua         # UI notifications
│       │   └── Libs/Particles/loot_beacon.xml # Particle definitions
│       └── Localization/                       # Multi-language support
├── TPVToggle/                  # C++ ASI mod - third person camera
│   ├── CMakeLists.txt
│   └── src/
│       ├── dllmain.cpp         # DLL entry, DetourModKit
│       ├── hooks/              # Game function hooks
│       ├── camera_profile*.cpp # Camera system
│       └── game_interface.cpp  # Game API interface
└── PizzleYanked/               # Simple localization mod
    └── src/
        ├── mod.manifest
        └── Localization/English_xml/  # Text override
```

## Key Code Patterns

### Mod Manifest Format
```xml
<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
    <info>
        <name>Loot Beacon</name>
        <modid>loot_beacon</modid>
        <description>Loot Beacon - Never Miss a Drop or Corpse</description>
        <author>tkhquang</author>
        <version>1.4.3</version>
        <created_on>10.04.2025</created_on>
        <modifies_level>false</modifies_level>
    </info>
</kcd_mod>
```

### Lua Module Bootstrap Pattern
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
            System.LogAlways("$4[Loot Beacon] Failed to load: " .. file)
            return false
        end
    end
    return true
end

if LootBeacon_LoadModules() then
    LootBeacon.Core:initialize()
end
```

### Object-Oriented Module Pattern
```lua
LootBeacon.Core = {
    MOD_NAME = "Loot Beacon",
    VERSION = "1.4.3",
    initialized = false
}

function LootBeacon.Core:initialize()
    if self.initialized then return end
    LootBeacon.Logger:initialize(self.MOD_NAME)
    LootBeacon.CommandRegistry:initialize()
    LootBeacon.Config:initialize()
    LootBeacon.Highlighter:initialize()
    LootBeacon.EntityDetector:initialize()
    LootBeacon.UIManager:initialize()
    LootBeacon.EventHandler:registerEvents()
    self.initialized = true
end
```

### Entity Detection Pattern (Scriptbinds)
```lua
function LootBeacon.EntityDetector:detectEntities()
    local playerPos = player:GetPos()
    local radius = LootBeacon.Config.detectionRadius
    local allEntities = System.GetEntitiesInSphere(playerPos, radius)
    
    for _, entity in pairs(allEntities) do
        if entity and not entity:IsHidden() then
            if entity["actor"] then
                if entity.actor:IsDead() then
                    -- Handle corpse
                end
            elseif entity.class == "PickableItem" then
                -- Handle pickable item
            end
        end
    end
end
```

### Event System Registration Pattern
```lua
function LootBeacon.EventHandler:registerEvents()
    UIAction.RegisterEventSystemListener(self, "System", "OnSystemStarted", "onSystemStarted")
    UIAction.RegisterEventSystemListener(self, "System", "OnGamePause", "onGamePause")
    UIAction.RegisterEventSystemListener(self, "System", "OnGameResume", "onGameResume")
end

function LootBeacon.EventHandler:unregisterEvents()
    UIAction.UnregisterEventSystemListener(self, "OnSystemStarted")
    UIAction.UnregisterEventSystemListener(self, "OnGamePause")
    UIAction.UnregisterEventSystemListener(self, "OnGameResume")
end
```

### Console Command Registration Pattern
```lua
function LootBeacon.CommandRegistry:initialize()
    self:registerCommand("loot_beacon_activate",
        "LootBeacon.Highlighter:activateHighlights()",
        "Activate entity highlighting")
    self:registerCommand("loot_beacon_set_detection_radius",
        "LootBeacon.Config:setDetectionRadius(%line)",
        "Set detection radius in meters")
end
```

### Timer Pattern
```lua
self.timerID = Script.SetTimer(duration * 1000, function()
    LootBeacon.Highlighter:removeAllHighlights()
end)
```

### Particle Effect XML (CryEngine)
```xml
<ParticleLibrary Name="loot_beacon" SandboxVersion="1.0.0.0" ParticleVersion="28">
    <Particles Name="pillar_red">
        <Params Facing="Free" Count="30" Continuous="true"
            ParticleLifeTime="1.5" BlendType="Additive"
            Texture="textures/particles/spark_single_diff.tif"
            Alpha="0.9" Size="0.2" Speed="2" Connection="true"
            Color="(x=1,y=0,z=0)" GravityScale="0"
            PhysicsType="SimpleCollision" CollideTerrain="true" />
    </Particles>
</ParticleLibrary>
```

### Configuration via mod.cfg
```
-- mod.cfg uses space-before-equals format
loot_beacon_set_detection_radius =15.0
loot_beacon_set_item_particle_effect_path ="loot_beacon.pillar_orange"
loot_beacon_set_highlight_duration =5.0
```

### C++ ASI Mod Pattern (TPVToggle) - DetourModKit
```cpp
#include <DetourModKit.hpp>
// Uses DMK for hooking, logging, config
// Hooks: camera, input, UI overlay, entity, FOV
void cleanupResources() {
    DMKLogger::get_instance().info("Cleanup: Starting...");
    // Cleanup hooks in reverse order
    cleanupUiMenuHooks();
    cleanupUiOverlayHooks();
    DMK_Shutdown();
}
```

## Modding Techniques
1. **Modular Lua Architecture**: Separated concerns across files
2. **Script.LoadScript()**: Module dependency loading
3. **UIAction Events**: System event listener registration
4. **System.GetEntitiesInSphere()**: Spatial entity queries
5. **Particle XML**: Custom particle effects for visual mods
6. **mod.cfg**: User-editable configuration with cvar-style syntax
7. **Localization XML**: Multi-language support via Localization folder
8. **DetourModKit**: C++ ASI modding framework
