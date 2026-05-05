# KCD2 Mod Manifest Format

Every KCD2 mod requires a `mod.manifest` XML file in its root directory.

---

## Standard Manifest

```xml
<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
    <info>
        <name>Mod Display Name</name>
        <modid>unique_mod_identifier</modid>
        <description>Brief description of the mod</description>
        <author>AuthorName</author>
        <version>1.0.0</version>
        <created_on>2025-01-15</created_on>
        <modifies_level>false</modifies_level>
    </info>
</kcd_mod>
```

Source: KCD2Tools (PizzleYanked, LootBeacon), KCD2-PAK (ModFolder.cs)

---

## Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `<name>` | Yes | Display name shown in mod manager |
| `<modid>` | Yes | Unique identifier — used for PAK filename and `mod_order.txt` reference |
| `<description>` | Yes | Brief description of what the mod does |
| `<author>` | Yes | Author name |
| `<version>` | Yes | Semantic versioning recommended (e.g., `1.0.0`) |
| `<created_on>` | Yes | Creation date |
| `<modifies_level>` | Yes | Set to `true` if mod changes level geometry/objects |

---

## Real-World Example (LootBeacon)

```xml
<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
    <info>
        <name>Loot Beacon</name>
        <modid>loot_beacon</modid>
        <description>Loot Beacon - Never Miss a Drop or Corpse</description>
        <author>tkhquang</author>
        <version>1.4.3</version>
        <created_on>10.04.2025</created_on>
        <modifies_level>false</modifies_level>
    </info>
</kcd_mod>
```

Source: KCD2Tools/LootBeacon

---

## C++ Manifest Structure (KCD2ModLoader)

The game internally represents manifests as:

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

Source: KCD2ModLoader

---

## Manifest Parsing (C# - KCD2-PAK)

```csharp
public static string? GetModId(DirectoryInfo directoryInfo) {
    var manifest = directoryInfo.File("mod.manifest");
    if (!manifest.Exists) return null;
    var document = XDocument.Load(manifest.FullName);
    return document.XPathSelectElement("/kcd_mod/info/modid")?.Value;
}
```

Source: KCD2-PAK (ModFolder.cs)

---

## Key Notes

- The `<modid>` value determines the PAK filename: `Data/{modid}.pak`
- The `<modid>` is used in `mod_order.txt` for load priority
- Set `<modifies_level>` to `true` only if your mod changes level geometry
  — this affects how the mod is packaged (separate level PAKs)
- Tools like ModForge and Warbox can auto-generate manifests
- Version should follow semantic versioning for compatibility tracking
