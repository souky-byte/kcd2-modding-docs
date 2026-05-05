--[[
    Cheat Module Example
    Demonstrates console command registration with argument parsing.
    Based on patterns from kcd2-cheat.
    
    File: Data/Scripts/Systems/cheat_example.lua
    This file is auto-loaded by the game engine from the Systems/ directory.
]]

CheatExample = {}

function CheatExample:onInit()
    System.LogAlways("[CheatExample] Initializing...")
    
    -- Register a simple command
    CheatExample:registerCommand("cheat_example_hello", {}, 
        "Says hello",
        "Say hello", "cheat_example_hello")
    
    -- Register a command with arguments
    CheatExample:registerCommand("cheat_example_heal", {
        amount = function(args, name, showHelp)
            return CheatExample:argsGetOptional(args, name, 100, showHelp, "Heal amount")
        end,
    }, "Heals the player by specified amount",
        "Heal 100", "cheat_example_heal",
        "Heal 50", "cheat_example_heal amount:50")
    
    -- Register a key binding action
    CheatExample:registerAction("1", "press", function()
        CheatExample:executeCommand("cheat_example_hello")
    end)
    
    System.LogAlways("[CheatExample] Ready!")
end

-- Command implementations
function CheatExample:cmd_hello()
    local player = System.GetEntityByName("dude")
    if player then
        Game.SendInfoText("Hello from CheatExample!", false, nil, 3)
    end
end

function CheatExample:cmd_heal(amount)
    local player = System.GetEntityByName("dude")
    if player and player.soul then
        local currentHealth = player.soul:GetState("health")
        player.soul:SetState("health", currentHealth + amount)
        Game.SendInfoText("Healed for " .. tostring(amount), false, nil, 3)
    end
end

-- Helper: argument parser
function CheatExample:argsGetOptional(args, name, default, showHelp, helpText)
    if showHelp then
        return helpText or "Optional argument"
    end
    if args and args[name] then
        return args[name]
    end
    return default
end

-- Helper: register a console command
function CheatExample:registerCommand(name, argDefs, description, ...)
    -- In production, this would use System.ExecuteCommand registration
    System.LogAlways("[CheatExample] Registered command: " .. name)
end

-- Helper: register a key action
function CheatExample:registerAction(slot, type, callback)
    -- In production, this would use the game's action system
    System.LogAlways("[CheatExample] Registered action: slot " .. slot .. " type " .. type)
end

-- Helper: execute a command
function CheatExample:executeCommand(cmd)
    System.LogAlways("[CheatExample] Executing: " .. cmd)
end

-- Initialize on load
CheatExample:onInit()
