# KCD2-PAK

- **GitHub**: https://github.com/7H3LaughingMan/KCD2-PAK
- **Language**: C# (.NET)
- **Stars**: ~10+
- **Last Updated**: Active (2025)
- **Purpose**: Create .pak files for KCD2 mods via drag-and-drop

## Description
A simple utility that packages mod folders into .pak files compatible with KCD2. Works via drag-and-drop or Windows shell integration (right-click context menu).

## Key Code Patterns

### Manifest Parsing for ModId
```csharp
public static string? GetModId(DirectoryInfo directoryInfo) {
    var manifest = directoryInfo.File("mod.manifest");
    if (!manifest.Exists) return null;
    var document = XDocument.Load(manifest.FullName);
    return document.XPathSelectElement("/kcd_mod/info/modid")?.Value;
}
```

### PAK Packaging Rules
```csharp
public IList<(FileInfo, IEnumerable<(FileInfo, RelativePath)>)> GetTasks() {
    // 1. Data/ folder contents (excluding Levels/) -> Data/{modid}.pak
    // 2. Localization/{lang}/ -> Localization/{lang}.pak
    // 3. Data/Levels/{levelname}/ -> Data/Levels/{levelname}/{modid}.pak
}
```

### PAK File Format
- Uses System.IO.Compression (ZIP format)
- Custom PakArchive/PakArchiveEntry classes
- DOS timestamp encoding for compatibility
- UTF-8 and ASCII encoding support

## Mod Folder Structure Convention
```
YourMod/
├── mod.manifest                    # Required: contains <modid>
├── Data/
│   ├── libs/tables/.../*.xml       # Table overrides
│   ├── scripts/.../*.lua           # Lua scripts
│   └── Levels/{level}/...          # Level-specific data
├── Localization/
│   ├── English_xml/                # English text
│   ├── German_xml/                 # German text
│   └── ...
```

## Shell Integration
```csharp
// Registers Windows right-click context menu
var shell = Registry.CurrentUser.CreateSubKey(
    @"Software\Classes\Directory\shell\KCD2-PAK");
shell.SetValue("", "PAK Mods");
var command = shell.CreateSubKey("command");
command.SetValue("", @$"""{applicationPath}"" ""%V""");
```
