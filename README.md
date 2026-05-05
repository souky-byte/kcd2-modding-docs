# KCD2 Modding Documentation

Comprehensive modding documentation for **Kingdom Come: Deliverance II** — compiled from the [official Warhorse Wiki](https://warhorse.youtrack.cloud/articles/KM-A-1/Modding-Kingdom-Come-Deliverance-2) and deep analysis of 15+ actively maintained GitHub repositories.

This repository covers everything from basic Lua scripting and XML data modification to advanced C++ ASI mods, 3D asset pipelines, and tooling. Includes real code examples extracted from production mods.

> **Sources**: [Warhorse YouTrack Wiki](https://warhorse.youtrack.cloud/articles/KM-A-1/Modding-Kingdom-Come-Deliverance-2) (78 articles) • 15 GitHub repositories analyzed • Community resources

## Table of Contents

### [modding-patterns/](modding-patterns/) — Modding Patterns & Reference
- [PATTERNS.md](modding-patterns/PATTERNS.md) — Comprehensive patterns summary (all 12 categories)
- [lua-patterns.md](modding-patterns/lua-patterns.md) — Lua scripting patterns (bootstrap, modules, events, timers)
- [manifest-format.md](modding-patterns/manifest-format.md) — Mod manifest XML format and fields
- [pak-packaging.md](modding-patterns/pak-packaging.md) — PAK file creation, loading order, packaging rules
- [data-modification.md](modding-patterns/data-modification.md) — XML data override and table patching patterns
- [advanced-examples.md](modding-patterns/advanced-examples.md) — Real code excerpts from production mods

### [mod-analysis/](mod-analysis/) — Repository Analysis
- [index.md](mod-analysis/index.md) — Overview table of all analyzed mods and tools
- [KCD2ModLoader.md](mod-analysis/KCD2ModLoader.md) — Lua mod loader framework (C++)
- [KCD2Tools.md](mod-analysis/KCD2Tools.md) — Mod collection + Scriptbind docs (Lua/C++)
- [KCD2-Mod-Manager.md](mod-analysis/KCD2-Mod-Manager.md) — Mod manager with MVVM (C#)
- [kcd2-mod-docs.md](mod-analysis/kcd2-mod-docs.md) — Official documentation mirror
- [kcd2db.md](mod-analysis/kcd2db.md) — SQLite Lua persistence (C++)
- [kcd2lua.md](mod-analysis/kcd2lua.md) — VS Code live Lua execution (C++/TS)
- [kcd2-cheat.md](mod-analysis/kcd2-cheat.md) — Comprehensive cheat/trainer mod (Lua)
- [ModForge.md](mod-analysis/ModForge.md) — XML editor WPF/Blazor (C#)
- [Warbox.md](mod-analysis/Warbox.md) — Table/localization editor (C#)
- [KCD2-PAK.md](mod-analysis/KCD2-PAK.md) — PAK file creator (C#)
- [kcd2-mod-dualdialog-tool.md](mod-analysis/kcd2-mod-dualdialog-tool.md) — Dual-language subtitles (C#)
- [kcd-toolkit.md](mod-analysis/kcd-toolkit.md) — Modding toolkit suite (C#)
- [KCD2-Blender-Toolkit.md](mod-analysis/KCD2-Blender-Toolkit.md) — 3D asset pipeline (Python/Blender)
- [kcd_coding_guide.md](mod-analysis/kcd_coding_guide.md) — Lua coding guide (Docs/Lua)

### [examples/](examples/) — Working Examples
- [basic-lua-mod/](examples/basic-lua-mod/) — Minimal Lua mod with bootstrap and module pattern
- [xml-override/](examples/xml-override/) — XML data override example (buff definition)
- [manifest-example.xml](examples/manifest-example.xml) — Complete mod.manifest template
- [cheat-module-example.lua](examples/cheat-module-example.lua) — Console command module pattern

### [wiki/](wiki/) — Extended Wiki Documentation
- Reorganized community wiki content covering visual modding, weapons, technical overview, and more

---

## Quick Start Guide

### 1. Creating a Basic Lua Mod

```
YourMod/
├── mod.manifest                  # Required: mod identity
├── mod.cfg                       # Optional: user config
└── Data/
    └── Scripts/
        ├── Systems/your_mod.lua  # Auto-loaded by game engine
        └── YourMod/
            └── core.lua          # Your module scripts
```

**Step 1**: Create `mod.manifest` — see [manifest-format.md](modding-patterns/manifest-format.md)

**Step 2**: Create a bootstrap script in `Data/Scripts/Systems/` — see [lua-patterns.md](modding-patterns/lua-patterns.md)

**Step 3**: Package as .pak — see [pak-packaging.md](modding-patterns/pak-packaging.md)

**Step 4**: Place in game's `Mods/` directory and add to `mod_order.txt`

### 2. Modifying Game Data (XML)

Override game tables by placing XML files with matching paths in your mod's `Data/Libs/` directory. See [data-modification.md](modding-patterns/data-modification.md) for detailed patterns.

### 3. Tools You May Need

| Tool | Purpose | Link |
|------|---------|------|
| KCD2-PAK | Create .pak files | [Analysis](mod-analysis/KCD2-PAK.md) |
| ModForge | Visual XML editor | [Analysis](mod-analysis/ModForge.md) |
| Warbox | Table/localization editor | [Analysis](mod-analysis/Warbox.md) |
| KCD2-Mod-Manager | Install & manage mods | [Analysis](mod-analysis/KCD2-Mod-Manager.md) |
| kcd2lua | Live Lua from VS Code | [Analysis](mod-analysis/kcd2lua.md) |
| KCD2-Blender-Toolkit | 3D asset import/export | [Analysis](mod-analysis/KCD2-Blender-Toolkit.md) |

---

## Engine Background

KCD2 runs on **CryEngine 5** (Warhorse fork). Key technical facts:

- **Lua scripting** is the primary modding interface — loaded from `Data/Scripts/Systems/`
- **PAK files** are renamed ZIP archives — the game loads them from `Mods/`
- **XML tables** define game data (buffs, items, perks, keybinds) — overridable per-mod
- **ASI/DLL mods** can hook game functions for advanced modifications (C++)
- **mod_order.txt** controls load priority in `Mods/` directory

---

## Credits

This documentation was compiled from analysis of the following repositories:

| Repository | Author | Contribution |
|-----------|--------|-------------|
| [KCD2ModLoader](https://github.com/xiaoxiao921/KCD2ModLoader) | xiaoxiao921 | Core mod loader framework |
| [KCD2Tools](https://github.com/tkhquang/KCD2Tools) | tkhquang | LootBeacon, Lua Scriptbind docs |
| [KCD2-Mod-Manager](https://github.com/KCD2ModManager/KCD2-Mod-Manager) | KCD2ModManager | Mod manager application |
| [kcd2-mod-docs](https://github.com/muyuanjin/kcd2-mod-docs) | muyuanjin | Official documentation mirror |
| [kcd2db](https://github.com/muyuanjin/kcd2db) | muyuanjin | SQLite persistence plugin |
| [kcd2lua](https://github.com/yobson1/kcd2lua) | yobson1 | VS Code Lua development tools |
| [kcd2-cheat](https://github.com/pryans/kcd2-cheat) | pryans | Comprehensive cheat mod |
| [ModForge](https://github.com/Destuur/ModForge) | Destuur | XML mod editor |
| [Warbox](https://github.com/vawser/Warbox) | vawser | Table/localization editor |
| [KCD2-PAK](https://github.com/7H3LaughingMan/KCD2-PAK) | 7H3LaughingMan | PAK file creator |
| [kcd2-mod-dualdialog-tool](https://github.com/SDxBacon/kcd2-mod-dualdialog-tool) | SDxBacon | Dual-language subtitles |
| [kcd-toolkit](https://github.com/altire-dev/kcd-toolkit) | altire-dev | Modding toolkit suite |
| [KCD2-Blender-Toolkit](https://github.com/Caseter/KCD2-Blender-Toolkit) | Caseter | 3D asset pipeline |
| [kcd_coding_guide](https://github.com/benjaminfoo/kcd_coding_guide) | benjaminfoo | Lua coding guide |

---

## License

This documentation is provided as-is for the KCD2 modding community. Individual mod repositories and tools retain their own licenses. Refer to each repository for specific licensing terms.
