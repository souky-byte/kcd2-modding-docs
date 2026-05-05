# KCD2 Advanced Mods Analysis: AI, Combat & NPC Behavior
# =====================================================
# Extracted from Nexus Mods pages - Undocumented Modding Patterns
# Generated: 2026-05-06

---

## 1. AGGRESSIVE COMBAT AI (mod ID: 1014)
- Author: Magus (MagusTheMagician)
- Version: 2 | Updated: 2025-04-18
- Type: PTF (Patched Table Files)
- Downloads: 5,048 unique | Endorsements: 132
- URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/1014

### What It Changes
- Removes artificial attack delays of NPCs
- NPCs are more aggressive and surround the player faster
- V2 achieved "KCD1 levels of dread" - opponents surround Henry faster
- V1 had keybindings to toggle on/off; V2 activates automatically

### Technical Details
- PTF format: modifies only specific lines in combat XML tables
- Compatible with game patches 1.2 through 1.5.3
- Safe to add/remove mid-save (no save corruption)
- Confirmed conflict with "Realish Enemies" mod (likely shares same XML lines)
- Installation: extract to KCD2/Mods folder

### UNDOCUMENTED PATTERNS
- Attack delay parameters are stored in combat XML tables
- The "artificial delay" is a specific numeric value that can be zeroed out
- NPC surrounding behavior is controlled by a separate flanking/positioning parameter
- V1 vs V2 shows that keybind activation is possible via alternative mod structure
- The mod was shown alongside "Better Combat and Immersion" (mod ID: 11) in demos,
  suggesting they are compatible (different XML line sets)

---

## 2. COMBAT GAMEPLAY OVERHAUL (mod ID: 509)
- Author: machinegod (machinegod420)
- Version: 2.9 | Updated: 2025-03-23
- Type: Full XML replacement (NOT PTF)
- Downloads: 977 unique | Endorsements: 42
- URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/509

### What It Changes
- Directional blocking requirement: must match attack direction for perfect block
- Zone system for blunt weapons/polearms (3 zones): Left, Top+Bottom, Right
- Thrust guard can perfect block top guard and vice versa
- Left/Right blocks are stricter (no cross-matching)
- Dodge overhaul: no iframes, standardized distance, direction matters
- Stamina: attack drain decoupled from stats, minimum stamina requirements
- AI switches directions more frequently and feints more aggressively

### XML Files Modified (CRITICAL - not listed elsewhere)
The mod wholesale replaces these combat XML files:
  - combat_action_block.xml
  - combat_zone_distance.xml
  - combat_zone_config.xml
  - combat_zone_attack.xml
  - combat_zone_guard_movement.xml
  - rpg_param (defense weight params)

### Key Parameters Discovered
  - CombatAutoZoneChangeDelayMaxMax  (AI zone change delay)
  - MaxPerfectBlockSlotModifier      (perfect block timing window)
  - guard_stance_id                  (used as blocking trigger hack)
  - guard_zone_id                    (original system - "incredibly fiddly")

### UNDOCUMENTED PATTERNS
- **guard_stance_id vs guard_zone_id**: The mod "abuses" guard_stance_id to make
  blocking work correctly. guard_zone_id does NOT result in correct action selection
  and is described as "incredibly fiddly". This is a CRITICAL insight for combat mods.
- **Duplicate guard_stance_id hack**: Used as a workaround to prevent incorrect
  center-guard blocks. The mod creates duplicate entries as a hack.
- **Animation events**: Guard stance changes rely on animation events, not just
  data values. This means combat mods must account for animation timing.
- **Fragile parameter relationship**: CombatAutoZoneChangeDelayMaxMax and
  MaxPerfectBlockSlotModifier are deeply interconnected - changing one affects
  the other. Must be tuned together carefully.
- **Not PTF compatible**: Cannot be combined with other combat mods that edit
  the same files. Load order: must be loaded LAST if using other mods by same author.
- **Requires -devmode launch argument** to function.
- **Engine limitation**: Non-locked-on NPC attacks have issues at this aggression level.

