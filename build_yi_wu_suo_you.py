import os
from tuxguitar_mcp.song_editor import SongEditor
from tuxguitar_mcp.models import NoteData, NoteEffectData, BeatData, MeasureData, ChordData, TrackData
from tuxguitar_mcp.tg_parser import write_tg

def create_fingerstyle_score():
    gp5_path = r"d:\Program Files\tuxguitar\yi_wu_suo_you_fingerstyle.gp5"
    tg_path = r"d:\Program Files\tuxguitar\yi_wu_suo_you_fingerstyle.tg"

    editor = SongEditor()
    editor.create_new(
        file_path=gp5_path,
        title="一无所有 (吉他指弹独奏版)",
        artist="崔健 (编配: Antigravity)",
        tempo=169,
        time_signature="4/4",
        track_presets=[
            {
                "name": "吉他指弹独奏 (Fingerstyle Solo)",
                "tuning": "standard_6",
                "instrument": "acoustic_steel"
            }
        ]
    )

    # -------------------------------------------------------------
    # TRACK 1: 吉他指弹独奏 (Fingerstyle Solo)
    # 标准 6 弦: 1=E4, 2=B3, 3=G3, 4=D3, 5=A2, 6=E2
    # 调性: C# minor (4 个升号)
    # -------------------------------------------------------------
    measures = []

    # Helper functions for chords and beats
    def make_chord(chord_name, strings):
        return {
            "chord": chord_name,
            "duration": "quarter",
            "stroke": "down",
            "notes": [{"string": idx + 1, "fret": f} for idx, f in enumerate(strings) if f >= 0]
        }

    # =============================================================
    # 一、序奏与散板 (Intro, M1 - M4)
    # =============================================================
    # M1: 散板大琶音 C#m9 (全音符慢速滚奏)
    measures.append({
        "marker": "Intro (散板大琶音 苍凉深沉)",
        "beats": [
            {
                "duration": "whole",
                "chord": "C#m",
                "stroke": "down",
                "text": "琶音轮指~",
                "notes": [
                    {"string": 5, "fret": 4, "letRing": True}, # C#3
                    {"string": 4, "fret": 6, "letRing": True}, # G#3
                    {"string": 3, "fret": 6, "letRing": True}, # C#4
                    {"string": 2, "fret": 5, "letRing": True}, # E4
                    {"string": 1, "fret": 4, "letRing": True, "vibrato": True}  # G#4
                ]
            }
        ]
    })

    # M2: 12品自然泛音延音 + 空弦颤音
    measures.append({
        "beats": [
            {
                "duration": "half",
                "text": "12品自然泛音",
                "notes": [
                    {"string": 1, "fret": 12, "letRing": True},
                    {"string": 2, "fret": 12, "letRing": True},
                    {"string": 3, "fret": 12, "letRing": True}
                ]
            },
            {
                "duration": "half",
                "notes": [
                    {"string": 5, "fret": 4, "letRing": True, "vibrato": True}
                ]
            }
        ]
    })

    # M3: 建立 169 BPM 摇滚律动 (低音底鼓 + 内声部切音)
    measures.append({
        "marker": "进入 169 摇滚低音律动",
        "beats": [
            # Beat 1: Bass + chord
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 6}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 5}]},
            # Beat 2: Palm Mute choke
            {"duration": "eighth", "notes": [{"string": 3, "fret": 6, "palmMute": True}, {"string": 4, "fret": 6, "palmMute": True}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 5}]},
            # Beat 3: Bass
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 6}]},
            # Beat 4: Chord
            {"duration": "eighth", "notes": [{"string": 3, "fret": 6, "palmMute": True}, {"string": 4, "fret": 6, "palmMute": True}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 5}]}
        ]
    })

    # M4: 摇滚律动推进
    measures.append({
        "beats": [
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 6}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 5}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 6, "palmMute": True}, {"string": 4, "fret": 6, "palmMute": True}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 5}]},
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 6}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 6, "palmMute": True}, {"string": 4, "fret": 6, "palmMute": True}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 5}]}
        ]
    })

    # =============================================================
    # 二、经典前奏唢呐旋律 (Suona Intro Riff, M5 - M13)
    # =============================================================
    # M5 (C#m): G#3 B3 C#4 E4
    measures.append({
        "marker": "经典前奏独奏 (唢呐主旋律)",
        "beats": [
            # Beat 1: Bass C#3 + Melody G#3
            {"duration": "eighth", "chord": "C#m", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 0}]}, # B3
            # Beat 2: Melody C#4, E4
            {"duration": "eighth", "notes": [{"string": 2, "fret": 2}]}, # C#4
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]}, # E4
            # Beat 3: Bass C#3 + Melody G#3
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 0}]},
            # Beat 4: Melody C#4, E4
            {"duration": "eighth", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # M6 (A): F#4 E4 F#4 G#4
    measures.append({
        "beats": [
            # Beat 1: Bass A2 (open 5th) + Melody F#4
            {"duration": "eighth", "chord": "A", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 2}]}, # F#4
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]}, # E4
            # Beat 2: Melody F#4, G#4
            {"duration": "eighth", "notes": [{"string": 1, "fret": 2}]}, # F#4
            {"duration": "eighth", "notes": [{"string": 1, "fret": 4, "vibrato": True}]}, # G#4
            # Beat 3: Bass A2 + Melody F#4
            {"duration": "eighth", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            # Beat 4: Melody F#4, G#4
            {"duration": "eighth", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 4, "vibrato": True}]}
        ]
    })

    # M7 (B): F#4 E4 C#4 B3
    measures.append({
        "beats": [
            # Beat 1: Bass B2 (5th string fret 2) + Melody F#4
            {"duration": "eighth", "chord": "B", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]}, # E4
            # Beat 2: Melody C#4, B3
            {"duration": "eighth", "notes": [{"string": 2, "fret": 2}]}, # C#4
            {"duration": "eighth", "notes": [{"string": 2, "fret": 0}]}, # B3
            # Beat 3: Bass B2 + Melody F#4
            {"duration": "eighth", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            # Beat 4: Melody C#4, B3
            {"duration": "eighth", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 0}]}
        ]
    })

    # M8 (C#m): C#4 (held vibrato) + C#m 和弦打板
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C#m", "notes": [{"string": 5, "fret": 4}, {"string": 2, "fret": 2, "vibrato": True}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]},
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]}
        ]
    })

    # M9 (C#m): 律动连接
    measures.append({
        "beats": [
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}, {"string": 2, "fret": 2}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]},
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]}
        ]
    })

    # M10 (C#m): 第二遍 G#3 B3 C#4 E4
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "C#m", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # M11 (A): F#4 E4 F#4 G#4
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "A", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 4, "vibrato": True}]},
            {"duration": "eighth", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 4, "vibrato": True}]}
        ]
    })

    # M12 (B): F#4 E4 C#4 B3
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "B", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 0}]}
        ]
    })

    # M13 (C#m): C#4 延音
    measures.append({
        "beats": [
            {"duration": "half", "chord": "C#m", "notes": [{"string": 5, "fret": 4}, {"string": 2, "fret": 2, "vibrato": True, "letRing": True}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]},
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}]}
        ]
    })

    # =============================================================
    # 三、过门与下行过渡 (Transition, M14 - M22)
    # =============================================================
    # M14 (A): E4 D#4 C#4 B3
    measures.append({
        "marker": "旋律下行回落",
        "beats": [
            {"duration": "quarter", "chord": "A", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 0}]}, # E4
            {"duration": "quarter", "notes": [{"string": 2, "fret": 4}]}, # D#4
            {"duration": "quarter", "notes": [{"string": 2, "fret": 2}]}, # C#4
            {"duration": "quarter", "notes": [{"string": 2, "fret": 0}]}  # B3
        ]
    })

    # M15 (B): C#4 B3 G#3 F#3
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "B", "notes": [{"string": 5, "fret": 2}, {"string": 2, "fret": 2}]}, # C#4
            {"duration": "quarter", "notes": [{"string": 2, "fret": 0}]}, # B3
            {"duration": "quarter", "notes": [{"string": 3, "fret": 1}]}, # G#3
            {"duration": "quarter", "notes": [{"string": 4, "fret": 4}]}  # F#3
        ]
    })

    # M16 (C#m): E3 落地低音
    measures.append({
        "beats": [
            {"duration": "whole", "chord": "C#m", "notes": [
                {"string": 5, "fret": 4, "letRing": True},
                {"string": 4, "fret": 2, "letRing": True}
            ]}
        ]
    })

    # M17: 慢速回落 滚奏和弦 (原谱滚奏)
    measures.append({
        "marker": "滚奏静止 (呼吸停顿)",
        "beats": [
            {
                "duration": "whole",
                "chord": "C#m",
                "stroke": "down",
                "text": "慢速滚奏~",
                "notes": [
                    {"string": 5, "fret": 4, "letRing": True},
                    {"string": 4, "fret": 6, "letRing": True},
                    {"string": 3, "fret": 6, "letRing": True},
                    {"string": 2, "fret": 5, "letRing": True}
                ]
            }
        ]
    })

    # M18 - M21: 摇滚低音鼓点再启，准备入唱
    for m_i in range(18, 22):
        measures.append({
            "beats": [
                {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
                {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
                {"duration": "eighth", "stroke": "down", "notes": [{"string": 3, "fret": 6, "palmMute": True}, {"string": 4, "fret": 6, "palmMute": True}]},
                {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
                {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
                {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
                {"duration": "eighth", "stroke": "down", "notes": [{"string": 3, "fret": 6, "palmMute": True}, {"string": 4, "fret": 6, "palmMute": True}]},
                {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]}
            ]
        })

    # M22 (Mark C): "我曾经" 弱起入唱
    measures.append({
        "marker": "Verse 1 (原唱入唱: 我曾经...)",
        "beats": [
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6, "palmMute": True}, {"string": 4, "fret": 6, "palmMute": True}]},
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "eighth", "text": "我", "notes": [{"string": 3, "fret": 1}]}, # G#3
            {"duration": "eighth", "text": "曾", "notes": [{"string": 3, "fret": 1}]}  # G#3
        ]
    })

    # =============================================================
    # 四、主歌段落 (Verse 1 & 2, M23 - M32)
    # =============================================================
    # M23 (C#m): "经问个不休"
    measures.append({
        "beats": [
            # Beat 1: Bass C#3 + Melody G#3 "经"
            {"duration": "eighth", "chord": "C#m", "text": "经", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "问", "notes": [{"string": 3, "fret": 1}]}, # G#3
            # Beat 2: "个不"
            {"duration": "eighth", "text": "个", "notes": [{"string": 4, "fret": 4}]}, # F#3
            {"duration": "eighth", "text": "不", "notes": [{"string": 4, "fret": 2}]}, # E3
            # Beat 3-4: "休~" + 伴奏打板
            {"duration": "quarter", "text": "休~", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 2, "vibrato": True}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]}
        ]
    })

    # M24 (B): "你何时跟我走"
    measures.append({
        "beats": [
            # Beat 1: "你" F#3
            {"duration": "quarter", "chord": "B", "text": "你", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]},
            # Beat 2: "何"
            {"duration": "eighth", "text": "何", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "时", "notes": [{"string": 3, "fret": 1}]}, # G#3
            # Beat 3-4: "跟我走"
            {"duration": "quarter", "text": "跟", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]}, # F#3
            {"duration": "quarter", "text": "我走~", "notes": [{"string": 4, "fret": 4, "vibrato": True}]}
        ]
    })

    # M25 (A): "可你却总是笑我"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "A", "text": "可", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}]}, # E3
            {"duration": "eighth", "text": "你", "notes": [{"string": 4, "fret": 4}]}, # F#3
            {"duration": "eighth", "text": "却", "notes": [{"string": 3, "fret": 1}]}, # G#3
            {"duration": "eighth", "text": "总", "notes": [{"string": 4, "fret": 4}]}, # F#3
            {"duration": "quarter", "text": "是", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}]}, # E3
            {"duration": "quarter", "text": "笑我", "notes": [{"string": 4, "fret": 2}]}
        ]
    })

    # M26 (C#m): "一无所有"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C#m", "text": "一", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 2}]},
            {"duration": "quarter", "text": "无", "notes": [{"string": 5, "fret": 4}]}, # C#3
            {"duration": "half", "text": "所~有~", "notes": [{"string": 5, "fret": 4, "vibrato": True, "letRing": True}]}
        ]
    })

    # M27: 间奏呼应短句
    measures.append({
        "beats": [
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 6}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]},
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 1}]}
        ]
    })

    # M28 (C#m): "我也想给你我的追求"
    measures.append({
        "marker": "Verse 2 (我也想给你我的追求...)",
        "beats": [
            {"duration": "eighth", "chord": "C#m", "text": "我", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "也", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "想", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "给", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "我", "notes": [{"string": 4, "fret": 2}]},
            {"duration": "quarter", "text": "追求~", "notes": [{"string": 4, "fret": 2, "vibrato": True}]}
        ]
    })

    # M29 (B): "给你我的自由"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "B", "text": "给", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "我", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "quarter", "text": "的", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]},
            {"duration": "quarter", "text": "自由~", "notes": [{"string": 4, "fret": 4, "vibrato": True}]}
        ]
    })

    # M30 (A): "可你却总是笑我"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "A", "text": "可", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "却", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "总", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "quarter", "text": "是", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}]},
            {"duration": "quarter", "text": "笑我", "notes": [{"string": 4, "fret": 2}]}
        ]
    })

    # M31 (C#m): "一无所有"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C#m", "text": "一", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 2}]},
            {"duration": "quarter", "text": "无", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "half", "text": "所~有~", "notes": [{"string": 5, "fret": 4, "vibrato": True, "letRing": True}]}
        ]
    })

    # M32: 渐强鼓点推进 进入副歌呐喊
    measures.append({
        "marker": "鼓点渐强准备 (Crescendo)",
        "beats": [
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]},
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "eighth", "notes": [{"string": 5, "fret": 4}]}
        ]
    })

    # =============================================================
    # 五、副歌前置呐喊 (Pre-Chorus, M33 - M37)
    # =============================================================
    # M33 (C#m): "噢~~~~" (高亢长音)
    measures.append({
        "marker": "副歌高亢呐喊 (噢~~~~)",
        "beats": [
            {"duration": "half", "chord": "C#m", "text": "噢~~~~", "notes": [
                {"string": 5, "fret": 4},
                {"string": 2, "fret": 2, "vibrato": True, "heavyAccentuated": True, "letRing": True}
            ]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 3, "fret": 6}, {"string": 4, "fret": 6}]},
            {"duration": "quarter", "notes": [{"string": 5, "fret": 4}]}
        ]
    })

    # M34 (B): "你何时跟我走"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "B", "text": "你", "notes": [{"string": 5, "fret": 2}, {"string": 2, "fret": 0}]},
            {"duration": "quarter", "text": "何", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "quarter", "text": "时", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "quarter", "text": "跟我走", "notes": [{"string": 4, "fret": 2}]}
        ]
    })

    # M35 (A): "噢~~~~" (再次呼喊)
    measures.append({
        "beats": [
            {"duration": "half", "chord": "A", "text": "噢~~~~", "notes": [
                {"string": 5, "fret": 0},
                {"string": 2, "fret": 2, "vibrato": True, "heavyAccentuated": True, "letRing": True}
            ]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 2, "fret": 2}, {"string": 3, "fret": 2}]},
            {"duration": "quarter", "notes": [{"string": 5, "fret": 0}]}
        ]
    })

    # M36 (B): "你何时跟我走"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "B", "text": "你", "notes": [{"string": 5, "fret": 2}, {"string": 2, "fret": 0}]},
            {"duration": "quarter", "text": "何", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "quarter", "text": "时", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "quarter", "text": "跟我走", "notes": [{"string": 4, "fret": 2}]}
        ]
    })

    # M37: ff 16分三连音超强爆发切入副歌
    measures.append({
        "marker": "ff 强力军鼓切入 (丹田爆发)",
        "beats": [
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}, {"string": 3, "fret": 4}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}, {"string": 3, "fret": 4}]},
            {"duration": "eighth", "stroke": "down", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]},
            {"duration": "eighth", "stroke": "down", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]},
            {"duration": "eighth", "stroke": "down", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]},
            {"duration": "eighth", "stroke": "down", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]}
        ]
    })

    # =============================================================
    # 六、全曲大副歌 (Chorus, M38 - M53)
    # =============================================================
    # M38 (C#m, Mark D): "脚下这地在走"
    measures.append({
        "marker": "Chorus 1 (脚下这地在走...)",
        "beats": [
            {"duration": "eighth", "chord": "C#m", "text": "脚", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]}, # G#3
            {"duration": "eighth", "text": "下", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "这", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "地", "notes": [{"string": 2, "fret": 0}]}, # B3
            {"duration": "quarter", "text": "在", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]}, # G#3
            {"duration": "quarter", "text": "走~", "notes": [{"string": 3, "fret": 1, "vibrato": True}]}
        ]
    })

    # M39 (B): "身边这水在流"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "B", "text": "身", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]}, # F#3
            {"duration": "eighth", "text": "边", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "这", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "水", "notes": [{"string": 3, "fret": 2}]}, # A3
            {"duration": "quarter", "text": "在", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]}, # F#3
            {"duration": "quarter", "text": "流~", "notes": [{"string": 4, "fret": 4, "vibrato": True}]}
        ]
    })

    # M40 (A): "可你却总是笑我"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "A", "text": "可", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "却", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "总", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "quarter", "text": "是", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}]},
            {"duration": "quarter", "text": "笑我", "notes": [{"string": 4, "fret": 2}]}
        ]
    })

    # M41 (C#m): "一无所有"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C#m", "text": "一", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 2}]},
            {"duration": "quarter", "text": "无", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "half", "text": "所~有~", "notes": [{"string": 5, "fret": 4, "vibrato": True, "letRing": True}]}
        ]
    })

    # M42 (C#m): "为何你总笑个没完"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "C#m", "text": "为", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "何", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "总", "notes": [{"string": 2, "fret": 0}]},
            {"duration": "quarter", "text": "笑个", "notes": [{"string": 5, "fret": 4}, {"string": 3, "fret": 1}]},
            {"duration": "quarter", "text": "没完~", "notes": [{"string": 3, "fret": 1, "vibrato": True}]}
        ]
    })

    # M43 (B): "为何我总要追求"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "B", "text": "为", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "何", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "我", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "总", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "quarter", "text": "要", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}]},
            {"duration": "quarter", "text": "追求~", "notes": [{"string": 4, "fret": 4, "vibrato": True}]}
        ]
    })

    # M44 (A): "难道你真的十分在乎"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "A", "text": "难", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}]},
            {"duration": "eighth", "text": "道", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 3, "fret": 1}]},
            {"duration": "eighth", "text": "真", "notes": [{"string": 4, "fret": 4}]},
            {"duration": "quarter", "text": "的", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}]},
            {"duration": "quarter", "text": "十分在乎", "notes": [{"string": 4, "fret": 2}]}
        ]
    })

    # M45 (C#m): "面对我一无所有"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C#m", "text": "面", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 2}]},
            {"duration": "quarter", "text": "对", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "half", "text": "一无所有~", "notes": [{"string": 5, "fret": 4, "vibrato": True, "letRing": True}]}
        ]
    })

    # M46 - M49 (高八度爆发 - 旋律跃升到 1、2 弦!)
    # M46 (C#m): "脚下这地在走" (高八度 G#4 G#4 G#4 B4 G#4)
    measures.append({
        "marker": "Chorus 2 (高八度升华 狂放全扫弦)",
        "beats": [
            {"duration": "eighth", "chord": "C#m", "text": "脚", "notes": [{"string": 5, "fret": 4}, {"string": 1, "fret": 4}]}, # G#4
            {"duration": "eighth", "text": "下", "notes": [{"string": 1, "fret": 4}]},
            {"duration": "eighth", "text": "这", "notes": [{"string": 1, "fret": 4}]},
            {"duration": "eighth", "text": "地", "notes": [{"string": 1, "fret": 7}]}, # B4
            {"duration": "quarter", "text": "在", "notes": [{"string": 5, "fret": 4}, {"string": 1, "fret": 4}]}, # G#4
            {"duration": "quarter", "text": "走~", "notes": [{"string": 1, "fret": 4, "vibrato": True}]}
        ]
    })

    # M47 (B): "身边这水在流" (高八度 F#4 F#4 F#4 A4 F#4)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "B", "text": "身", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 2}]}, # F#4
            {"duration": "eighth", "text": "边", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "eighth", "text": "这", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "eighth", "text": "水", "notes": [{"string": 1, "fret": 5}]}, # A4
            {"duration": "quarter", "text": "在", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 2}]}, # F#4
            {"duration": "quarter", "text": "流~", "notes": [{"string": 1, "fret": 2, "vibrato": True}]}
        ]
    })

    # M48 (A): "可你却总是笑我" (高八度 E4 F#4 G#4 F#4 E4)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "A", "text": "可", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 0}]}, # E4
            {"duration": "eighth", "text": "你", "notes": [{"string": 1, "fret": 2}]}, # F#4
            {"duration": "eighth", "text": "却", "notes": [{"string": 1, "fret": 4}]}, # G#4
            {"duration": "eighth", "text": "总", "notes": [{"string": 1, "fret": 2}]}, # F#4
            {"duration": "quarter", "text": "是", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 0}]}, # E4
            {"duration": "quarter", "text": "笑我", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # M49 (C#m): "一无所有"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C#m", "text": "一", "notes": [{"string": 5, "fret": 4}, {"string": 2, "fret": 2}]},
            {"duration": "quarter", "text": "无", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "half", "text": "所~有~", "notes": [{"string": 5, "fret": 4, "vibrato": True, "letRing": True}]}
        ]
    })

    # M50 (C#m): "为何你总笑个没完" (高八度)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "C#m", "text": "为", "notes": [{"string": 5, "fret": 4}, {"string": 1, "fret": 4}]},
            {"duration": "eighth", "text": "何", "notes": [{"string": 1, "fret": 4}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 1, "fret": 4}]},
            {"duration": "eighth", "text": "总", "notes": [{"string": 1, "fret": 7}]},
            {"duration": "quarter", "text": "笑个", "notes": [{"string": 5, "fret": 4}, {"string": 1, "fret": 4}]},
            {"duration": "quarter", "text": "没完~", "notes": [{"string": 1, "fret": 4, "vibrato": True}]}
        ]
    })

    # M51 (B): "为何我总要追求" (高八度)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "B", "text": "为", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 2}]},
            {"duration": "eighth", "text": "何", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "eighth", "text": "我", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "eighth", "text": "总", "notes": [{"string": 1, "fret": 5}]},
            {"duration": "quarter", "text": "要", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 2}]},
            {"duration": "quarter", "text": "追求~", "notes": [{"string": 1, "fret": 2, "vibrato": True}]}
        ]
    })

    # M52 (A): "难道你真的十分在乎" (高八度)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "A", "text": "难", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "道", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 1, "fret": 4}]},
            {"duration": "eighth", "text": "真", "notes": [{"string": 1, "fret": 2}]},
            {"duration": "quarter", "text": "的", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "quarter", "text": "十分在乎", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # M53 (C#m): "面对我一无所有"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C#m", "text": "面", "notes": [{"string": 5, "fret": 4}, {"string": 2, "fret": 2}]},
            {"duration": "quarter", "text": "对", "notes": [{"string": 5, "fret": 4}]},
            {"duration": "half", "text": "一无所有~", "notes": [{"string": 5, "fret": 4, "vibrato": True, "letRing": True}]}
        ]
    })

    # =============================================================
    # 七、终极呼喊与尾声 (Outro, M54 - M62)
    # =============================================================
    # M54 (A): "噢~~~~" (极高音 C#5, 1弦9品!)
    measures.append({
        "marker": "终极呼唤 (极高音 C#5 震撼呐喊)",
        "beats": [
            {"duration": "half", "chord": "A", "text": "噢~~~~", "notes": [
                {"string": 5, "fret": 0},
                {"string": 1, "fret": 9, "heavyAccentuated": True, "vibrato": True, "letRing": True}
            ]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 1, "fret": 9}, {"string": 2, "fret": 10}]},
            {"duration": "quarter", "notes": [{"string": 5, "fret": 0}]}
        ]
    })

    # M55 (B): "你何时跟我走" (下行推进)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "B", "text": "你", "notes": [{"string": 5, "fret": 2}, {"string": 1, "fret": 7}]}, # B4
            {"duration": "quarter", "text": "何", "notes": [{"string": 1, "fret": 4}]}, # G#4
            {"duration": "quarter", "text": "时", "notes": [{"string": 1, "fret": 2}]}, # F#4
            {"duration": "quarter", "text": "跟我走", "notes": [{"string": 1, "fret": 0}]}  # E4
        ]
    })

    # M56 (Mark E): 终曲慢速滚奏琶音 (原谱 E 标记滚奏)
    measures.append({
        "marker": "Outro (大滚奏和弦 归于沉思)",
        "beats": [
            {
                "duration": "whole",
                "chord": "C#m",
                "stroke": "down",
                "text": "慢速深情滚奏~",
                "notes": [
                    {"string": 5, "fret": 4, "letRing": True},
                    {"string": 4, "fret": 6, "letRing": True},
                    {"string": 3, "fret": 6, "letRing": True},
                    {"string": 2, "fret": 5, "letRing": True},
                    {"string": 1, "fret": 4, "letRing": True, "vibrato": True}
                ]
            }
        ]
    })

    # M57 - M58: 低音余韵沉淀
    measures.append({
        "beats": [
            {"duration": "half", "notes": [{"string": 5, "fret": 4, "letRing": True}]},
            {"duration": "quarter", "notes": [{"string": 4, "fret": 6}]},
            {"duration": "quarter", "notes": [{"string": 3, "fret": 6}]}
        ]
    })
    measures.append({
        "beats": [
            {"duration": "whole", "notes": [{"string": 5, "fret": 4, "letRing": True, "vibrato": True}]}
        ]
    })

    # M59 - M61: 强力断音扫弦扫尾 (C#m - A - B - C#m)
    measures.append({
        "marker": "终局有力卡点扫弦",
        "beats": [
            {"duration": "quarter", "chord": "C#m", "stroke": "down", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 6}, {"string": 3, "fret": 6}, {"string": 2, "fret": 5}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 6}, {"string": 3, "fret": 6}, {"string": 2, "fret": 5}]},
            {"duration": "quarter", "chord": "A", "stroke": "down", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}, {"string": 3, "fret": 2}, {"string": 2, "fret": 2}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 0}, {"string": 4, "fret": 2}, {"string": 3, "fret": 2}, {"string": 2, "fret": 2}]}
        ]
    })

    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "B", "stroke": "down", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}, {"string": 3, "fret": 4}, {"string": 2, "fret": 4}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 2}, {"string": 4, "fret": 4}, {"string": 3, "fret": 4}, {"string": 2, "fret": 4}]},
            {"duration": "quarter", "chord": "C#m", "stroke": "down", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 6}, {"string": 3, "fret": 6}, {"string": 2, "fret": 5}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 6}, {"string": 3, "fret": 6}, {"string": 2, "fret": 5}]}
        ]
    })

    measures.append({
        "beats": [
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 6}]},
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 6}]},
            {"duration": "half", "stroke": "down", "notes": [{"string": 5, "fret": 4}, {"string": 4, "fret": 6}, {"string": 3, "fret": 6}, {"string": 2, "fret": 5}]}
        ]
    })

    # M62: 震撼空灵大和弦延音 (Double Bar Line)
    measures.append({
        "marker": "终曲泛音长鸣 (Fine)",
        "beats": [
            {
                "duration": "whole",
                "chord": "C#m",
                "stroke": "down",
                "notes": [
                    {"string": 5, "fret": 4, "letRing": True},
                    {"string": 4, "fret": 6, "letRing": True},
                    {"string": 3, "fret": 6, "letRing": True},
                    {"string": 2, "fret": 5, "letRing": True},
                    {"string": 1, "fret": 0, "letRing": True, "vibrato": True} # C#m(add9)
                ]
            }
        ]
    })

    print(f"Total measures prepared: {len(measures)}")
    editor.write_measures(track_number=1, start_measure=1, measures_data=measures)

    # 保存 GP5
    editor.save(gp5_path, backup=False)
    print(f"GP5 saved: {gp5_path}")

    # 保存 TG
    write_tg(editor.song, tg_path)
    print(f"TG saved: {tg_path}")

if __name__ == "__main__":
    create_fingerstyle_score()
