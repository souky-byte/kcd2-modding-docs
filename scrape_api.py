#!/usr/bin/env python3
"""Scrape KCD2 modding wiki from YouTrack REST API."""

import json
import os
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

# Article list from _TREE.md
ARTICLES = [
    {"id": 0, "title": "Modding Kingdom Come: Deliverance 2", "file": "index.md"},
    {"id": 87, "title": "Modding Rules", "file": "modding-rules.md"},
    {"id": 56, "title": "Installing Mods", "file": "installing-mods.md"},
    {"id": 36, "title": "Technical Overview", "file": "technical-overview/index.md"},
    {"id": 55, "title": "The Modding Tools", "file": "technical-overview/the-modding-tools.md"},
    {"id": 3, "title": "Structure of a Mod", "file": "technical-overview/structure-of-a-mod/index.md"},
    {"id": 57, "title": "Mod Manifest", "file": "technical-overview/structure-of-a-mod/mod-manifest.md"},
    {"id": 35, "title": "Reserved ModIds", "file": "technical-overview/structure-of-a-mod/reserved-modids.md"},
    {"id": 12, "title": "Database Tables", "file": "technical-overview/structure-of-a-mod/database-tables.md"},
    {"id": 58, "title": "Publishing a Mod", "file": "technical-overview/publishing-a-mod/index.md"},
    {"id": 85, "title": "Publishing to Steam Workshop", "file": "technical-overview/publishing-a-mod/publishing-to-steam-workshop.md"},
    {"id": 83, "title": "Walkthroughs", "file": "walkthroughs/index.md"},
    {"id": 8, "title": "Simple Mod - Modifying CVars", "file": "walkthroughs/simple-mod-cvars.md"},
    {"id": 17, "title": "Adding a New Item", "file": "walkthroughs/adding-a-new-item.md"},
    {"id": 18, "title": "Skald", "file": "walkthroughs/skald.md"},
    {"id": 84, "title": "Modifying RPG Parameters and NPC Stats", "file": "walkthroughs/modifying-rpg-parameters.md"},
    {"id": 37, "title": "Modding - Game Data", "file": "game-data/index.md"},
    {"id": 15, "title": "LUA Scripting", "file": "game-data/skald/lua-scripting.md"},
    {"id": 86, "title": "Excel Addin", "file": "game-data/skald/excel-addin.md"},
    {"id": 16, "title": "RPG System", "file": "game-data/skald/rpg-system/index.md"},
    {"id": 20, "title": "RPG Parameters Reference", "file": "game-data/skald/rpg-system/rpg-params.md"},
    {"id": 21, "title": "Soul Stats and Skills Reference", "file": "game-data/skald/rpg-system/soul-stats.md"},
    {"id": 27, "title": "Crime System", "file": "game-data/skald/rpg-system/crime.md"},
    {"id": 32, "title": "STORM", "file": "game-data/skald/rpg-system/storm/index.md"},
    {"id": 33, "title": "STORM Selectors", "file": "game-data/skald/rpg-system/storm/selectors.md"},
    {"id": 34, "title": "STORM Operations", "file": "game-data/skald/rpg-system/storm/operations.md"},
    {"id": 29, "title": "Quest System", "file": "game-data/quest-system/index.md"},
    {"id": 30, "title": "Quest System Details", "file": "game-data/quest-system/quest-system-detail.md"},
    {"id": 31, "title": "Tourist Mod Example", "file": "game-data/quest-system/tourist-mod-example.md"},
    {"id": 67, "title": "Events", "file": "game-data/events/index.md"},
    {"id": 71, "title": "Random Events", "file": "game-data/events/random-events/index.md"},
    {"id": 68, "title": "Events Tutorial", "file": "game-data/events/random-events/events-tutorial.md"},
    {"id": 69, "title": "Event Place Tutorial", "file": "game-data/events/random-events/event-place-tutorial.md"},
    {"id": 70, "title": "Fast Travel Events", "file": "game-data/events/random-events/fast-travel-events.md"},
    {"id": 72, "title": "Skald Event Nodes", "file": "game-data/events/skald-nodes/index.md"},
    {"id": 73, "title": "Event Place Node", "file": "game-data/events/skald-nodes/event-place-node.md"},
    {"id": 74, "title": "Random Event Node", "file": "game-data/events/skald-nodes/random-event-node.md"},
    {"id": 75, "title": "Random Event Variant Node", "file": "game-data/events/skald-nodes/random-event-variant-node.md"},
    {"id": 76, "title": "Static Ports", "file": "game-data/events/skald-nodes/static-ports.md"},
    {"id": 89, "title": "Item Health and Quality", "file": "game-data/item-health.md"},
    {"id": 90, "title": "Inventory Presets", "file": "game-data/inventory-presets.md"},
    {"id": 91, "title": "Localization", "file": "game-data/localization.md"},
    {"id": 92, "title": "Level Data", "file": "game-data/level-data/index.md"},
    {"id": 93, "title": "Entity Links", "file": "game-data/level-data/entity-links.md"},
    {"id": 18, "title": "Skald Tool Documentation", "file": "game-data/skald-tool-docs.md"},
    {"id": 38, "title": "Modding - Visuals", "file": "visuals/index.md"},
    {"id": 82, "title": "Building Shader Cache", "file": "visuals/shaders.md"},
    {"id": 39, "title": "Character Art", "file": "visuals/character-art/index.md"},
    {"id": 66, "title": "Maya Plugin", "file": "visuals/character-art/maya-plugin.md"},
    {"id": 22, "title": "Layering System", "file": "visuals/character-art/layering-system/index.md"},
    {"id": 23, "title": "Layering System Infographic", "file": "visuals/character-art/layering-system/infographic.md"},
    {"id": 24, "title": "Feature ID", "file": "visuals/character-art/layering-system/feature-id.md"},
    {"id": 14, "title": "Smid", "file": "visuals/character-art/layering-system/smid/index.md"},
    {"id": 26, "title": "Material Atlas", "file": "visuals/character-art/layering-system/smid/material-atlas.md"},
    {"id": 25, "title": "Creating Components", "file": "visuals/character-art/layering-system/smid/creating-components.md"},
    {"id": 64, "title": "Hiding Groups", "file": "visuals/character-art/layering-system/smid/creating-components/hiding-groups.md"},
    {"id": 65, "title": "Morphs", "file": "visuals/character-art/layering-system/smid/creating-components/morphs.md"},
    {"id": 77, "title": "Example Mods", "file": "visuals/character-art/example-mods/index.md"},
    {"id": 78, "title": "Dress Mod Example", "file": "visuals/character-art/example-mods/dress-mod.md"},
    {"id": 79, "title": "Horse Mod Example", "file": "visuals/character-art/example-mods/horse-mod.md"},
    {"id": 81, "title": "Helmet Mod Example", "file": "visuals/character-art/example-mods/helmet-mod.md"},
    {"id": 40, "title": "Environment Art", "file": "visuals/environment-art/index.md"},
    {"id": 41, "title": "3D Max Tools", "file": "visuals/environment-art/3ds-max-tools.md"},
    {"id": 42, "title": "How to Set Up Your 3ds Max", "file": "visuals/environment-art/3ds-max-setup.md"},
    {"id": 43, "title": "3D Max Template File", "file": "visuals/environment-art/template-file.md"},
    {"id": 44, "title": "Asset Creation Pipeline", "file": "visuals/environment-art/weapons-modeling.md"},
    {"id": 50, "title": "Important Topics and Guidelines", "file": "visuals/environment-art/standards/useful-rules.md"},
    {"id": 51, "title": "Useful Rules", "file": "visuals/environment-art/standards/useful-rules.md"},
    {"id": 52, "title": "Dimensions and Standards", "file": "visuals/environment-art/standards/dimensions.md"},
    {"id": 54, "title": "Texel Ratio", "file": "visuals/environment-art/standards/texel-ratio.md"},
    {"id": 53, "title": "Detail Mapping", "file": "visuals/environment-art/standards/detail-mapping/index.md"},
    {"id": 59, "title": "Detail Map Library", "file": "visuals/environment-art/standards/detail-mapping/detail-map-library.md"},
    {"id": 45, "title": "Proxies", "file": "visuals/environment-art/proxies/index.md"},
    {"id": 46, "title": "Visual Assets Overview", "file": "visuals/environment-art/proxies/visual-assets-overview.md"},
    {"id": 47, "title": "Physics Proxies", "file": "visuals/environment-art/proxies/physics-proxies.md"},
    {"id": 48, "title": "Shadow Proxy", "file": "visuals/environment-art/proxies/shadow-proxy.md"},
    {"id": 49, "title": "Occlusion Proxy", "file": "visuals/environment-art/proxies/occlusion-proxy.md"},
    {"id": 88, "title": "Weapons", "file": "visuals/environment-art/proxies/lods.md"},
]

