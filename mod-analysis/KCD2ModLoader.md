# KCD2ModLoader

- **GitHub**: https://github.com/xiaoxiao921/KCD2ModLoader
- **Language**: C++
- **Stars**: ~50+
- **Last Updated**: Active (2025)
- **Purpose**: Lua Mod Loader framework for KCD2 (CryEngine 5 fork)

## Description
KCD2ModLoader is the primary modding framework for KCD2. It acts as a DLL proxy (d3d12.dll) that hooks into the game process, providing Lua scripting, ImGui UI, FMOD audio modding, XML merging, ASI loading, and file replacement.

## File Structure
```
KCD2ModLoader/
├── CMakeLists.txt
├── src/
│   ├── main.cpp              # DLL entry point, initializes all subsystems
│   ├── kcd2_init.hpp          # Game structure definitions (CEntity, IRenderNode, etc.)
│   ├── kcd2_init.cpp          # Game address resolution
│   ├── kcd2_address.hpp       # Memory address definitions
│   └── version.hpp
├── docs/
│   ├── cvars.md               # Console variables documentation
│   └── console_commands.md    # Console commands documentation
└── examples/
    └── plugins/KCD2ModLoader-TestMod/  # Example mod
```

## Key Code Patterns

### DLL Proxy Loading Pattern
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

### Mod Manifest Structure (vanilla_mod_system_info)
```cpp
struct vanilla_mod_system_info {
    std::string m_name;
    std::string m_mod_id;
    std::string m_description;
    std::string m_author;
    std::string m_version;
    std::string m_folder_name;
    std::string m_created_on;
    std::vector<std::string> m_loaded_paks;
};
```

### XML Patching System
```cpp
// Global XML context -> filename -> modifications buffer
ankerl::unordered_dense::map<std::string, 
    ankerl::unordered_dense::map<std::string, std::vector<std::string>>> 
    g_xml_context_to_xml_filename_to_modifications;

void apply_xml_patches(std::string &originalFileContent, 
                       const std::vector<std::string> &patchFileContents, 
                       bool is_inventory_preset);
```

### Table Patching (Data Table Overrides)
```cpp
// Table name -> line -> patch info
std::map<std::string, std::map<std::string, std::vector<table_patch_info_t>>> 
    g_table_name_to_added_line_to_info;
std::map<std::string, std::map<std::string, std::vector<table_patch_info_t>>> 
    g_table_name_to_modified_line_to_info;
```

### Lua API Events
- `rom.game_data.on_cryfile_open` - Hook file loading for replacement
- `rom.game_data.on_pak_openable` - Load custom PAK files early
- `rom.game_data.open_pak` - Open PAK files programmatically
- ImGui integration via `rom.gui` namespace

## Modding Techniques
1. **DLL Proxy Injection**: Masquerades as d3d12.dll
2. **Memory Hooking**: Hooks game functions via byte patches
3. **XML Merging**: Runtime XML modification for game data
4. **File Watching**: Hot reload of Lua files on save
5. **FMOD Hooking**: Sound replacement via event string modification
6. **ASI Loading**: Chains other ASI mods
