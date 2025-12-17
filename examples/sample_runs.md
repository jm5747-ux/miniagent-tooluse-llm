## Sample Runs

### 1) Calculator
Command:
python -m miniagent.cli --task "calculate (45*3) / 5"

Expected:
- tool_called: calculator
- final result printed

### 2) Notes Lookup
Command:
python -m miniagent.cli --task "lookup notes: hallucinations"

Expected:
- matches from data/notes.txt

Output:
- Line X: RAG systems reduce hallucinations by grounding answers in retrieved text.
- Line Y: Hallucinations occur when language models generate information not grounded in source data.

### 3) URL Fetch
Command:
python -m miniagent.cli --task "fetch https://example.com"

Expected:
- fetched content preview