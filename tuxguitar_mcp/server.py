from __future__ import annotations
import os
import json
from typing import List, Optional, Dict, Any, Union
from mcp.server.fastmcp import FastMCP

from .song_editor import SongEditor
from .chords import get_chord, list_available_chords, STRUM_PATTERNS
from .app_launcher import open_in_tuxguitar, get_tuxguitar_status

# Initialize FastMCP Server
mcp = FastMCP("TuxGuitar-MCP", dependencies=["pyguitarpro", "mcp"])


@mcp.tool()
def tuxguitar_get_score_summary(file_path: str) -> str:
    """Read a summary of a guitar score file (.tg, .gp5, .gp4, .gp3).
    Returns title, artist, tempo, time signature, total measure count, and track details."""
    try:
        editor = SongEditor(file_path)
        summary = editor.get_summary()
        return json.dumps(summary, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to read score summary: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_read_measures(
    file_path: str,
    track_number: int = 1,
    start_measure: int = 1,
    end_measure: int = 4
) -> str:
    """Read detailed measure data for a specific track, including beats, notes (frets, strings), durations, and techniques.
    
    Args:
        file_path: Path to score file (.tg, .gp5, etc.)
        track_number: 1-based track index (default 1)
        start_measure: 1-based start measure number (default 1)
        end_measure: 1-based end measure number (default 4)
    """
    try:
        editor = SongEditor(file_path)
        res = editor.read_measures(track_number, start_measure, end_measure)
        return json.dumps(res, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to read measures: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_get_ascii_tab(
    file_path: str,
    track_number: int = 1,
    start_measure: int = 1,
    end_measure: Optional[int] = 4
) -> str:
    """Render a section of a track as visual ASCII guitar tablature, complete with strings, frets, chords, and techniques.
    Ideal for displaying guitar tablature directly in AI responses and markdown.
    
    Args:
        file_path: Path to score file (.tg, .gp5, etc.)
        track_number: 1-based track index
        start_measure: Start measure number
        end_measure: End measure number (optional, defaults to 4)
    """
    try:
        editor = SongEditor(file_path)
        return editor.render_ascii(track_number, start_measure, end_measure)
    except Exception as e:
        return f"Error rendering ASCII tab: {str(e)}"


@mcp.tool()
def tuxguitar_create_score(
    file_path: str,
    title: str = "New Song",
    artist: str = "AI Composer",
    tempo: int = 120,
    time_signature: str = "4/4",
    tracks: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Create a new guitar tablature score from scratch (.gp5 or .tg).
    
    Args:
        file_path: Target file path ending in .gp5 or .tg
        title: Song title
        artist: Artist / composer name
        tempo: Tempo in BPM (e.g. 120)
        time_signature: Time signature string (e.g. "4/4", "3/4", "6/8")
        tracks: Optional list of track configurations. E.g. [
            {"name": "Lead Guitar", "tuning": "standard_6", "instrument": "electric_clean"},
            {"name": "Bass", "tuning": "bass_4_standard", "instrument": "electric_bass_finger"}
        ]
    """
    try:
        editor = SongEditor()
        editor.create_new(
            file_path=file_path,
            title=title,
            artist=artist,
            tempo=tempo,
            time_signature=time_signature,
            track_presets=tracks,
        )
        saved_path = editor.save(backup=False)
        return json.dumps({
            "success": True,
            "message": f"Successfully created score at {saved_path}",
            "summary": editor.get_summary()
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to create score: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_add_track(
    file_path: str,
    name: str,
    tuning: str = "standard_6",
    instrument: str = "distortion_guitar",
    backup: bool = True
) -> str:
    """Add a new instrument track to an existing score file.
    
    Args:
        file_path: Path to score file
        name: Name of track (e.g. "Overdriven Rhythm", "Bass", "Acoustic Solo")
        tuning: Tuning preset ("standard_6", "drop_d", "dadgad", "half_step_down", "bass_4_standard", "7_string_standard")
        instrument: MIDI instrument preset ("electric_clean", "distortion_guitar", "acoustic_steel", "electric_bass_finger", etc.)
        backup: Whether to create a backup file (.bak) before modifying
    """
    try:
        editor = SongEditor(file_path)
        track = editor.add_track(name=name, tuning=tuning, instrument=instrument)
        editor.save(backup=backup)
        return json.dumps({
            "success": True,
            "message": f"Added track '{name}' (track #{track.number})",
            "track": track.to_dict(include_measures=False)
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to add track: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_remove_track(file_path: str, track_number: int, backup: bool = True) -> str:
    """Remove a track from a score file by 1-based track number."""
    try:
        editor = SongEditor(file_path)
        ok = editor.remove_track(track_number)
        if ok:
            editor.save(backup=backup)
            return json.dumps({"success": True, "message": f"Removed track #{track_number}"}, ensure_ascii=False)
        return json.dumps({"error": f"Track #{track_number} not found."}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to remove track: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_write_measures(
    file_path: str,
    track_number: int,
    start_measure: int,
    measures_data: List[Dict[str, Any]],
    backup: bool = True
) -> str:
    """Write or overwrite measures, beats, notes, and effects in a specific track.
    
    Args:
        file_path: Path to score file
        track_number: 1-based track index
        start_measure: 1-based start measure index
        measures_data: List of measure definitions. Example:
            [
              {
                "marker": "Verse 1",
                "beats": [
                  {
                    "duration": "quarter",
                    "chord": "Am",
                    "notes": [
                      {"string": 5, "fret": 0},
                      {"string": 4, "fret": 2},
                      {"string": 3, "fret": 2},
                      {"string": 2, "fret": 1},
                      {"string": 1, "fret": 0}
                    ]
                  },
                  {
                    "duration": "eighth",
                    "notes": [{"string": 3, "fret": 2, "hammer": True}]
                  }
                ]
              }
            ]
        backup: Whether to create a backup file (.bak)
    """
    try:
        editor = SongEditor(file_path)
        res = editor.write_measures(track_number, start_measure, measures_data)
        if "error" in res:
            return json.dumps(res, ensure_ascii=False)
        editor.save(backup=backup)
        # Generate ASCII tab preview of updated measures
        end_m = start_measure + len(measures_data) - 1
        tab_preview = editor.render_ascii(track_number, start_measure, end_m)
        return json.dumps({
            "success": True,
            "message": f"Successfully updated measures {start_measure}..{end_m} on track {track_number}.",
            "tab_preview": tab_preview
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to write measures: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_add_riff(
    file_path: str,
    track_number: int,
    start_measure: int,
    notes_list: List[Dict[str, Any]],
    default_duration: str = "eighth",
    backup: bool = True
) -> str:
    """Convenience tool to write a guitar solo, riff, or melody line note-by-note.
    Automatically distributes notes into beats and measures.
    
    Args:
        file_path: Path to score file
        track_number: 1-based track index
        start_measure: 1-based starting measure
        notes_list: List of note objects, e.g.:
            [
              {"string": 1, "fret": 12, "duration": "eighth"},
              {"string": 2, "fret": 15, "bend_semitones": 2.0},
              {"string": 1, "fret": 12},
              {"string": 2, "fret": 15, "hammer": True},
              {"string": 3, "fret": 14, "vibrato": True, "duration": "quarter"}
            ]
        default_duration: Default note duration if not specified ("quarter", "eighth", "16th", etc.)
        backup: Create backup file
    """
    try:
        editor = SongEditor(file_path)
        res = editor.add_riff(track_number, start_measure, notes_list, default_duration)
        if "error" in res:
            return json.dumps(res, ensure_ascii=False)
        editor.save(backup=backup)
        end_m = res.get("end_measure", start_measure)
        tab_preview = editor.render_ascii(track_number, start_measure, end_m)
        return json.dumps({
            "success": True,
            "message": f"Added riff across measures {start_measure}..{end_m}.",
            "tab_preview": tab_preview
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to add riff: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_add_chord_progression(
    file_path: str,
    track_number: int,
    start_measure: int,
    progression: List[str],
    strum_pattern: str = "down_down_up_down_up",
    backup: bool = True
) -> str:
    """Write a rhythmic chord progression (e.g. C - G - Am - F) with automatic strumming patterns.
    
    Args:
        file_path: Path to score file
        track_number: 1-based track index
        start_measure: Starting measure (1-based)
        progression: List of chord names (e.g. ["C", "G", "Am", "F"] or ["Em", "C", "G", "D"])
        strum_pattern: Rhythm pattern:
            - "down_down_up_down_up" (standard pop/folk strumming)
            - "quarter_4" (4 quarter down strums per measure)
            - "half_half" (2 half down strums per measure)
            - "whole" (1 whole strum per measure)
            - "eighth_8" (continuous 8th note strumming)
            - "folk_arpeggio" (fingerpicked arpeggio)
            - "metal_chug" (palm muted power chord chugs)
        backup: Create backup file
    """
    try:
        editor = SongEditor(file_path)
        res = editor.add_chord_progression(track_number, start_measure, progression, strum_pattern)
        if "error" in res:
            return json.dumps(res, ensure_ascii=False)
        editor.save(backup=backup)
        end_m = start_measure + len(progression) - 1
        tab_preview = editor.render_ascii(track_number, start_measure, end_m)
        return json.dumps({
            "success": True,
            "message": f"Added chord progression {progression} to measures {start_measure}..{end_m}.",
            "tab_preview": tab_preview
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to add chord progression: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_transpose(
    file_path: str,
    track_number: int = 0,
    semitones: int = 2,
    backup: bool = True
) -> str:
    """Transpose notes in a score up or down by semitones.
    
    Args:
        file_path: Path to score file
        track_number: Track index to transpose (0 = all tracks in song)
        semitones: Number of semitones (+2 = up one whole step, -1 = down half step, etc.)
        backup: Create backup file
    """
    try:
        editor = SongEditor(file_path)
        res = editor.transpose(track_number, semitones)
        editor.save(backup=backup)
        return json.dumps(res, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to transpose: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_add_marker(
    file_path: str,
    measure_number: int,
    title: str,
    backup: bool = True
) -> str:
    """Add a section label / marker (e.g. 'Intro', 'Verse 1', 'Chorus', 'Solo', 'Outro') at a specific measure."""
    try:
        editor = SongEditor(file_path)
        ok = editor.set_marker(measure_number, title)
        if ok:
            editor.save(backup=backup)
            return json.dumps({"success": True, "message": f"Added marker '{title}' at measure {measure_number}"}, ensure_ascii=False)
        return json.dumps({"error": "Failed to set marker."}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to set marker: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_set_tempo(
    file_path: str,
    measure_number: int,
    tempo: int,
    backup: bool = True
) -> str:
    """Change the tempo (BPM) at a specific measure."""
    try:
        editor = SongEditor(file_path)
        ok = editor.set_tempo(measure_number, tempo)
        if ok:
            editor.save(backup=backup)
            return json.dumps({"success": True, "message": f"Set tempo to {tempo} BPM at measure {measure_number}"}, ensure_ascii=False)
        return json.dumps({"error": "Failed to set tempo."}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to set tempo: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_set_time_signature(
    file_path: str,
    measure_number: int,
    numerator: int = 4,
    denominator: int = 4,
    backup: bool = True
) -> str:
    """Change the time signature (e.g. 4/4, 3/4, 6/8) at a specific measure."""
    try:
        editor = SongEditor(file_path)
        ok = editor.set_time_signature(measure_number, numerator, denominator)
        if ok:
            editor.save(backup=backup)
            return json.dumps({"success": True, "message": f"Set time signature to {numerator}/{denominator} at measure {measure_number}"}, ensure_ascii=False)
        return json.dumps({"error": "Failed to set time signature."}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to set time signature: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_get_chord_info(chord_name: str) -> str:
    """Look up fingering, strings, notes, and first fret for a chord on 6-string guitar standard tuning."""
    info = get_chord(chord_name)
    if info:
        return json.dumps(info, indent=2, ensure_ascii=False)
    return json.dumps({"error": f"Chord '{chord_name}' not found in dictionary."}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_list_chords() -> str:
    """List all available chord voicings in the built-in chord library."""
    chords = list_available_chords()
    return json.dumps({"count": len(chords), "chords": chords}, indent=2, ensure_ascii=False)


@mcp.tool()
def tuxguitar_convert_format(input_path: str, output_path: str) -> str:
    """Convert a guitar score between TuxGuitar (.tg) and Guitar Pro (.gp5, .gp4, .gp3) formats."""
    try:
        editor = SongEditor(input_path)
        out = editor.save(output_path, backup=False)
        return json.dumps({
            "success": True,
            "message": f"Successfully converted {input_path} -> {out}"
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Failed to convert format: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def tuxguitar_open_in_app(file_path: str) -> str:
    """Open a guitar score file in the TuxGuitar desktop application (tuxguitar.exe)."""
    res = open_in_tuxguitar(file_path)
    return json.dumps(res, indent=2, ensure_ascii=False)


@mcp.tool()
def tuxguitar_app_status() -> str:
    """Check whether TuxGuitar is installed, executable path, version, and whether it is currently running."""
    status = get_tuxguitar_status()
    return json.dumps(status, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