BASE_URL = "https://warhorse.youtrack.cloud/api/articles/KM-A-{id}?fields=id,title,content"
OUTPUT_DIR = Path("/home/pavel/repos/kcd2-modding-docs/wiki")

def fetch_article(article_id):
    """Fetch article content from YouTrack API."""
    url = BASE_URL.format(id=article_id)
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/json')
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('content', '')
    except Exception as e:
        print(f"  Error fetching KM-A-{article_id}: {e}")
        return None

def clean_content(content, article_id, title):
    """Clean up the scraped content."""
    if not content:
        return None
    
    # Add header with source info
    header = f"# {title}\n\n> Source: [https://youtrack.warhorsestudios.cz/articles/KM-A-{article_id}](https://youtrack.warhorsestudios.cz/articles/KM-A-{article_id})\n\n"
    
    # Remove image references that won't work
    content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'*(image: \1)*', content)
    
    return header + content.strip() + "\n"

def main():
    print(f"Scraping {len(ARTICLES)} articles from YouTrack API...")
    
    success = 0
    failed = 0
    skipped = 0
    
    for i, article in enumerate(ARTICLES):
        article_id = article['id']
        title = article['title']
        file_path = OUTPUT_DIR / article['file']
        
        print(f"[{i+1}/{len(ARTICLES)}] KM-A-{article_id}: {title}")
        
        # Check if file already exists and is substantial
        if file_path.exists():
            existing_lines = file_path.read_text().count('\n')
            if existing_lines > 50:
                print(f"  Skipping (existing {existing_lines} lines)")
                skipped += 1
                continue
        
        # Fetch content
        content = fetch_article(article_id)
        if content:
            cleaned = clean_content(content, article_id, title)
            if cleaned:
                # Create directory if needed
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(cleaned)
                lines = cleaned.count('\n')
                print(f"  Saved ({lines} lines)")
                success += 1
            else:
                print(f"  Empty content")
                failed += 1
        else:
            print(f"  Failed to fetch")
            failed += 1
        
        # Small delay to be polite
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print(f"Results: {success} saved, {skipped} skipped, {failed} failed")
    print(f"Total: {len(ARTICLES)} articles")

if __name__ == '__main__':
    main()
