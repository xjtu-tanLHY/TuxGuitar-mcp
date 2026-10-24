from __future__ import annotations
import zipfile
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Optional, Dict, Any

from .models import (
    SongData, TrackData, MeasureData, BeatData, NoteData, NoteEffectData, ChordData,
    DURATION_VALUES, VALUE_TO_DURATION, TUNING_PRESETS
)

TG_QUARTER_TICKS = 2882880  # TuxGuitar standard precise ticks for a quarter note
TG_START_OFFSET = 2882880   # TuxGuitar start offset for measure 1


def parse_tg(file_path: str) -> SongData:
    with zipfile.ZipFile(file_path, "r") as z:
        xml_bytes = z.read("content.xml")
    
    root = ET.fromstring(xml_bytes)
    song_el = root.find("TGSong")
    if song_el is None:
        raise ValueError(f"Invalid TuxGuitar file: missing <TGSong> root in {file_path}")

    song = SongData(
        title=song_el.findtext("name", "") or "Untitled",
        artist=song_el.findtext("artist", "") or "",
        album=song_el.findtext("album", "") or "",
        author=song_el.findtext("author", "") or "",
        copyright=song_el.findtext("copyright", "") or "",
        comments=song_el.findtext("comments", "") or "",
    )

    # Parse Measure Headers (time signatures, tempos, markers)
    headers = song_el.findall("TGMeasureHeader")
    measure_headers_info: List[Dict[str, Any]] = []
    default_tempo = 120
    default_ts = "4/4"

    for h in headers:
        info: Dict[str, Any] = {}
        ts_el = h.find("timeSignature")
        if ts_el is not None:
            num = ts_el.attrib.get("numerator", "4")
            den = ts_el.attrib.get("denominator", "4")
            info["time_signature"] = f"{num}/{den}"
        else:
            info["time_signature"] = default_ts

        tempo_text = h.findtext("tempo")
        if tempo_text:
            try:
                info["tempo"] = int(tempo_text)
                default_tempo = info["tempo"]
            except ValueError:
                pass
        
        marker_el = h.find("marker")
        if marker_el is not None:
            info["marker"] = marker_el.findtext("title", "")
        
        measure_headers_info.append(info)

    if measure_headers_info:
        song.tempo = measure_headers_info[0].get("tempo", default_tempo)
        song.time_signature = measure_headers_info[0].get("time_signature", default_ts)

    # Parse Tracks
    track_els = song_el.findall("TGTrack")
    for t_idx, t_el in enumerate(track_els):
        t_name = t_el.findtext("name", f"Track {t_idx + 1}")
        try:
            channel_id = int(t_el.findtext("channelId", "1"))
        except ValueError:
            channel_id = 1
        
        strings = [int(s.text) for s in t_el.findall("TGString") if s.text]
        if not strings:
            strings = list(TUNING_PRESETS["standard_6"])
        
        color_el = t_el.find("color")
        color = (255, 0, 0)
        if color_el is not None:
            try:
                r = int(color_el.attrib.get("R", "255"))
                g = int(color_el.attrib.get("G", "0"))
                b = int(color_el.attrib.get("B", "0"))
                color = (r, g, b)
            except ValueError:
                pass

        track = TrackData(
            number=t_idx + 1,
            name=t_name,
            channel=channel_id,
            strings=strings,
            color=color,
        )

        # Measures in track
        measure_els = t_el.findall("TGMeasure")
        for m_idx, m_el in enumerate(measure_els):
            m_info = measure_headers_info[m_idx] if m_idx < len(measure_headers_info) else {}
            measure = MeasureData(
                number=m_idx + 1,
                time_signature=m_info.get("time_signature", "4/4"),
                tempo=m_info.get("tempo"),
                marker=m_info.get("marker"),
                clef=m_el.findtext("clef", "treble"),
            )

            beat_els = m_el.findall("TGBeat")
            for b_el in beat_els:
                beat = BeatData()
                
                # Check chord
                chord_el = b_el.find("chord")
                if chord_el is not None:
                    c_name = chord_el.attrib.get("name", "")
                    try:
                        c_first_fret = int(chord_el.attrib.get("firstFret", "1"))
                    except ValueError:
                        c_first_fret = 1
                    
                    c_strings = [-1] * len(strings)
                    for f_el in chord_el.findall("fret"):
                        try:
                            s_num = int(f_el.attrib.get("string", "1")) - 1
                            f_val = int(f_el.attrib.get("value", "-1"))
                            if 0 <= s_num < len(c_strings):
                                c_strings[s_num] = f_val
                        except ValueError:
                            pass
                    beat.chord = ChordData(name=c_name, first_fret=c_first_fret, strings=c_strings)

                # Text / stroke
                text_el = b_el.find("text")
                if text_el is not None and text_el.text:
                    beat.text = text_el.text

                # Voices
                voice_els = b_el.findall("voice")
                for v_el in voice_els:
                    if v_el.attrib.get("empty") == "true":
                        continue
                    
                    dur_el = v_el.find("duration")
                    if dur_el is not None:
                        try:
                            d_val = int(dur_el.attrib.get("value", "4"))
                            beat.duration = VALUE_TO_DURATION.get(d_val, "quarter")
                            beat.dotted = dur_el.attrib.get("dotted") == "true"
                        except ValueError:
                            beat.duration = "quarter"

                    for n_el in v_el.findall("note"):
                        try:
                            s_num = int(n_el.attrib.get("string", "1"))
                            f_val = int(n_el.attrib.get("value", "0"))
                            vel = int(n_el.attrib.get("velocity", "95"))
                        except ValueError:
                            continue

                        eff = NoteEffectData()
                        if n_el.find("hammer") is not None:
                            eff.hammer = True
                        if n_el.find("vibrato") is not None:
                            eff.vibrato = True
                        if n_el.find("palmMute") is not None:
                            eff.palmMute = True
                        if n_el.find("ghostNote") is not None:
                            eff.ghostNote = True
                        if n_el.find("deadNote") is not None:
                            eff.deadNote = True
                        if n_el.find("letRing") is not None:
                            eff.letRing = True
                        if n_el.find("staccato") is not None:
                            eff.staccato = True
                        if n_el.find("slide") is not None:
                            eff.slide = n_el.find("slide").attrib.get("type", "shift")
                        
                        bend_el = n_el.find("bend")
                        if bend_el is not None:
                            eff.bend_semitones = 2.0

                        beat.notes.append(NoteData(string=s_num, fret=f_val, velocity=vel, effect=eff))

                measure.beats.append(beat)

            track.measures.append(measure)

        song.tracks.append(track)

    return song


