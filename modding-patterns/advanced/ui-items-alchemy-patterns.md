# KCD2 Advanced Mods Analysis: UI, HUD, Alchemy, Crafting, Items & QoL
## Batch 3 — Deep-Dive Modding Pattern Extraction

**Analysis Date:** 2026-05-06
**Sources:** Nexus Mods pages, modding wiki, community documentation, blog posts

---

## TABLE OF CONTENTS

1. [HUD & UI Mods](#1-hud--ui-mods)
2. [Alchemy Mods](#2-alchemy-mods)
3. [Crafting & Item Mods](#3-crafting--item-mods)
4. [Keybinding System](#4-keybinding-system)
5. [Persistence (LuaDB)](#5-persistence-luadb)
6. [Master Pattern Summary](#6-master-pattern-summary)

---

## 1. HUD & UI MODS

### 1.1 HUD and Inventory Rework
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/309
- **Author:** CHECKER90 | **Version:** 1.2 | **Downloads:** 7,457
- **Type:** Texture Replacer (not PTF)

**What it does:** Complete visual overhaul of HUD and inventory textures. Improves quality for 1K-4K resolutions. Custom icons, sharper details, cleaner look.

**Technical Approach:**
- Replaces `.dds` texture files inside a `.pak` archive
- Mod structure: `mod.manifest` + `Data/<ModName>.pak`
- The `.pak` is a ZIP archive — rename to `.zip` to inspect/modify
- Textures stored at paths like `Libs/UI/Textures/Hud_main.dds`
- Texture format: BC3 (Linear, DXT5) for `.dds` compatibility
- Part of a 4-mod series: HUD Rework, Book Rework, Icon Rework, Interactive UI Rework
- All-in-One version available (mod #431) combining all 4

**PATTERN: Texture Replacement**
```
Mod folder structure:
  modname/
    mod.manifest
    Data/
      modname.pak   (ZIP archive)
        Libs/
          UI/
            Textures/
              Hud_main.dds
              inventory_icons.dds
              ...
```

### 1.2 Interactive UI Rework
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/312
- **Author:** CHECKER90 | **Version:** 1.3 | **Downloads:** 9,258
- **Type:** Texture Replacer

**What it does:** Overhauls interactive UI elements — skip time buttons, game over screens, lockpicking, maps, minigames, alchemy/crafting interfaces.

**Key Finding:** v1.3 added alchemy, crafting, and learning skills UI overhauls. This confirms that **alchemy/crafting UI textures are separate from the alchemy logic XML** — you can visually reskin the crafting interface independently of changing recipe behavior.

### 1.3 Sleek Modular HUD
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/1388
- **Author:** r0ughers | **Version:** 1.3.3 | **Downloads:** 7,570
- **Type:** Texture + GFX Modification

**What it does:** Compact, modular HUD with smaller health bars, transparent elements, repositioned icons, multiple themes (Vanilla Remix, Bronze, Silver, Vanilla).

**Technical Details:**
- Modifies `hud.gfx` (Flash-based HUD definition file)
- Also replaces textures (`.dds` files)
- **INCOMPATIBLE** with any mod that alters HUD textures or `hud.gfx`
- Optional modules: hide buff icons, compass, combat border, cursor, rabbit indicator, wanted/trespassing icons
- Offers a **Merger Script** to combine main + optional files into single mod (reduces mod count)
- Has Transparency Module and Ultrawide/4K Support Module
- Can disable Cinematic Letterboxes

**PATTERN: Modular HUD via GFX + Texture**
- `hud.gfx` controls layout, positioning, and some logic (Flash/Scaleform)
- Textures control visual appearance
- Modules can selectively hide elements by modifying GFX or replacing textures with transparent ones
- Multiple optional modules = multiple `.pak` files, load order matters (main before optional)

### 1.4 No HUD Except Button Prompts
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/299
- **Author:** Riordan | **Version:** 1.0 | **Downloads:** 1,660
- **Type:** Console Commands via user.cfg

**What it does:** Removes all HUD except button prompts and dialog choices.

**CRITICAL FINDING — Complete HUD Control Command List:**

```cfg
wh_ui_ShowStats = 0        # Health/Stamina bars
wh_ui_showCompass = 0      # Compass
wh_ui_ShowBuffs = 0        # Buff/Debuff icons
wh_ui_showQAMFood = 0     # Food quick slot
wh_ui_showQAMWeapon = 0   # Weapon quick slot
wh_ui_ShowCursor = 0       # Directional crosshair
wh_ui_ShowTrespassing = 0  # Trespassing bunny icon
wh_ui_ShowCrime = 0        # Crime bunny icon
wh_ui_ShowWanted = 0       # Wanted shield icon
wh_ui_ShowCommonEvent = 0  # Perk activation / reputation notifications
wh_ui_ShowFancyEvent = 0   # "Level Up!" notification
wh_ui_ShowHints = 0        # ALL button prompts
wh_ui_showHUD = 0          # ENTIRE HUD (master toggle)
```

**Installation Pattern:**
- Place `user.cfg` in game root (next to `system.cfg`)
- Launch with `+exec user.cfg` in Steam/Epic launch options
- Optional: `-devmode` for console access

**KNOWN BUG:** Some commands (`wh_ui_ShowStats`, `wh_ui_ShowWanted`, `wh_ui_ShowCrime`, `wh_ui_ShowTrespassing`) only apply AFTER loading a save. Requires companion mod "Load CFG After Level" (mod #927) to fix.

### 1.5 Toggle HUD
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/43
- **Author:** Riordan | **Downloads:** 5,215
- **Type:** user.cfg keybinds

**What it does:** Toggle HUD on/off with F2/F3.

**PATTERN: Keybind via user.cfg**
```cfg
bind f2 wh_ui_showHUD 0
bind f3 wh_ui_showHUD 1
```
- F-keys only (F2-F12), lowercase
- Avoid F5/F6/F9 (quick save/load)
- Controller support via Steam Input (D-Pad Right long press)

### 1.6 Auto Hide HUD
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/128
- **Author:** WinterElfeas | **Version:** 1.0.13 | **Downloads:** 6,937
- **Type:** Lua Script + GFX Modification

**What it does:** Automatically hides HUD elements when not in combat/injured. Smart buff display with threshold-based visibility.

**Technical Details:**
- Uses **Lua scripts** for logic (combat detection, injury detection)
- Configuration via `mod.cfg` (in mod folder, not user.cfg)
- Modifies `hud.gfx` for buff auto-display feature (uses `flash.external.ExternalInterface.call`)
- Hooks into `Player:OnAction(action, activation, value)` for input detection
- Manual HUD commands available: `autohidehud_show_hud`, `autohidehud_toggle_hide_hints`
- Has slow-motion option for pouch opening

**CRITICAL COMPATIBILITY NOTES:**
- Incompatible with ANY mod using `Player:OnAction()` function
- Buff feature incompatible with mods that modify `hud.gfx`
- Offers compatibility patch for own "Semi Transparent HUD" mod

**PATTERN: Lua-based HUD Control**
```lua
-- Hooks into player action system
function Player:OnAction(action, activation, value)
  -- Detect combat/injury state
  -- Toggle HUD elements via console commands
end
```

### 1.7 Dream HUD Customizable
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/1014 (approx)
- **Type:** Texture/GFX modification
- **Note:** Another modular HUD option in the User Interface category

---

## 2. ALCHEMY MODS

### 2.1 Easy Alchemy (249K+ downloads — most popular alchemy mod)
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/283
- **Author:** CryptLoad | **Downloads:** 250,807
- **Type:** PAK replacement (possibly PTF)

**What it does:** Removes boil, grind, and bellows steps from alchemy.

**Modular File Structure (CRITICAL PATTERN):**
```
Category A: Main File (Brewing Mechanics) — choose ONE:
  A - Never Boil - Never Grind (recommended)
  A - Never Boil
  A - Never Grind
  A - Never Boil - Never Grind - Never Distill

Category B: Yield Modifier — choose ONE:
  x2, x4, x8, x12, x20, x40 yield

Category C: Experience Modifier — choose ONE:
  x2, x4, x8, x12, x20, x40 XP
```

**Key Rule:** Only ONE file per category. Files from same category conflict. Game uses defaults for omitted categories.

**Technical Insight:** The alchemy system has SEPARATE controls for:
1. **Process steps** (boil, grind, distill, bellows)
2. **Yield/output quantity** (base yield * multiplier + perk bonuses)
3. **XP gain** (experience multiplier)

These are independently moddable, suggesting separate XML table rows or separate table files.

**Windows 10 Tip:** Use Total Commander for zipping `.PAK` files (WinRAR 7.01 causes issues).

### 2.2 Alchemy Made Easy
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/2722
- **Author:** VinceCZ | **Version:** 1.0 | **Downloads:** 11,630
- **Type:** PTF (Patched Table File)

**What it does:** Only requires adding ingredients in correct order. All other steps ignored. Always produces 200 potions per brew. Henry-level quality with appropriate perk.

**Technical Details:**
- Edits `AlchemyRecipe.xml` (CRITICAL FILE for alchemy modding)
- Supports ALL base game + DLC potions (up to Mysteria Ecclesiae)
- **NOT compatible** with any other mod editing `AlchemyRecipe.xml`
- Created from game version 1.5.2 files with reverse-engineering
- Nighthawk variant requires separate mod (UNTESTED)

**PATTERN: Alchemy Recipe Modification**
```
Key file: AlchemyRecipe.xml (inside Data.pak)
Controls:
  - Required ingredients and order
  - Process steps (boil, grind, distill, bellows)
  - Output quantity
  - Quality/tier determination
```

### 2.3 Really Simple Alchemy
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/520
- **Author:** Alp (JustAlp) | **Downloads:** 21,415
- **Type:** PTF (Patched Table File)

**What it does:** Reduces alchemy to: select base (water/wine), add herbs, drain into bottle. No other steps needed. Multiple multiplier versions (x2, x5, x10, x20, x100).

**Technical Insight:** The fact that this uses PTF format confirms that alchemy recipe data lives in **table files** that can be patched. The simplified process (base + herbs + drain) suggests the recipe XML has fields for each step type that can be individually set to "skip" or removed.

### ALCHEMY MODDING PATTERN SUMMARY

```
Key Files:
  AlchemyRecipe.xml          — Recipe definitions, steps, outputs
  
Moddable Parameters:
  - Ingredient list and order
  - Process steps: boil (turns), grind, distill, bellows (turns)
  - Base liquid (water, wine, etc.)
  - Output quantity (base yield)
  - Quality/tier system
  - XP gain multiplier
  
Modding Methods:
  1. PTF (recommended) — Patch specific rows in AlchemyRecipe.xml
  2. Full replacement — Replace entire AlchemyRecipe.xml (conflicts with all other alchemy mods)
  3. Modular categories — Separate files for mechanics, yield, XP

Known Limitations:
  - Only ONE mod can edit AlchemyRecipe.xml (unless all use PTF on different rows)
  - Output = (base_yield * multiplier) + perk_bonuses
  - Quality tiers: Standard → Henry-level (requires Martin's Secret perk or equivalent)
```

---

## 3. CRAFTING & ITEM MODS

### 3.1 Armor Recipes (and Recipe Generator)
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/827
- **Author:** HadronVanguard | **Version:** 1.04 | **Downloads:** 51,648
- **Type:** PTF + Generator Tool

**What it does:** Adds Tier 4 (Henry Tier) armor crafting recipes. Includes mod generator for customization.

**Technical Details:**
- Main mod is PTF — won't conflict with other PTF mods
- Recipes appear under "Other" crafting category
- Uses forging axe animation
- Requires "Martin's Secret" perk for Tier 4
- Mod generator (`generate_all.exe`) randomly selects ingredients based on item values
- Optional shop modifications conflict with other merchant mods

**PATTERN: Adding Crafting Recipes via PTF**
```
Recipe structure:
  - Recipe ID (GUID)
  - Result item ID (GUID)  
  - Ingredients (item IDs + quantities)
  - Category ("Other", etc.)
  - Animation type (forging axe, etc.)
  - Required perk
  - Skill level requirement
```

### 3.2 KCD2 Recipe Builder (Utility)
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/2391
- **Author:** jigsawpizzle | **Version:** 0.2 | **Downloads:** 285
- **Type:** External Tool (GUI application)

**What it does:** Automatically generates crafting recipe XML files from item definitions.

**Technical Workflow:**
1. Requires `uuids.txt` file (GUID database)
2. Import `item_<modid>.xml` + associated localization file
3. Auto-populates recipe fields from item data
4. Select ingredients via dropdown or "quick recipes" (templates)
5. Customize: weight, price, fade, visibility, type (recipe background color), UI description, category, min skill level
6. Build outputs: modified item XML + localization + recipe XML
7. **WARNING:** Overwrites original files — use different output directory

**PATTERN: Item + Recipe XML Relationship**
```
Required files for new items with recipes:
  item__<modid>.xml          — Item definitions (stats, appearance, etc.)
  Localization/<lang>.xml    — Display names and descriptions
  recipe__<modid>.xml        — Crafting recipes (generated by Recipe Builder)
  
Output directory structure:
  Data/
    libs/
      Tables/
        Item/
          item__<modid>.xml
        Recipe/
          recipe__<modid>.xml
    Localization/
      <lang>.xml
```

### 3.3 The KCD2 Cooking Mod (91 New Recipes)
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/1578
- **Author:** djb | **Version:** 3.1 | **Downloads:** 25,625
- **Type:** Lua Script + XML Tables

**What it does:** Overhauls cooking system with 91 new recipes, new ingredients, vendor integration, skill XP.

**Technical Details:**
- "Hijacks" existing cooking system via Lua scripts
- Extends it to support complex recipe system
- Recipes sold by profession-appropriate vendors (innkeepers, cooks, etc.)
- Stock is randomized and refreshes
- Survival XP scaled by recipe complexity (2-15 XP)
- Recipe discovery: auto-adds to Crafting Menu on first successful creation
- Recipe books as alternative learning method
- Full 12-language localization
- **Source code on GitLab:** https://gitlab.com/kcd2-mods/the-cooking-mod

**PATTERN: Lua-based Recipe System Extension**
```lua
-- Hijacks existing cooking system
-- Adds new recipe definitions
-- Integrates with vendor inventory system
-- Hooks into crafting completion for XP awards
-- Auto-discovers recipes on successful craft
```

### 3.4 Henry's Crafting Recipes (KCD1-Style Items)
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/1098
- **Author:** PetrHrdlicka | **Version:** 2.4 | **Downloads:** 5,808
- **Type:** PTF + New Items

**What it does:** Adds new crafting recipes and items inspired by KCD1. Armor, weapons, ammo, clothes.

**Technical Details:**
- Uses PTF for NPC inventory modifications (shop stock)
- Items have both Recipe IDs and Item IDs (separate GUIDs)
- Skill books teach recipes (Henry's Sketch Books)
- Console commands: `wh_cheat_additem <GUID>`
- Also uses: `#player.inventory:CreateItem('ItemID', condition, amount)`
- Sister mod for items without recipes

**PATTERN: Item ID System**
```
Every item has TWO GUIDs:
  - Recipe ID: The crafting recipe that teaches how to make it
  - Item ID: The actual item that gets created/spawned
  
Console spawn: wh_cheat_additem <ItemGUID>
Console create: #player.inventory:CreateItem('ItemGUID', condition, amount)
```

### 3.5 Kit Craft (Master Repair Kits)
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/1657
- **Author:** LiveBait | **Version:** 1.1 | **Downloads:** 932
- **Type:** PTF

**What it does:** Adds smithing recipes for master repair kits and smithing materials (Toledo Steel, Frankfurt Steel).

**Technical Insight:** Notes that the game's smithing system only produces ONE item per activity — this is a hardcoded limitation that affects bulk crafting mods.

### 3.6 DDV - Craftable Vanilla Arrows and Bolts
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/2534
- **Author:** DDVaMpZzz | **Version:** 1.0 | **Downloads:** 6,093
- **Type:** PTF + Lua Script

**What it does:** Adds bulk arrow/bolt crafting (10x per craft).

**Technical Details:**
- PTF for recipes
- **Lua script** handles bulk conversion: craft "bundle" item → script auto-converts to 10 arrows/bolts
- New material: "wooden stick" (purchasable/lootable)
- Recipes from specific vendors
- Debug command: `ddvammovanilla` (requires `-devmode`)

**PATTERN: Scripted Item Conversion**
```lua
-- Craft a "bundle" item at forge
-- Script detects bundle creation
-- Automatically converts to 10x actual item
-- Workaround for single-item crafting limitation
```

### ITEM MODDING PATTERN SUMMARY

```
Key Files:
  item__<modid>.xml          — Item definitions (stats, appearance, GUID, weight, price)
  recipe__<modid>.xml        — Crafting recipes (ingredients, output, category, animation)
  Localization/<lang>.xml    — Display names, descriptions
  shop__<modid>.xml          — Merchant inventory additions (PTF)
  
Item Structure:
  - Unique GUID (UUID format)
  - Stats: weight, price, durability, visibility, fade
  - Visual: model, texture references
  - Type/category determines UI icon color and sorting
  
Recipe Structure:
  - Recipe GUID (separate from item GUID)
  - Result item GUID
  - Ingredients: list of (item GUID, quantity) pairs
  - Category: determines which crafting station and UI section
  - Animation type
  - Skill requirement / perk requirement
  
Adding New Items:
  1. Define item in item__<modid>.xml
  2. Add localization strings
  3. Create recipe in recipe__<modid>.xml (optional)
  4. Add to merchant inventory (optional, via PTF)
  5. Pack into .pak, add mod.manifest
  
Console Testing:
  wh_cheat_additem <GUID>           — Add to inventory
  #player.inventory:CreateItem()    — Create with condition/amount
```

---

## 4. KEYBINDING SYSTEM

### 4.1 KCD2 Keybinder
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/2447
- **Author:** Destuur | **Version:** 0.1.3 | **Downloads:** 2,599
- **Type:** ASI Plugin + External Tool

**What it does:** Automatically merges keybinding definitions from multiple mods into a single unified `keybindSuperactions.xml`.

**Architecture:**
```
Components:
  KCD2KeybinderPlugin.asi    — Runtime plugin (injects into game)
  dinput8.dll                — Ultimate ASI Loader (DLL injection)
  KCD2Keybinder.exe          — Scanning/merging tool
  
Installation:
  Place all files in: Bin\Win64MasterMasterSteamPGO\ (next to KingdomCome.exe)
  
Activation:
  Add -keybinder to Steam launch options
  
Note: If LuaDB is installed, dinput8.dll is already present (shared dependency)
```

**How Keybindings Work:**

The game uses `keybindSuperactions.xml` as its SINGLE keybinding definition file. Without this tool, only ONE mod can define custom keybindings.

**Modder API (Lua):**
```lua
--- @bindingCommand hw_toggle          -- Command triggered by keybind
--- @bindingMap movement | player | ... -- Context where keybind is active
KCDUtils.Command.AddFunction("hw", "toggle", toggleMod, "Toggles Henry's Whistle")
```

**Localization for Keybinds (XML):**
```xml
<Table>
  <Row>
    <Cell>ui_keybinds_group_<modId></Cell>    <!-- Group name in settings -->
    <Cell>Henrys Whistle</Cell>               <!-- English -->
    <Cell>Heinrichs Pfeifen</Cell>            <!-- German -->
  </Row>
  <Row>
    <Cell>ui_keybind_<console_command></Cell>  <!-- Individual keybind label -->
    <Cell>Toggle Henrys Whistle</Cell>
    <Cell>Heinrichs Pfeifen umschalten</Cell>
  </Row>
</Table>
```

**Merging Behavior:**
- Scans all mods at game launch
- Merges `<superaction>` elements from each mod's `keybindSuperactions.xml`
- Creates unified file in standalone mod folder (prefixed `zz` to load last)
- Groups mod keybindings at top of settings list

**LIMITATION:** Cannot merge mods that edit `<conflict>` elements in keybindSuperactions.xml. Only pure `<superaction>` additions work.

**PATTERN: Two Keybinding Systems**

```
1. user.cfg binds (simple):
   bind f2 "command args"
   - Limited to F-keys
   - Console commands only
   - No UI integration in settings menu
   
2. keybindSuperactions.xml (advanced):
   <superaction> definitions
   - Any key mappable
   - Appears in game settings menu
   - Supports localization
   - Supports context maps (movement, combat, etc.)
   - Requires KCD2 Keybinder for multi-mod support
   - Annotations: @bindingCommand, @bindingMap
```

---

## 5. PERSISTENCE (LuaDB)

### 5.1 LuaDB
- **URL:** https://www.nexusmods.com/kingdomcomedeliverance2/mods/1523
- **Author:** muyuanjin | **Version:** 0.1.7 | **Downloads:** 13,397
- **Type:** ASI Plugin (SQLite-backed persistence layer)

**What it does:** Provides SQLite-based data persistence for Lua mods. Saves/loads data across game sessions.

**Architecture:**
```
Components:
  kcd2db.asi                 — Runtime plugin (SQLite persistence)
  dinput8.dll                — Ultimate ASI Loader (shared with Keybinder)
  
Files Created:
  kcd2db.db                  — SQLite database file
  kcd2db.log                 — Debug log
  
Installation:
  Place in: Bin\Win64MasterMasterSteamPGO\
  
Linux (Proton):
  WINEDLLOVERRIDES="dinput8=n,b" %command%
```

**Two Storage Modes:**

```
1. Save-Associated Storage (default):
   - Data bound to specific game save file
   - Auto-saved when game saves
   - Auto-loaded when that save loads
   - Perfect for: player progress, quest states, inventory mods
   
2. Global Storage (G suffix):
   - Persists across ALL game saves
   - Independent of save file
   - Perfect for: settings, preferences, statistics, cross-save data
```

**API (Recommended — OOP Style):**
```lua
-- Create namespaced database instance
local myDB = DB.Create("MyModName")

-- Save-associated data
myDB.Set("player_health", 85.6)
myDB:Set("config", { difficulty = "hard", weapons = { sword = true } })
local health = myDB.Get("player_health")

-- Global data
myDB.SetG("global_settings", { volume = 0.8 })
local settings = myDB.GetG("global_settings")

-- Other operations
myDB.Del("old_key")        -- Delete key
myDB.Exi("key")            -- Check existence
myDB.All()                 -- Get all data
myDB.Dump()                -- Debug print to console

-- Quick access (property-style)
local val = myDB.L.someKey    -- Local data
local val = myDB.G.someKey    -- Global data
```

**Legacy API:**
```lua
LuaDB.Set(key, value)      -- Store local
LuaDB.Get(key)             -- Retrieve local
LuaDB.SetG(key, value)     -- Store global
LuaDB.GetG(key)            -- Retrieve global
```

**PATTERN: Mod Initialization with Optional Persistence**
```lua
MyMod = MyMod or (function()
    local db = LuaDB and DB and select(2, pcall(DB.Create, "MyMod"))
    return {
        version = "__VERSION__",
        localData = db and db.L or {},    -- Graceful fallback if no LuaDB
        globalData = db and db.G or {}
    }
end)()

function MyMod:Init()
    local settingA = MyMod.localData.settingA  -- nil if first run
    -- Initialize with defaults if needed
end
```

**Important Constraints:**
- Names cannot contain colons (`:`) — used as namespace separator
- Key names conflict with method names (e.g., `Get`, `Set`) — use `DB.L.Get` for data access
- All values auto-JSON encoded/decoded
- Max single JSON object: ~953MB
- Uses reverse-engineered internals — may break after game updates
- If crashes occur, remove/disable the `.asi` file

---

## 6. MASTER PATTERN SUMMARY

### 6.1 Mod File Structure

```
ModName/
  mod.manifest                    — Required metadata file
  mod.cfg                         — Mod-specific configuration (some mods)
  Data/
    Data.pak                      — Main data archive (ZIP format)
      libs/
        Tables/
          Item/
            item__<modid>.xml     — Item definitions
          Recipe/
            recipe__<modid>.xml   — Crafting recipes
          Alchemy/
            AlchemyRecipe.xml     — Alchemy recipes (CAUTION: conflicts)
          Combat/
            combat_action_*.xml   — Combat tables
        UI/
          hud.gfx                 — Flash-based HUD layout (CAUTION: conflicts)
          Textures/
            *.dds                 — UI textures (BC3/DXT5 format)
      Scripts/
        *.lua                     — Lua gameplay scripts
      Localization/
        <lang>.xml                — String tables
```

### 6.2 Modding Approaches (by compatibility)

```
BEST COMPATIBILITY:
  PTF (Patched Table Files)  — Targeted row changes, mergeable
  Lua Scripts                — New logic, hooks into game events
  Texture Replacements       — Visual-only changes
  
MODERATE COMPATIBILITY:
  user.cfg commands          — Console variables, keybinds
  ASI Plugins                — DLL injection (LuaDB, Keybinder)
  
LOW COMPATIBILITY:
  Full Table Replacement     — Overwrites entire XML files
  hud.gfx modification       — Only one mod can modify
  AlchemyRecipe.xml changes  — Only one non-PTF mod at a time
```

### 6.3 Key Technical Files

| File | Controls | Modifiability |
|------|----------|---------------|
| `AlchemyRecipe.xml` | Alchemy steps, outputs, ingredients | PTF (row-level) or full replace |
| `item__<modid>.xml` | Item stats, appearance, GUIDs | Additive (new items) or PTF |
| `recipe__<modid>.xml` | Crafting recipes | Additive (new recipes) |
| `hud.gfx` | HUD layout, positioning, logic | Flash decompile (JPEXS) |
| `*.dds` textures | Visual appearance | Full replacement |
| `keybindSuperactions.xml` | Keybinding definitions | Merged by Keybinder tool |
| `user.cfg` | Console variables, simple binds | Additive |
| `mod.cfg` | Per-mod settings | Per-mod |
| `Lua scripts` | Game logic, hooks, events | Additive/mod-specific |
| `kcd2db.db` | LuaDB persistent data | Automatic via API |

### 6.4 Console Commands for Testing

```cfg
# HUD Control
wh_ui_showHUD 0/1           # Master HUD toggle
wh_ui_ShowStats 0/1          # Health bars
wh_ui_showCompass 0/1        # Compass
wh_ui_ShowBuffs 0/1          # Buffs
wh_ui_showQAMFood 0/1        # Food slot
wh_ui_showQAMWeapon 0/1      # Weapon slot
wh_ui_ShowCursor 0/1         # Crosshair
wh_ui_ShowTrespassing 0/1    # Trespassing icon
wh_ui_ShowCrime 0/1          # Crime icon
wh_ui_ShowWanted 0/1         # Wanted icon
wh_ui_ShowCommonEvent 0/1    # Notifications
wh_ui_ShowFancyEvent 0/1     # Level up
wh_ui_ShowHints 0/1          # Button prompts

# Item Management
wh_cheat_additem <GUID>      # Add item to inventory
#player.inventory:CreateItem('GUID', condition, amount)

# Keybinding
bind <key> "<command>"        # Simple keybind (F-keys preferred)
```

### 6.5 Tool Ecosystem

| Tool | Purpose | Source |
|------|---------|--------|
| JPEXS Free Flash Decompiler | Edit .gfx/.swf UI files | github.com/jindrapetrik/jpexs-decompiler |
| paint.net + BoltBait plugins | Edit .dds textures | getpaint.net |
| KCD2 Recipe Builder | Generate recipe XML from items | Nexus mod #2391 |
| Armor Recipe Generator | Generate armor recipes | Nexus mod #827 |
| KCD2 Keybinder | Merge keybinding XMLs | Nexus mod #2447 / GitHub |
| LuaDB | SQLite persistence for Lua | Nexus mod #1523 / GitHub |
| Ultimate ASI Loader | DLL injection for .asi plugins | GitHub/ThirteenAG |
| Total Commander | Reliable .pak zipping | (WinRAR 7.01 has issues) |
| altire's KCD toolkit | General modding tools | Referenced by Recipe Builder |

### 6.6 UNDOCUMENTED / LESSER-KNOWN FINDINGS

1. **Load Order Suffix Trick:** LuaDB and Keybinder create mod folders prefixed with `zz` to ensure they load last. This is a community convention, not documented by Warhorse.

2. **Alchemy Has 3 Independent Control Axes:** Process steps, yield, and XP are separately moddable — the Easy Alchemy mod demonstrates this with its Category A/B/C system.

3. **hud.gfx Uses Flash ExternalInterface:** Auto Hide HUD's buff feature calls `flash.external.ExternalInterface.call` from within the GFX file to communicate with Lua scripts. This is the bridge between Flash UI and game logic.

4. **Player:OnAction Hook Conflict:** Any Lua mod that defines `Player:OnAction()` will conflict with Auto Hide HUD. This is a single-dispatch pattern — only one handler can exist.

5. **AlchemyRecipe.xml is the Bottleneck:** Multiple alchemy mods explicitly warn about incompatibility. PTF helps but only if mods target different rows. The community has NOT found a way to merge multiple alchemy recipe changes.

6. **Smithing System Limitation:** The crafting system produces only ONE item per activity. Bulk crafting mods (like DDV Arrows) work around this with Lua scripts that convert "bundle" items into multiple actual items.

7. **CFG Timing Bug:** Several `user.cfg` commands only apply AFTER loading a save, not at game start. The "Load CFG After Level" companion mod (Nexus #927) fixes this by re-executing cfg after level load.

8. **dinput8.dll is Shared Infrastructure:** Both LuaDB and KCD2 Keybinder use Ultimate ASI Loader via `dinput8.dll`. If you have one, you don't need to install the other's copy. This is a de facto standard injection point.

9. **Recipe Discovery is Scriptable:** The Cooking Mod demonstrates that recipes can be auto-discovered and added to the Crafting Menu via Lua, without requiring recipe books/items.

10. **GFX Mod + Texture Mod Conflict Pattern:** Mods that modify `hud.gfx` are incompatible with each other, BUT texture-only mods can coexist with GFX mods (different files). However, some GFX mods also modify textures, creating implicit conflicts.

11. **Vendor Stock is PTF-Compatible:** Adding items to merchant inventories works via PTF, but "rich merchant" modifications (changing gold amounts) conflict with ANY other merchant-modifying mod.

12. **UUID-based Item System:** All items use UUID format GUIDs (e.g., `fb7b99cb-d278-4e8d-8135-3806094a3540`). Recipes have separate UUIDs from their output items. The Recipe Builder tool requires a `uuids.txt` database file.

---

## MOD STATISTICS SUMMARY

| Mod | Type | Downloads | Key Pattern |
|-----|------|-----------|-------------|
| Easy Alchemy | PAK/PTF | 250,807 | Modular categories (A/B/C) |
| Armor Recipes | PTF + Tool | 51,648 | PTF + generator tool |
| Cooking Mod | Lua + XML | 25,625 | Lua system extension |
| Really Simple Alchemy | PTF | 21,415 | PTF table patching |
| Alchemy Made Easy | PTF | 11,630 | AlchemyRecipe.xml editing |
| LuaDB | ASI Plugin | 13,397 | SQLite persistence |
| Interactive UI Rework | Texture | 9,258 | Texture replacement |
| HUD Inventory Rework | Texture | 7,457 | Texture replacement |
| Sleek Modular HUD | GFX + Texture | 7,570 | Modular GFX + merger script |
| Auto Hide HUD | Lua + GFX | 6,937 | Lua hooks + GFX ExternalInterface |
| DDV Arrows | PTF + Lua | 6,093 | Bundle→bulk conversion |
| Henry's Recipes | PTF + Items | 5,808 | New items + recipes |
| Toggle HUD | user.cfg | 5,215 | Console variable keybinds |
| No HUD Except Prompts | user.cfg | 1,660 | Complete HUD command list |
| KCD2 Keybinder | ASI + Tool | 2,599 | XML keybind merging |
| Kit Craft | PTF | 932 | Simple recipe addition |
| Recipe Builder | Tool | 285 | XML generation utility |
