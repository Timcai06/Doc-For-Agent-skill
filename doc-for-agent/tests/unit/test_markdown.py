from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from doc_for_agent_generator.markdown import MANUAL_END, MANUAL_START, merge_markdown


class MarkdownMergeTests(unittest.TestCase):
    def test_merge_markdown_preserves_explicit_manual_blocks(self) -> None:
        existing = f"""# Product

## Confirmed Facts

- Auto-generated fact.

{MANUAL_START}
- Keep this human note.
{MANUAL_END}
"""
        generated = """# Product

## Confirmed Facts

- Regenerated fact.
"""
        merged = merge_markdown(existing, generated)

        self.assertIn("- Regenerated fact.", merged)
        self.assertIn("- Keep this human note.", merged)
        self.assertIn(MANUAL_START, merged)
        self.assertIn(MANUAL_END, merged)

    def test_merge_markdown_preserves_manual_sections_not_in_generated_output(self) -> None:
        existing = """# Product

## Custom Section

- This note was written by a human and should stay.
"""
        generated = """# Product

## Confirmed Facts

- Generated replacement.
"""
        merged = merge_markdown(existing, generated)

        self.assertIn("## Preserved Notes", merged)
        self.assertIn("Custom Section", merged)
        self.assertIn("This note was written by a human and should stay.", merged)


if __name__ == "__main__":
    unittest.main()
