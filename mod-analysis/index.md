# KCD2 Modding Tools & Repositories — Analysis Index

Overview of all analyzed KCD2 modding repositories. Each entry links to a detailed analysis document.

## Repository Table

| # | Repository | Author | Stars | Language | Type | Analysis |
|---|-----------|--------|-------|----------|------|----------|
| 1 | [KCD2ModLoader](https://github.com/xiaoxiao921/KCD2ModLoader) | xiaoxiao921 | ~50+ | C++ | Lua mod loader framework | [Details](KCD2ModLoader.md) |
| 2 | [KCD2Tools](https://github.com/tkhquang/KCD2Tools) | tkhquang | ~2 | Lua + C++ | Mod collection + Scriptbind docs | [Details](KCD2Tools.md) |
| 3 | [KCD2-Mod-Manager](https://github.com/KCD2ModManager/KCD2-Mod-Manager) | KCD2ModManager | ~20+ | C# | Mod manager (MVVM/WPF) | [Details](KCD2-Mod-Manager.md) |
| 4 | [kcd2-mod-docs](https://github.com/muyuanjin/kcd2-mod-docs) | muyuanjin | ~4 | Lua/HTML | Official docs mirror | [Details](kcd2-mod-docs.md) |
| 5 | [kcd2db](https://github.com/muyuanjin/kcd2db) | muyuanjin | ~5+ | C++ | SQLite Lua persistence | [Details](kcd2db.md) |
| 6 | [kcd2lua](https://github.com/yobson1/kcd2lua) | yobson1 | ~10+ | C++ + TS | VS Code Lua dev tools | [Details](kcd2lua.md) |
| 7 | [kcd2-cheat](https://github.com/pryans/kcd2-cheat) | pryans | ~10+ | Lua | Comprehensive cheat mod | [Details](kcd2-cheat.md) |
| 8 | [ModForge](https://github.com/Destuur/ModForge) | Destuur | ~10+ | C# | XML editor (WPF/Blazor) | [Details](ModForge.md) |
| 9 | [Warbox](https://github.com/vawser/Warbox) | vawser | ~30+ | C# | Table/localization editor | [Details](Warbox.md) |
| 10 | [KCD2-PAK](https://github.com/7H3LaughingMan/KCD2-PAK) | 7H3LaughingMan | ~10+ | C# | PAK file creator | [Details](KCD2-PAK.md) |
| 11 | [kcd2-mod-dualdialog-tool](https://github.com/SDxBacon/kcd2-mod-dualdialog-tool) | SDxBacon | ~5+ | C# | Dual-language subtitles | [Details](kcd2-mod-dualdialog-tool.md) |
| 12 | [kcd-toolkit](https://github.com/altire-dev/kcd-toolkit) | altire-dev | ~10+ | C# | Modding toolkit suite | [Details](kcd-toolkit.md) |
| 13 | [KCD2-Blender-Toolkit](https://github.com/Caseter/KCD2-Blender-Toolkit) | Caseter | ~10+ | Python | 3D asset pipeline | [Details](KCD2-Blender-Toolkit.md) |
| 14 | [kcd_coding_guide](https://github.com/benjaminfoo/kcd_coding_guide) | benjaminfoo | ~9 | Docs/Lua | KCD Lua coding guide | [Details](kcd_coding_guide.md) |

---

## By Category

### Mod Loaders & Frameworks
- **KCD2ModLoader** — The primary modding framework. DLL proxy providing Lua scripting, ImGui UI, FMOD audio, XML merging, ASI loading, and file replacement.
- **kcd2lua** — VS Code extension for live Lua execution in the running game via TCP socket.

### Mod Managers
- **KCD2-Mod-Manager** — Full-featured mod manager with Nexus Mods integration, conflict detection, and Steam Workshop support.

### Persistence & Data
- **kcd2db** — SQLite-backed persistent storage for Lua mods. Supports Global (cross-save) and Local (per-save) modes.

### Cheat / Gameplay Mods
- **kcd2-cheat** — Comprehensive cheat/trainer with commands for stats, items, buffs, teleportation, weather, and NPC manipulation.
- **KCD2Tools** — Collection including LootBeacon (item highlighting), TPVToggle (third person camera), PizzleYanked (localization).

### Modding Tools
- **ModForge** — Desktop XML editor for perks, buffs, and localizations with PAK export.
- **Warbox** — Table/localization editor with PTF patch system.
- **KCD2-PAK** — Simple PAK file creator via drag-and-drop.
- **kcd-toolkit** — Suite: PAK builder, mod scaffolder, asset finder.
- **kcd2-mod-dualdialog-tool** — Dual-language subtitle generator for language learning.

### Asset Pipeline
- **KCD2-Blender-Toolkit** — Blender addon for importing/exporting KCD2 3D models and textures.

### Documentation
- **kcd2-mod-docs** — Official mod documentation mirror including extracted game scripts.
- **kcd_coding_guide** — Comprehensive Lua coding guide for KCD engine (applicable to KCD2).
