from __future__ import annotations
from typing import List, Dict, Optional, Tuple, Any
from .models import TrackData, MeasureData, BeatData, NoteData

# Standard string label prefixes
GUITAR_6_NAMES = ["e", "B", "G", "D", "A", "E"]
BASS_4_NAMES = ["G", "D", "A", "E"]
BASS_5_NAMES = ["G", "D", "A", "E", "B"]
GUITAR_7_NAMES = ["e", "B", "G", "D", "A", "E", "B"]

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_to_note_name(midi_val: int) -> str:
    octave = (midi_val // 12) - 1
    name = NOTE_NAMES[midi_val % 12]
    return f"{name}{octave}"


def get_string_labels(tuning: List[int]) -> List[str]:
    count = len(tuning)
    if count == 6:
        # Check if standard
        if tuning == [64, 59, 55, 50, 45, 40]:
            return GUITAR_6_NAMES
        if tuning == [64, 59, 55, 50, 45, 38]:
            return ["e", "B", "G", "D", "A", "D"]
    elif count == 4:
        return BASS_4_NAMES
    elif count == 5:
        return BASS_5_NAMES
    elif count == 7:
        return GUITAR_7_NAMES
    # Default to note names
    return [NOTE_NAMES[val % 12] for val in tuning]


def format_note_cell(note: NoteData) -> str:
    if note.fret < 0:
        return "x"
    s = str(note.fret)
    eff = note.effect
    if eff.ghostNote:
        s = f"({s})"
    if eff.bend_semitones:
        target = note.fret + int(round(eff.bend_semitones))
        s = f"{s}b{target}"
    elif eff.slide:
        s = f"{s}/"
    elif eff.hammer:
        s = f"{s}h"
    elif eff.vibrato:
        s = f"{s}~"
    elif eff.harmonic:
        s = f"<{s}>"
    return s


def render_ascii_tab(track: TrackData, start_measure: int = 1, end_measure: Optional[int] = None, measures_per_line: int = 2) -> str:
    total_m = len(track.measures)
    if total_m == 0:
        return f"Track '{track.name}' has no measures."

    start_idx = max(1, start_measure) - 1
    end_idx = min(total_m, end_measure) if end_measure is not None else total_m

    selected_measures = track.measures[start_idx:end_idx]
    if not selected_measures:
        return f"No measures found in range {start_measure}..{end_measure}."

    num_strings = len(track.strings)
    string_labels = get_string_labels(track.strings)

    output_lines: List[str] = []
    output_lines.append(f"Track: {track.number}. {track.name} (Tuning: {' '.join(string_labels)})")
    output_lines.append("=" * 70)

    # Chunk measures into groups
    for chunk_start in range(0, len(selected_measures), measures_per_line):
        chunk = selected_measures[chunk_start:chunk_start + measures_per_line]
        
        # Prepare text rows for this chunk:
        # row_header: markers / measure numbers
        # row_chords: chord names / lyrics
        # rows_strings: one per string (0..num_strings-1)
        # row_pm: palm mute indicators
        
        header_parts: List[str] = []
        chord_parts: List[str] = []
        string_parts: List[List[str]] = [[] for _ in range(num_strings)]
        pm_parts: List[str] = []

        for m in chunk:
            m_num_str = f"M{m.number}"
            if m.marker:
                m_num_str += f" [{m.marker}]"
            
            # Build measure content
            # Determine slots for beats
            beats = m.beats
            # If measure has no beats, render empty bar
            if not beats:
                slot_width = 16
                header_parts.append(m_num_str.ljust(slot_width))
                chord_parts.append(" " * slot_width)
                for s_i in range(num_strings):
                    string_parts[s_i].append("-" * slot_width)
                pm_parts.append(" " * slot_width)
                continue

            # Compute column slots for beats
            beat_cols: List[Dict[str, Any]] = []
            for b in beats:
                chord_name = b.chord.name if b.chord else (b.text or "")
                # Notes indexed by string (1-based string -> cell text)
                string_cells: Dict[int, str] = {}
                has_pm = False
                for n in b.notes:
                    string_cells[n.string] = format_note_cell(n)
                    if n.effect.palmMute:
                        has_pm = True
                
                # Minimum cell width based on longest note text
                max_cell_len = max([len(v) for v in string_cells.values()] + [len(chord_name), 1])
                width = max(max_cell_len + 2, 4)
                beat_cols.append({
                    "chord": chord_name,
                    "string_cells": string_cells,
                    "has_pm": has_pm,
                    "width": width
                })

            # Assemble measure strings
            m_header_str = m_num_str
            m_chord_str = ""
            m_string_strs = ["" for _ in range(num_strings)]
            m_pm_str = ""

            for b_col in beat_cols:
                w = b_col["width"]
                # chord line
                c_text = b_col["chord"]
                m_chord_str += c_text.ljust(w)
                
                # pm line
                if b_col["has_pm"]:
                    m_pm_str += "P.M.".ljust(w)
                else:
                    m_pm_str += " " * w

                # each string
                for s_idx in range(num_strings):
                    s_num = s_idx + 1
                    cell = b_col["string_cells"].get(s_num, "")
                    if cell:
                        # e.g. "-7---" or "--12--"
                        fill_len = w - len(cell) - 1
                        left = "-"
                        right = "-" * max(0, fill_len)
                        seg = f"{left}{cell}{right}"
                    else:
                        seg = "-" * w
                    m_string_strs[s_idx] += seg

            total_m_width = len(m_string_strs[0])
            m_header_padded = m_header_str.ljust(total_m_width)

            header_parts.append(m_header_padded)
            chord_parts.append(m_chord_str.ljust(total_m_width))
            for s_i in range(num_strings):
                string_parts[s_i].append(m_string_strs[s_i])
            pm_parts.append(m_pm_str.ljust(total_m_width))

        # Join chunk with barline separators
        header_line = "   " + "  ".join(header_parts)
        chord_line = "   " + "  ".join(chord_parts)
        
        output_lines.append(header_line)
        if any(c.strip() for c in chord_parts):
            output_lines.append(chord_line)

        for s_idx in range(num_strings):
            label = string_labels[s_idx].rjust(2)
            joined_row = "|".join(string_parts[s_idx])
            output_lines.append(f"{label}|{joined_row}|")

        if any(p.strip() for p in pm_parts):
            pm_line = "   " + "  ".join(pm_parts)
            output_lines.append(pm_line)

        output_lines.append("")  # blank separator line between measure chunks

    return "\n".join(output_lines)
