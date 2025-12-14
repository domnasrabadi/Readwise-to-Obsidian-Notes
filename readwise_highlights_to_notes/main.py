#!/usr/bin/env python3
from __future__ import annotations

import os
import runpy


def main() -> int:
    project_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(project_dir, "08_make_notes.py")
    runpy.run_path(script_path, run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
