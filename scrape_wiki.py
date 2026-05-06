#!/usr/bin/env python3
"""Scrape KCD2 modding wiki from YouTrack using browser automation."""

import json
import os
import re
import subprocess
import time
from pathlib import Path

# Article list
ARTICLES = [
    {"id": 0, "title": "Modding Kingdom Come: Deliverance 2"},
    {"id": 87, "title": "Modding Rules"},
    {"id": 56, "title": "Installing Mods"},
    {"id": 36, "title": "Technical Overview"},
    {"id": 55, "title": "The Modding Tools"},
    {"id": 3, "title": "Structure of a Mod"},
    {"id": 57, "title": "Mod Manifest"},
    {"id": 35, "title": "Reserved ModIds"},
    {"id": 12, "title": "Database Tables"},
    {"id": 58, "title": "Publishing a Mod"},
    {"id": 85, "title": "Publishing to Steam Workshop"},
    {"id": 83, "title": "Walkthroughs"},
    {"id": 8, "title": "Simple Mod - Modifying CVars"},
    {"id": 17, "title": "Adding a New Item"},
    {"id": 18, "title": "Skald"},
    {"id": 84, "title": "Modifying RPG Parameters and NPC Stats"},
    {"id": 37, "title": "Modding - Game Data"},
    {"id": 15, "title": "LUA Scripting"},
    {"id": 86, "title": "Excel Addin"},
    {"id": 16, "title": "RPG System"},
    {"id": 20, "title": "RPG Parameters Reference"},
    {"id": 21, "title": "Soul Stats and Skills Reference"},
    {"id": 27, "title": "Crime System"},
    {"id": 32, "title": "STORM"},
    {"id": 33, "title": "STORM Selectors"},
    {"id": 34, "title": "STORM Operations"},
    {"id": 29, "title": "Quest System"},
    {"id": 30, "title": "Quest System Details"},
    {"id": 31, "title": "Tourist Mod Example"},
    {"id": 67, "title": "Events"},
    {"id": 71, "title": "Random Events"},
    {"id": 68, "title": "Events Tutorial"},
    {"id": 69, "title": "Event Place Tutorial"},
    {"id": 70, "title": "Fast Travel Events"},
    {"id": 72, "title": "Skald Event Nodes"},
    {"id": 73, "title": "Event Place Node"},
    {"id": 74, "title": "Random Event Node"},
    {"id": 75, "title": "Random Event Variant Node"},
    {"id": 76, "title": "Static Ports"},
    {"id": 89, "title": "Item Health and Quality"},
    {"id": 90, "title": "Inventory Presets"},
    {"id": 91, "title": "Localization"},
    {"id": 92, "title": "Level Data"},
    {"id": 93, "title": "Entity Links"},
    {"id": 38, "title": "Modding - Visuals"},
    {"id": 82, "title": "Building Shader Cache"},
    {"id": 39, "title": "Character Art"},
    {"id": 66, "title": "Maya Plugin"},
    {"id": 22, "title": "Layering System"},
    {"id": 23, "title": "Layering System Infographic"},
    {"id": 24, "title": "Feature ID"},
    {"id": 14, "title": "Smid"},
    {"id": 26, "title": "Material Atlas"},
    {"id": 25, "title": "Creating Components"},
    {"id": 64, "title": "Hiding Groups"},
    {"id": 65, "title": "Morphs"},
    {"id": 77, "title": "Example Mods"},
    {"id": 78, "title": "Dress Mod Example"},
    {"id": 79, "title": "Horse Mod Example"},
    {"id": 81, "title": "Helmet Mod Example"},
    {"id": 40, "title": "Environment Art"},
    {"id": 41, "title": "3D Max Tools"},
    {"id": 42, "title": "How to Set Up Your 3ds Max"},
    {"id": 43, "title": "3D Max Template File"},
    {"id": 44, "title": "Asset Creation Pipeline"},
    {"id": 50, "title": "Important Topics and Guidelines"},
    {"id": 51, "title": "Useful Rules"},
    {"id": 52, "title": "Dimensions and Standards"},
    {"id": 54, "title": "Texel Ratio"},
    {"id": 53, "title": "Detail Mapping"},
    {"id": 59, "title": "Detail Map Library"},
    {"id": 45, "title": "Proxies"},
    {"id": 46, "title": "Visual Assets Overview"},
    {"id": 47, "title": "Physics Proxies"},
    {"id": 48, "title": "Shadow Proxy"},
    {"id": 49, "title": "Occlusion Proxy"},
    {"id": 88, "title": "Weapons"},
]

BASE_URL = "https://warhorse.youtrack.cloud/articles/KM-A-{id}"
OUTPUT_DIR = Path("/tmp/kcd2_scraped")

def get_article_url(article_id):
    return BASE_URL.format(id=article_id)

print(f"Total articles to scrape: {len(ARTICLES)}")
print(f"Output directory: {OUTPUT_DIR}")

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

# Save article list
with open(OUTPUT_DIR / "articles.json", "w") as f:
    json.dump(ARTICLES, f, indent=2)

print("Article list saved. Ready for browser scraping.")
