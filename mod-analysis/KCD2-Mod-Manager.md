# KCD2-Mod-Manager

- **GitHub**: https://github.com/KCD2ModManager/KCD2-Mod-Manager
- **Language**: C# (.NET 10, WPF)
- **Stars**: ~20+
- **Last Updated**: Active (2025)
- **Purpose**: Open-source mod manager for KCD2 with MVVM architecture

## Description
A full-featured mod manager with modern C#/WPF architecture, featuring mod installation, load order management, Nexus Mods integration, conflict detection, and Steam Workshop support.

## File Structure
```
KCD2-Mod-Manager/
├── KCD2 mod manager/
│   ├── Models/
│   │   ├── Mod.cs                    # Mod data model
│   │   ├── ModVersionInfo.cs
│   │   ├── ModProfile.cs
│   │   ├── ModCategory.cs
│   │   └── NexusModFile.cs
│   ├── Services/
│   │   ├── ModInstallerService.cs    # Mod installation logic
│   │   ├── ModOrderFileManager.cs    # Load order management
│   │   ├── ManifestUpdateService.cs  # Manifest parsing/generation
│   │   ├── GameInstallService.cs     # Game path detection
│   │   ├── ConflictCheckerService.cs # File conflict detection
│   │   ├── NexusDownloadService.cs   # Nexus API integration
│   │   └── LocalizationService.cs
│   ├── ViewModels/
│   │   ├── MainWindowViewModel.cs
│   │   ├── SettingsWindowViewModel.cs
│   │   └── RelayCommand.cs
│   └── Views/                        # XAML UI
└── KCD2 mod manager.Tests/           # Unit tests
```

## Key Code Patterns

### Mod Model (MVVM)
```csharp
public class Mod : ViewModelBase {
    public string Id { get; set; }
    public string Name { get; set; }
    public string Version { get; set; }
    public string Path { get; set; }
    public bool IsEnabled { get; set; }
    public bool IsWorkshopMod { get; set; }
    public string WorkshopId { get; set; }
    public string CategoryId { get; set; }
}
```

### Manifest Parsing Pattern
```csharp
// Parses mod.manifest XML to extract modid, name, version
// Generates manifests for mods that lack them
// Corrects XML version attributes
var manifestData = await _manifestService.ParseManifestAsync(manifestPath);
// Returns: modid, name, version, description, author
```

### Mod Installation Flow
```csharp
public async Task<Mod?> ProcessModFileAsync(string filePath, string modFolder) {
    // 1. Extract archive to temp directory
    // 2. Find mod.manifest (or generate one from .pak files)
    // 3. Parse manifest for metadata
    // 4. Move to Mods/ folder with correct structure
    // 5. Return Mod object with all metadata
}
```

### Mod Order File
```
# mod_order.txt - determines load priority
modid_1
modid_2
modid_3
```

## Modding Techniques
1. **Dependency Injection**: Microsoft.Extensions.DependencyInjection
2. **MVVM Pattern**: Clean separation of UI and logic
3. **Async/Await**: All IO operations are async
4. **Nexus API**: SSO login, mod update checking
5. **PAK File Handling**: Automatic mod packaging
6. **Conflict Detection**: File-level conflict analysis between mods