### KNOWN ISSUES (Important for modders)
- Master strikes broken in 1.5.2+ (only work from right side)
- Knee strike combo broken
- Animation blending off: guard switches can appear faster/slower than animation shows
- AI parameter changes are largely "guess-and-check" per author admission
- Game patches (especially 1.2+) broke core mechanics in ways that may not be fixable

---

## 3. HARDCORE COMBAT FOR NORMAL MODE (mod ID: 2408)
- Author: saul0097
- Version: 1.0 | Updated: 2026-02-12
- Type: PTF (Patched Table Files)
- Downloads: 2,374 unique | Endorsements: 54
- URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/2408

### What It Changes
- Applies Hardcore Mode combat AI and parameters to Normal Mode
- Keeps Normal Mode QoL: HUD, map markers, fast travel

### Three File Variants (IMPORTANT - mod structure pattern)
1. **Hardcore Param Override (Negative Only)** - RECOMMENDED
   - Only difficulty-increasing parameters
   - No XP bonuses or buffs
   - Strictly harder experience

2. **Hardcore Param Override (Full)**
   - All RPG parameters from Hardcore Mode
   - Includes XP bonuses and system changes

3. **Combat Only**
   - Only hardcore combat enemy AI behavior
   - No RPG parameter overrides

### UNDOCUMENTED PATTERNS
- **Separation of combat AI from RPG params**: This mod proves that combat AI behavior
  and RPG parameters are in SEPARATE XML files and can be independently overridden.
- **Selective parameter extraction**: The "Negative Only" version shows that specific
  difficulty-increasing parameters can be isolated from the full Hardcore Mode table
  and applied independently.
- **RPG params include both buffs and debuffs**: Hardcore Mode's "Full" version includes
  XP bonuses (beneficial) alongside combat difficulty (detrimental). These are mixed
  in the same XML file.
- **Three-way mod split pattern**: Combat AI / Negative Params / Full Params - this
  is a reusable pattern for any difficulty mod.
- Installation: file goes in mods folder, named "hardcore_param_override"
- Old versions must be manually deleted before updating (name change from hccombatfornormal)

---

## 4. CIVIL BRAWLING (mod ID: 2654)
- Author: Oshzak
- Version: 0.3 | Updated: 2025-12-03
- Type: PAK with modified XML (crimepunishment.xml)
- Downloads: 2,659 unique | Endorsements: 44
- URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/2654

### What It Changes
- Outdoor brawls: no longer considered a crime
- Indoor fights: small fine + escort out instead of full aggression
- Knockouts: moderate fine, no jail time
- Civilians: shout/back away instead of sprinting to guards
- Guards: don't attack for street fights unless you escalate or ignore warnings

### What It Does NOT Change
- Weapon combat/crimes
- Player damage, armor, skills, combat stats
- Quests, scripted fights, story events
- Stealth, theft, other crime categories
- No new animations or brawl mechanics

### Technical Details
- Modifies: crimepunishment.xml (crime and punishment system)
- Uses PAK file format
- Requires mod.manifest file in correct structure

### UNDOCUMENTED PATTERNS
- **crimepunishment.xml**: Controls guard NPC crime response behavior
  - Indoor vs outdoor detection system
  - Crime severity thresholds (assault vs fine vs full aggression)
  - NPC crowd reaction behavior (scream, flee, fetch guards)
  - Knockout penalty classification
- **PAK file structure is critical**: Author had a bug where wrong file structure
  inside .pak caused game to not load any crime changes. File path within PAK matters.
- **Manifest version check**: mod.manifest must have correct game_version or the game
  disables the mod silently. Author had version "2.*" when game was "1.5.2".
- **crime.tbl with .txt extension bug**: Leaving crime.tbl as .txt caused unintended
  mass escalation of fights in entire towns.
- **Incompatible with mods editing same file**: Confirmed incompatible with
  "More Reasonable Crime (MRC)" (mod ID: 123) - both modify crimepunishment.xml.
  Workaround: manually merge values between mods.