def write_tg(song: SongData, file_path: str) -> None:
    root = ET.Element("TuxGuitarFile")
    ET.SubElement(root, "TGVersion", major="1", minor="6", revision="6")
    
    song_el = ET.SubElement(root, "TGSong")
    ET.SubElement(song_el, "name").text = song.title
    ET.SubElement(song_el, "artist").text = song.artist
    ET.SubElement(song_el, "album").text = song.album
    ET.SubElement(song_el, "author").text = song.author
    ET.SubElement(song_el, "date").text = ""
    ET.SubElement(song_el, "copyright").text = song.copyright
    ET.SubElement(song_el, "writer").text = ""
    ET.SubElement(song_el, "transcriber").text = ""
    ET.SubElement(song_el, "comments").text = song.comments

    # TGChannels
    # Map channels
    used_channels: Dict[int, TrackData] = {}
    for t in song.tracks:
        used_channels[t.channel or 1] = t

    for ch_id, trk in used_channels.items():
        ch_el = ET.SubElement(song_el, "TGChannel")
        ET.SubElement(ch_el, "id").text = str(ch_id)
        ET.SubElement(ch_el, "bank").text = "0"
        ET.SubElement(ch_el, "program").text = str(trk.instrument)
        ET.SubElement(ch_el, "volume").text = "127"
        ET.SubElement(ch_el, "balance").text = "64"
        ET.SubElement(ch_el, "chorus").text = "0"
        ET.SubElement(ch_el, "reverb").text = "0"
        ET.SubElement(ch_el, "phaser").text = "0"
        ET.SubElement(ch_el, "tremolo").text = "0"
        ET.SubElement(ch_el, "name").text = trk.name

    total_measures = song.measure_count
    if total_measures == 0 and song.tracks:
        total_measures = 1

    # Measure Headers
    for m_idx in range(total_measures):
        h_el = ET.SubElement(song_el, "TGMeasureHeader")
        
        # Get ts and tempo from tracks if available
        ts_str = song.time_signature
        tempo_val = song.tempo
        marker_text = None

        if song.tracks and m_idx < len(song.tracks[0].measures):
            m = song.tracks[0].measures[m_idx]
            if m.time_signature:
                ts_str = m.time_signature
            if m.tempo is not None:
                tempo_val = m.tempo
            if m.marker:
                marker_text = m.marker

        parts = ts_str.split("/")
        num = parts[0] if len(parts) == 2 else "4"
        den = parts[1] if len(parts) == 2 else "4"

        ET.SubElement(h_el, "timeSignature", numerator=num, denominator=den)
        ET.SubElement(h_el, "tempo").text = str(tempo_val)
        if marker_text:
            m_node = ET.SubElement(h_el, "marker")
            ET.SubElement(m_node, "title").text = marker_text

    # Tracks
    measure_start_tick = TG_START_OFFSET
    for trk in song.tracks:
        trk_el = ET.SubElement(song_el, "TGTrack", maxFret=str(trk.fret_count))
        ET.SubElement(trk_el, "name").text = trk.name
        ET.SubElement(trk_el, "channelId").text = str(trk.channel or 1)
        r, g, b = trk.color
        ET.SubElement(trk_el, "color", R=str(r), G=str(g), B=str(b))
        
        for s_val in trk.strings:
            ET.SubElement(trk_el, "TGString").text = str(s_val)

        curr_tick = TG_START_OFFSET
        for m_idx, m in enumerate(trk.measures):
            m_el = ET.SubElement(trk_el, "TGMeasure")
            ET.SubElement(m_el, "clef").text = m.clef or "treble"
            ET.SubElement(m_el, "keySignature").text = str(m.key_signature)

            for b in m.beats:
                b_el = ET.SubElement(m_el, "TGBeat")
                ET.SubElement(b_el, "preciseStart").text = str(curr_tick)

                if b.chord:
                    c_el = ET.SubElement(b_el, "chord", firstFret=str(b.chord.first_fret), name=b.chord.name)
                    for s_i, f_val in enumerate(b.chord.strings):
                        if f_val >= 0:
                            ET.SubElement(c_el, "fret", string=str(s_i + 1), value=str(f_val))

                if b.text:
                    ET.SubElement(b_el, "text").text = b.text

                # Voice
                v_el = ET.SubElement(b_el, "voice", empty="false" if b.notes else "true")
                d_val = DURATION_VALUES.get(b.duration, 4)
                dur_attrs = {"value": str(d_val)}
                if b.dotted:
                    dur_attrs["dotted"] = "true"
                dur_node = ET.SubElement(v_el, "duration", **dur_attrs)
                ET.SubElement(dur_node, "divisionType", enters=str(b.tuplet_enters), times=str(b.tuplet_times))

                for n in b.notes:
                    n_el = ET.SubElement(v_el, "note", string=str(n.string), value=str(n.fret), velocity=str(n.velocity))
                    eff = n.effect
                    if eff.hammer:
                        ET.SubElement(n_el, "hammer")
                    if eff.vibrato:
                        ET.SubElement(n_el, "vibrato")
                    if eff.palmMute:
                        ET.SubElement(n_el, "palmMute")
                    if eff.ghostNote:
                        ET.SubElement(n_el, "ghostNote")
                    if eff.deadNote:
                        ET.SubElement(n_el, "deadNote")
                    if eff.letRing:
                        ET.SubElement(n_el, "letRing")
                    if eff.staccato:
                        ET.SubElement(n_el, "staccato")
                    if eff.slide:
                        ET.SubElement(n_el, "slide", type=eff.slide)
                    if eff.bend_semitones:
                        bend_node = ET.SubElement(n_el, "bend")
                        ET.SubElement(bend_node, "point", position="0", value="0")
                        ET.SubElement(bend_node, "point", position="6", value=str(int(eff.bend_semitones)))
                        ET.SubElement(bend_node, "point", position="12", value=str(int(eff.bend_semitones)))

                # Add dummy empty second voice for TuxGuitar compatibility
                v2_el = ET.SubElement(b_el, "voice", empty="true")
                dur2 = ET.SubElement(v2_el, "duration", value="4")
                ET.SubElement(dur2, "divisionType", enters="1", times="1")

                # Advance tick
                quarter_fraction = 4.0 / d_val
                if b.dotted:
                    quarter_fraction *= 1.5
                curr_tick += int(TG_QUARTER_TICKS * quarter_fraction)

    # Convert to XML string
    rough_str = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough_str)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8")

    # Write Zip
    with zipfile.ZipFile(file_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("version.txt", "TuxGuitar_file_format 2.0\n")
        z.writestr("content.xml", pretty_xml)
