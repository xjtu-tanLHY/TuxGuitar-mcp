from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any

# Standard MIDI tuning values (String 1 high -> String N low)
TUNING_PRESETS: Dict[str, List[int]] = {
    "standard_6": [64, 59, 55, 50, 45, 40],        # E4, B3, G3, D3, A2, E2
    "drop_d": [64, 59, 55, 50, 45, 38],            # E4, B3, G3, D3, A2, D2
    "dadgad": [62, 57, 55, 50, 45, 38],            # D4, A3, G3, D3, A2, D2
    "open_d": [62, 57, 54, 50, 45, 38],            # D4, A3, F#3, D3, A2, D2
    "open_g": [62, 59, 55, 50, 43, 38],            # D4, B3, G3, D3, G2, D2
    "half_step_down": [63, 58, 54, 49, 44, 39],    # Eb4, Bb3, Gb3, Db3, Ab2, Eb2
    "full_step_down": [62, 57, 53, 48, 43, 38],    # D4, A3, F3, C3, G2, D2
    "7_string_standard": [64, 59, 55, 50, 45, 40, 35], # E4, B3, G3, D3, A2, E2, B1
    "bass_4_standard": [43, 38, 33, 28],           # G2, D2, A1, E1
    "bass_5_standard": [43, 38, 33, 28, 23],       # G2, D2, A1, E1, B0
}

# Common General MIDI instruments
MIDI_INSTRUMENTS: Dict[str, int] = {
    "acoustic_nylon": 24,
    "acoustic_steel": 25,
    "electric_jazz": 26,
    "electric_clean": 27,
    "electric_muted": 28,
    "overdriven_guitar": 29,
    "distortion_guitar": 30,
    "guitar_harmonics": 31,
    "acoustic_bass": 32,
    "electric_bass_finger": 33,
    "electric_bass_pick": 34,
    "fretless_bass": 35,
    "slap_bass_1": 36,
    "slap_bass_2": 37,
    "synth_bass_1": 38,
    "acoustic_grand_piano": 0,
    "bright_acoustic_piano": 1,
    "string_ensemble": 48,
    "standard_drums": 0, # on channel 9 (10 in 1-based)
}

# Note duration mapping to standard fractions / ticks (960 ticks = quarter note)
DURATION_TICKS: Dict[str, int] = {
    "whole": 3840,
    "half": 1920,
    "quarter": 960,
    "eighth": 480,
    "16th": 240,
    "32nd": 120,
    "64th": 60,
}

DURATION_VALUES: Dict[str, int] = {
    "whole": 1,
    "half": 2,
    "quarter": 4,
    "eighth": 8,
    "16th": 16,
    "32nd": 32,
    "64th": 64,
}

VALUE_TO_DURATION: Dict[int, str] = {v: k for k, v in DURATION_VALUES.items()}


@dataclass
class NoteEffectData:
    hammer: bool = False
    slide: Optional[str] = None  # "shift", "legato", "out_down", "out_up", "into_below", "into_above"
    bend_semitones: Optional[float] = None  # e.g. 1.0 (half step), 2.0 (full step)
    vibrato: bool = False
    palmMute: bool = False
    ghostNote: bool = False
    deadNote: bool = False
    accentuated: bool = False
    heavyAccentuated: bool = False
    letRing: bool = False
    staccato: bool = False
    harmonic: Optional[str] = None  # "natural", "artificial", "pinch", "tap"


@dataclass
class NoteData:
    string: int  # 1-based, 1=highest pitch (high E on guitar)
    fret: int    # 0=open, 1..30=fret, -1=dead note
    velocity: int = 95
    effect: NoteEffectData = field(default_factory=NoteEffectData)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "string": self.string,
            "fret": self.fret,
            "velocity": self.velocity,
        }
        eff = {}
        for k, v in self.effect.__dict__.items():
            if v:
                eff[k] = v
        if eff:
            d["effect"] = eff
        return d


@dataclass
class ChordData:
    name: str
    first_fret: int = 1
    # strings: fret per string from String 1 (high E) to String N (low E), -1 means muted/unplayed
    strings: List[int] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "first_fret": self.first_fret,
            "strings": self.strings,
        }


@dataclass
class BeatData:
    duration: str = "quarter"  # "whole", "half", "quarter", "eighth", "16th", "32nd"
    dotted: bool = False
    tuplet_enters: int = 1     # 3 for triplet
    tuplet_times: int = 1      # 2 for triplet
    notes: List[NoteData] = field(default_factory=list)
    chord: Optional[ChordData] = None
    text: Optional[str] = None
    stroke: Optional[str] = None  # "down", "up"

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {
            "duration": self.duration,
            "dotted": self.dotted,
            "notes": [n.to_dict() for n in self.notes],
        }
        if self.tuplet_enters != 1 or self.tuplet_times != 1:
            res["tuplet"] = f"{self.tuplet_enters}:{self.tuplet_times}"
        if self.chord:
            res["chord"] = self.chord.to_dict()
        if self.text:
            res["text"] = self.text
        if self.stroke:
            res["stroke"] = self.stroke
        return res


@dataclass
class MeasureData:
    number: int  # 1-based index
    time_signature: str = "4/4"
    tempo: Optional[int] = None
    marker: Optional[str] = None
    clef: str = "treble"
    key_signature: int = 0
    beats: List[BeatData] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {
            "number": self.number,
            "time_signature": self.time_signature,
        }
        if self.tempo is not None:
            res["tempo"] = self.tempo
        if self.marker:
            res["marker"] = self.marker
        res["beats"] = [b.to_dict() for b in self.beats]
        return res


@dataclass
class TrackData:
    number: int  # 1-based index
    name: str
    instrument: int = 27  # MIDI program number
    channel: int = 0
    strings: List[int] = field(default_factory=lambda: list(TUNING_PRESETS["standard_6"]))
    fret_count: int = 24
    color: Tuple[int, int, int] = (255, 0, 0)
    is_percussion: bool = False
    is_mute: bool = False
    is_solo: bool = False
    measures: List[MeasureData] = field(default_factory=list)

    def to_dict(self, include_measures: bool = True) -> Dict[str, Any]:
        res: Dict[str, Any] = {
            "number": self.number,
            "name": self.name,
            "instrument": self.instrument,
            "channel": self.channel,
            "strings_count": len(self.strings),
            "tuning": self.strings,
            "fret_count": self.fret_count,
            "is_percussion": self.is_percussion,
            "is_mute": self.is_mute,
            "is_solo": self.is_solo,
            "measure_count": len(self.measures),
        }
        if include_measures:
            res["measures"] = [m.to_dict() for m in self.measures]
        return res


@dataclass
class SongData:
    title: str = "Untitled"
    artist: str = ""
    album: str = ""
    author: str = ""
    copyright: str = ""
    comments: str = ""
    tempo: int = 120
    time_signature: str = "4/4"
    tracks: List[TrackData] = field(default_factory=list)

    @property
    def measure_count(self) -> int:
        if not self.tracks:
            return 0
        return max(len(t.measures) for t in self.tracks)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "author": self.author,
            "tempo": self.tempo,
            "time_signature": self.time_signature,
            "total_measures": self.measure_count,
            "tracks": [t.to_dict(include_measures=False) for t in self.tracks],
        }
