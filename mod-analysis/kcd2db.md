# kcd2db (LuaDB)

- **GitHub**: https://github.com/muyuanjin/kcd2db
- **Language**: C++ (produces .asi DLL)
- **Stars**: ~5+
- **Last Updated**: Active (2025)
- **Purpose**: SQLite-based Lua data persistence for KCD2 mods

## Description
An ASI plugin that provides SQLite-backed persistent storage for KCD2 Lua mods. Supports two modes: Global (cross-save) and Local (per-save-file, auto-saved/loaded with game saves).

## File Structure
```
kcd2db/
├── CMakeLists.txt
├── AGENTS.md              # Development guidelines
├── CLAUDE.md              # AI assistant context
├── src/
│   ├── kcd2db.cpp         # Main DLL: gEnv resolution, vtable hooking
│   ├── db/LuaDB.h         # LuaDB implementation
│   ├── log/log.h          # Logging macros
│   └── lua/               # Lua API wrappers
├── external/cryengine/    # Minimal CryEngine headers
├── openspec/              # Reverse-engineered offsets
└── tests/                 # Unit tests (hooks, luadb, stubs)
```

## Key Code Patterns

### gEnv Resolution via Signature Scanning
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

### VTable Hooking Pattern
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

### LuaDB API (exposed to Lua)
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

### DB API Methods
```lua
-- Local (per-save)
DB.Get(key)    -- Get value
DB.Set(key, value)  -- Set value  
DB.Del(key)    -- Delete key
DB.Exi(key)    -- Check existence
DB.All()       -- Get all keys

-- Global (cross-save)
DB.GetG(key), DB.SetG(key, value), DB.DelG(key), DB.ExiG(key), DB.AllG()

-- Namespaced (recommended)
local db = DB.Create("MyMod")
db.Set("key", "value")  -- or db:Set("key", "value")
db.Get("key")
```

### Module Integration Pattern
```lua
YourMod = YourMod or (function()
    local db = LuaDB and DB and select(2, pcall(DB.Create, "YourMod"))
    return {
        version = "__VERSION__",
        localData = db and db.L or {},
        globalData = db and db.G or {}
    }
end)()
```

## Modding Techniques
1. **ASI Injection**: DLL loaded via Ultimate ASI Loader
2. **Signature Scanning**: Runtime address resolution across game versions
3. **VTable Hooking**: IGame::CompleteInit interception
4. **Lua C API**: Registering C++ functions as Lua globals
5. **SQLite Storage**: JSON serialization for complex Lua objects
6. **Version-Agnostic**: Pattern scanning handles game updates
