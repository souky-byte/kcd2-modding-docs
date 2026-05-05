# KCD2 Advanced Mods Analysis: Crime, Economy, Stealth, Reputation
# Batch 2 - Deep Technical Analysis

Generated: 2026-05-06
Sources: NexusMods descriptions, modding.wiki, community discussions, Cheat mod database

================================================================================
## TABLE OF CONTENTS
================================================================================

1. PER-MOD ANALYSIS (8 mods)
2. CRIME SYSTEM ARCHITECTURE
3. ECONOMY SYSTEM ARCHITECTURE
4. STEALTH SYSTEM ARCHITECTURE
5. REPUTATION SYSTEM ARCHITECTURE
6. PTF PATTERN ANALYSIS
7. UNDOCUMENTED FINDINGS

================================================================================
## 1. PER-MOD ANALYSIS
================================================================================

--------------------------------------------------------------------------------
### 1.1 More Reasonable Crime (MRC) - PTF
--------------------------------------------------------------------------------
URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/123
Author: Revan | Version: 0.9 | Downloads: 11,337 unique
Type: PTF (Patched Table File)
Status: Active, updated March 2025

FILES MODIFIED:
  - crime.xml (crime type definitions: importance, fine, expiration, jail, isCrime, isSpreadable)
  - angriness_enum.xml (NPC anger/suspicion levels)

CRIME TYPE CHANGES (Original -> Modded):
  Crime Type          | Importance | Fine    | Expiration | Jail
  --------------------|------------|---------|------------|-----
  Aggression          | 110 -> 90  | 750->500| -          | -
  Assault             | 130 -> 120 | 1500->1300| -        | -
  Assault by Dog      | 124 -> 105 | 1500->900| 5->3      | -
  Corpse Violation    | 170 -> 140 | 2000->1500| -        | -
  Grave Robbing       | 85 -> 75   | 2000->1600| -        | -
  Horse Theft         | 95 -> 85   | 2000->1800| -        | -
  Lockpicking         | 70 -> 80   | 600->500 | -          | -
  Murder              | 190 -> 180 | 20000->19000| -      | -
  Murder by Dog       | 180 -> 160 | 20000->15000| 7->5  | 7->5
  Pickpocket          | -          | 550->300 | -          | -
  Poaching            | 125 -> 115 | 7500->5000| -        | -
  Trespass            | 50 -> 40   | 250->150 | -          | -
  nonAttributedCrime  | 2 -> 0     | -        | 0.2 (unchanged) | -
                      | isCrime=false (unchanged)

KEY XML STRUCTURE DISCOVERED:
  <crime label="nonAttributedCrime" importance="0" isCrime="false" isSpreadable="false" expiration="0.2" />

  Crime attributes:
    - label: string identifier (e.g., "Murder", "Assault", "nonAttributedCrime")
    - importance: integer (higher = faster NPC reaction, escalates severity)
    - fine: integer (groschen penalty)
    - expiration: float (days until crime is forgotten)
    - jail: integer (days in prison)
    - isCrime: boolean (whether it registers as a crime)
    - isSpreadable: boolean (whether crime spreads via rumors)

ANGRINESS_ENUM.XML:
  - Controls NPC initial mood/suspicion level toward player
  - MRC reduces ALL values by 50%
  - v0.9 added two new values from a game patch

IMPORTANT INSIGHT: Setting importance=0 on nonAttributedCrime effectively
disables the automated suspicion system where NPCs blame player without
evidence. The crime still EXISTS but NPCs won't act on it.

UNATTRIBUTED THEFT EXCEPTION: If player steals many items from same NPC
in short time, NPC eventually deduces it was player. Suspicion starts slow,
takes longer to trigger, but once connected, opinion suffers (no report).

KNOWN LIMITATIONS (require Lua, not XML):
  - Self-defense kills still count as crime
  - Hostile enemies misclassified as "civilian" tag
  - Looting enemy corpses flagged as theft in wrong contexts
  - Reputation rumor-spread system unmodified

