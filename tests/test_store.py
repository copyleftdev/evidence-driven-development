from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tiny_tasks.store import Conflict, Store, validate


class Tasks(unittest.TestCase):
    def setUp(self):
        self.scratch = TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.store = Store(Path(self.scratch.name) / "tasks.sqlite")

    def test_retry_returns_the_original_task(self):
        original = self.store.add("Water plants", "one")
        retry = self.store.add("Water plants", "one")
        self.assertEqual(original["task"], retry["task"])
        self.assertTrue(original["created"])
        self.assertFalse(retry["created"])

    def test_conflicting_request_preserves_the_original_title(self):
        original = self.store.add("Water plants", "one")
        with self.assertRaises(Conflict):
            self.store.add("Read a chapter", "one")
        self.assertEqual(self.store.list(), [original["task"]])

    def test_different_requests_can_have_the_same_title(self):
        first = self.store.add("Read a chapter", "one")
        second = self.store.add("Read a chapter", "two")
        self.assertNotEqual(first["task"]["id"], second["task"]["id"])
        self.assertEqual(len(self.store.list()), 2)

    def test_titles_are_normalized_before_comparing_a_retry(self):
        first = self.store.add(" Water plants ", "one")
        self.assertEqual(first["task"], self.store.add("Water plants", "one")["task"])

    def test_invalid_titles_and_request_ids_add_nothing(self):
        for title, key in (("", "one"), (" " * 4, "one"), ("x" * 121, "one"),
                           ("bad\x00title", "one"), ("Task", ""), ("Task", "bad key")):
            with self.subTest(title=repr(title), key=key), self.assertRaises(ValueError):
                self.store.add(title, key)
        self.assertEqual(self.store.list(), [])

    def test_title_boundary_and_unicode_are_valid(self):
        self.assertEqual(validate("x" * 120, "a" * 80), "x" * 120)
        self.assertEqual(self.store.add("Read café notes", "unicode")["task"]["title"], "Read café notes")


if __name__ == "__main__":
    unittest.main()
