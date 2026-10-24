import os
import json
import unittest
import tempfile

from tuxguitar_mcp.models import SongData, TrackData, MeasureData, BeatData, NoteData, NoteEffectData, ChordData
from tuxguitar_mcp.tg_parser import parse_tg, write_tg
from tuxguitar_mcp.gp_adapter import parse_gp, write_gp
from tuxguitar_mcp.song_editor import SongEditor
from tuxguitar_mcp.ascii_tab import render_ascii_tab
from tuxguitar_mcp.chords import get_chord, list_available_chords
from tuxguitar_mcp.server import (
    tuxguitar_get_score_summary,
    tuxguitar_read_measures,
    tuxguitar_get_ascii_tab,
    tuxguitar_create_score,
    tuxguitar_add_track,
    tuxguitar_write_measures,
    tuxguitar_add_riff,
    tuxguitar_add_chord_progression,
    tuxguitar_transpose,
    tuxguitar_get_chord_info,
    tuxguitar_list_chords,
    tuxguitar_convert_format,
    tuxguitar_app_status
)


class TestTuxGuitarMCP(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.demo_tg = os.path.join(os.path.dirname(__file__), "..", "..", "share", "demo-songs", "tuxguitar.tg")

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_demo_tg_parsing(self):
        self.assertTrue(os.path.exists(self.demo_tg), f"Demo file missing: {self.demo_tg}")
        song = parse_tg(self.demo_tg)
        self.assertEqual(song.title, "Guitar tuner")
        self.assertGreater(len(song.tracks), 0)
        self.assertEqual(song.tracks[0].strings, [64, 59, 55, 50, 45, 40])
        self.assertEqual(song.measure_count, 18)

    def test_tg_roundtrip(self):
        song = parse_tg(self.demo_tg)
        out_tg = os.path.join(self.temp_dir, "roundtrip.tg")
        write_tg(song, out_tg)
        
        song2 = parse_tg(out_tg)
        self.assertEqual(song2.title, song.title)
        self.assertEqual(song2.measure_count, song.measure_count)
        self.assertEqual(len(song2.tracks), len(song.tracks))

    def test_create_and_edit_gp5(self):
        gp5_path = os.path.join(self.temp_dir, "test_song.gp5")
        editor = SongEditor()
        editor.create_new(
            file_path=gp5_path,
            title="Antigravity Riff",
            artist="DeepMind AI",
            tempo=130,
            time_signature="4/4",
            track_presets=[
                {"name": "Lead Guitar", "tuning": "standard_6", "instrument": "distortion_guitar"},
                {"name": "Bass", "tuning": "bass_4_standard", "instrument": "electric_bass_pick"}
            ]
        )
        editor.save(backup=False)
        self.assertTrue(os.path.exists(gp5_path))

        # Add chord progression to rhythm
        res_chords = editor.add_chord_progression(
            track_number=1,
            start_measure=1,
            progression=["Am", "C", "G", "F"],
            strum_pattern="quarter_4"
        )
        self.assertTrue(res_chords.get("success"))
        editor.save(backup=False)

        # Add solo riff to lead
        solo_notes = [
            {"string": 3, "fret": 7, "duration": "eighth"},
            {"string": 3, "fret": 9, "duration": "eighth", "hammer": True},
            {"string": 2, "fret": 8, "duration": "eighth"},
            {"string": 2, "fret": 10, "duration": "eighth", "bend_semitones": 2.0},
            {"string": 1, "fret": 8, "duration": "quarter"},
            {"string": 1, "fret": 10, "duration": "quarter", "vibrato": True},
        ]
        res_riff = editor.add_riff(
            track_number=1,
            start_measure=5,
            notes_list=solo_notes,
            default_duration="eighth"
        )
        self.assertTrue(res_riff.get("success"))
        editor.save(backup=False)

        # Transpose
        trans_res = editor.transpose(track_number=1, semitones=2)
        self.assertTrue(trans_res.get("success"))
        editor.save(backup=False)

        # Read back
        editor2 = SongEditor(gp5_path)
        summary = editor2.get_summary()
        self.assertEqual(summary["title"], "Antigravity Riff")
        self.assertEqual(len(summary["tracks"]), 2)
        self.assertGreaterEqual(summary["total_measures"], 5)

        # Render ASCII
        ascii_tab = editor2.render_ascii(track_number=1, start_measure=1, end_measure=4)
        self.assertIn("Lead Guitar", ascii_tab)
        self.assertIn("Am", ascii_tab)

    def test_tg_format_conversion(self):
        # TG -> GP5 -> TG
        gp5_out = os.path.join(self.temp_dir, "converted.gp5")
        tg_out = os.path.join(self.temp_dir, "converted_back.tg")

        ed1 = SongEditor(self.demo_tg)
        ed1.save(gp5_out, backup=False)
        self.assertTrue(os.path.exists(gp5_out))

        ed2 = SongEditor(gp5_out)
        self.assertEqual(ed2.song.title, "Guitar tuner")
        ed2.save(tg_out, backup=False)
        self.assertTrue(os.path.exists(tg_out))

        ed3 = SongEditor(tg_out)
        self.assertEqual(ed3.song.title, "Guitar tuner")

    def test_chord_library(self):
        chord_c = get_chord("C")
        self.assertIsNotNone(chord_c)
        self.assertEqual(chord_c["strings"], [0, 1, 0, 2, 3, -1])

        all_chords = list_available_chords()
        self.assertIn("Am", all_chords)
        self.assertIn("G7", all_chords)
        self.assertIn("Cmaj7", all_chords)
        self.assertIn("E5", all_chords)

    def test_mcp_tools_api(self):
        # 1. Status
        status_json = json.loads(tuxguitar_app_status())
        self.assertTrue(status_json["installed"])

        # 2. Chord info
        chord_json = json.loads(tuxguitar_get_chord_info("Am"))
        self.assertEqual(chord_json["name"], "Am")

        # 3. Create score via MCP tool
        test_file = os.path.join(self.temp_dir, "mcp_created.gp5")
        create_res = json.loads(tuxguitar_create_score(
            file_path=test_file,
            title="MCP Test Song",
            artist="AI Bot",
            tempo=120,
            time_signature="4/4"
        ))
        self.assertTrue(create_res["success"])

        # 4. Summary via MCP tool
        summary_res = json.loads(tuxguitar_get_score_summary(test_file))
        self.assertEqual(summary_res["title"], "MCP Test Song")

        # 5. Add chord progression
        chords_res = json.loads(tuxguitar_add_chord_progression(
            file_path=test_file,
            track_number=1,
            start_measure=1,
            progression=["Em", "G", "D", "A"],
            strum_pattern="quarter_4"
        ))
        self.assertTrue(chords_res["success"])

        # 6. Read measures
        measures_res = json.loads(tuxguitar_read_measures(test_file, track_number=1, start_measure=1, end_measure=2))
        self.assertEqual(len(measures_res["measures"]), 2)

        # 7. Render tab
        tab_str = tuxguitar_get_ascii_tab(test_file, track_number=1, start_measure=1, end_measure=2)
        self.assertIn("Track: 1", tab_str)


if __name__ == "__main__":
    unittest.main()
