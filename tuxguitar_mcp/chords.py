from __future__ import annotations
from typing import Dict, List, Optional, Any, Tuple

# Chord frets mapping: [String 1 (high E), String 2 (B), String 3 (G), String 4 (D), String 5 (A), String 6 (low E)]
# -1 indicates the string is muted / not played.
CHORD_DICTIONARY: Dict[str, Dict[str, Any]] = {
    # Major Open & Barre Chords
    "C": {"first_fret": 1, "strings": [0, 1, 0, 2, 3, -1], "notes": ["C", "E", "G"]},
    "D": {"first_fret": 1, "strings": [2, 3, 2, 0, -1, -1], "notes": ["D", "F#", "A"]},
    "E": {"first_fret": 1, "strings": [0, 0, 1, 2, 2, 0], "notes": ["E", "G#", "B"]},
    "F": {"first_fret": 1, "strings": [1, 1, 2, 3, 3, 1], "notes": ["F", "A", "C"]},
    "G": {"first_fret": 1, "strings": [3, 0, 0, 0, 2, 3], "notes": ["G", "B", "D"]},
    "A": {"first_fret": 1, "strings": [0, 2, 2, 2, 0, -1], "notes": ["A", "C#", "E"]},
    "B": {"first_fret": 2, "strings": [2, 4, 4, 4, 2, -1], "notes": ["B", "D#", "F#"]},
    "Bb": {"first_fret": 1, "strings": [1, 3, 3, 3, 1, -1], "notes": ["Bb", "D", "F"]},
    "A#": {"first_fret": 1, "strings": [1, 3, 3, 3, 1, -1], "notes": ["A#", "D", "F"]},
    "C#": {"first_fret": 4, "strings": [4, 6, 6, 6, 4, -1], "notes": ["C#", "E#", "G#"]},
    "Db": {"first_fret": 4, "strings": [4, 6, 6, 6, 4, -1], "notes": ["Db", "F", "Ab"]},
    "Eb": {"first_fret": 6, "strings": [6, 8, 8, 8, 6, -1], "notes": ["Eb", "G", "Bb"]},
    "D#": {"first_fret": 6, "strings": [6, 8, 8, 8, 6, -1], "notes": ["D#", "G", "A#"]},
    "F#": {"first_fret": 2, "strings": [2, 2, 3, 4, 4, 2], "notes": ["F#", "A#", "C#"]},
    "Gb": {"first_fret": 2, "strings": [2, 2, 3, 4, 4, 2], "notes": ["Gb", "Bb", "Db"]},
    "Ab": {"first_fret": 4, "strings": [4, 4, 5, 6, 6, 4], "notes": ["Ab", "C", "Eb"]},
    "G#": {"first_fret": 4, "strings": [4, 4, 5, 6, 6, 4], "notes": ["G#", "B#", "D#"]},

    # Minor Chords
    "Am": {"first_fret": 1, "strings": [0, 1, 2, 2, 0, -1], "notes": ["A", "C", "E"]},
    "Bm": {"first_fret": 2, "strings": [2, 3, 4, 4, 2, -1], "notes": ["B", "D", "F#"]},
    "Cm": {"first_fret": 3, "strings": [3, 4, 5, 5, 3, -1], "notes": ["C", "Eb", "G"]},
    "Dm": {"first_fret": 1, "strings": [1, 3, 2, 0, -1, -1], "notes": ["D", "F", "A"]},
    "Em": {"first_fret": 1, "strings": [0, 0, 0, 2, 2, 0], "notes": ["E", "G", "B"]},
    "Fm": {"first_fret": 1, "strings": [1, 1, 1, 3, 3, 1], "notes": ["F", "Ab", "C"]},
    "Gm": {"first_fret": 3, "strings": [3, 3, 3, 5, 5, 3], "notes": ["G", "Bb", "D"]},
    "F#m": {"first_fret": 2, "strings": [2, 2, 2, 4, 4, 2], "notes": ["F#", "A", "C#"]},
    "G#m": {"first_fret": 4, "strings": [4, 4, 4, 6, 6, 4], "notes": ["G#", "B", "D#"]},
    "Bbm": {"first_fret": 1, "strings": [1, 2, 3, 3, 1, -1], "notes": ["Bb", "Db", "F"]},
    "C#m": {"first_fret": 4, "strings": [4, 5, 6, 6, 4, -1], "notes": ["C#", "E", "G#"]},
    "Ebm": {"first_fret": 6, "strings": [6, 7, 8, 8, 6, -1], "notes": ["Eb", "Gb", "Bb"]},

    # Dominant 7th Chords
    "C7": {"first_fret": 1, "strings": [0, 1, 3, 2, 3, -1], "notes": ["C", "E", "G", "Bb"]},
    "D7": {"first_fret": 1, "strings": [2, 1, 2, 0, -1, -1], "notes": ["D", "F#", "A", "C"]},
    "E7": {"first_fret": 1, "strings": [0, 0, 1, 0, 2, 0], "notes": ["E", "G#", "B", "D"]},
    "F7": {"first_fret": 1, "strings": [1, 1, 2, 1, 3, 1], "notes": ["F", "A", "C", "Eb"]},
    "G7": {"first_fret": 1, "strings": [1, 0, 0, 0, 2, 3], "notes": ["G", "B", "D", "F"]},
    "A7": {"first_fret": 1, "strings": [0, 2, 0, 2, 0, -1], "notes": ["A", "C#", "E", "G"]},
    "B7": {"first_fret": 1, "strings": [2, 0, 2, 1, 2, -1], "notes": ["B", "D#", "F#", "A"]},

    # Major 7th Chords
    "Cmaj7": {"first_fret": 1, "strings": [0, 0, 0, 2, 3, -1], "notes": ["C", "E", "G", "B"]},
    "Dmaj7": {"first_fret": 1, "strings": [2, 2, 2, 0, -1, -1], "notes": ["D", "F#", "A", "C#"]},
    "Emaj7": {"first_fret": 1, "strings": [0, 0, 1, 1, 2, 0], "notes": ["E", "G#", "B", "D#"]},
    "Fmaj7": {"first_fret": 1, "strings": [0, 1, 2, 3, -1, -1], "notes": ["F", "A", "C", "E"]},
    "Gmaj7": {"first_fret": 1, "strings": [2, 0, 0, 0, 2, 3], "notes": ["G", "B", "D", "F#"]},
    "Amaj7": {"first_fret": 1, "strings": [0, 2, 1, 2, 0, -1], "notes": ["A", "C#", "E", "G#"]},
    "Bmaj7": {"first_fret": 2, "strings": [2, 4, 3, 4, 2, -1], "notes": ["B", "D#", "F#", "A#"]},

    # Minor 7th Chords
    "Am7": {"first_fret": 1, "strings": [0, 1, 0, 2, 0, -1], "notes": ["A", "C", "E", "G"]},
    "Bm7": {"first_fret": 2, "strings": [2, 3, 2, 4, 2, -1], "notes": ["B", "D", "F#", "A"]},
    "Cm7": {"first_fret": 3, "strings": [3, 4, 3, 5, 3, -1], "notes": ["C", "Eb", "G", "Bb"]},
    "Dm7": {"first_fret": 1, "strings": [1, 1, 2, 0, -1, -1], "notes": ["D", "F", "A", "C"]},
    "Em7": {"first_fret": 1, "strings": [0, 0, 0, 0, 2, 0], "notes": ["E", "G", "B", "D"]},
    "Fm7": {"first_fret": 1, "strings": [1, 1, 1, 1, 3, 1], "notes": ["F", "Ab", "C", "Eb"]},
    "Gm7": {"first_fret": 3, "strings": [3, 3, 3, 3, 5, 3], "notes": ["G", "Bb", "D", "F"]},
    "F#m7": {"first_fret": 2, "strings": [2, 2, 2, 2, 4, 2], "notes": ["F#", "A", "C#", "E"]},

    # Suspended Chords
    "Csus2": {"first_fret": 1, "strings": [3, 3, 0, -1, 3, -1], "notes": ["C", "D", "G"]},
    "Dsus2": {"first_fret": 1, "strings": [0, 3, 2, 0, -1, -1], "notes": ["D", "E", "A"]},
    "Asus2": {"first_fret": 1, "strings": [0, 0, 2, 2, 0, -1], "notes": ["A", "B", "E"]},
    "Esus4": {"first_fret": 1, "strings": [0, 0, 2, 2, 2, 0], "notes": ["E", "A", "B"]},
    "Asus4": {"first_fret": 1, "strings": [0, 3, 2, 2, 0, -1], "notes": ["A", "D", "E"]},
    "Dsus4": {"first_fret": 1, "strings": [3, 3, 2, 0, -1, -1], "notes": ["D", "G", "A"]},
    "Gsus4": {"first_fret": 1, "strings": [3, 1, 0, 0, -1, 3], "notes": ["G", "C", "D"]},

    # Add9
    "Cadd9": {"first_fret": 1, "strings": [3, 3, 0, 2, 3, -1], "notes": ["C", "E", "G", "D"]},
    "Gadd9": {"first_fret": 1, "strings": [3, 0, 2, 0, 0, 3], "notes": ["G", "B", "D", "A"]},

    # Power Chords (Root + 5th)
    "C5": {"first_fret": 3, "strings": [-1, -1, -1, 5, 3, -1], "notes": ["C", "G"]},
    "D5": {"first_fret": 5, "strings": [-1, -1, -1, 7, 5, -1], "notes": ["D", "A"]},
    "E5": {"first_fret": 1, "strings": [-1, -1, -1, 2, 2, 0], "notes": ["E", "B"]},
    "F5": {"first_fret": 1, "strings": [-1, -1, -1, 3, 3, 1], "notes": ["F", "C"]},
    "F#5": {"first_fret": 2, "strings": [-1, -1, -1, 4, 4, 2], "notes": ["F#", "C#"]},
    "G5": {"first_fret": 3, "strings": [-1, -1, -1, 5, 5, 3], "notes": ["G", "D"]},
    "G#5": {"first_fret": 4, "strings": [-1, -1, -1, 6, 6, 4], "notes": ["G#", "D#"]},
    "A5": {"first_fret": 1, "strings": [-1, -1, 2, 2, 0, -1], "notes": ["A", "E"]},
    "Bb5": {"first_fret": 1, "strings": [-1, -1, -1, 3, 1, -1], "notes": ["Bb", "F"]},
    "B5": {"first_fret": 2, "strings": [-1, -1, -1, 4, 2, -1], "notes": ["B", "F#"]},
}

