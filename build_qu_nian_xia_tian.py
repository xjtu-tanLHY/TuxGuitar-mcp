import os
from tuxguitar_mcp.song_editor import SongEditor
from tuxguitar_mcp.models import NoteData, NoteEffectData, BeatData, MeasureData, ChordData, TrackData
from tuxguitar_mcp.tg_parser import write_tg

def create_score():
    gp5_path = r"d:\Program Files\tuxguitar\qu_nian_xia_tian_fingerstyle.gp5"
    tg_path = r"d:\Program Files\tuxguitar\qu_nian_xia_tian_fingerstyle.tg"

    editor = SongEditor()
    editor.create_new(
        file_path=gp5_path,
        title="去年夏天 (吉他指弹独奏版)",
        artist="王大毛 / 家家 (编配: Antigravity)",
        tempo=62,
        time_signature="2/4",
        track_presets=[
            {
                "name": "指弹吉他 (Capo 2 选调C)",
                "tuning": "standard_6",
                "instrument": "acoustic_steel"
            }
        ]
    )

    # -------------------------------------------------------------
    # 调式与变调夹: C调指法编配, Capo 2品 = 原调D调
    # 2/4 拍, 每小节 2 拍 (2个四分音符 = 4个八分音符 = 8个十六分音符)
    # 标准 6 弦: 1=E4, 2=B3, 3=G3, 4=D3, 5=A2, 6=E2
    # -------------------------------------------------------------
    measures = []

    # =============================================================
    # 一、前奏 (Intro, M1 - M8)
    # 标志性八音盒/合成器音型: 3 5 5 2 (Mi Sol Sol Re)
    # =============================================================
    # M1: 弱起前置 + C和弦分解 (0 5 5 2)
    measures.append({
        "marker": "Intro (清脆八音盒音色 Capo 2)",
        "beats": [
            # Beat 1: Bass C3 (5弦3品) + G3 (3弦0品)
            {"duration": "eighth", "chord": "C", "notes": [{"string": 5, "fret": 3}, {"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: D4 (2弦3品)
            {"duration": "quarter", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M2: Am7 和弦 (3 5 5 2 -> E4 G3 G3 D4)
    measures.append({
        "beats": [
            # Beat 1: Bass A2 (5弦空弦) + E4 (1弦0品)
            {"duration": "eighth", "chord": "Am7", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: G3, D4
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M3: Fmaj7 和弦 (3 5 5 2)
    measures.append({
        "beats": [
            # Beat 1: Bass F3 (4弦3品) + E4 (1弦0品)
            {"duration": "eighth", "chord": "Fmaj7", "notes": [{"string": 4, "fret": 3}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: G3, D4
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M4: G 和弦 (3 5 5 2)
    measures.append({
        "beats": [
            # Beat 1: Bass G2 (6弦3品) + E4 (1弦0品)
            {"duration": "eighth", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: G3, D4
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M5: C 和弦 (3 5 3 5)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "C", "notes": [{"string": 5, "fret": 3}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]}
        ]
    })

    # M6: Am7 (6. 5 -> A4 G4, 2拍完整)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "Am7", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 5}]}, # A4 (1拍)
            {"duration": "quarter", "notes": [{"string": 1, "fret": 3}]}  # G4 (1拍)
        ]
    })

    # M7: Fmaj7 (3 1 6 -> E4 C4 A3)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Fmaj7", "notes": [{"string": 4, "fret": 3}, {"string": 1, "fret": 0}]}, # E4
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]}, # C4
            {"duration": "quarter", "notes": [{"string": 3, "fret": 2}]}  # A3
        ]
    })

    # M8: G 和弦延音 + 弱起准备 (2 - | 0 5 5 6 1 6)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 3, "letRing": True}]},
            # 弱起准备: "还有什么等"
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "还", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "有", "notes": [{"string": 3, "fret": 2}]}  # 6
        ]
    })

    # =============================================================
    # 二、主歌第一段 (Verse 1, M9 - M24)
    # "还有什么等待？还有什么悲哀？这故事中的人不太精彩..."
    # =============================================================
    # M9 (Fmaj7): "什 么 等"
    measures.append({
        "marker": "Verse 1 (主歌抒情进唱)",
        "beats": [
            {"duration": "eighth", "chord": "Fmaj7", "text": "什", "notes": [{"string": 4, "fret": 3}, {"string": 2, "fret": 1}]}, # 1
            {"duration": "eighth", "text": "么", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "quarter", "text": "等", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M10 (Fmaj7): "待？ 还有什么悲"
    measures.append({
        "beats": [
            {"duration": "quarter", "text": "待？", "notes": [{"string": 4, "fret": 3}, {"string": 1, "fret": 0, "vibrato": True}]}, # 3
            {"duration": "16th", "text": "还", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "有", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "什", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "16th", "text": "么", "notes": [{"string": 2, "fret": 1}]}  # 1
        ]
    })

    # M11 (G): "哀？ 这故事中的"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "G", "text": "哀？", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 3, "vibrato": True}]}, # 2
            {"duration": "16th", "text": "这", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "故", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "事", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "16th", "text": "中", "notes": [{"string": 2, "fret": 1}]}  # 1
        ]
    })

    # M12 (Em7): "的人不太精"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Em7", "text": "的", "notes": [{"string": 6, "fret": 0}, {"string": 3, "fret": 2}]}, # 6
            {"duration": "eighth", "text": "人", "notes": [{"string": 1, "fret": 0}]}, # 3
            {"duration": "eighth", "text": "不", "notes": [{"string": 2, "fret": 3}]}, # 2
            {"duration": "eighth", "text": "太", "notes": [{"string": 2, "fret": 3}]}  # 2
        ]
    })

    # M13 (Am7): "彩。 夏去了又回"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Am7", "text": "彩", "notes": [{"string": 5, "fret": 0}, {"string": 2, "fret": 1}]}, # 1
            {"duration": "eighth", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "16th", "text": "夏", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "16th", "text": "去", "notes": [{"string": 2, "fret": 1}]}, # 1
            {"duration": "eighth", "text": "了", "notes": [{"string": 3, "fret": 0}]}  # 5
        ]
    })

    # M14 (Dm7): "又回来，"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Dm7", "text": "又", "notes": [{"string": 4, "fret": 0}, {"string": 3, "fret": 0}]}, # 5
            {"duration": "eighth", "text": "回", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "quarter", "text": "来，", "notes": [{"string": 2, "fret": 1, "vibrato": True}]} # 1
        ]
    })

    # M15 (G): "而人却已不"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "而", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "人", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "却", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "16th", "text": "已", "notes": [{"string": 2, "fret": 1}]}  # 1
        ]
    })

    # M16 (C): "在， 它重复着我"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C", "text": "在，", "notes": [{"string": 5, "fret": 3}, {"string": 2, "fret": 3, "vibrato": True}]}, # 2
            {"duration": "16th", "text": "它", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "重", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "复", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "16th", "text": "着", "notes": [{"string": 2, "fret": 1}]}  # 1
        ]
    })

    # M17 (Em7): "汹涌的忍耐。"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Em7", "text": "我", "notes": [{"string": 6, "fret": 0}, {"string": 3, "fret": 2}]}, # 6
            {"duration": "eighth", "text": "汹", "notes": [{"string": 1, "fret": 0}]}, # 3
            {"duration": "eighth", "text": "涌", "notes": [{"string": 2, "fret": 3}]}, # 2
            {"duration": "eighth", "text": "的", "notes": [{"string": 2, "fret": 3}]}  # 2
        ]
    })

    # M18 (Am7): "忍耐。 今年兰花又"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Am7", "text": "忍", "notes": [{"string": 5, "fret": 0}, {"string": 2, "fret": 1}]}, # 1
            {"duration": "eighth", "text": "耐", "notes": [{"string": 2, "fret": 3}]}, # 2
            {"duration": "eighth", "text": "今", "notes": [{"string": 2, "fret": 3, "letRing": True}]},
            {"duration": "16th", "text": "年", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "兰", "notes": [{"string": 3, "fret": 0}]}  # 5
        ]
    })

    # =============================================================
    # 三、主歌第二段 (Verse 2, M19 - M28)
    # "今年兰花又开，开了它也会败，我想要一个人活得精彩..."
    # =============================================================
    # M19 (Fmaj7): "花又开， 开了它也会"
    measures.append({
        "marker": "Verse 2 (兰花又开)",
        "beats": [
            {"duration": "eighth", "chord": "Fmaj7", "text": "花", "notes": [{"string": 4, "fret": 3}, {"string": 3, "fret": 2}]}, # 6
            {"duration": "eighth", "text": "又", "notes": [{"string": 2, "fret": 1}]}, # 1
            {"duration": "quarter", "text": "开，", "notes": [{"string": 1, "fret": 0, "vibrato": True}]} # 3
        ]
    })

    # M20 (G): "开了它也会败，"
    measures.append({
        "beats": [
            {"duration": "16th", "chord": "G", "text": "开", "notes": [{"string": 6, "fret": 3}, {"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "了", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "它", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "16th", "text": "也", "notes": [{"string": 2, "fret": 1}]}, # 1
            {"duration": "eighth", "text": "会", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "eighth", "text": "败，", "notes": [{"string": 2, "fret": 3, "vibrato": True}]} # 2
        ]
    })

    # M21 (Em7): "我想要一个人活得精彩"
    measures.append({
        "beats": [
            {"duration": "16th", "chord": "Em7", "text": "我", "notes": [{"string": 6, "fret": 0}, {"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "想", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "要", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "一", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "个", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "人", "notes": [{"string": 1, "fret": 0}]} # 3
        ]
    })

    # M22 (Am7): "活得精彩。"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Am7", "text": "活", "notes": [{"string": 5, "fret": 0}, {"string": 2, "fret": 3}]}, # 2
            {"duration": "eighth", "text": "得", "notes": [{"string": 2, "fret": 3}]}, # 2
            {"duration": "eighth", "text": "精", "notes": [{"string": 2, "fret": 1}]}, # 1
            {"duration": "eighth", "text": "彩", "notes": [{"string": 3, "fret": 2}]}  # 6
        ]
    })

    # M23 (Dm7): "有些人总会来，" (4个八分音符 = 2拍)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Dm7", "text": "有", "notes": [{"string": 4, "fret": 0}, {"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "些", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "人", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "text": "来，", "notes": [{"string": 2, "fret": 1, "vibrato": True}]}
        ]
    })

    # M24 (G): "有些人在我心中在徘徊"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "有", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "些", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "人", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "在", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "心", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # =============================================================
    # 四、副歌抒情高潮 (Pre-Chorus & Chorus, M25 - M40)
    # "我拿了总会还，你拿了就逃开... 我给你的爱，我给你的爱..."
    # =============================================================
    # M25 (Fmaj7): "我拿了总会还"
    measures.append({
        "marker": "Chorus (副歌推进: 我拿了总会还)",
        "beats": [
            {"duration": "eighth", "chord": "Fmaj7", "text": "我", "notes": [{"string": 4, "fret": 3}, {"string": 3, "fret": 0}]},
            {"duration": "eighth", "text": "拿", "notes": [{"string": 1, "fret": 0}]}, # 3
            {"duration": "eighth", "text": "了", "notes": [{"string": 2, "fret": 3}]}, # 2
            {"duration": "eighth", "text": "还", "notes": [{"string": 1, "fret": 0}]}  # 3
        ]
    })

    # M26 (G): "你拿了就逃开"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "G", "text": "你", "notes": [{"string": 6, "fret": 3}, {"string": 1, "fret": 3, "vibrato": True}]}, # 5
            {"duration": "eighth", "text": "拿", "notes": [{"string": 1, "fret": 0}]}, # 3
            {"duration": "eighth", "text": "逃开", "notes": [{"string": 2, "fret": 3}]} # 2
        ]
    })

    # M27 (Em7): "在失去中我慢慢的变呆"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Em7", "text": "在", "notes": [{"string": 6, "fret": 0}, {"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "失", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "去", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "变呆", "notes": [{"string": 2, "fret": 0}]}
        ]
    })

    # M28 (Am7): "是不同步的未来"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "Am7", "notes": [{"string": 5, "fret": 0}, {"string": 2, "fret": 1, "vibrato": True}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # M29 (Dm7): "却把书包中的日记更改"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Dm7", "notes": [{"string": 4, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 3}]}, # 5
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]}, # 3
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3}]}  # 2
        ]
    })

    # M30 (G): "把心慢慢的释怀"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 3}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M31 (C): "我相信总有一天你会明白"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "C", "notes": [{"string": 5, "fret": 3}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "quarter", "notes": [{"string": 2, "fret": 3, "vibrato": True, "letRing": True}]}
        ]
    })

    # M32 (C): 节奏过渡
    measures.append({
        "beats": [
            {"duration": "quarter", "stroke": "down", "notes": [{"string": 5, "fret": 3}, {"string": 4, "fret": 2}, {"string": 3, "fret": 0}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M33 (Fmaj7): "我给你的爱" (第1遍)
    measures.append({
        "marker": "我给你的爱 (核心Hook段)",
        "beats": [
            {"duration": "quarter", "chord": "Fmaj7", "text": "我给", "notes": [{"string": 4, "fret": 3}, {"string": 2, "fret": 3}]}, # 2
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "的", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "eighth", "text": "爱", "notes": [{"string": 2, "fret": 1, "vibrato": True}]} # 1
        ]
    })

    # M34 (G): "我给你的爱" (第2遍 旋律升至Mi 1弦0品)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "G", "text": "我给", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 1}]}, # 1
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 0}]}, # 5
            {"duration": "16th", "text": "的", "notes": [{"string": 3, "fret": 2}]}, # 6
            {"duration": "eighth", "text": "爱", "notes": [{"string": 1, "fret": 0, "vibrato": True}]} # 3
        ]
    })

    # M35 (Em7): "我给你的爱" (第3遍)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "Em7", "text": "我给", "notes": [{"string": 6, "fret": 0}, {"string": 2, "fret": 3}]}, # 2
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "的", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "爱", "notes": [{"string": 2, "fret": 1, "vibrato": True}]}
        ]
    })

    # M36 (Am7): "我给你的爱" (第4遍 情感浓郁)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "Am7", "text": "我给", "notes": [{"string": 5, "fret": 0}, {"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "的", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "爱~", "notes": [{"string": 2, "fret": 1, "vibrato": True, "letRing": True}]}
        ]
    })

    # =============================================================
    # 五、间奏与快嘴说唱律动段 (Rap Bridge, M37 - M44)
    # "噢疼不疼痛不痛这样一直被动，幻想中我的梦总会过分要命的冏..."
    # 结合拇指切音打板 (P.M.) 与 16分音符快速点弹
    # =============================================================
    # M37 (Fmaj7): 掌根轻闷音律动 (Palm Mute)
    measures.append({
        "marker": "Rap Bridge (轻快闷音打板节奏)",
        "beats": [
            {"duration": "eighth", "chord": "Fmaj7", "notes": [{"string": 4, "fret": 3}, {"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M38 (G): "疼不疼痛不痛"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]}
        ]
    })

    # M39 (Em7): "幻想中我的梦"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Em7", "notes": [{"string": 6, "fret": 0}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]}, # 3
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3}]}  # 2
        ]
    })

    # M40 (Am7): "总会过分要命的冏"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Am7", "notes": [{"string": 5, "fret": 0}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M41 (Dm7): "在去年夏天跟你说了一个小小要求"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Dm7", "notes": [{"string": 4, "fret": 0}, {"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M42 (G): "答应了不放手而如今也再不回头"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3}]}
        ]
    })

    # =============================================================
    # 六、尾声 (Outro, M43 - M46)
    # 重现前奏 Mi Sol Sol Re 音型，渐慢弱化，空灵泛音收尾
    # =============================================================
    # M43 (Fmaj7): 渐慢 (Ritardando)
    measures.append({
        "marker": "Outro (尾声回味 渐慢渐弱)",
        "beats": [
            {"duration": "eighth", "chord": "Fmaj7", "notes": [{"string": 4, "fret": 3}, {"string": 1, "fret": 0, "letRing": True}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M44 (G): G 和弦分解
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 1, "fret": 0, "letRing": True}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "quarter", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M45 (Cadd9): 慢速滚奏琶音
    measures.append({
        "beats": [
            {
                "duration": "half",
                "chord": "C",
                "stroke": "down",
                "text": "慢速琶音~",
                "notes": [
                    {"string": 5, "fret": 3, "letRing": True},
                    {"string": 4, "fret": 2, "letRing": True},
                    {"string": 3, "fret": 0, "letRing": True},
                    {"string": 2, "fret": 1, "letRing": True},
                    {"string": 1, "fret": 0, "letRing": True, "vibrato": True}
                ]
            }
        ]
    })

    # M46: 12品自然泛音长鸣 (Fine)
    measures.append({
        "marker": "12品自然泛音长鸣 (Fine)",
        "beats": [
            {
                "duration": "half",
                "text": "12品自然泛音~",
                "notes": [
                    {"string": 1, "fret": 12, "letRing": True},
                    {"string": 2, "fret": 12, "letRing": True},
                    {"string": 3, "fret": 12, "letRing": True}
                ]
            }
        ]
    })

    print(f"Total measures created: {len(measures)}")
    editor.write_measures(track_number=1, start_measure=1, measures_data=measures)

    # 保存 GP5
    editor.save(gp5_path, backup=False)
    print(f"GP5 saved: {gp5_path}")

    # 保存 TG
    write_tg(editor.song, tg_path)
    print(f"TG saved: {tg_path}")

if __name__ == "__main__":
    create_score()