--------------------------------------------------------------------------------
### 1.2 nocrimesystem
--------------------------------------------------------------------------------
URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/2948
Author: klmer369 | Version: 1.0.0 | Downloads: 718 unique
Type: Full XML override (NOT PTF - full file replacement)
Status: Active, February 2026, tested in v1.5

APPROACH: Complete removal of crime system by overriding crime.xml entirely.

EFFECTS:
  1. NPCs do not react to player-caused harm
  2. NPCs do not react to trespassing
  3. NPCs do not react to theft
  4. Normal combat tournaments unaffected

RECOMMENDATION: Install AFTER completing prologue.
INCOMPATIBILITY: Incompatible with any other mod modifying crime.xml.

TECHNICAL PATTERN: This mod replaces the entire crime.xml with a version
where all crime entries have isCrime="false" or equivalent nullification.
This is the "nuclear option" approach vs MRC's surgical PTF edits.

--------------------------------------------------------------------------------
### 1.3 No Player Attribution After Unnoticed Theft
--------------------------------------------------------------------------------
URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/2750
Author: Farmose | Version: 1.0 | Downloads: 1,793 unique
Type: PTF (modifies crime attribution logic)
Status: Experimental, December 2025

FILES MODIFIED: crime.xml (attribution subsystem)

WHAT IT DOES:
  - Disables automatic player attribution for UNWITNESSED thefts
  - NPCs still notice missing items (panic, call guards, investigate)
  - But the final "it was the player" step is removed
  - Witnessed thefts still attributed normally

AFFECTED SCENARIOS:
  - Items missing from chests (scheduled checks)
  - Items missing after item disappearance
  - Items missing after being seen in restricted area
  - Items missing from private areas (shelves)
  - Items stolen from pockets (pickpocket)
  - Wearing stolen clothing

NOT AFFECTED:
  - Criminal actions other than theft
  - Theft witnessed by NPCs

KNOWN ISSUES:
  - Crime may still assign if stealing multiple items from private area
    while very close to scene when NPC notices
  - UI remnants (pop-ups, yellow rabbit icon) may appear but are cosmetic
  - Only real indicator of failure: actual consequences (reputation loss, etc.)

TECHNICAL INSIGHT: The crime system has a multi-step attribution pipeline:
  1. Crime occurs
  2. Witnesses check (line of sight, proximity)
  3. Attribution logic assigns blame
  4. Consequence applied (fine, reputation, hostility)
  This mod intercepts step 3 for unwitnessed crimes.

--------------------------------------------------------------------------------
### 1.4 No Crimes
--------------------------------------------------------------------------------
URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/510
Author: Sey (seymordius) | Version: 1.0 | Downloads: 2,196 unique
Type: Full XML override (NOT PTF)
Status: WIP, February 2025

MOTIVATION: Author was getting caught at night with 0 Conspicuousness,
0 Noise, 0 Visibility, 30 Stealth/Thieving skills, everyone asleep.
Felt broken. Created mod to remove all crime reactions.

FILES MODIFIED: crime.xml (direct overwrite of Tables.pak\libs\Tables\crime.xml)