# Aliases
ALIASES = {
    "C#": "Db",
    "D#": "Eb",
    "F#": "Gb",
    "G#": "Ab",
    "A#": "Bb",
    "CM": "C",
    "DM": "D",
    "EM": "E",
    "FM": "F",
    "GM": "G",
    "AM": "A",
    "BM": "B",
}


def normalize_chord_name(name: str) -> str:
    cleaned = name.strip()
    return ALIASES.get(cleaned, cleaned)


def get_chord(name: str) -> Optional[Dict[str, Any]]:
    norm = normalize_chord_name(name)
    if norm in CHORD_DICTIONARY:
        data = dict(CHORD_DICTIONARY[norm])
        data["name"] = name
        return data
    # Check case insensitive
    for k, v in CHORD_DICTIONARY.items():
        if k.lower() == norm.lower():
            data = dict(v)
            data["name"] = k
            return data
    return None


def list_available_chords() -> List[str]:
    return sorted(list(CHORD_DICTIONARY.keys()))


# Strumming pattern definitions
# Each item in pattern is a dict with: duration, stroke ("down", "up", None), strings_to_play (None for all chord strings)
STRUM_PATTERNS: Dict[str, List[Dict[str, Any]]] = {
    "whole": [
        {"duration": "whole", "stroke": "down"}
    ],
    "half_half": [
        {"duration": "half", "stroke": "down"},
        {"duration": "half", "stroke": "down"}
    ],
    "quarter_4": [
        {"duration": "quarter", "stroke": "down"},
        {"duration": "quarter", "stroke": "down"},
        {"duration": "quarter", "stroke": "down"},
        {"duration": "quarter", "stroke": "down"}
    ],
    "down_down_up_down_up": [
        # Measure in 4/4: Beat 1: Quarter D; Beat 2: Eighth D, Eighth U; Beat 3: Quarter D; Beat 4: Eighth D, Eighth U
        {"duration": "quarter", "stroke": "down"},
        {"duration": "eighth", "stroke": "down"},
        {"duration": "eighth", "stroke": "up"},
        {"duration": "quarter", "stroke": "down"},
        {"duration": "eighth", "stroke": "down"},
        {"duration": "eighth", "stroke": "up"},
    ],
    "eighth_8": [
        {"duration": "eighth", "stroke": "down"},
        {"duration": "eighth", "stroke": "up"},
        {"duration": "eighth", "stroke": "down"},
        {"duration": "eighth", "stroke": "up"},
        {"duration": "eighth", "stroke": "down"},
        {"duration": "eighth", "stroke": "up"},
        {"duration": "eighth", "stroke": "down"},
        {"duration": "eighth", "stroke": "up"},
    ],
    "folk_arpeggio": [
        # Fingerpicking pattern: 8 eighth notes: Bass note, string 3, string 2, string 1, string 2, string 3, string 1, string 2
        {"duration": "eighth", "arpeggio_role": "bass"},
        {"duration": "eighth", "arpeggio_role": "3"},
        {"duration": "eighth", "arpeggio_role": "2"},
        {"duration": "eighth", "arpeggio_role": "1"},
        {"duration": "eighth", "arpeggio_role": "2"},
        {"duration": "eighth", "arpeggio_role": "3"},
        {"duration": "eighth", "arpeggio_role": "1"},
        {"duration": "eighth", "arpeggio_role": "2"},
    ],
    "metal_chug": [
        # 8 eighth notes, palm muted power chord chugs
        {"duration": "eighth", "stroke": "down", "palm_mute": True},
        {"duration": "eighth", "stroke": "down", "palm_mute": True},
        {"duration": "eighth", "stroke": "down", "palm_mute": True},
        {"duration": "eighth", "stroke": "down", "palm_mute": True},
        {"duration": "eighth", "stroke": "down", "palm_mute": True},
        {"duration": "eighth", "stroke": "down", "palm_mute": True},
        {"duration": "eighth", "stroke": "down", "palm_mute": True},
        {"duration": "eighth", "stroke": "down", "palm_mute": True},
    ]
}
