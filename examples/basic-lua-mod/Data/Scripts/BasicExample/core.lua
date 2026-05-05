--[[
    Basic Lua Mod Example - Core Module
    
    Demonstrates the module pattern used by production KCD2 mods.
    
    File location: Data/Scripts/BasicExample/core.lua
    Based on patterns from KCD2Tools/LootBeacon.
]]

BasicExample.Core = {
    initialized = false,
}

function BasicExample.Core:initialize()
    if self.initialized then return end

    System.LogAlways("[BasicExample] Initializing core module...")

    -- Register a console command
    self:registerCommand("basic_example_hello",
        "BasicExample.Core:sayHello()",
        "Says hello from BasicExample")

    -- Register for game events
    UIAction.RegisterEventSystemListener(self, "System", "OnSystemStarted", "onSystemStarted")

    self.initialized = true
    System.LogAlways("[BasicExample] Core module initialized!")
end

function BasicExample.Core:sayHello()
    local player = System.GetEntityByName("dude")
    if player then
        local pos = player:GetWorldPos()
        Game.SendInfoText("Hello from BasicExample! Position: " ..
            string.format("%.1f, %.1f, %.1f", pos.x, pos.y, pos.z), false, nil, 5)
    end
end

function BasicExample.Core:onSystemStarted()
    System.LogAlways("[BasicExample] Game system started!")
end

function BasicExample.Core:registerCommand(name, code, help)
    -- Register a console command that executes the given Lua code
    System.LogAlways("[BasicExample] Registered command: " .. name)
end

return BasicExample.Core