CRITICAL TECHNICAL NOTE:
  "Changes only work when directly overwriting crime.xml, not through PTF"
  
  This is an IMPORTANT finding. Some crime system changes require FULL FILE
  OVERRIDES rather than PTF patching. This suggests the crime.xml structure
  may have attributes that PTF cannot selectively patch (possibly nested
  elements or attribute-level changes that PTF merge logic doesn't support).

KNOWN ISSUES:
  - Guard interaction bug: surrendering after guard yell -> indefinite
    black loading screen
  - Incompatible with other crime.xml mods
  - WIP status

--------------------------------------------------------------------------------
### 1.5 Economy Improved
--------------------------------------------------------------------------------
URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/3004
Author: EnigManic | Version: 1.5 | Downloads: 550 unique
Type: PTF (Patched Table File)
Status: Active, March 2026, tested in v1.5

FILES MODIFIED (inferred from description):
  - Item price tables (sell prices lowered for merchants)
  - Quest reward tables (groschen rewards increased)
  - Crime fine tables (fines increased for various crimes)
  - Item cost tables (armor, skill books, trainers, recipes, crafting sketches)
  - Service cost tables (inn room rentals, bath house services)
  - Dice tables (bet amounts)
  - Horse price tables (better stats = more expensive)
  - Merchant inventory tables (bandit loot reduced, Cuman gear devalued)
  - Repair kit prices (cheaper, especially from blacksmiths)

DESIGN PHILOSOPHY:
  "Sell prices are modestly reduced for nearly all merchants, while quest
   rewards are modestly increased."
  "My goal was to adjust the game's economy for better immersion."

SPECIFIC CHANGES:
  - Sell prices: Lowered across merchants
  - Quest rewards: Raised modestly
  - Best armors: More expensive
  - Inns: Higher room rental
  - Bath houses: Higher special service cost
  - Skill books/trainers/recipes/crafting sketches: More expensive
  - Crime fines: Increased (v1.5)
  - Dice bets: Higher
  - Belts/pouches/saddles/weighted dice/dice badges: Cost more, sell for less
  - Some bandits: Less likely to carry top-tier armor
  - Cuman gear: Slightly less valuable
  - Repair kits: Cheaper (especially blacksmiths)

COMPATIBILITY: PTF format ensures compatibility with other mods that don't
touch the same price values.

--------------------------------------------------------------------------------
### 1.6 Poorer Shops and Harsher Economy
--------------------------------------------------------------------------------
URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/2150
Author: Taylorsd722 | Version: 1.0 | Downloads: 302 unique
Type: XML override (two versions)
Status: Active, June 2025

TWO VERSIONS:
  1. "Poorer Shops" (22KB) - Only reduces shop money
  2. "Poor and Harsh" (28KB) - Less money + less Savior Schnapps +
     lower buy prices from player

FILES MODIFIED (inferred):
  - Merchant assortment/money tables (shop_npc or similar)
  - Item sell-to-merchant price modifiers
  - Savior Schnapps availability in shop inventories

ECONOMIC INSIGHT:
  "Selling equipment to a trader with only 5 coins will make that shop
   richer within 24-48 hours as they sell the items"
  
  This reveals that merchant economy is DYNAMIC - merchants earn money
  from selling items to other NPCs over time. Shop money isn't static.

DESIGN: Built for Hardcore Mode, meant to force inventory management.
Originally created for KCD1 but never released.

--------------------------------------------------------------------------------
### 1.7 KCDII Reputation Rebalance - A Quarter at a Time
--------------------------------------------------------------------------------
URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/367
Author: RobThePCGuy | Version: 2.2 | Downloads: 1,473 unique
Type: PTF (Patched Table File)
Status: BROKEN with latest KCD2 version. Author opened files for takeover.

FILES MODIFIED:
  - angriness_enum.xml (NPC anger levels)
  - crime.xml (crime penalties: fines, jail time, importance, expiration)
  - reputation.xml (reputation gain/loss values, thresholds)

TWO VARIANTS:
  1. "A Quarter Easier" (-25%):
     - NPC anger reduced
     - Crime penalties reduced (fines, jail, expiration)
     - Negative reputation impacts softened
     - Positive reputation gains boosted
  
  2. "A Quarter Harder" (+25%):
     - NPC anger increased
     - Crime penalties increased (fines, jail, importance)
     - Reputation harder to gain, easier to lose

DESIGN PRINCIPLES:
  - Global 25% adjustment to all relevant values
  - Does NOT modify values set to zero (preserves vanilla design)
  - Maintains original decimal precision
  - Modifications reasoned based on value function

REPUTATION.XML STRUCTURE (inferred):
  - Contains reputation gain/loss multipliers
  - Contains threshold values for reputation levels
  - Negative and positive gain values are separate
  - Zero values are intentional design choices (not modified)

--------------------------------------------------------------------------------
### 1.8 Cura Equi - Care of the Horse
--------------------------------------------------------------------------------
URL: https://www.nexusmods.com/kingdomcomedeliverance2/mods/2409
Author: hoskope (with RainyKnights) | Version: 1.0 | Downloads: 524 unique
Type: Lua script mod (requires LuaDB framework)
Status: Active, December 2025, tested in v1.4-1.5

REQUIRES: LuaDB (https://www.nexusmods.com/kingdomcomedeliverance2/mods/1523)

THIS MOD DOES NOT USE PTF/XML - it uses Lua scripting for custom logic.

HUNGER SYSTEM:
  Tiers: Sated -> OK -> Mild -> Moderate -> Critical
  Thresholds: 50/70/90 (configurable via HUD.thresholds)
  
  Effects:
    Sated:    No penalties, slower hunger gain
    OK:       Normal stamina and courage
    Mild:     Small stamina reduction
    Moderate: Large stamina penalty, reduced courage
    Critical: Severe stamina loss, courage halved, sprinting restricted

CONFIG.LUA PARAMETERS:
  Hunger.tickSec = 10                    (simulation tick interval)
  Hunger.ratePerMinIdle = 0.10          (hunger gain when idle)
  Hunger.ratePerMinMounted = 0.24       (hunger gain when mounted)
  Hunger.ratePerKmMounted = 0.55        (hunger gain per km ridden)
  Hunger.grazePerMinIdleUnmtd = -0.12   (grazing recovery rate)
  Feeding.needCapPerFeed = 35           (max nutrition per feed)
  HUD.thresholds = {50, 70, 90}         (tier breakpoints)

PRESETS:
  laidback: Relaxed rates
  moderate: Balanced
  hardcore: High hunger rates, night penalties
  
  Hardcore preset example:
    ratePerMinIdle       = 0.10
    ratePerMinMounted    = 0.24
    ratePerKmMounted     = 0.55
    grazePerMinIdleUnmtd = -0.001
    night = { disableGrazing = true, timeDrainMul = 1.25, maxDeltaPerNight = 50 }

FEEDING MECHANICS:
  - "Feed Horse" action near horse
  - Filtered item transfer window (like feeding Mutt)
  - Custom horse foods: Hay Bundle, Oat Sack, Apple Sack, Pear Sack, Carrot Bundle
  - Found at: horse traders, grocers, inns
  - Sated buff blocks further feeding (configurable)
  - Hunger increases slower while Sated

GRAZING:
  - Passive recovery when unmounted and idle
  - Scaled recovery (more effective at higher hunger)
  - Session cap prevents AFK exploitation
  - Disabled at night by default (configurable)

HEARTBEAT SYSTEM:
  - Runs every 10 seconds
  - Tracks horse position, speed, hunger state
  - Lightweight: no continuous scripts, no raycasts

CUSTOM BUFF LOGIC:
  - Sated buff tiers (buff system integration)
  - Buffs affect stamina, courage, sprint ability
  - Buff params inferred from Cheat mod database pattern:
    stamina*X, courage*X, LimitSprint type modifiers

FUTURE PLANS: Killable horses, horse sickness from spoiled food,
bonding system, horse drinking, distance-based fast travel hunger


================================================================================
## 2. CRIME SYSTEM ARCHITECTURE
================================================================================

### Core Files:
  crime.xml           - Crime type definitions
  angriness_enum.xml  - NPC anger/suspicion levels
  (reputation.xml)    - Reputation consequences of crimes

### Location:
  Tables.pak\libs\Tables\crime.xml
  Tables.pak\libs\Tables\angriness_enum.xml

### Crime XML Schema:
  <crime
    label="string"          // Crime type identifier
    importance="integer"    // How fast NPCs react (higher = faster)
    fine="integer"          // Groschen penalty
    expiration="float"      // Days until crime forgotten
    jail="integer"          // Days in prison
    isCrime="boolean"       // Whether it registers as crime
    isSpreadable="boolean"  // Whether it spreads via rumors
  />

### Known Crime Types (from MRC):
  - Aggression
  - Assault
  - Assault by Dog
  - Corpse Violation
  - Grave Robbing
  - Horse Theft
  - Lockpicking
  - Murder
  - Murder by Dog
  - Pickpocket
  - Poaching
  - Trespass
  - nonAttributedCrime (special: crimes not directly witnessed)

### Crime Attribution Pipeline:
  1. Crime event occurs (theft, assault, murder, trespass)
  2. Witness detection (line of sight, proximity, hearing)
  3. Attribution logic:
     a. Witnessed -> attributed to player immediately
     b. Unwitnessed -> "nonAttributedCrime" path
        - Scheduled NPC checks (chest contents, inventory)
        - Proximity check when crime discovered
        - Accumulation check (multiple thefts from same NPC)
  4. Consequence application:
     - Fine calculation (from crime.xml fine value)
     - Reputation impact (from reputation.xml)
     - NPC hostility (from angriness_enum.xml)
     - Guard pursuit (from importance value)
     - Jail sentence (from crime.xml jail value)
  5. Crime expiration (time-based forgetting)

### Anger Enum System:
  - angriness_enum.xml defines NPC anger/suspicion thresholds
  - Controls how quickly NPCs escalate from suspicion to hostility
  - 50% reduction (MRC) makes NPCs significantly less reactive
  - Values are per-crime-type modifiers

### Key Modding Patterns:
  - Set importance=0 + isCrime=false to disable a crime type
  - Reducing fine values makes crime less punishing
  - Increasing expiration makes crimes forgotten faster
  - Disabling isSpreadable prevents rumor-based crime propagation
  - nonAttributedCrime is the KEY crime type for stealth players
  - Full override needed for some crime.xml changes (per "No Crimes" author)

### Incompatibilities:
  - Any two mods modifying crime.xml are incompatible unless both use PTF
  - Even PTF mods conflict if they modify the same lines/values
  - Full override mods (nocrimesystem, No Crimes) are incompatible with all


================================================================================
## 3. ECONOMY SYSTEM ARCHITECTURE
================================================================================

### Core Files (inferred from multiple mods):
  - Item price/definition tables (sell prices, base values)
  - Merchant assortment tables (shop inventory + money)
  - Quest reward tables (groschen rewards)
  - Service cost tables (inns, bath houses, trainers)
  - Crime fine tables (overlaps with crime.xml)
  - Horse price tables
  - Dice/betting tables

### Economy Control Points:

  A. SELL PRICES:
     - Base selling price is a multiplier on item base value
     - Vanilla: players sell for ~5-10% of inventory value
     - Fair Trade mod: raises to ~50% of base value
     - Additional modifiers: item condition, reputation, merchant specialty
     
  B. BUY PRICES:
     - Separate from sell prices
     - Can be scaled independently
     - Scaled Economy uses BMA (Buy Multiplier Adjustment)
     - Level-based scaling possible

  C. MERCHANT MONEY:
     - Each merchant has a money pool
     - Pool is DYNAMIC: merchants earn from selling items to NPCs
     - 24-48 hour cycle for merchant wealth recovery
     - Assortment and money are in same file (child property relationship)
     - Can't change money without affecting assortment structure

  D. QUEST REWARDS:
     - Groschen rewards defined in quest tables
     - Can be increased independently of item prices
     - Supports non-looting playstyles

  E. SERVICE COSTS:
     - Inn room rentals
     - Bath house services
     - Trainer fees
     - Skill book prices
     - Recipe/crafting sketch costs

### Economy Scaling (from Scaled Economy Hardship):
  Level 1-5:   Sell -50%, Buy +50%
  Level 6-10:  Sell -75%, Buy +150%
  Level 11-15: Sell -80%, Buy +200%
  Level 16-20: Sell -85%, Buy +250%
  Level 21-25: Sell -90%, Buy +300%
  Level 26-30: Sell -95%, Buy +350%

### Key Modding Patterns:
  - PTF can modify individual price values
  - Merchant money/assortment: more complex, may break on patches
  - Sell/buy multipliers are separate parameters (SMA/BMA)
  - Item-specific pricing (specialty merchant bonuses) preserved in some mods
  - Economy mods tagged "Patched Table Files (PTF)" use PTF format


================================================================================
## 4. STEALTH SYSTEM ARCHITECTURE
================================================================================

### Stealth Stats (from Cheat mod database + community):
  - Conspicuousness (con): How recognizable the player is
  - Noise (noi): Sound generated by movement/actions
  - Visibility (vib): How visible the player is (light-based)

### Detection Formula (inferred):
  Detection = f(Conspicuousness, Noise, Visibility, NPC Perception, Distance)
  
  NPC Perception stats:
    - vision: NPC sight range/acuity
    - hearing: NPC hearing range/acuity

### Stealth Modifiers from Buff Database:
  Sprint:    fsm*2, noi+0.1 (faster but louder)
  Crouch:    vib-0.5, fsm*0.3, con-0.5 (slower, quieter, less conspicuous)
  Vigilant:  vision*1.65, hearing*1.33 (enhanced NPC perception)
  Poor Vision: vision*0.3
  Poor Hearing: hearing*0.3
  Deafness:  hearing=0
  Blindness: vision*0

### Stealth-Related Buffs:
  - Reeky: Stink makes player more noticeable while sneaking
  - Hangover: Increases Conspicuousness
  - Sprint: Increases noise
  - Crouch: Reduces visibility and conspicuousness

### Crime-Stealth Interaction:
  - Even with 0 Conspicuousness/Noise/Visibility, player can get caught
    (motivation for "No Crimes" mod author)
  - Detection is probabilistic, not binary
  - Night time reduces NPC perception but doesn't eliminate it
  - Sleeping NPCs have reduced but non-zero detection

### Key Insight from "No Crimes" Author:
  "I'd randomly get caught at night with 0 Conspicuousness, Noise, and
   Visibility with 30 skills in Thieving and Stealth with everyone
   around me asleep."
  
  This suggests the detection system has minimum detection chances or
  hidden checks beyond the three visible stats.


================================================================================
## 5. REPUTATION SYSTEM ARCHITECTURE
================================================================================

### Core File:
  reputation.xml (in Tables.pak)

### Reputation Structure (inferred from KCDIIRR and Easier/Harder mods):
  - Positive gain values (separate from negative)
  - Negative gain values (separate from positive)
  - Threshold values for reputation levels
  - Decay/expiration rates
  - Zero values are intentional design choices

### Reputation Modifiers:
  - grm (grind/reputation gain multiplier): Freshly Branded sets grm*0.5
  - Reputation gains can be multiplied (x2, x20)
  - Negative gains can be reduced (x0.75) or eliminated
  - Separate control over positive and negative channels

### Reputation Flow:
  1. Action occurs (crime, quest completion, trade, interaction)
  2. Reputation change calculated (positive or negative)
  3. Applied to relevant settlement/region
  4. Crime reputation can spread via "rumors" (isSpreadable)
  5. Reputation decays over time toward neutral

### Key Modding Patterns:
  - Multiply all positive gains by X (e.g., x2)
  - Multiply all negative gains by X (e.g., x0.75)
  - Set all negative gains to 0 (no negatives)
  - Combine: x2 positive + no negative
  - Global 25% adjustment (KCDIIRR approach)
  - Preserve zero values (don't change intentional design)

### Reputation Effects on Economy:
  - Reputation affects sell/buy prices
  - Higher reputation = better prices from merchants
  - Criminal reputation = worse prices, guard hostility

### Known Incompatibilities:
  - "Instant Rep Notification" conflicts with reputation PTF mods
  - Can overwrite reputation values back to vanilla
  - Must choose one or merge manually


================================================================================
## 6. PTF PATTERN ANALYSIS
================================================================================

### What is PTF?
  Patched Table Files = targeted modifications to XML table files
  Instead of replacing entire files, PTF overlays specific changes
  allowing multiple mods to coexist if they don't touch same lines

### PTF vs Full Override:
  PTF Format:
    - Selective line-by-line changes
    - Multiple mods can modify same file (different lines)
    - Maximum compatibility
    - Used by: MRC, Economy Improved, Fair Trade, KCDIIRR, Reputation mods
    - File extension: .pak (but internally structured as patches)
  
  Full Override:
    - Replaces entire XML file
    - Incompatible with any other mod touching same file
    - Simpler but breaks modularity
    - Used by: nocrimesystem, No Crimes
    - Required for some crime.xml changes (per No Crimes author)

### PTF Installation:
  - Extract mod folder to KCD2\Mods\ directory
  - Each mod in its own subfolder
  - mod.manifest file required (some mods had bugs from missing this)
  - mod_order.txt for controlling load order

### PTF Compatibility Matrix:
  Mod                    | PTF? | crime.xml | angriness | reputation | economy
  -----------------------|------|-----------|-----------|------------|--------
  MRC                    | YES  | YES       | YES       | NO         | NO
  nocrimesystem          | NO   | FULL      | NO        | NO         | NO
  No Attribution Theft   | YES? | YES       | NO        | NO         | NO
  No Crimes              | NO   | FULL      | NO        | NO         | NO
  Economy Improved       | YES  | YES(fines)| NO        | NO         | YES
  Poorer Shops           | NO?  | NO        | NO        | NO         | YES
  KCDIIRR                | YES  | YES       | YES       | YES        | NO
  Easier/Harder Rep      | YES  | NO        | NO        | YES        | NO

### Conflict Rules:
  1. Two PTF mods modifying same file = OK if different lines
  2. Two PTF mods modifying same line = last loaded wins
  3. PTF + Full Override = Full Override wins entirely
  4. Two Full Overrides = last loaded wins entirely
  5. Lua mods (Cura Equi) = no XML conflicts possible

### Game Version Sensitivity:
  - "A little richer merchants" broke on v1.3+
  - KCDIIRR broken on latest KCD2
  - MRC needed updates for new values added in patches
  - Crime.xml structure changes between patches break mods
  - PTF format is more resilient to patches than full overrides


================================================================================
## 7. UNDOCUMENTED FINDINGS
================================================================================

### 1. nonAttributedCrime is a FIRST-CLASS CRIME TYPE
   Not just a flag - it has its own entry in crime.xml with importance,
   expiration, isCrime, isSpreadable attributes. Disabling it (importance=0)
   is the surgical way to stop phantom accusations without removing the
   entire crime system.

### 2. Merchant Economy is DYNAMIC
   Merchants don't have static money. They earn groschen by selling items
   to other NPCs over 24-48 hour game-time cycles. This means:
   - Selling to a poor merchant makes them richer over time
   - Shop money regeneration is an emergent property, not a fixed timer
   - Economy mods need to account for this dynamic loop

### 3. Crime Attribution Has Multiple Pathways
   The crime system has at least 3 attribution paths:
   a. Direct witness (NPC sees crime)
   b. Proximity detection (NPC near scene when crime discovered)
   c. Accumulation detection (multiple thefts from same source)
   
   Path (c) is a delayed attribution that builds suspicion over time.
   Even with attribution disabled, accumulation can still trigger
   opinion changes (though not formal crime reports).

### 4. PTF Has Structural Limitations for crime.xml
   The "No Crimes" author discovered that some crime.xml changes only work
   with full file override, not PTF. This suggests:
   - Some XML attributes may not be patchable via PTF merge logic
   - Boolean attributes (isCrime, isSpreadable) may be particularly tricky
   - Nested or inherited properties may resist selective patching

### 5. Stealth Detection Has Hidden Minimums
   Players report being caught with perfectly min-maxed stealth stats
   (0/0/0 Conspicuousness/Noise/Visibility, max skills, sleeping NPCs).
   This implies:
   - There's a minimum detection chance not shown in UI
   - Some detection checks bypass the three visible stats
   - The crime system may have "plot armor" checks for certain areas

### 6. Reputation Zero Values Are Sacred
   KCDIIRR explicitly preserves zero values in reputation.xml as
   "intentional design choices." This means:
   - Some reputation modifiers are deliberately zeroed out
   - Blindly multiplying all values by X would break these
   - Modders must check for zeros before applying multipliers

### 7. Horse Hunger Uses Buff System
   Cura Equi integrates with the buff/debuff system for hunger effects.
   The buff parameter format is:
     stat*multiplier (multiplicative) or stat+value (additive)
     LimitSprint (boolean flag)
   Buffs: stamina, courage, sprint ability
   This pattern could be reused for any custom status system.

### 8. Dual Economy Control Axes
   Economy mods control TWO independent axes:
   - Sell Multiplier Adjustment (SMA): How much player gets when selling
   - Buy Multiplier Adjustment (BMA): How much player pays when buying
   These can be set independently, allowing fine-grained control.
   Vanilla game has significant gap between buy/sell prices.

### 9. Crime System Has "Spread" Mechanic
   The isSpreadable attribute means crimes can propagate via NPC gossip.
   A crime committed in one area can affect reputation in connected areas.
   This is a separate system from direct witness attribution.

### 10. LuaDB Enables Non-XML Modding
   Cura Equi demonstrates that complex logic (hunger systems, buff
   application, feed mechanics) can be implemented via Lua scripts
   using the LuaDB framework. This bypasses XML table limitations entirely
   and enables:
   - Custom game loops (heartbeat every 10 seconds)
   - State persistence between sessions
   - Dynamic buff application/removal
   - Console command registration
   - Preset systems
   This is the frontier for complex gameplay overhauls.

### 11. Game Version Breakage Pattern
   Mods break between patches because:
   - New crime types added (MRC had to add 2 new values in v0.9)
   - Table structure changes
   - New XML attributes introduced
   - File paths or PAK structure changes
   PTF mods are more resilient (only affected if their specific lines change)
   but full overrides break if any new content is added to the file.

### 12. Economy Mod Size = Complexity Indicator
   Mod file sizes correlate with scope:
   - 22KB: "Poorer Shops" (just shop money)
   - 28KB: "Poor and Harsh" (money + prices + schnapps)
   - 37-38KB: "Economy Improved" (comprehensive overhaul)
   Larger PAK files = more XML entries modified = broader scope


================================================================================
## SUMMARY TABLE: MOD TECHNIQUES
================================================================================

Mod                    | Technique         | Files           | Scope
-----------------------|-------------------|-----------------|------------------
MRC                    | PTF selective     | crime.xml,      | Crime tuning
                       |                   | angriness_enum  |
nocrimesystem          | Full override     | crime.xml       | Complete removal
No Attribution Theft   | PTF selective     | crime.xml       | Attribution only
No Crimes              | Full override     | crime.xml       | Complete removal
Economy Improved       | PTF selective     | Multiple econ   | Comprehensive
Poorer Shops           | Full override?    | Merchant tables | Shop money
KCDIIRR                | PTF selective     | crime+anger+rep | All 3 systems
Cura Equi              | Lua scripting     | Config.lua      | Custom systems

================================================================================
END OF ANALYSIS
================================================================================
