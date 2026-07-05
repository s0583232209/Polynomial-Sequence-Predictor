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
