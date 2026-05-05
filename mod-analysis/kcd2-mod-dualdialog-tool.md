# kcd2-mod-dualdialog-tool

- **GitHub**: https://github.com/SDxBacon/kcd2-mod-dualdialog-tool
- **Language**: C# (WPF application)
- **Stars**: ~5+
- **Last Updated**: Active (2025)
- **Purpose**: Dual-language subtitle display for KCD2 dialogue

## Description
A tool that generates localization mods to display NPC dialogue subtitles in two languages simultaneously. Great for language learners.

## Key Modding Patterns
1. **Localization XML Manipulation**: Merges two language XML files
2. **Font Pack Awareness**: Understands KCD2's font pack system
3. **Dialog Types**: Handles overhead, speech, and sequence dialogs
4. **ZIP Export**: Generates installable mod packages

## Font Pack Limitations
- Latin-based fonts: Most European languages work
- Chinese/Japanese/Korean: Separate font packs, limited cross-compatibility
- Mod merges text from secondary language into primary language XML

## Localization XML Structure
```
Localization/
├── English_xml/
│   └── text_my_mod.xml     # English text entries
├── German_xml/
│   └── text_my_mod.xml     # German text entries
└── ChineseSimplified_xml/
    └── text_my_mod.xml     # Chinese text entries
```
