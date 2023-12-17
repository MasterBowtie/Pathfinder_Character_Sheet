
SCORELIST = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

PROFICIENCIES = ['untrained', 'trained', 'expert', 'master', 'legendary']

SKILLSLIST = [
    'acrobatics',
    'arcana',
    'athletics',
    'crafting',
    'deception',
    'diplomacy',
    'intimidation',
    'lore0',
    'lore1',
    'medicine',
    'nature',
    'occultism',
    'perception',
    'performance',
    'religion',
    'society',
    'stealth',
    'survival',
    'thievery']

SAVES = ['fortitude', 'reflex', 'will']

ARMORTYPES = ['unarmored', 'light', 'medium', 'heavy']

WEAPON = {
    "name": "",
    "to_hit": {
        "score": None,
        "proficiency": "untrained",
        "item_bonus": 0
    },
    "damage": {
        "dice": {
            "number": 0,
            "size": 0
        },
        "type": {
            "blunt": 0,
            "piercing": 0,
            "slashing": 0
        },
        "weapon_special": 0,
    },
    "attack_type": "",
    "other": "",
    "traits": "",
    "bulk": 0,
    "description": ""
}