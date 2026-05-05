--[[
    Basic Lua Mod Example - Bootstrap Script
    
    This file is auto-loaded by the game engine from Data/Scripts/Systems/.
    It loads all module scripts and initializes the mod.
    
    File location: Data/Scripts/Systems/basic_example.lua
    Based on patterns from KCD2Tools/LootBeacon and kcd2-cheat.
]]

BasicExample = {}

function BasicExample_LoadModules()
    local modPath = "Scripts/BasicExample"
    local moduleFiles = {
        "/core.lua",
    }

    for _, file in ipairs(moduleFiles) do
        local success = Script.LoadScript(modPath .. file)
        if success ~= 1 then
            System.LogAlways("$4[BasicExample] Failed to load: " .. file)
            return false
        end
    end

    return true
end

if BasicExample_LoadModules() then
    BasicExample.Core:initialize()
end
