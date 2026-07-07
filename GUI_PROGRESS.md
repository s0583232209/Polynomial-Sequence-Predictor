# GUI Build Progress

Working log for the PyQt5 GUI. Updated after every file so nothing is lost if the
session drops (previous attempt lost everything to a network-filter error before
any file reached disk).

## Plan

- `predict.py` — refactor into a reusable `predict_sequence(sequence) -> list[float]` function
  (kept the old CLI behavior under `if __name__ == "__main__"`).
- `gui/styles.py` — light "mathematics" theme QSS stylesheet.
- `gui/graph_canvas.py` — matplotlib canvas embedded in Qt, plots input points + predicted points.
- `gui/predict_worker.py` — QThread worker so inference doesn't freeze the UI.
- `gui/main_window.py` — QMainWindow: 8 input fields, Predict/Clear/Load-example buttons,
  3 output fields, embedded graph.
- `main.py` — entry point that launches `QApplication` + `MainWindow`.
- `requirements.txt` — add `PyQt5`.

## Status

| File | Status |
|---|---|
| predict.py refactor | done |
| gui/styles.py | done |
| gui/graph_canvas.py | done |
| gui/predict_worker.py | done |
| gui/main_window.py | done |
| main.py | done |
| requirements.txt | done |
| Smoke test (imports without crashing) | done |

## How to run

```bash
pip install -r requirements.txt
python main.py
```

Requires `best_model.pth` at the project root (already present, gitignored).
If it's missing, the GUI still opens but the Predict button is disabled and shows
"Model not found".

## Notes / gotchas discovered while building

- **Critical: import `predict` (torch) before PyQt5, anywhere in the process.**
  On this machine, if PyQt5 is imported before torch, torch's `c10.dll` fails
  to initialize (`OSError: [WinError 1114]`). Once PyQt5's bundled Qt5 DLL
  directory is added to the process's DLL search path, it appears to shadow a
  dependency torch needs. Fix applied in `main.py`: `import predict` is the
  very first import, before any `PyQt5`/`gui` import. If you ever add a new
  entry point, keep that ordering.
- The system Python (`AppData\Local\Python\bin\python.exe`) has torch
  installed and working; the project's `.venv` does not have torch installed
  (only matplotlib/PyQt5 were added there during testing). Run the GUI with
  whichever interpreter has torch — check with
  `python -c "import torch"` first if unsure.
- Verified end-to-end with the real trained `best_model.pth`: example sequence
  `[5, 8, 13, 20, 29, 40, 53, 68]` → predicted `[86.1, 107, 130.8]` (true
  continuation is `85, 104, 125` — close, consistent with the ~0.08 test loss
  in `markdown.md`).
- Tested both the synchronous `predict_sequence()` call and the full async
  path (clicking Predict → `PredictWorker` QThread → output labels update).
  Both pass headlessly with `QT_QPA_PLATFORM=offscreen`.
- `gui/graph_canvas.py` uses matplotlib's generic `"QtAgg"` backend (not
  `"Qt5Agg"`) so it auto-detects whichever Qt binding is installed.

## Round 2 — visual feedback fixes

User feedback: input labels (a0, a1, ...) were too small/unreadable, and the
navy+gold palette read as "depressing". Changes made:

- `gui/styles.py` — repalletted from navy/gold to a livelier blue (`#2F80ED`)
  + teal (`#0FA88F`) + coral (`#FF6B4A`) scheme; body font switched from
  serif Georgia to sans-serif Segoe UI (friendlier). Input/output section
  labels and field-index labels (`a0`, `a1`, ...) now use distinct object
  names (`sectionLabelInput`/`sectionLabelOutput`,
  `fieldIndexInput`/`fieldIndexOutput`) so each card gets its own accent
  color.
- `gui/main_window.py` — input/output fields grew from 72x28 to a fixed
  96x46; field-index label font 11px → 17px bold; window minimum size bumped
  to 1220x700 (was 900x650) to fit the bigger fields; title now renders the
  ∑ symbol in coral via rich-text HTML in the QLabel.
- `gui/graph_canvas.py` — plot colors updated to match (blue input line/dots,
  coral predicted line/diamonds).
- Verified layout/sizing/colors via an offscreen `grab()` screenshot.
  **Note:** text does not render at all in `QT_QPA_PLATFORM=offscreen`
  screenshots on this machine — confirmed with a blank throwaway QLabel test,
  it's a headless-platform limitation, not a bug. Only trust screenshots for
  layout/color/sizing; verify text by running the real windowed app.

## Round 3 — still too small / graph too dominant

User feedback: font still not readable enough, graph section should be much
smaller, input section much bigger.

- `gui/main_window.py` — swapped the vertical stretch: `body` (input +
  output cards) now gets `root.addLayout(body, 1)` so it claims the
  window's spare height; the graph card gets `setMaximumHeight(190)` (was
  `setMinimumHeight(300)`) so it stays small and fixed instead of expanding.
  Input:output card width ratio set to 2:1 via stretch factors.
  Input/output fields grew again, 96x46 → **150x84**. Output card's 3 fields
  switched from a horizontal row to a vertical stack (fits better in the
  now-narrower output column). Window minimum size bumped to 1400x820
  (was 1220x700). Added `layout.addStretch()` at the top of both card
  layouts (in addition to the existing one at the bottom) so the now-taller
  cards center their content vertically instead of pooling empty space at
  the bottom.
- `gui/styles.py` — most font sizes roughly doubled again: field values
  20px → **34px**, field index labels (a0, a1...) 17px → **30px**, section
  labels 14px → 22px, title 26px → 34px, buttons scaled up to match.
- `gui/graph_canvas.py` — figure height shrunk (`figsize=(5, 3)` →
  `(5, 1.7)`), the "Sequence" title above the plot was dropped to save
  vertical space, tick/axis label font sizes trimmed slightly (9/10 → 8/9)
  since the plot area is now much more compact.
- Re-verified with a fresh offscreen screenshot (layout/color only, per the
  known text-rendering limitation above) and the full async
  Predict-button → QThread → output-label regression test — both pass.
