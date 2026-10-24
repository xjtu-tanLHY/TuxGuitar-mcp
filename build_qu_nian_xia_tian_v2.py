import os
from tuxguitar_mcp.song_editor import SongEditor
from tuxguitar_mcp.models import NoteData, NoteEffectData, BeatData, MeasureData, ChordData, TrackData
from tuxguitar_mcp.tg_parser import write_tg

def create_score_v2():
    gp5_path = r"d:\Program Files\tuxguitar\qu_nian_xia_tian_fingerstyle.gp5"
    tg_path = r"d:\Program Files\tuxguitar\qu_nian_xia_tian_fingerstyle.tg"

    editor = SongEditor()
    editor.create_new(
        file_path=gp5_path,
        title="去年夏天 (吉他指弹独奏版 - 歌词根音精准对位版)",
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
    # 2/4 拍, 每小节 2 拍 (1920 ticks)
    # 标准 6 弦: 1=E4, 2=B3, 3=G3, 4=D3, 5=A2, 6=E2
    # 核心特点:
    # 1. 根音与每句话的押韵句尾字(如"在"、"待"、"哀"、"来")强拍完全重合对齐!
    # 2. 强拍采用双音(低音根音+高音旋律音)同时发声, 丰满动听!
    # 3. 每一个唱词字都有精准对应的十六分音符/八分音符旋律!
    # -------------------------------------------------------------
    measures = []

    # =============================================================
    # 一、前奏 (Intro, M1 - M8)
    # 标志性八音盒合成器音型: 3 5 5 2 (Mi Sol Sol Re)
    # =============================================================
    # M1: C和弦开场 (0 5 5 2)
    measures.append({
        "marker": "Intro (清脆八音盒开场)",
        "beats": [
            {"duration": "eighth", "chord": "C", "notes": [{"string": 5, "fret": 3}, {"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "quarter", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M2: Am7 和弦 (3 5 5 2)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Am7", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M3: Fmaj7 和弦 (3 5 5 2)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Fmaj7", "notes": [{"string": 4, "fret": 3}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M4: G 和弦 (3 5 5 2)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
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

    # M6: Am7 (6. 5 -> A4 G4, 2拍整)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "Am7", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 5}]}, # A4
            {"duration": "quarter", "notes": [{"string": 1, "fret": 3}]}  # G4
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

    # M8: G 和弦长音 + 弱起进唱 "还有什么" (0 5 5 6 1 6)
    measures.append({
        "beats": [
            # Beat 1: G 和弦根音 + 旋律 D4 (半拍) + 八分休止符
            {"duration": "quarter", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 3, "letRing": True}]},
            # Beat 2: 弱起进唱 4个十六分音符 "还有什么" (5 5 6 1)
            {"duration": "16th", "text": "还", "notes": [{"string": 3, "fret": 0}]}, # 5 (G3)
            {"duration": "16th", "text": "有", "notes": [{"string": 3, "fret": 0}]}, # 5 (G3)
            {"duration": "16th", "text": "什", "notes": [{"string": 3, "fret": 2}]}, # 6 (A3)
            {"duration": "16th", "text": "么", "notes": [{"string": 2, "fret": 1}]}  # 1 (C4)
        ]
    })

    # =============================================================
    # 二、主歌第一段 (Verse 1, M9 - M16)
    # 严格对齐:
    # M9:  "待？" + Fmaj7 根音! 紧接着 "还有什么悲"
    # M10: "哀？" + G 根音! 紧接着 "这故事中的"
    # M11: "人不太精彩" + Em7 根音!
    # M12: "夏去了又回" + Am7 根音!
    # M13: "来，" + Fmaj7 根音! 紧接着 "而人却已不"
    # M14: "在，" + G 根音! 紧接着 "它重复着我" (用户特别指出的关键点!)
    # M15: "汹涌的忍耐" + Em7 根音!
    # M16: "今年兰花又" + Am7 根音!
    # =============================================================
    # M9 (Fmaj7): "待？" 双音卡点! + "还有什么悲"
    measures.append({
        "marker": "Verse 1 (待？还有什么悲)",
        "beats": [
            # Beat 1: 双音! F3(4弦3品根音) + E4(1弦0品旋律"待？") (附点八分) + "还"(16分)
            {"duration": "eighth", "dotted": True, "chord": "Fmaj7", "text": "待？", "notes": [
                {"string": 4, "fret": 3},
                {"string": 1, "fret": 0, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "还", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: 4个十六分音符 "有什么悲" (5 6 1 6)
            {"duration": "16th", "text": "有", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "什", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "么", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "悲", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M10 (G): "哀？" 双音卡点! + "这故事中的"
    measures.append({
        "beats": [
            # Beat 1: 双音! G2(6弦3品根音) + D4(2弦3品旋律"哀？") (附点八分) + "这"(16分)
            {"duration": "eighth", "dotted": True, "chord": "G", "text": "哀？", "notes": [
                {"string": 6, "fret": 3},
                {"string": 2, "fret": 3, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "这", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: 4个十六分音符 "故事中的" (5 6 1 6)
            {"duration": "16th", "text": "故", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "事", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "中", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "的", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M11 (Em7): "人不太精彩" (3 2 2 2 1 6)
    measures.append({
        "beats": [
            # Beat 1: 双音! E2(6弦0品根音) + E4(1弦0品"人") (八分) + D4(2弦3品"不") (八分)
            {"duration": "eighth", "chord": "Em7", "text": "人", "notes": [{"string": 6, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "不", "notes": [{"string": 2, "fret": 3}]},
            # Beat 2: 4个十六分音符 "太精彩。" (2 2 1 6)
            {"duration": "16th", "text": "太", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "精", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "彩", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M12 (Am7): "夏去了又回" (6 6 1 5 5 6 1 6)
    measures.append({
        "beats": [
            # Beat 1: 双音! A2(5弦0品根音) + A3(3弦2品"夏") (16分) + A3("去") + C4("了") + G3("又")
            {"duration": "16th", "chord": "Am7", "text": "夏", "notes": [{"string": 5, "fret": 0}, {"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "去", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "了", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "又", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: 4个十六分音符 "回..." (5 6 1 6)
            {"duration": "16th", "text": "回", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M13 (Fmaj7): "来，" 双音卡点! + "而人却已不"
    measures.append({
        "beats": [
            # Beat 1: 双音! F3(4弦3品根音) + C4(2弦1品旋律"来，") (附点八分) + "而"(16分)
            {"duration": "eighth", "dotted": True, "chord": "Fmaj7", "text": "来，", "notes": [
                {"string": 4, "fret": 3},
                {"string": 2, "fret": 1, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "而", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: 4个十六分音符 "人却已不" (5 6 1 6)
            {"duration": "16th", "text": "人", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "却", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "已", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "不", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M14 (G): "在，" 双音卡点 (用户最强调的核心点: 根音接到"在"上!)
    measures.append({
        "marker": "人却已不在 (在接G根音双音!)",
        "beats": [
            # Beat 1: 双音! G2(6弦3品G根音) + D4(2弦3品旋律"在，") (附点八分) + "它"(16分)
            {"duration": "eighth", "dotted": True, "chord": "G", "text": "在，", "notes": [
                {"string": 6, "fret": 3},
                {"string": 2, "fret": 3, "heavyAccentuated": True, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "它", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: 4个十六分音符 "重复着我" (5 6 1 6)
            {"duration": "16th", "text": "重", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "复", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "着", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "我", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M15 (Em7): "汹涌的忍耐" (3 2 2 2 1 2)
    measures.append({
        "beats": [
            # Beat 1: 双音! E2(6弦0品根音) + E4(1弦0品"汹") + D4("涌")
            {"duration": "eighth", "chord": "Em7", "text": "汹", "notes": [{"string": 6, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "涌", "notes": [{"string": 2, "fret": 3}]},
            # Beat 2: "的忍耐" (2 2 1 2)
            {"duration": "16th", "text": "的", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "忍", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "耐", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 3}]}
        ]
    })

    # M16 (Am7): "今年兰花又"
    measures.append({
        "beats": [
            # Beat 1: 双音! A2(5弦0品根音) + D4(2弦3品) (附点八分) + "今"(16分)
            {"duration": "eighth", "dotted": True, "chord": "Am7", "notes": [{"string": 5, "fret": 0}, {"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "今", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: "年兰花又" (5 6 1 6)
            {"duration": "16th", "text": "年", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "兰", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "花", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "又", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # =============================================================
    # 三、主歌第二段 (Verse 2, M17 - M24)
    # 开、败、精彩、来、徘徊
    # =============================================================
    # M17 (Fmaj7): "开，" 双音卡点! + "开了它也会"
    measures.append({
        "marker": "Verse 2 (兰花又开，开了它也会败)",
        "beats": [
            # Beat 1: 双音! F3(4弦3品根音) + E4(1弦0品"开，") (附点八分) + "开"(16分)
            {"duration": "eighth", "dotted": True, "chord": "Fmaj7", "text": "开，", "notes": [
                {"string": 4, "fret": 3},
                {"string": 1, "fret": 0, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "开", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: "了它也会" (5 6 1 6)
            {"duration": "16th", "text": "了", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "它", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "也", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "会", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M18 (G): "败，" 双音卡点! + "我想要一个"
    measures.append({
        "beats": [
            # Beat 1: 双音! G2(6弦3品根音) + D4(2弦3品"败，") (附点八分) + "我"(16分)
            {"duration": "eighth", "dotted": True, "chord": "G", "text": "败，", "notes": [
                {"string": 6, "fret": 3},
                {"string": 2, "fret": 3, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "我", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: "想要一个" (5 6 1 6)
            {"duration": "16th", "text": "想", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "要", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "一", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "个", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M19 (Em7): "人活得精彩" (3 2 2 2 1 6)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Em7", "text": "人", "notes": [{"string": 6, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "活", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "得", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "精", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "彩", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M20 (Am7): "有些人总会" (6 1 5 5 6 1 6)
    measures.append({
        "beats": [
            {"duration": "16th", "chord": "Am7", "text": "有", "notes": [{"string": 5, "fret": 0}, {"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "些", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "人", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "总", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "会", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M21 (Dm7): "来，" 双音卡点! + "有些人在我"
    measures.append({
        "beats": [
            {"duration": "eighth", "dotted": True, "chord": "Dm7", "text": "来，", "notes": [
                {"string": 4, "fret": 0},
                {"string": 2, "fret": 1, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "有", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "些", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "人", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "在", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "我", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M22 (G): "心中在徘徊" (3 2 2 2 1)
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "text": "心", "notes": [{"string": 6, "fret": 3}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "中", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "在", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "徘徊", "notes": [{"string": 2, "fret": 1, "vibrato": True}]}
        ]
    })

    # M23 (C): 间奏过渡解决 (1 1 1 2)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C", "notes": [{"string": 5, "fret": 3}, {"string": 2, "fret": 1}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "notes": [{"string": 2, "fret": 3}]}
        ]
    })

    # M24 (G): "我拿了总会" (弱起连接)
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "我", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "拿", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "16th", "text": "了", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "总", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # =============================================================
    # 四、副歌抒情段 (Pre-Chorus & Chorus, M25 - M40)
    # 还、开、呆、改、盖、该、白
    # =============================================================
    # M25 (Fmaj7): "还，" 双音卡点! + "你拿了就逃"
    measures.append({
        "marker": "Chorus (我拿了总会还，你拿了就逃开)",
        "beats": [
            # Beat 1: 双音! F3(4弦3品根音) + G4(1弦3品"还，") (附点八分) + "你"(16分)
            {"duration": "eighth", "dotted": True, "chord": "Fmaj7", "text": "还，", "notes": [
                {"string": 4, "fret": 3},
                {"string": 1, "fret": 3, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: "拿了就逃"
            {"duration": "16th", "text": "拿", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "16th", "text": "了", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "就逃", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # M26 (G): "开，" 双音卡点! + "在失去中我"
    measures.append({
        "beats": [
            # Beat 1: 双音! G2(6弦3品根音) + D4(2弦3品"开，") (附点八分) + "在"(16分)
            {"duration": "eighth", "dotted": True, "chord": "G", "text": "开，", "notes": [
                {"string": 6, "fret": 3},
                {"string": 2, "fret": 3, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "在", "notes": [{"string": 2, "fret": 3}]},
            # Beat 2: "失去中我" (2 1 6 7)
            {"duration": "16th", "text": "失", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "去", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "中", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "我", "notes": [{"string": 2, "fret": 0}]}
        ]
    })

    # M27 (Em7): "慢慢的变呆。" 双音卡点
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Em7", "text": "慢", "notes": [{"string": 6, "fret": 0}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "慢", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "的", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "变", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "呆", "notes": [{"string": 1, "fret": 0, "vibrato": True}]}
        ]
    })

    # M28 (Am7): "是不同步的未来"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Am7", "text": "是", "notes": [{"string": 5, "fret": 0}, {"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "不", "notes": [{"string": 1, "fret": 3}]},
            {"duration": "eighth", "text": "同", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "步", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M29 (Dm7): "却把书包中的日记"
    measures.append({
        "beats": [
            {"duration": "16th", "chord": "Dm7", "text": "却", "notes": [{"string": 4, "fret": 0}, {"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "把", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "书", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "包", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "text": "中", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "日记", "notes": [{"string": 2, "fret": 3}]}
        ]
    })

    # M30 (G): "更改。" 双音卡点
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "text": "更", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "改", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M31 (C): "把虚伪的尘埃"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "C", "notes": [{"string": 5, "fret": 3}, {"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "把", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "虚", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "16th", "text": "伪", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "的", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # M32 (Fmaj7): "尘埃，" 双音卡点! + "也全部都掩"
    measures.append({
        "beats": [
            {"duration": "eighth", "dotted": True, "chord": "Fmaj7", "text": "埃，", "notes": [
                {"string": 4, "fret": 3},
                {"string": 1, "fret": 3, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "也", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "全", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "16th", "text": "部", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "都掩", "notes": [{"string": 1, "fret": 0}]}
        ]
    })

    # M33 (G): "盖，" 双音卡点! + "把每次心痛"
    measures.append({
        "beats": [
            {"duration": "eighth", "dotted": True, "chord": "G", "text": "盖，", "notes": [
                {"string": 6, "fret": 3},
                {"string": 2, "fret": 3, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "把", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "每", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "次", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "心", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "痛", "notes": [{"string": 2, "fret": 0}]}
        ]
    })

    # M34 (Em7): "都当成活该。" 双音卡点
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Em7", "text": "都", "notes": [{"string": 6, "fret": 0}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "当", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "成", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "活", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "text": "该", "notes": [{"string": 3, "fret": 0, "vibrato": True}]}
        ]
    })

    # M35 (Am7): "把心慢慢的释怀"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Am7", "text": "把", "notes": [{"string": 5, "fret": 0}, {"string": 3, "fret": 0}]},
            {"duration": "eighth", "text": "心", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "释", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "怀", "notes": [{"string": 3, "fret": 2}]}
        ]
    })

    # M36 (Dm7): "我相信总有一天"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "Dm7", "text": "我", "notes": [{"string": 4, "fret": 0}, {"string": 3, "fret": 0}]},
            {"duration": "eighth", "text": "相", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "信", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "总有", "notes": [{"string": 2, "fret": 3}]}
        ]
    })

    # M37 (G): "一天你会"
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "text": "一", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 3}]},
            {"duration": "eighth", "text": "天", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "你", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "会", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M38 (C): "明白。" 双音落地解决
    measures.append({
        "beats": [
            {"duration": "half", "chord": "C", "text": "明白~", "notes": [
                {"string": 5, "fret": 3},
                {"string": 2, "fret": 1, "vibrato": True, "letRing": True}
            ]}
        ]
    })

    # M39 (G): 弱起过渡 "我给你的爱"
    measures.append({
        "beats": [
            {"duration": "quarter", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "我", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "给", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "16th", "text": "的", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # =============================================================
    # 五、核心 Hook: "我给你的爱" (M40 - M45)
    # 4 连强力卡点: 每次"爱"都带低音根音与双音共鸣!
    # =============================================================
    # M40 (Fmaj7): "爱，" 双音卡点! + "我给你的"
    measures.append({
        "marker": "我给你的爱 (核心Hook段)",
        "beats": [
            # Beat 1: 双音! F3(4弦3品根音) + D4(2弦3品"爱，") (附点八分) + "我"(16分)
            {"duration": "eighth", "dotted": True, "chord": "Fmaj7", "text": "爱，", "notes": [
                {"string": 4, "fret": 3},
                {"string": 2, "fret": 3, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "我", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: "给你的"
            {"duration": "16th", "text": "给", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "的", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M41 (G): "爱，" 双音卡点 (高音Mi空弦爆发!) + "我给你的"
    measures.append({
        "beats": [
            # Beat 1: 双音! G2(6弦3品根音) + E4(1弦0品"爱，") (附点八分) + "我"(16分)
            {"duration": "eighth", "dotted": True, "chord": "G", "text": "爱，", "notes": [
                {"string": 6, "fret": 3},
                {"string": 1, "fret": 0, "heavyAccentuated": True, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "我", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: "给你的"
            {"duration": "16th", "text": "给", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "的", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M42 (Em7): "爱，" 双音卡点! + "我给你的"
    measures.append({
        "beats": [
            # Beat 1: 双音! E2(6弦0品根音) + D4(2弦3品"爱，") (附点八分) + "我"(16分)
            {"duration": "eighth", "dotted": True, "chord": "Em7", "text": "爱，", "notes": [
                {"string": 6, "fret": 0},
                {"string": 2, "fret": 3, "vibrato": True, "letRing": True}
            ]},
            {"duration": "16th", "text": "我", "notes": [{"string": 3, "fret": 0}]},
            # Beat 2: "给你的"
            {"duration": "16th", "text": "给", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "16th", "text": "你", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "text": "的", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M43 (Am7): "爱。" 双音终结卡点!
    measures.append({
        "beats": [
            # Beat 1: 双音! A2(5弦0品根音) + C4(2弦1品"爱。") (quarter)
            {"duration": "quarter", "chord": "Am7", "text": "爱~", "notes": [
                {"string": 5, "fret": 0},
                {"string": 2, "fret": 1, "vibrato": True, "letRing": True}
            ]},
            # Beat 2: 和弦拨弦分解
            {"duration": "eighth", "notes": [{"string": 3, "fret": 2}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M44 (C): 落地
    measures.append({
        "beats": [
            {"duration": "half", "chord": "C", "notes": [
                {"string": 5, "fret": 3},
                {"string": 2, "fret": 1, "letRing": True}
            ]}
        ]
    })

    # M45 (间奏过门): E4 -> D4 -> C4
    measures.append({
        "beats": [
            {"duration": "quarter", "notes": [{"string": 1, "fret": 0, "vibrato": True}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # =============================================================
    # 六、快嘴说唱律动段 (Rap Bridge, M46 - M52)
    # "噢疼不疼痛不痛这样一直被动，幻想中我的梦总会过分要命的冏..."
    # 结合每小节强拍低音根音双音 + 十六分音符快速点弹与闷音律动
    # =============================================================
    # M46 (Fmaj7): "噢疼不疼痛不痛"
    measures.append({
        "marker": "Rap Bridge (字字对音快嘴律动)",
        "beats": [
            # Beat 1: 双音! F3(4弦3品) + C4(2弦1品"噢") (16分) + "疼"("不")("疼")
            {"duration": "16th", "chord": "Fmaj7", "text": "噢", "notes": [{"string": 4, "fret": 3}, {"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "疼", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "text": "不", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "text": "疼", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            # Beat 2: "痛不痛这"
            {"duration": "16th", "text": "痛", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "text": "不", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "text": "痛", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "text": "这", "notes": [{"string": 2, "fret": 1, "palmMute": True}]}
        ]
    })

    # M47 (G): "样一直被动"
    measures.append({
        "beats": [
            # Beat 1: 双音! G2(6弦3品) + C4(2弦1品"样") + "一"("直")("被")
            {"duration": "16th", "chord": "G", "text": "样", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "一", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "text": "直", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            {"duration": "16th", "text": "被", "notes": [{"string": 2, "fret": 1, "palmMute": True}]},
            # Beat 2: "动" (G3)
            {"duration": "quarter", "text": "动", "notes": [{"string": 3, "fret": 0, "vibrato": True}]}
        ]
    })

    # M48 (Em7): "幻想中我的梦"
    measures.append({
        "beats": [
            # Beat 1: 双音! E2(6弦0品) + C4("幻") + "想"("中")("我")
            {"duration": "16th", "chord": "Em7", "text": "幻", "notes": [{"string": 6, "fret": 0}, {"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "想", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "中", "notes": [{"string": 2, "fret": 1}]},
            {"duration": "16th", "text": "我", "notes": [{"string": 2, "fret": 1}]},
            # Beat 2: "的梦" (1弦0品 Mi 空弦点缀)
            {"duration": "eighth", "text": "的", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "梦", "notes": [{"string": 2, "fret": 3, "vibrato": True}]}
        ]
    })

    # M49 (Am7): "总会过分要命的冏"
    measures.append({
        "beats": [
            # Beat 1: 双音! A2(5弦0品) + C4(2弦1品"总")
            {"duration": "eighth", "chord": "Am7", "text": "总", "notes": [{"string": 5, "fret": 0}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "会", "notes": [{"string": 3, "fret": 2}]},
            # Beat 2: "过分要命的冏"
            {"duration": "16th", "text": "要", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "命", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "的冏", "notes": [{"string": 2, "fret": 1, "vibrato": True}]}
        ]
    })

    # M50 (Dm7): "在去年夏天跟你说了一个小小要求"
    measures.append({
        "beats": [
            # Beat 1: 双音! D3(4弦0品) + G3("在")
            {"duration": "eighth", "chord": "Dm7", "text": "在", "notes": [{"string": 4, "fret": 0}, {"string": 3, "fret": 0}]},
            {"duration": "eighth", "text": "去", "notes": [{"string": 2, "fret": 1}]},
            # Beat 2: "年夏天"
            {"duration": "16th", "text": "夏", "notes": [{"string": 2, "fret": 3}]},
            {"duration": "16th", "text": "天", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "跟说", "notes": [{"string": 2, "fret": 1}]}
        ]
    })

    # M51 (G): "答应了不放手而如今也再不回头"
    measures.append({
        "beats": [
            # Beat 1: 双音! G2(6弦3品) + C4("答")
            {"duration": "eighth", "chord": "G", "text": "答", "notes": [{"string": 6, "fret": 3}, {"string": 2, "fret": 1}]},
            {"duration": "eighth", "text": "应", "notes": [{"string": 2, "fret": 3}]},
            # Beat 2: "再不回头"
            {"duration": "eighth", "text": "不放", "notes": [{"string": 1, "fret": 0}]},
            {"duration": "eighth", "text": "回头", "notes": [{"string": 2, "fret": 3, "vibrato": True}]}
        ]
    })

    # M52 (C): 落地收束
    measures.append({
        "beats": [
            {"duration": "half", "chord": "C", "notes": [
                {"string": 5, "fret": 3},
                {"string": 2, "fret": 1, "letRing": True}
            ]}
        ]
    })

    # =============================================================
    # 七、尾声 (Outro, M53 - M56)
    # 重现前奏 3 5 5 2，渐慢渐弱，12品泛音长鸣收官
    # =============================================================
    # M53 (Fmaj7): 尾声渐慢 (Ritardando)
    measures.append({
        "marker": "Outro (尾声回味 渐慢渐弱)",
        "beats": [
            {"duration": "eighth", "chord": "Fmaj7", "notes": [{"string": 4, "fret": 3}, {"string": 1, "fret": 0, "letRing": True}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "eighth", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M54 (G): G 和弦分解
    measures.append({
        "beats": [
            {"duration": "eighth", "chord": "G", "notes": [{"string": 6, "fret": 3}, {"string": 1, "fret": 0, "letRing": True}]},
            {"duration": "eighth", "notes": [{"string": 3, "fret": 0}]},
            {"duration": "quarter", "notes": [{"string": 2, "fret": 3, "letRing": True}]}
        ]
    })

    # M55 (Cadd9): 慢速深情滚奏
    measures.append({
        "beats": [
            {
                "duration": "half",
                "chord": "C",
                "stroke": "down",
                "text": "慢速深情滚奏~",
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

    # M56: 12品自然泛音长鸣 (Fine)
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
    create_score_v2()