- **Saving/loading mid-brawl resets guard behavior to vanilla** - engine limitation.
- **Indoor/outdoor detection is spatial**: Uses doorway/balcony boundary detection
  which can misfire in borderline spaces.
- **Reputation-based system possible but requires scripting**: Author notes that
  making brawls depend on clothing/reputation "would require deeper scripting and
  AI logic changes" beyond XML editing.

---

## 5. BEETHY'S FUN MODS (mod ID: 1691)
- Author: beethy
- Version: 1.0 | Updated: 2025-04-10
- Status: MAINTENANCE MODE (author retired from KCD2 modding)
- Downloads: 67,215 unique | Endorsements: 1,117
- URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/1691

### Included Mods (Safe)
1. **Permadeath** - Dead NPCs no longer revive (vanilla: everyone revives after days)
2. **Black Loading Screens** - Removes loading screen art, saves VRAM
3. **Knockout Essential NPCs** - Essential NPCs can be knocked out/smacked, not a crime
4. **Carry NPCs** - Carry any NPC including essential ones
5. **Loot NPCs** - Any NPC becomes lootable (Skyrim-style inventory access)
6. **Carry and Loot NPCs** - Combined version (separate files conflict)

### Included Mods (Silly)
- Invisible Bows, Invisible Men, Ragdoll Women

### BREAKS SAVE: Kill All Men, Kill All NPCs, Trosky Hellbox, Kuttenberg Hellbox

### UNDOCUMENTED PATTERNS
- **Essential NPC flag**: NPCs have an "essential" flag that prevents them from being
  harmed. This can be toggled via XML/data modification to allow knockout.
- **Essential NPCs and crime**: Knockout Essential NPCs mod makes it "not labeled as
  a crime" - suggests the crime system checks the essential flag.
- **NPC revive system**: Vanilla game has ALL dead NPCs revive after a few days.
  Permadeath mod disables this. This is a global flag/system, not per-NPC.
- **Carry system is separate from loot system**: They must be combined in one mod
  because separate files conflict. This suggests they modify overlapping data.
- **Recommended dependency**: KCD Nude mod (mod ID: 223) for carry/loot functionality -
  suggests NPC inventory display depends on character model state.
- **Loot NPCs gives access to unobtainable items**: NPC inventories contain items
  that cannot be obtained through normal gameplay.
- **Hellbox mods**: Create objects that draw all NPCs toward them via AI pathfinding -
  shows NPC attraction/homing can be triggered by placed objects.

---

## 6. BETTER STEALTH KILL-KNOCKDOWN CHANCE (mod ID: 2325)
- Author: pashabulek
- Version: 1.0.0 | Updated: 2025-08-01
- Type: PTF (Patched Table Files)
- Downloads: 2,932 unique | Endorsements: 73
- URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/2325

### What It Changes
- Increases stealth kill/knockdown chance from vanilla (low) to 50%, 60%, or 70%
- Three versions available (50%, 60%, 70%)
- Does NOT make it 100% because Tight Grip perk adds to the chance

### Technical Details
- PTF format
- Does not change any perks
- File size: ~1KB per version
- Modifies a single probability parameter

### UNDOCUMENTED PATTERNS
- **Stealth kill probability is a single numeric value** in the game's XML tables
- **Perk interaction**: The Tight Grip perk adds a bonus to this base probability.
  The base value + perk value = final chance. Setting base to 100% would make
  the Tight Grip perk meaningless.
- **Separate from perk system**: The mod explicitly states "this does not change any
  perks" - the stealth kill probability is independent of perk definitions.
- **HeadHitKnockOutBaseProbability parameter**: Based on the Finishers mod analysis
  (mod ID: 3043), this is likely the rpg_param key: "HeadHitKnockOutBaseProbability"
  with values like 0.05 (vanilla), 0.50, 0.60, 0.70 (mod versions).
- **Related parameters from Finishers mod**:
  - UnconsciousDepthFadeoutSpeedBase (how fast NPCs wake up)
  - VitalityToUnconsciousDepthFadeoutSpeed (vitality-based wake speed)
  - HeadHitKnockOutBaseProbability (base knockout chance on head hit)

---

