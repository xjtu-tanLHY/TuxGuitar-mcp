from __future__ import annotations
import guitarpro
from typing import List, Optional, Dict, Any

from .models import (
    SongData, TrackData, MeasureData, BeatData, NoteData, NoteEffectData, ChordData,
    DURATION_VALUES, VALUE_TO_DURATION, TUNING_PRESETS
)


def gp_duration_to_name(val: int) -> str:
    return VALUE_TO_DURATION.get(val, "quarter")


def name_to_gp_duration(name: str) -> int:
    return DURATION_VALUES.get(name, 4)


def parse_gp(file_path: str) -> SongData:
    try:
        gp_song = guitarpro.parse(file_path, encoding="utf-8")
    except Exception:
        gp_song = guitarpro.parse(file_path)
    
    song = SongData(
        title=gp_song.title or "Untitled",
        artist=gp_song.artist or "",
        album=gp_song.album or "",
        author=gp_song.words or gp_song.music or "",
        copyright=gp_song.copyright or "",
        comments=gp_song.notice or "",
        tempo=gp_song.tempo or 120,
    )

    if gp_song.tracks and gp_song.tracks[0].measures:
        first_m = gp_song.tracks[0].measures[0]
        ts = first_m.timeSignature
        song.time_signature = f"{ts.numerator}/{ts.denominator.value}"

    for t_idx, gp_track in enumerate(gp_song.tracks):
        # Strings are stored in gp_track.strings: 1=highest pitch (high E)
        strings_tuning = [s.value for s in gp_track.strings]
        color = (gp_track.color.r, gp_track.color.g, gp_track.color.b) if gp_track.color else (255, 0, 0)
        
        track = TrackData(
            number=t_idx + 1,
            name=gp_track.name or f"Track {t_idx + 1}",
            instrument=gp_track.channel.instrument if gp_track.channel else 27,
            channel=gp_track.channel.channel if gp_track.channel else 0,
            strings=strings_tuning,
            fret_count=gp_track.fretCount or 24,
            color=color,
            is_percussion=gp_track.isPercussionTrack,
            is_mute=gp_track.isMute,
            is_solo=gp_track.isSolo,
        )

        for m_idx, gp_measure in enumerate(gp_track.measures):
            ts = gp_measure.timeSignature
            ts_str = f"{ts.numerator}/{ts.denominator.value}" if ts else song.time_signature
            marker_str = gp_measure.marker.title if gp_measure.marker else None

            measure = MeasureData(
                number=m_idx + 1,
                time_signature=ts_str,
                tempo=song.tempo,
                marker=marker_str,
            )

            # Look at voice 0 (lead/main voice)
            if gp_measure.voices:
                gp_voice = gp_measure.voices[0]
                for gp_beat in gp_voice.beats:
                    t_enters = gp_beat.duration.tuplet.enters if gp_beat.duration and gp_beat.duration.tuplet else 1
                    t_times = gp_beat.duration.tuplet.times if gp_beat.duration and gp_beat.duration.tuplet else 1
                    beat = BeatData(
                        duration=gp_duration_to_name(gp_beat.duration.value),
                        dotted=gp_beat.duration.isDotted,
                        tuplet_enters=t_enters,
                        tuplet_times=t_times,
                        text=gp_beat.text,
                    )

                    # Chord
                    if gp_beat.effect and gp_beat.effect.chord:
                        ch = gp_beat.effect.chord
                        c_strings = list(ch.strings[:len(strings_tuning)]) if ch.strings else [-1] * len(strings_tuning)
                        beat.chord = ChordData(
                            name=ch.name or "",
                            first_fret=ch.firstFret or 1,
                            strings=c_strings
                        )

                    for gp_note in gp_beat.notes:
                        eff = NoteEffectData()
                        if gp_note.effect:
                            ne = gp_note.effect
                            eff.hammer = ne.hammer
                            eff.vibrato = ne.vibrato
                            eff.palmMute = ne.palmMute
                            eff.ghostNote = ne.ghostNote
                            eff.deadNote = (gp_note.type == guitarpro.NoteType.dead) if hasattr(guitarpro, 'NoteType') else False
                            eff.accentuated = ne.accentuatedNote
                            eff.heavyAccentuated = ne.heavyAccentuatedNote
                            eff.letRing = ne.letRing
                            eff.staccato = ne.staccato
                            if ne.slides:
                                eff.slide = str(ne.slides[0].name) if hasattr(ne.slides[0], 'name') else "slide"
                            if ne.bend and ne.bend.points:
                                # Maximum bend point height
                                max_p = max((p.value for p in ne.bend.points), default=0)
                                eff.bend_semitones = float(max_p)

                        note = NoteData(
                            string=gp_note.string,
                            fret=gp_note.value,
                            velocity=gp_note.velocity or 95,
                            effect=eff
                        )
                        beat.notes.append(note)

                    measure.beats.append(beat)

            track.measures.append(measure)

        song.tracks.append(track)

    return song


