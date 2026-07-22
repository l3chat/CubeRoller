from pathlib import Path

path = Path("cube4d2.html")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        "return Boolean(target.closest('input, textarea, select, button, [contenteditable=\"true\"]'));",
        "return Boolean(target.closest('input, textarea, select, [contenteditable=\"true\"]'));"
    ),
    (
        "function numberLimitFromKeyboardEvent(e){\n  const match = /^(?:Digit|Numpad)([0-7])$/.exec(e.code);\n  return match ? Number(match[1]) : null;\n}",
        "function numberLimitFromKeyboardEvent(e){\n  const codeMatch = /^(?:Digit|Numpad)([0-7])$/.exec(e.code || \"\");\n  if(codeMatch) return Number(codeMatch[1]);\n  return /^[0-7]$/.test(e.key) ? Number(e.key) : null;\n}"
    ),
    (
        "    if(numberLimit !== null){\n      if(!e.repeat) setNumberVisibilityLimit(numberLimit);\n      e.preventDefault();\n      return;\n    }",
        "    if(numberLimit !== null){\n      setNumberVisibilityLimit(numberLimit);\n      e.preventDefault();\n      return;\n    }"
    ),
]

for old, new in replacements:
    if new in text:
        continue
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old!r}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Fixed repeated number shortcuts and button-focus blocking.")
