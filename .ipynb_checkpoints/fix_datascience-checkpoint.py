"""
fix_datascience.py  --  makes the course autograder checks match locally.

WHY: the `datascience` library hard-codes  np.set_printoptions(legacy='1.13')
on import (datascience/tables.py, from data-8/datascience issue #491). That
forces numpy to print scalars the OLD way (True / 1732) instead of the numpy-2
way (np.True_ / np.float64(1732.0)). The course's otter tests were written
expecting the numpy-2 way, so every "check the printed value" test fails
locally even when the answer is correct.

WHAT: flips that one setting to legacy=False and silences the warning that
datascience raises when legacy mode is off. Nothing about your answers or
the math changes -- only how numbers are *printed*.

Safe to run any number of times. Re-run it if `datascience` ever gets
reinstalled (e.g. by a notebook's `!pip install` cell) and the checks start
showing `True` vs `np.True_` again.

Run:   python fix_datascience.py      (from inside the dat1001 environment)
"""
import importlib.util
import pathlib
import sys

spec = importlib.util.find_spec("datascience")
if spec is None or not spec.submodule_search_locations:
    sys.exit("datascience is not installed in this Python: " + sys.executable)

tables = pathlib.Path(list(spec.submodule_search_locations)[0]) / "tables.py"
src = tables.read_text(encoding="utf-8")
orig = src

OLD_SET = "np.set_printoptions(legacy='1.13')"
NEW_SET = ("np.set_printoptions(legacy=False)"
           "  # PATCHED by fix_datascience.py: was legacy='1.13'; disabled so scalars "
           "print numpy-2 style (np.True_) to match the course autograder")

OLD_WARN = "if np.get_printoptions()['legacy'] != '1.13':"
NEW_WARN = "if False:  # PATCHED by fix_datascience.py: legacy-mode warning disabled"

changed = []
if OLD_SET in src:
    src = src.replace(OLD_SET, NEW_SET, 1)
    changed.append("legacy print mode -> off")
if OLD_WARN in src:
    src = src.replace(OLD_WARN, NEW_WARN, 1)
    changed.append("legacy-mode nag warning -> silenced")

if src != orig:
    tables.write_text(src, encoding="utf-8")
    print("Patched", tables)
    for c in changed:
        print("  -", c)
elif "PATCHED by fix_datascience.py" in src:
    print("Already patched, nothing to do:", tables)
else:
    sys.exit("Could not find the expected lines in " + str(tables) +
             " -- datascience may have changed; patch not applied.")
