import os
from tuxguitar_mcp.song_editor import SongEditor
from tuxguitar_mcp.models import NoteData, NoteEffectData, BeatData, MeasureData, ChordData, TrackData
from tuxguitar_mcp.tg_parser import write_tg

def create_yu_ai_score():
    gp5_path = r"d:\Program Files\tuxguitar\yu_ai_sifeng.gp5"
    tg_path = r"d:\Program Files\tuxguitar\yu_ai_sifeng.tg"

    editor = SongEditor()
    editor.create_new(
        file_path=gp5_path,
        title="雨爱 (司凤版)",
        artist="金大洲 / 荒宣铭 / 席迅",
        tempo=162,
        time_signature="4/4",
        track_presets=[
            {
                "name": "民谣吉他 1 (主旋律)",
                "tuning": "standard_6",
                "instrument": "acoustic_steel"
            },
            {
                "name": "民谣吉他 2 (和弦伴奏)",
                "tuning": "standard_6",
                "instrument": "acoustic_steel"
            },
            {
                "name": "贝斯 (低音)",
                "tuning": "bass_4_standard",
                "instrument": "electric_bass_finger"
            }
        ]
    )

    # -------------------------------------------------------------
    # TRACK 1: 民谣吉他 1 (主旋律 / Lead Melody)
    # -------------------------------------------------------------
    track1_measures = []

    # Measure 1: 前奏长音 "嗯"
    track1_measures.append({
        "marker": "Intro (沙哑慵懒)",
        "beats": [
            {
                "duration": "whole",
                "text": "嗯~",
                "notes": [
                    {"string": 3, "fret": 4, "vibrato": True, "letRing": True} # B3
                ]
            }
        ]
    })

    # Measure 2: 哒啦嗯哒嗯哒嗯 (shuffle 3:2)
    # 5 5 6 5 7/1 5 6 5 -> B3 B3, C#4 B3, E4 B3, C#4 B3
    track1_measures.append({
        "beats": [
            # Beat 1: B3 (quarter), B3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "哒", "notes": [{"string": 3, "fret": 4}]},
            # Beat 2: C#4 (quarter), B3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "啦", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "嗯", "notes": [{"string": 3, "fret": 4}]},
            # Beat 3: E4 (quarter, grace 7/1), B3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哒", "notes": [{"string": 1, "fret": 0, "hammer": True}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "嗯", "notes": [{"string": 3, "fret": 4}]},
            # Beat 4: C#4 (quarter), B3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哒", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "嗯", "notes": [{"string": 3, "fret": 4}]}
        ]
    })

    # Measure 3: 哆啰哆啰哆啰哆啰 (shuffle 3:2)
    # 3 5. 3 2 1 6. 5. 6. -> G#3 B2, G#3 F#3, E3 C#3, B2 C#3
    track1_measures.append({
        "beats": [
            # Beat 1: G#3 (quarter), B2 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 5, "fret": 2}]},
            # Beat 2: G#3 (quarter), F#3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 4, "fret": 4}]},
            # Beat 3: E3 (quarter), C#3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 4, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 5, "fret": 4}]},
            # Beat 4: B2 (quarter), C#3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 5, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 5, "fret": 4}]}
        ]
    })

    # Measure 4: 嗯 - 暴 暴 暴 (三连暴 ff)
    # 1 (quarter), rest+1' (ff), rest+1' (ff), rest+1' (ff)
    track1_measures.append({
        "marker": "三连暴 (ff 丹田发力)",
        "beats": [
            # Beat 1: E3 quarter
            {"duration": "quarter", "text": "嗯", "notes": [{"string": 4, "fret": 2}]},
            # Beat 2: rest + E4 accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []}, # rest
            {"duration": "eighth", "tuplet": "3:2", "text": "暴!", "notes": [{"string": 1, "fret": 0, "heavyAccentuated": True, "staccato": True}]},
            # Beat 3: rest + E4 accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []}, # rest
            {"duration": "eighth", "tuplet": "3:2", "text": "暴!", "notes": [{"string": 1, "fret": 0, "heavyAccentuated": True, "staccato": True}]},
            # Beat 4: rest + E4 accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []}, # rest
            {"duration": "eighth", "tuplet": "3:2", "text": "暴!", "notes": [{"string": 1, "fret": 0, "heavyAccentuated": True, "staccato": True}]}
        ]
    })

    # Measure 5: 哆咯咯咯噶啦嘚嗯 (mp < f)
    # 1 1 1 1 3 5 6 5 -> E3 E3, E3 E3, G#3 B3, C#4 B3
    track1_measures.append({
        "beats": [
            # Beat 1: E3 (quarter), E3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 4, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "咯", "notes": [{"string": 4, "fret": 2}]},
            # Beat 2: E3 (quarter), E3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "咯", "notes": [{"string": 4, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "咯", "notes": [{"string": 4, "fret": 2}]},
            # Beat 3: G#3 (quarter), B3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "噶", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啦", "notes": [{"string": 3, "fret": 4}]},
            # Beat 4: C#4 (quarter), B3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "嘚", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "嗯", "notes": [{"string": 3, "fret": 4}]}
        ]
    })

    # Measure 6: 嘚呦 - 暴 暴 (呼喊卖艺)
    # 1 6(eighth) ~ 6(quarter) - rest+1' - rest+1'
    track1_measures.append({
        "marker": "呼喊街头 (暴暴)",
        "beats": [
            # Beat 1: E3 (quarter), C#4 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "嘚", "notes": [{"string": 4, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "呦~", "notes": [{"string": 2, "fret": 2}]},
            # Beat 2: C#4 tied (quarter), rest (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 2, "fret": 2, "vibrato": True}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": []},
            # Beat 3: rest + E4 accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "text": "暴!", "notes": [{"string": 1, "fret": 0, "heavyAccentuated": True, "staccato": True}]},
            # Beat 4: rest + E4 accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "text": "暴!", "notes": [{"string": 1, "fret": 0, "heavyAccentuated": True, "staccato": True}]}
        ]
    })

    # Measure 7: 8va 哆哆啰哆啰哆啰嘚呕 (高低对比 瞬间懒散收回)
    # rest+6., 1 2, 3 2, 1 6. -> C#4, E4 F#4, G#4 F#4, E4 C#4
    track1_measures.append({
        "marker": "8va 对比收回",
        "beats": [
            # Beat 1: rest + C#4
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "text": "哆", "notes": [{"string": 2, "fret": 2}]},
            # Beat 2: E4 (quarter), F#4 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 1, "fret": 2}]},
            # Beat 3: G#4 (quarter), F#4 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 1, "fret": 4, "hammer": True}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 1, "fret": 2}]},
            # Beat 4: E4 (quarter), C#4 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "嘚", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "呕", "notes": [{"string": 2, "fret": 2}]}
        ]
    })

    # Measure 8: 呃哆啰 (三连音引出)
    # 1 6. rest - rest - 呃哆啰 (triplet 1 6. 1)
    track1_measures.append({
        "beats": [
            # Beat 1: E4 (quarter), C#4 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "嗯", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 2}]},
            # Beat 2: Quarter rest
            {"duration": "quarter", "notes": []},
            # Beat 3: Quarter rest
            {"duration": "quarter", "notes": []},
            # Beat 4: 呃哆啰 3连音
            {"duration": "eighth", "tuplet": "3:2", "text": "呃", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "哆", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # Measure 9: 哆啰哆啰哆呕 嗬哒(弹舌)
    # 3 4, #4 5, 3 1, 1.(eighth) + 5 5 5 (16th triplet trill)
    track1_measures.append({
        "marker": "弹舌连音 (轻快引出)",
        "beats": [
            # Beat 1: G#3 (quarter), A3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 3, "fret": 2}]},
            # Beat 2: A#3 (quarter), B3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 3, "fret": 3}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "啰", "notes": [{"string": 3, "fret": 4}]},
            # Beat 3: G#3 (quarter), E3 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "text": "哆", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "呕", "notes": [{"string": 4, "fret": 2}]},
            # Beat 4: E3 (eighth) + 弹舌三连音 B3
            {"duration": "eighth", "tuplet": "3:2", "text": "嗬", "notes": [{"string": 4, "fret": 2}]},
            {"duration": "16th", "tuplet": "3:2", "text": "哒(弹舌)", "notes": [{"string": 3, "fret": 4}]},
            {"duration": "16th", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            {"duration": "16th", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]}
        ]
    })

    # Measure 10: 郎吧崩吧崩吧崩吧 (四连崩吧 - 郎要轻)
    # B2 (string 5 fret 2) 全部 8 个 shuffle 音符
    track1_measures.append({
        "marker": "郎吧四连崩 (郎要轻)",
        "beats": [
            # Beat 1: 郎(轻) 吧
            {"duration": "quarter", "tuplet": "3:2", "text": "郎(轻)", "notes": [{"string": 5, "fret": 2, "velocity": 70}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "吧", "notes": [{"string": 5, "fret": 2, "velocity": 95}]},
            # Beat 2: 崩 吧
            {"duration": "quarter", "tuplet": "3:2", "text": "崩", "notes": [{"string": 5, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "吧", "notes": [{"string": 5, "fret": 2}]},
            # Beat 3: 崩 吧
            {"duration": "quarter", "tuplet": "3:2", "text": "崩", "notes": [{"string": 5, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "吧", "notes": [{"string": 5, "fret": 2}]},
            # Beat 4: 崩 吧
            {"duration": "quarter", "tuplet": "3:2", "text": "崩", "notes": [{"string": 5, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "吧", "notes": [{"string": 5, "fret": 2}]}
        ]
    })

    # Measure 11: 崩吧崩吧 嗷 (通透大滑音)
    # B2 B2, B2 B2, B4 -> High slide "嗷 (gliss.)"
    track1_measures.append({
        "marker": "通透嗷 (超强滑音高潮)",
        "beats": [
            # Beat 1: 崩 吧
            {"duration": "quarter", "tuplet": "3:2", "text": "崩", "notes": [{"string": 5, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "吧", "notes": [{"string": 5, "fret": 2}]},
            # Beat 2: 崩 吧
            {"duration": "quarter", "tuplet": "3:2", "text": "崩", "notes": [{"string": 5, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "text": "吧", "notes": [{"string": 5, "fret": 2}]},
            # Beat 3-4: 嗷! 超高音滑音 gliss. (Half note)
            {"duration": "half", "text": "嗷!! (gliss.)", "notes": [{"string": 1, "fret": 7, "slide": "out_up", "vibrato": True, "heavyAccentuated": True, "letRing": True}]}
        ]
    })

    editor.write_measures(track_number=1, start_measure=1, measures_data=track1_measures)


    # -------------------------------------------------------------
    # TRACK 2: 民谣吉他 2 (和弦伴奏 / Rhythm Acoustic Guitar)
    # -------------------------------------------------------------
    track2_measures = []

    # Emaj7: [0, 0, 1, 1, 2, 0] (High E to Low E: 1st=0, 2nd=0, 3rd=1, 4th=1, 5th=2, 6th=0)
    # E: [0, 0, 1, 2, 2, 0]
    # C#m: [4, 5, 6, 6, 4, -1]
    # A: [0, 2, 2, 2, 0, -1]
    # F#m7: [2, 2, 2, 2, 4, 2]
    # B7: [2, 0, 2, 1, 2, -1]
    # B: [2, 4, 4, 4, 2, -1]

    def make_chord_notes(fret_list):
        return [{"string": idx + 1, "fret": f} for idx, f in enumerate(fret_list) if f >= 0]

    def make_shuffle_strum_measure(chord_name, fret_list, dynamic="normal"):
        c_notes = make_chord_notes(fret_list)
        beats = []
        for beat_idx in range(4):
            beats.append({
                "duration": "quarter",
                "tuplet": "3:2",
                "chord": chord_name if beat_idx == 0 else None,
                "stroke": "down",
                "notes": c_notes
            })
            beats.append({
                "duration": "eighth",
                "tuplet": "3:2",
                "stroke": "up",
                "notes": [{"string": n["string"], "fret": n["fret"]} for n in c_notes if n["string"] <= 4] # higher strings on upstroke
            })
        return {"beats": beats}

    # Measure 1: Emaj7 慢速琶音/全音符扫弦
    track2_measures.append({
        "beats": [
            {
                "duration": "whole",
                "chord": "Emaj7",
                "stroke": "down",
                "notes": make_chord_notes([0, 0, 1, 1, 2, 0])
            }
        ]
    })

    # Measure 2: E 和弦 shuffle 摇摆扫弦
    track2_measures.append(make_shuffle_strum_measure("E", [0, 0, 1, 2, 2, 0]))

    # Measure 3: C#m 和弦 shuffle 扫弦
    track2_measures.append(make_shuffle_strum_measure("C#m", [4, 5, 6, 6, 4, -1]))

    # Measure 4: A 和弦 + 强拍切音制音 (暴暴暴)
    track2_measures.append({
        "beats": [
            # Beat 1: A chord down
            {"duration": "quarter", "chord": "A", "stroke": "down", "notes": make_chord_notes([0, 2, 2, 2, 0, -1])},
            # Beat 2: Rest + A chord choke/accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "down", "notes": [{"string": 2, "fret": 2, "heavyAccentuated": True}, {"string": 3, "fret": 2, "heavyAccentuated": True}, {"string": 4, "fret": 2, "heavyAccentuated": True}]},
            # Beat 3: Rest + A chord choke/accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "down", "notes": [{"string": 2, "fret": 2, "heavyAccentuated": True}, {"string": 3, "fret": 2, "heavyAccentuated": True}, {"string": 4, "fret": 2, "heavyAccentuated": True}]},
            # Beat 4: Rest + A chord choke/accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "down", "notes": [{"string": 2, "fret": 2, "heavyAccentuated": True}, {"string": 3, "fret": 2, "heavyAccentuated": True}, {"string": 4, "fret": 2, "heavyAccentuated": True}]}
        ]
    })

    # Measure 5: E 和弦渐强扫弦
    track2_measures.append(make_shuffle_strum_measure("E", [0, 0, 1, 2, 2, 0]))

    # Measure 6: C#m (前两拍) -> A 和弦两连暴 (后两拍)
    track2_measures.append({
        "beats": [
            # Beat 1: C#m quarter + eighth
            {"duration": "quarter", "tuplet": "3:2", "chord": "C#m", "stroke": "down", "notes": make_chord_notes([4, 5, 6, 6, 4, -1])},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "up", "notes": make_chord_notes([4, 5, 6, -1, -1, -1])},
            # Beat 2: C#m quarter + rest
            {"duration": "quarter", "tuplet": "3:2", "stroke": "down", "notes": make_chord_notes([4, 5, 6, 6, 4, -1])},
            {"duration": "eighth", "tuplet": "3:2", "notes": []},
            # Beat 3: rest + A choke
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "chord": "A", "stroke": "down", "notes": [{"string": 2, "fret": 2, "heavyAccentuated": True}, {"string": 3, "fret": 2, "heavyAccentuated": True}, {"string": 4, "fret": 2, "heavyAccentuated": True}]},
            # Beat 4: rest + A choke
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "down", "notes": [{"string": 2, "fret": 2, "heavyAccentuated": True}, {"string": 3, "fret": 2, "heavyAccentuated": True}, {"string": 4, "fret": 2, "heavyAccentuated": True}]}
        ]
    })

    # Measure 7: F#m7 细腻民谣扫弦
    track2_measures.append(make_shuffle_strum_measure("F#m7", [2, 2, 2, 2, 4, 2]))

    # Measure 8: B7 推动性进行
    track2_measures.append({
        "beats": [
            # Beat 1: B7
            {"duration": "quarter", "tuplet": "3:2", "chord": "B7", "stroke": "down", "notes": make_chord_notes([2, 0, 2, 1, 2, -1])},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "up", "notes": make_chord_notes([2, 0, 2, -1, -1, -1])},
            # Beat 2: B7
            {"duration": "quarter", "stroke": "down", "notes": make_chord_notes([2, 0, 2, 1, 2, -1])},
            # Beat 3: Rest
            {"duration": "quarter", "notes": []},
            # Beat 4: Triplet pickup
            {"duration": "eighth", "tuplet": "3:2", "stroke": "down", "notes": make_chord_notes([2, 0, 2, 1, 2, -1])},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "up", "notes": make_chord_notes([2, 0, 2, 1, 2, -1])},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "down", "notes": make_chord_notes([2, 0, 2, 1, 2, -1])}
        ]
    })

    # Measure 9: E 和弦爬升
    track2_measures.append(make_shuffle_strum_measure("E", [0, 0, 1, 2, 2, 0]))

    # Measure 10: B 和弦强劲节奏四连崩伴奏
    track2_measures.append(make_shuffle_strum_measure("B", [2, 4, 4, 4, 2, -1]))

    # Measure 11: B7 (前半) -> E 大三和弦长鸣结束 (后半)
    track2_measures.append({
        "beats": [
            # Beat 1: B7
            {"duration": "quarter", "tuplet": "3:2", "chord": "B7", "stroke": "down", "notes": make_chord_notes([2, 0, 2, 1, 2, -1])},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "up", "notes": make_chord_notes([2, 0, 2, -1, -1, -1])},
            # Beat 2: B7
            {"duration": "quarter", "tuplet": "3:2", "stroke": "down", "notes": make_chord_notes([2, 0, 2, 1, 2, -1])},
            {"duration": "eighth", "tuplet": "3:2", "stroke": "up", "notes": make_chord_notes([2, 0, 2, -1, -1, -1])},
            # Beat 3-4: 辉煌 E 和弦长鸣
            {"duration": "half", "chord": "E", "stroke": "down", "notes": [
                {"string": 1, "fret": 0, "letRing": True},
                {"string": 2, "fret": 0, "letRing": True},
                {"string": 3, "fret": 1, "letRing": True},
                {"string": 4, "fret": 2, "letRing": True},
                {"string": 5, "fret": 2, "letRing": True},
                {"string": 6, "fret": 0, "letRing": True}
            ]}
        ]
    })

    editor.write_measures(track_number=2, start_measure=1, measures_data=track2_measures)


    # -------------------------------------------------------------
    # TRACK 3: 贝斯 (低音 / Electric Bass Finger)
    # -------------------------------------------------------------
    # 4 strings standard: 1=G2, 2=D2, 3=A1, 4=E1
    # E1 = str 4 fret 0
    # F#1 = str 4 fret 2
    # G#1 = str 4 fret 4
    # A1 = str 3 fret 0
    # A#1 = str 3 fret 1
    # B1 = str 3 fret 2
    # C#2 = str 3 fret 4
    # D#2 = str 2 fret 1
    # E2 = str 2 fret 2
    # F#2 = str 2 fret 4
    # G#2 = str 1 fret 1

    track3_measures = []

    # Measure 1: E1 持续全音符
    track3_measures.append({
        "beats": [
            {"duration": "whole", "notes": [{"string": 4, "fret": 0, "letRing": True}]}
        ]
    })

    # Measure 2: E 调 Walking/Shuffle Bass
    track3_measures.append({
        "beats": [
            # Beat 1: E1 (quarter), G#1 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 4, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 4, "fret": 4}]},
            # Beat 2: B1 (quarter), C#2 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            # Beat 3: E2 (quarter), B1 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            # Beat 4: G#1 (quarter), F#1 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 4, "fret": 2}]}
        ]
    })

    # Measure 3: C#m Walking Bass
    track3_measures.append({
        "beats": [
            # Beat 1: C#2 (quarter), E2 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 2}]},
            # Beat 2: G#2 (quarter), F#2 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 1, "fret": 1}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 4}]},
            # Beat 3: E2 (quarter), C#2 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            # Beat 4: B1 (quarter), A#1 (eighth)
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 1}]}
        ]
    })

    # Measure 4: A 强力重音切音 (暴暴暴)
    track3_measures.append({
        "beats": [
            # Beat 1: A1 quarter
            {"duration": "quarter", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: rest + A1 heavy accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 0, "heavyAccentuated": True, "staccato": True}]},
            # Beat 3: rest + A1 heavy accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 0, "heavyAccentuated": True, "staccato": True}]},
            # Beat 4: rest + B1 heavy accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2, "heavyAccentuated": True, "staccato": True}]}
        ]
    })

    # Measure 5: E 律动贝斯
    track3_measures.append({
        "beats": [
            # Beat 1: E1, E1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 4, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 4, "fret": 0}]},
            # Beat 2: G#1, B1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            # Beat 3: C#2, D#2
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 1}]},
            # Beat 4: E2, D#2
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # Measure 6: C#2 -> A 强音切入 (暴暴)
    track3_measures.append({
        "beats": [
            # Beat 1: C#2, C#2
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            # Beat 2: C#2, rest
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": []},
            # Beat 3: rest + A1 heavy accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 0, "heavyAccentuated": True, "staccato": True}]},
            # Beat 4: rest + A1 heavy accent
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 0, "heavyAccentuated": True, "staccato": True}]}
        ]
    })

    # Measure 7: F#m 贝斯声线
    track3_measures.append({
        "beats": [
            # Beat 1: rest + F#1
            {"duration": "quarter", "tuplet": "3:2", "notes": []},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 4, "fret": 2}]},
            # Beat 2: A1, C#2
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            # Beat 3: E2, F#2
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 4}]},
            # Beat 4: C#2, A1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 0}]}
        ]
    })

    # Measure 8: B 贝斯走向
    track3_measures.append({
        "beats": [
            # Beat 1: B1, D#2
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 1}]},
            # Beat 2: F#2
            {"duration": "quarter", "notes": [{"string": 2, "fret": 4}]},
            # Beat 3: rest
            {"duration": "quarter", "notes": []},
            # Beat 4: Triplet pickup B1, D#2, F#2
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 2, "fret": 4}]}
        ]
    })

    # Measure 9: E 调爬升走向
    track3_measures.append({
        "beats": [
            # Beat 1: E1, G#1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 4, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 4, "fret": 4}]},
            # Beat 2: A1, A#1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 1}]},
            # Beat 3: B1, C#2
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 4}]},
            # Beat 4: B1, B1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # Measure 10: B pedal 贝斯重击 (郎吧四连崩)
    track3_measures.append({
        "beats": [
            # Beat 1: B1, B1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2, "velocity": 75}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            # Beat 2: B1, B1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            # Beat 3: B1, B1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            # Beat 4: B1, B1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # Measure 11: B -> E 根音震撼落音
    track3_measures.append({
        "beats": [
            # Beat 1: B1, B1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            # Beat 2: B1, B1
            {"duration": "quarter", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2, "accentuated": True}]},
            {"duration": "eighth", "tuplet": "3:2", "notes": [{"string": 3, "fret": 2}]},
            # Beat 3-4: 震撼低音 E1 (Half note)
            {"duration": "half", "notes": [{"string": 4, "fret": 0, "heavyAccentuated": True, "vibrato": True, "letRing": True}]}
        ]
    })

    editor.write_measures(track_number=3, start_measure=1, measures_data=track3_measures)

    # 保存 GP5
    editor.save(gp5_path, backup=False)
    print(f"GP5 saved: {gp5_path}")

    # 同时导出为 TuxGuitar 原生 .tg 格式
    write_tg(editor.song, tg_path)
    print(f"TG saved: {tg_path}")

if __name__ == "__main__":
    create_yu_ai_score()
