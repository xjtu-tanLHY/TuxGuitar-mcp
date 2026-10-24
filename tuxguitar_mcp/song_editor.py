from __future__ import annotations
import os
import shutil
from typing import List, Optional, Dict, Any, Union

from .models import (
    SongData, TrackData, MeasureData, BeatData, NoteData, NoteEffectData, ChordData,
    TUNING_PRESETS, MIDI_INSTRUMENTS, DURATION_VALUES, VALUE_TO_DURATION, DURATION_TICKS
)
from .tg_parser import parse_tg, write_tg
from .gp_adapter import parse_gp, write_gp
from .ascii_tab import render_ascii_tab
from .chords import get_chord, STRUM_PATTERNS


class SongEditor:
    def __init__(self, file_path: Optional[str] = None):
        self.file_path: Optional[str] = file_path
        self.song: SongData = SongData()
        if file_path and os.path.exists(file_path):
            self.load(file_path)

    def load(self, file_path: str) -> SongData:
        self.file_path = os.path.abspath(file_path)
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".tg":
            self.song = parse_tg(self.file_path)
        elif ext in [".gp3", ".gp4", ".gp5", ".gpx"]:
            self.song = parse_gp(self.file_path)
        else:
            # Try GP first then TG
            try:
                self.song = parse_gp(self.file_path)
            except Exception:
                self.song = parse_tg(self.file_path)
        return self.song

    def save(self, file_path: Optional[str] = None, backup: bool = True) -> str:
        target = os.path.abspath(file_path) if file_path else self.file_path
        if not target:
            raise ValueError("No file path specified for saving.")

        # Ensure directory exists
        os.makedirs(os.path.dirname(target), exist_ok=True)

        if backup and os.path.exists(target):
            bak_path = f"{target}.bak"
            shutil.copy2(target, bak_path)

        ext = os.path.splitext(target)[1].lower()
        if ext == ".tg":
            write_tg(self.song, target)
        else:
            write_gp(self.song, target)

        self.file_path = target
        return target

    def create_new(
        self,
        file_path: str,
        title: str = "New Song",
        artist: str = "AI Composer",
        tempo: int = 120,
        time_signature: str = "4/4",
        track_presets: Optional[List[Dict[str, Any]]] = None
    ) -> SongData:
        self.file_path = os.path.abspath(file_path)
        self.song = SongData(
            title=title,
            artist=artist,
            tempo=tempo,
            time_signature=time_signature,
        )

        if not track_presets:
            track_presets = [
                {
                    "name": "Electric Guitar",
                    "tuning": "standard_6",
                    "instrument": "electric_clean"
                }
            ]

        for idx, tp in enumerate(track_presets):
            name = tp.get("name", f"Track {idx + 1}")
            tuning_key = tp.get("tuning", "standard_6")
            tuning = TUNING_PRESETS.get(tuning_key, TUNING_PRESETS["standard_6"])
            inst_key = tp.get("instrument", "electric_clean")
            inst_val = MIDI_INSTRUMENTS.get(inst_key, 27) if isinstance(inst_key, str) else inst_key

            track = TrackData(
                number=idx + 1,
                name=name,
                instrument=inst_val,
                channel=idx,
                strings=list(tuning),
                color=(0, 100, 255) if idx % 2 == 0 else (255, 100, 0),
            )
            # Create first empty measure
            m = MeasureData(
                number=1,
                time_signature=time_signature,
                tempo=tempo,
            )
            track.measures.append(m)
            self.song.tracks.append(track)

        return self.song

    def get_summary(self) -> Dict[str, Any]:
        return self.song.get_summary()

    def read_measures(self, track_number: int = 1, start_measure: int = 1, end_measure: int = 4) -> Dict[str, Any]:
        if not self.song.tracks:
            return {"error": "Song has no tracks."}
        
        t_idx = track_number - 1
        if t_idx < 0 or t_idx >= len(self.song.tracks):
            return {"error": f"Track {track_number} does not exist (available: 1..{len(self.song.tracks)})."}

        track = self.song.tracks[t_idx]
        total_m = len(track.measures)
        s_idx = max(1, start_measure) - 1
        e_idx = min(total_m, end_measure)

        selected = [m.to_dict() for m in track.measures[s_idx:e_idx]]
        return {
            "track_number": track.number,
            "track_name": track.name,
            "tuning": track.strings,
            "start_measure": start_measure,
            "end_measure": end_measure,
            "total_measures_in_track": total_m,
            "measures": selected,
        }

    def render_ascii(self, track_number: int = 1, start_measure: int = 1, end_measure: Optional[int] = None) -> str:
        if not self.song.tracks:
            return "Song has no tracks."
        t_idx = track_number - 1
        if t_idx < 0 or t_idx >= len(self.song.tracks):
            return f"Track {track_number} not found (available: 1..{len(self.song.tracks)})."
        return render_ascii_tab(self.song.tracks[t_idx], start_measure, end_measure)

    def add_track(
        self,
        name: str,
        tuning: str = "standard_6",
        instrument: str = "distortion_guitar",
        color: Optional[Tuple[int, int, int]] = None
    ) -> TrackData:
        t_num = len(self.song.tracks) + 1
        tuning_list = TUNING_PRESETS.get(tuning, TUNING_PRESETS["standard_6"])
        inst_val = MIDI_INSTRUMENTS.get(instrument, 27) if isinstance(instrument, str) else instrument
        col = color or (200, 50, 50)

        track = TrackData(
            number=t_num,
            name=name,
            instrument=inst_val,
            channel=t_num - 1,
            strings=list(tuning_list),
            color=col,
        )

        # Match measures count of first track
        total_m = self.song.measure_count
        if total_m == 0:
            total_m = 1

        for m_idx in range(total_m):
            ts = self.song.time_signature
            tempo = self.song.tempo
            if self.song.tracks and m_idx < len(self.song.tracks[0].measures):
                ts = self.song.tracks[0].measures[m_idx].time_signature
                tempo = self.song.tracks[0].measures[m_idx].tempo
            m = MeasureData(number=m_idx + 1, time_signature=ts, tempo=tempo)
            track.measures.append(m)

        self.song.tracks.append(track)
        return track

    def remove_track(self, track_number: int) -> bool:
        t_idx = track_number - 1
        if 0 <= t_idx < len(self.song.tracks):
            self.song.tracks.pop(t_idx)
            # Re-number
            for i, t in enumerate(self.song.tracks):
                t.number = i + 1
            return True
        return False

    def ensure_measure_count(self, target_count: int) -> None:
        """Ensures all tracks have at least target_count measures."""
        for trk in self.song.tracks:
            while len(trk.measures) < target_count:
                m_num = len(trk.measures) + 1
                trk.measures.append(MeasureData(
                    number=m_num,
                    time_signature=self.song.time_signature,
                    tempo=self.song.tempo
                ))

    def write_measures(self, track_number: int, start_measure: int, measures_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.song.tracks:
            return {"error": "Song has no tracks."}
        t_idx = track_number - 1
        if t_idx < 0 or t_idx >= len(self.song.tracks):
            return {"error": f"Track {track_number} not found."}

        target_track = self.song.tracks[t_idx]
        needed_measures = start_measure + len(measures_data) - 1
        self.ensure_measure_count(needed_measures)

        for offset, m_dict in enumerate(measures_data):
            m_num = start_measure + offset
            m_idx = m_num - 1
            
            # Find or get measure
            m_obj = target_track.measures[m_idx]
            if "time_signature" in m_dict:
                m_obj.time_signature = m_dict["time_signature"]
                # propagate to other tracks as well for consistency
                for trk in self.song.tracks:
                    if m_idx < len(trk.measures):
                        trk.measures[m_idx].time_signature = m_dict["time_signature"]
            if "tempo" in m_dict:
                m_obj.tempo = m_dict["tempo"]
            if "marker" in m_dict:
                m_obj.marker = m_dict["marker"]
                for trk in self.song.tracks:
                    if m_idx < len(trk.measures):
                        trk.measures[m_idx].marker = m_dict["marker"]

            # Replace beats
            beats_list: List[BeatData] = []
            for b_dict in m_dict.get("beats", []):
                dur = b_dict.get("duration", "quarter")
                dotted = b_dict.get("dotted", False)
                text = b_dict.get("text")
                stroke = b_dict.get("stroke")

                chord_obj = None
                if "chord" in b_dict:
                    c_info = b_dict["chord"]
                    if isinstance(c_info, str):
                        c_dict = get_chord(c_info)
                        if c_dict:
                            chord_obj = ChordData(name=c_dict["name"], first_fret=c_dict["first_fret"], strings=c_dict["strings"])
                    elif isinstance(c_info, dict):
                        chord_obj = ChordData(
                            name=c_info.get("name", ""),
                            first_fret=c_info.get("first_fret", 1),
                            strings=c_info.get("strings", [])
                        )

                tuplet_enters = b_dict.get("tuplet_enters", 1)
                tuplet_times = b_dict.get("tuplet_times", 1)
                if b_dict.get("tuplet") == "3:2" or b_dict.get("tuplet") == "triplet":
                    tuplet_enters = 3
                    tuplet_times = 2

                beat = BeatData(
                    duration=dur,
                    dotted=dotted,
                    tuplet_enters=tuplet_enters,
                    tuplet_times=tuplet_times,
                    chord=chord_obj,
                    text=text,
                    stroke=stroke,
                )

                for n_dict in b_dict.get("notes", []):
                    s_num = n_dict.get("string", 1)
                    f_val = n_dict.get("fret", 0)
                    vel = n_dict.get("velocity", 95)
                    
                    eff_dict = n_dict.get("effect", {})
                    eff = NoteEffectData(
                        hammer=n_dict.get("hammer", eff_dict.get("hammer", False)),
                        slide=n_dict.get("slide", eff_dict.get("slide")),
                        bend_semitones=n_dict.get("bend_semitones", eff_dict.get("bend_semitones")),
                        vibrato=n_dict.get("vibrato", eff_dict.get("vibrato", False)),
                        palmMute=n_dict.get("palmMute", eff_dict.get("palmMute", False)),
                        ghostNote=n_dict.get("ghostNote", eff_dict.get("ghostNote", False)),
                        deadNote=n_dict.get("deadNote", eff_dict.get("deadNote", False)),
                        accentuated=n_dict.get("accentuated", eff_dict.get("accentuated", False)),
                        heavyAccentuated=n_dict.get("heavyAccentuated", eff_dict.get("heavyAccentuated", False)),
                        letRing=n_dict.get("letRing", eff_dict.get("letRing", False)),
                        staccato=n_dict.get("staccato", eff_dict.get("staccato", False)),
                    )
                    beat.notes.append(NoteData(string=s_num, fret=f_val, velocity=vel, effect=eff))

                beats_list.append(beat)

            m_obj.beats = beats_list

        return {
            "success": True,
            "track_number": track_number,
            "start_measure": start_measure,
            "end_measure": needed_measures,
            "total_measures": self.song.measure_count,
        }

    def add_riff(
        self,
        track_number: int,
        start_measure: int,
        notes_list: List[Dict[str, Any]],
        default_duration: str = "eighth"
    ) -> Dict[str, Any]:
        """Convenience method to write a sequence of notes into measures automatically."""
        if not self.song.tracks:
            return {"error": "Song has no tracks."}
        t_idx = track_number - 1
        if t_idx < 0 or t_idx >= len(self.song.tracks):
            return {"error": f"Track {track_number} not found."}

        # Calculate ticks per measure (e.g. 4/4 = 3840 ticks)
        # Parse time signature
        ts = self.song.time_signature
        parts = ts.split("/")
        num, den = (int(parts[0]), int(parts[1])) if len(parts) == 2 else (4, 4)
        ticks_per_measure = int(3840 * (num / den))

        measures_data: List[Dict[str, Any]] = []
        current_beats: List[Dict[str, Any]] = []
        current_m_ticks = 0

        for n_item in notes_list:
            dur = n_item.get("duration", default_duration)
            dotted = n_item.get("dotted", False)
            dur_ticks = DURATION_TICKS.get(dur, 480)
            if dotted:
                dur_ticks = int(dur_ticks * 1.5)

            if current_m_ticks + dur_ticks > ticks_per_measure:
                # Close current measure
                measures_data.append({"beats": current_beats})
                current_beats = []
                current_m_ticks = 0

            beat_dict = {
                "duration": dur,
                "dotted": dotted,
                "notes": [
                    {
                        "string": n_item.get("string", 1),
                        "fret": n_item.get("fret", 0),
                        "hammer": n_item.get("hammer", False),
                        "slide": n_item.get("slide"),
                        "bend_semitones": n_item.get("bend_semitones"),
                        "vibrato": n_item.get("vibrato", False),
                        "palmMute": n_item.get("palmMute", False),
                    }
                ]
            }
            if "text" in n_item:
                beat_dict["text"] = n_item["text"]

            current_beats.append(beat_dict)
            current_m_ticks += dur_ticks

        if current_beats:
            measures_data.append({"beats": current_beats})

        return self.write_measures(track_number, start_measure, measures_data)

    def add_chord_progression(
        self,
        track_number: int,
        start_measure: int,
        progression: List[str],
        strum_pattern: str = "down_down_up_down_up"
    ) -> Dict[str, Any]:
        """Fills measures with chords following a strumming rhythm pattern."""
        pattern = STRUM_PATTERNS.get(strum_pattern, STRUM_PATTERNS["down_down_up_down_up"])
        measures_data: List[Dict[str, Any]] = []

        for ch_name in progression:
            c_dict = get_chord(ch_name)
            if not c_dict:
                # Fallback chord
                c_dict = {"name": ch_name, "first_fret": 1, "strings": [0, 0, 0, 0, 0, 0]}

            chord_beats: List[Dict[str, Any]] = []
            for pat_step in pattern:
                dur = pat_step["duration"]
                stroke = pat_step.get("stroke")
                is_pm = pat_step.get("palm_mute", False)

                notes: List[Dict[str, Any]] = []
                for s_idx, f_val in enumerate(c_dict["strings"]):
                    if f_val >= 0:
                        notes.append({
                            "string": s_idx + 1,
                            "fret": f_val,
                            "palmMute": is_pm
                        })

                chord_beats.append({
                    "duration": dur,
                    "chord": c_dict,
                    "stroke": stroke,
                    "notes": notes,
                })

            measures_data.append({
                "marker": ch_name,
                "beats": chord_beats
            })

        return self.write_measures(track_number, start_measure, measures_data)

    def transpose(self, track_number: int = 0, semitones: int = 2) -> Dict[str, Any]:
        """Transposes notes by semitones. track_number=0 transposes all tracks."""
        tracks_to_process = self.song.tracks if track_number == 0 else [self.song.tracks[track_number - 1]]
        notes_modified = 0

        for trk in tracks_to_process:
            for m in trk.measures:
                for b in m.beats:
                    # Transpose chord frets if present
                    if b.chord and b.chord.strings:
                        new_c_strings = []
                        for f in b.chord.strings:
                            if f >= 0:
                                new_c_strings.append(max(0, min(24, f + semitones)))
                            else:
                                new_c_strings.append(-1)
                        b.chord.strings = new_c_strings

                    # Transpose notes
                    for n in b.notes:
                        if n.fret >= 0:
                            n.fret = max(0, min(trk.fret_count, n.fret + semitones))
                            notes_modified += 1

        return {
            "success": True,
            "semitones": semitones,
            "notes_modified": notes_modified,
            "tracks_processed": len(tracks_to_process),
        }

    def set_marker(self, measure_number: int, title: str) -> bool:
        if not self.song.tracks:
            return False
        self.ensure_measure_count(measure_number)
        m_idx = measure_number - 1
        for trk in self.song.tracks:
            if m_idx < len(trk.measures):
                trk.measures[m_idx].marker = title
        return True

    def set_tempo(self, measure_number: int, tempo: int) -> bool:
        if not self.song.tracks:
            return False
        self.ensure_measure_count(measure_number)
        m_idx = measure_number - 1
        for trk in self.song.tracks:
            if m_idx < len(trk.measures):
                trk.measures[m_idx].tempo = tempo
        if measure_number == 1:
            self.song.tempo = tempo
        return True

    def set_time_signature(self, measure_number: int, num: int, den: int) -> bool:
        if not self.song.tracks:
            return False
        self.ensure_measure_count(measure_number)
        m_idx = measure_number - 1
        ts_str = f"{num}/{den}"
        for trk in self.song.tracks:
            if m_idx < len(trk.measures):
                trk.measures[m_idx].time_signature = ts_str
        if measure_number == 1:
            self.song.time_signature = ts_str
        return True
