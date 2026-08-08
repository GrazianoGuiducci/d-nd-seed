import importlib.util
import pathlib
import types
import unittest

SCRIPT = pathlib.Path(__file__).parents[1] / "scripts" / "transcribe.py"
SPEC = importlib.util.spec_from_file_location("seed_youtube_transcript", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class FakeTranscript:
    def __init__(self, language_code, generated):
        self.language_code = language_code
        self.is_generated = generated

    def fetch(self):
        return [types.SimpleNamespace(start=1.5, duration=2.0, text="hello world")]


class TranscriptContractTests(unittest.TestCase):
    def test_extracts_supported_url_shapes(self):
        video_id = "xgkjtF89-44"
        urls = [
            video_id,
            f"https://www.youtube.com/watch?v={video_id}",
            f"https://youtu.be/{video_id}",
            f"https://www.youtube.com/shorts/{video_id}",
            f"https://www.youtube.com/embed/{video_id}",
        ]
        self.assertEqual([MODULE.extract_video_id(url) for url in urls], [video_id] * len(urls))

    def test_rejects_non_youtube_hosts(self):
        self.assertIsNone(MODULE.extract_video_id("https://example.com/watch?v=xgkjtF89-44"))

    def test_prefers_manual_requested_language(self):
        generated_it = FakeTranscript("it", True)
        manual_en = FakeTranscript("en", False)
        manual_it = FakeTranscript("it", False)
        chosen = MODULE.select_transcript([generated_it, manual_en, manual_it], ["it", "en"])
        self.assertIs(chosen, manual_it)

    def test_falls_back_to_any_available_transcript(self):
        transcript = FakeTranscript("de", True)
        self.assertIs(MODULE.select_transcript([transcript], ["it", "en"]), transcript)

    def test_normalizes_object_segments(self):
        segment = MODULE._segment_dict(types.SimpleNamespace(start=1, duration=2, text="hello"))
        self.assertEqual(segment, {"start": 1.0, "duration": 2.0, "text": "hello"})


if __name__ == "__main__":
    unittest.main()