def write_gp(song: SongData, file_path: str) -> None:
    gp_song = guitarpro.Song()
    gp_song.title = song.title
    gp_song.artist = song.artist
    gp_song.album = song.album
    gp_song.words = song.author
    gp_song.copyright = song.copyright
    gp_song.notice = song.comments
    gp_song.tempo = song.tempo

    # Prepare tracks
    # Remove default track 0
    gp_song.tracks.clear()
    gp_song.measureHeaders.clear()

    total_measures = song.measure_count
    if total_measures == 0:
        total_measures = 1

    # Create measure headers for the song
    for m_idx in range(total_measures):
        header = guitarpro.MeasureHeader()
        header.number = m_idx + 1
        
        # Default ts & tempo
        ts_str = song.time_signature
        tempo_val = song.tempo
        marker_title = None

        if song.tracks and m_idx < len(song.tracks[0].measures):
            m = song.tracks[0].measures[m_idx]
            if m.time_signature:
                ts_str = m.time_signature
            if m.tempo is not None:
                tempo_val = m.tempo
            if m.marker:
                marker_title = m.marker

        num, den = 4, 4
        parts = ts_str.split("/")
        if len(parts) == 2:
            try:
                num = int(parts[0])
                den = int(parts[1])
            except ValueError:
                pass

        header.timeSignature.numerator = num
        header.timeSignature.denominator.value = den
        if marker_title:
            header.marker = guitarpro.Marker()
            header.marker.title = marker_title
            header.marker.color = guitarpro.Color(255, 0, 0)

        gp_song.addMeasureHeader(header)

    # Add tracks
    for t_idx, trk in enumerate(song.tracks):
        gp_track = guitarpro.Track(gp_song)
        gp_track.number = t_idx + 1
        gp_track.name = trk.name
        gp_track.fretCount = trk.fret_count
        r, g, b = trk.color
        gp_track.color = guitarpro.Color(r, g, b)
        
        # Strings
        gp_track.strings.clear()
        for s_idx, s_val in enumerate(trk.strings):
            g_str = guitarpro.GuitarString(s_idx + 1, s_val)
            gp_track.strings.append(g_str)

        # Channel
        channel = guitarpro.MidiChannel()
        channel.channel = trk.channel
        channel.program = trk.instrument
        channel.volume = 127
        channel.balance = 64
        gp_track.channel = channel

        # Populate measures
        gp_track.measures.clear()
        for m_idx in range(total_measures):
            header = gp_song.measureHeaders[m_idx]
            gp_measure = guitarpro.Measure(gp_track, header)
            
            # Voice 0
            gp_voice = gp_measure.voices[0]
            
            # Check if track has this measure
            if m_idx < len(trk.measures):
                m_data = trk.measures[m_idx]
                for b_data in m_data.beats:
                    beat = guitarpro.Beat(gp_voice)
                    dur_val = name_to_gp_duration(b_data.duration)
                    beat.duration.value = dur_val
                    beat.duration.isDotted = b_data.dotted
                    if b_data.tuplet_enters and b_data.tuplet_enters != 1:
                        beat.duration.tuplet.enters = b_data.tuplet_enters
                        beat.duration.tuplet.times = b_data.tuplet_times
                    if b_data.text:
                        beat.text = b_data.text
                    
                    # Chord
                    if b_data.chord:
                        c = guitarpro.Chord(length=len(trk.strings))
                        c.name = b_data.chord.name
                        c.firstFret = b_data.chord.first_fret or 1
                        chord_strings = list(b_data.chord.strings)
                        while len(chord_strings) < len(trk.strings):
                            chord_strings.append(-1)
                        c.strings = chord_strings
                        beat.effect.chord = c

                    # Notes
                    for n_data in b_data.notes:
                        note = guitarpro.Note(beat)
                        note.string = n_data.string
                        note.value = max(0, n_data.fret) if n_data.fret >= 0 else 0
                        if n_data.fret < 0:
                            note.type = guitarpro.NoteType.dead
                        note.velocity = n_data.velocity

                        eff = n_data.effect
                        if eff.hammer:
                            note.effect.hammer = True
                        if eff.vibrato:
                            note.effect.vibrato = True
                        if eff.palmMute:
                            note.effect.palmMute = True
                        if eff.ghostNote:
                            note.effect.ghostNote = True
                        if eff.accentuated:
                            note.effect.accentuatedNote = True
                        if eff.heavyAccentuated:
                            note.effect.heavyAccentuatedNote = True
                        if eff.letRing:
                            note.effect.letRing = True
                        if eff.staccato:
                            note.effect.staccato = True
                        if eff.slide:
                            note.effect.slides.append(guitarpro.SlideType.shiftSlideTo)
                        if eff.bend_semitones:
                            bend = guitarpro.BendEffect()
                            bend.type = guitarpro.BendType.bend
                            bend.points.append(guitarpro.BendPoint(position=0, value=0))
                            bend.points.append(guitarpro.BendPoint(position=6, value=int(eff.bend_semitones)))
                            bend.points.append(guitarpro.BendPoint(position=12, value=int(eff.bend_semitones)))
                            note.effect.bend = bend

                        beat.notes.append(note)

                    gp_voice.beats.append(beat)

            # If voice has no beats, add an empty whole rest
            if not gp_voice.beats:
                rest_beat = guitarpro.Beat(gp_voice)
                rest_beat.status = guitarpro.BeatStatus.rest
                rest_beat.duration.value = guitarpro.Duration.whole
                gp_voice.beats.append(rest_beat)

            gp_track.measures.append(gp_measure)

        gp_song.tracks.append(gp_track)

    try:
        guitarpro.write(gp_song, file_path, encoding="utf-8")
    except Exception:
        guitarpro.write(gp_song, file_path)