## 7. TRUE HARDCORE (mod ID: 2590)
- Author: Lazarus (Lazarus119)
- Version: 1.2 | Updated: 2026-03-04
- Type: Balance overhaul (multiple XML files)
- Downloads: 280 unique | Endorsements: 14
- URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/2590
- Requirement: Mysteria Ecclesiae DLC

### Changes (v1.2)
**Economy & Combat:**
- Sell prices reduced by 60%
- Melee weapon attack power reduced by 30%
- Hunting Sword, Work Axe, Horseshoes prices increased
- Reforged Radzig/Henry sword: attack increased, stat requirement raised to 30/30
- Radovan sells more armor pieces
- Reduced shooting contest bids in Trosky region

**Perk Nerfs:**
- Numbskull: XP gain reduced by 60% (from 40%), blacksmithing prestige doubled,
  additional -25% survival XP gain nerf
- Punchable Face: incoming damage +20% (from 10%), added -25% charisma debuff
- Hangry Henry: food fills 60% less (from 50%), digestion speed 2x (eat every ~12 hrs)

**Survival:**
- Exhaustion speed increased
- Added -10% melee weapon damage debuff
- Honey: reduced nutrition and weight

**Horse:**
- Pebbles and Herring perks much weaker
- Increased stats and prices of buyable horses

**Weapons Fixed:**
- Madman's Longsword, Guild Longsword, St. George sword stats corrected

### UNDOCUMENTED PATTERNS
- **Perk parameter modification**: Perks like Numbskull, Punchable Face, Hangry Henry
  have configurable numeric values (XP%, damage%, food%, digestion rate) in XML.
- **Sell price is a global multiplier**: 60% reduction suggests a single sell_price
  multiplier in rpg_param or economy XML.
- **Melee weapon attack power is a global value**: 30% reduction across all melee
  weapons suggests a master modifier, not per-weapon.
- **Weapon stat corrections**: Individual weapons (Madman's, Guild, St. George) have
  incorrect stats in vanilla that need XML fixes.
- **Perk stacking**: True Hardcore + Numbskull perk creates compound XP reduction.
  Author recommends specific negative perks: Bad Back, Hangry Henry, Numbskull,
  Punchable Face.
- **Can be added/removed at any time** but will NOT retroactively change earned XP.
- **Shop chests break economy**: Author recommends companion mod to disable them.
- **Artemis Crossbow from pre-order is overpowered**: Author recommends not using
  DLC bonuses until reaching Kuttenberg.

---

## SUPPLEMENTARY MOD ANALYSIS

### EXTENDED COMBO TIMING WINDOW (mod ID: 2862)
- Author: egro08 | Version: 1.0 | Updated: 2026-01-30
- Type: PTF (modifies rpg_param.xml)
- Changes combo reaction time from vanilla 0.6s to 2.0s
- Requires: -devmode -cheat launch arguments
- mod_order.txt placement matters: place at bottom if other rpg_param mods exist
- Parameter: combo timing window in rpg_param.xml

### NORMAL HARDCORE (mod ID: 2178)
- Author: marykerry02 | Version: 1.0 | Updated: 2025-06-30
- Uses .cfg files and user.cfg with -devmode +exec user.cfg
- F7 key to activate perks in-game
- Combines: buff XML files, .cfg configuration, perk system
- Critical: perks activated via F7 CANNOT be simply removed (need new game or prior save)
- Integrates: Realish Stealth, No Fast Travel systems
- Incompatible with mods affecting player.xml

### FINISHERS ARE BACK (mod ID: 3043)
- Author: Elfi0044 | Version: 1 | Updated: 2026-04-14
- Type: PTF (rpg_param)
- Key XML structure for PTF combat mod:
```
<?xml version="1.0" encoding="us-ascii"?>
<database xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" name="barbora"
  xsi:noNamespaceSchemaLocation="../database.xsd">
    <rpg_params version="1">
        <rpg_param rpg_param_key="UnconsciousDepthFadeoutSpeedBase" rpg_param_value="34"/>
        <rpg_param rpg_param_key="VitalityToUnconsciousDepthFadeoutSpeed" rpg_param_value="40"/>
        <rpg_param rpg_param_key="HeadHitKnockOutBaseProbability" rpg_param_value="0.05"/>
    </rpg_params>
</database>
```

### KCD2 MOD TWEAKER APP (mod ID: 830)
- Author: cgize | Version: 1.2.1
- GUI tool for rpg_param.xml editing
- Includes: Better Combat AI toggle, melee damage slider, stamina consumption,
  slow motion disable, ammo damage, aim zoom disable
- Uses multiplicative sliders (0=disable, 10=10x default)
- Launch args: -devmode +exec user.cfg

### HARDCOREISH (mod ID: 578)
- Author: Greenwillow Mods | Version: 2.1
- Uses buff_params system: `xpm*0.4,dig*2.5,exh*2.5,srg*0.85,fdm*1.20,ibi*0.5`
- Parameters: xpm=XP multiplier, dig=digestion, exh=exhaustion, srg=something,
  fdm=food modifier, ibi=something
- Adds NEW values to rpg_param files rather than multiplying vanilla values
  (can cause conflicts if stacking with other mods that do the same)
- Reverse-engineered XML files with Notepad++

---

## COMMON PATTERNS
## ================

### XML Tables That Control Combat AI

Based on analysis of all mods, these are the key XML files:

1. **rpg_param / rpg_params.xml**
   - Master gameplay parameters file
   - Contains: combo timing, knockout probability, unconscious depth, stamina
   - PTF naming: rpg_param__modname.xml (double underscore)
   - Location: Libs/Tables/rpg/
   - Has "version" attribute in rpg_params tag

2. **combat_action_block.xml**
   - Controls blocking mechanics
   - Defines perfect block windows and conditions

3. **combat_zone_distance.xml**
   - Distance parameters for combat zones
   - Affects when NPCs engage/retreat

4. **combat_zone_config.xml**
   - Combat zone configuration
   - Defines zone boundaries and transitions

5. **combat_zone_attack.xml**
   - Attack behavior per zone
   - Controls NPC attack direction selection

6. **combat_zone_guard_movement.xml**
   - Guard movement behavior
   - Controls how NPCs move between guard positions

7. **crimepunishment.xml**
   - Crime and punishment system
   - Controls: guard response, fines, aggression thresholds
   - Indoor/outdoor crime classification
   - NPC crowd reactions

8. **buff__modname.xml**
   - Buff/debuff system
   - Uses buff_params with multiplicative syntax: `xpm*0.4,dig*2.5`
   - Can stack or conflict if adding new values vs multiplying existing

### How the PTF System Works for Combat Mods

**PTF (Patched Table Files) Format:**
- Instead of replacing entire XML files, PTF modifies only specific lines
- Multiple PTF mods can coexist IF they don't modify the same lines
- Changes are "overlaid and merged" at runtime
- Naming convention: filename__modname.xml (double underscore separator)

**PTF vs Full Replacement:**
- PTF: Safe, composable, limited scope. Preferred for single-parameter changes.
- Full replacement: Complete file override. Required for major system overhauls.
  Incompatible with other mods editing same files.

**Creating a PTF Combat Mod (Step by Step):**
1. Create folder structure: `modname/Libs/Tables/rpg/`
2. Create XML file: `rpg_param__modname.xml`
3. Use PTF XML structure (see Finishers mod example above)
4. Build with KCD PAK Builder:
   - PAK Filename: mod name
   - PAK Output: KCD2/Mods/modname/Data/
   - Directory to PAK: your mod folder
5. Create mod.manifest with correct game_version
6. Optionally create mod_order.txt entry

**PTF Limitations:**
- Cannot modify lines that another PTF mod also modifies
- Some XML files don't support PTF (must do full replacement)
- Folder structure inside PAK must be exact or changes won't load
- Manifest version must match game version or mod is silently disabled

### Values Typically Modified in Combat Mods

| Parameter | File | Effect |
|-----------|------|--------|
| Attack delay | combat XML | Time before NPCs attack |
| CombatAutoZoneChangeDelayMaxMax | combat XML | AI zone change speed |
| MaxPerfectBlockSlotModifier | combat XML | Perfect block timing window |
| guard_stance_id | combat XML | Guard direction (blocking trigger) |
| guard_zone_id | combat XML | Guard zone (fiddly, avoid) |
| HeadHitKnockOutBaseProbability | rpg_param | Stealth/head hit knockout chance |
| UnconsciousDepthFadeoutSpeedBase | rpg_param | How fast NPCs wake up |
| VitalityToUnconsciousDepthFadeoutSpeed | rpg_param | Vitality-based wake speed |
| Combo timing window | rpg_param | Default 0.6s |
| Sell price multiplier | rpg_param/economy | Global sell price modifier |
| Melee weapon attack power | rpg_param/combat | Global melee damage modifier |
| XP multiplier (xpm) | buff/rpg_param | Experience gain rate |
| Digestion rate (dig) | buff/rpg_param | Hunger speed |
| Exhaustion rate (exh) | buff/rpg_param | Sleep need speed |

---

## UNDOCUMENTED FINDINGS
## =====================

### Things Not in Official Wiki

1. **guard_stance_id vs guard_zone_id**: The Combat Gameplay Overhaul author
   discovered that guard_stance_id is the reliable way to trigger blocking logic.
   guard_zone_id is "incredibly fiddly" and doesn't result in correct action
   selection. This is NOT documented anywhere official.

2. **Duplicate guard_stance_id hack**: Creating duplicate entries in the XML
   prevents incorrect center-guard blocks. This is a workaround for engine bugs.

3. **Animation events control guard stance**: Guard stance changes are tied to
   animation events, not just data values. Combat mods must account for animation
   timing or they'll desync visually.

4. **CombatAutoZoneChangeDelayMaxMax and MaxPerfectBlockSlotModifier are coupled**:
   These two parameters have a "complex, fragile relationship" and must be tuned
   together. Changing one alone breaks the other.

5. **NPC revive is a global system**: All dead NPCs revive after a few days in
   vanilla. This is a global toggle, not per-NPC.

6. **Essential flag affects crime system**: Making an NPC non-essential also
   changes whether attacking them is a crime.

7. **PAK file structure bugs are silent**: Wrong file structure inside .pak causes
   changes to silently not load. No error message. The author of Civil Brawling
   had this exact issue.

8. **Manifest version causes silent disable**: If mod.manifest has wrong
   game_version, the mod is disabled with no error. Civil Brawling author had
   "2.*" when game was "1.5.2".

9. **crime.tbl with .txt extension causes mass escalation**: File extension
   errors in crime XML cause entire towns to attack you.

10. **Saving/loading mid-combat resets guard behavior**: Engine limitation where
    reloading a save during a brawl resets all guard AI to vanilla aggression.

11. **buff_params syntax**: Multiplicative format `xpm*0.4,dig*2.5,exh*2.5`
    where each parameter has a 3-letter code and a multiplier.

12. **rpg_param adds new values vs multiplies**: Some mods ADD new values to
    rpg_param files rather than multiplying vanilla values. This can cause
    0 XP gain when stacking with other mods (e.g., Numbskull -40% + mod -60% = 0%).

13. **Stealth kill probability interacts with perks**: The base probability +
    perk bonus (Tight Grip) = final chance. They're separate systems.

14. **Combat AI and RPG params are in separate files**: Can be independently
    overridden. The "Combat Only" variant of Hardcore Combat mod proves this.

15. **Packaging matters**: When repacking with WinRAR/7zip, MUST uncheck
    "High precision time format" and use "zip" archive format or effects won't apply.

---

## ACTIONABLE PATTERNS
## ===================

### How to Create Similar Mods

#### Pattern 1: Simple Combat Parameter Mod (PTF)
```
Goal: Change a single combat parameter
File: rpg_param__yourmodname.xml
Location: Libs/Tables/rpg/
Format: PTF (only changed lines)
Build: KCD PAK Builder
Install: Mods/yourmodname/Data/yourmodname.pak
```

#### Pattern 2: Combat AI Behavior Mod (PTF)
```
Goal: Change NPC attack patterns, delays, aggression
Files: Combat XML files in Libs/Tables/ (exact names TBD)
Method: Extract vanilla files, modify specific values, repackage as PTF
Limitation: PTF only works if no other mod changes same lines
```

#### Pattern 3: Full Combat Overhaul (Non-PTF)
```
Goal: Rewrite entire combat system
Files: combat_action_block.xml, combat_zone_*.xml, rpg_param
Method: Full file replacement
Warning: Incompatible with all other combat mods
Requires: -devmode launch argument
```

#### Pattern 4: Crime System Mod
```
Goal: Change guard/NPC crime response
File: crimepunishment.xml
Method: Modify values, ensure correct PAK structure
Warning: Check file extension (no .txt), verify manifest version
Test: Save/load during brawl to check for reset behavior
```

#### Pattern 5: NPC Essential/Knockout Mod
```
Goal: Make essential NPCs vulnerable
Method: Toggle essential flag in NPC data
Bonus: Also modify crime flag so attack isn't criminal
Related: Permadeath (toggle NPC revive system)
```

#### Pattern 6: Difficulty Overhaul
```
Goal: Comprehensive balance changes
Method: Combine multiple PTF mods or full XML replacements
Key files: rpg_param, combat XML, economy XML, perk XML
Pattern: Separate into optional components (Combat Only, Full, etc.)
```

#### Pattern 7: Stealth Mechanic Mod
```
Goal: Change stealth kill/knockdown probability
File: rpg_param (PTF format)
Key param: HeadHitKnockOutBaseProbability (0.0 to 1.0)
Consider: Perk interaction (Tight Grip adds to base value)
Related params: UnconsciousDepthFadeoutSpeedBase, VitalityToUnconsciousDepthFadeoutSpeed
```

### Critical Build/Install Checklist
1. Correct folder structure inside PAK (Libs/Tables/rpg/ for params)
2. Correct file naming (double underscore for PTF: rpg_param__modname.xml)
3. Correct XML structure (database > rpg_params > rpg_param)
4. Use KCD PAK Builder (not manual WinRAR repack)
5. mod.manifest with correct game_version
6. mod_order.txt entry for load order control
7. Launch with -devmode (required for many mods)
8. Test with save/load during combat to check for behavior resets

### Official Resources
- Warhorse RPG Constants Params: https://warhorse.youtrack.cloud/articles/KM-A-20/RPG-Constants-Params
- Modding Wiki PTF Guide: https://modding.wiki/en/kingdomcomedeliverance2/mod-development/fundamentals/ptf
- KCD PAK Builder: https://www.nexusmods.com/kingdomcomedeliverance2/mods/78
- Base RPG Params (vanilla XML): https://www.nexusmods.com/kingdomcomedeliverance2/mods/608
- KCD2 Mod Tweaker App: https://www.nexusmods.com/kingdomcomedeliverance2/mods/830

---

## MOD COMPATIBILITY MATRIX
## ========================

| Mod | PTF? | Conflicts With | Notes |
|-----|------|---------------|-------|
| Aggressive Combat AI | Yes | Realish Enemies | Safe add/remove |
| Combat Gameplay Overhaul | No | ALL combat mods | Must load LAST, requires -devmode |
| Hardcore Combat | Yes | Other rpg_param mods | 3 variants available |
| Civil Brawling | PAK | MRC (mod ID: 123) | crimepunishment.xml conflict |
| Beethy's Fun Mods | PAK | Unknown | Maintenance mode |
| Stealth Kill Chance | Yes | Unknown | Small footprint, single param |
| True Hardcore | Multiple | Unknown | Can add/remove, not retroactive |
| Extended Combo Timing | Yes | Other rpg_param mods | Place at bottom of mod_order.txt |
| Normal Hardcore | cfg+pak | player.xml mods | F7 activation is permanent |
| Finishers Are Back | Yes | Unknown | Customizable via XML editing |
| Hardcoreish | PAK | Similar buff mods | Adds new values, can cause 0 XP |
