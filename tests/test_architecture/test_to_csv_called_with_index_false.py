"""Architecture test.

Vérifie que tous les appels à `to_csv` faits dans le package
`formation_mlops_2` sont bien appelés avec l'argument `index=False`.

Cela évite d'écrire l'index du DataFrame dans les fichiers CSV générés
(données, prédictions, etc.).
"""

import re
from pathlib import Path

PACKAGE_ROOT = Path(__file__).parents[2] / "formation_mlops_2"


def _extract_to_csv_calls(content):
    """Extrait le texte de chaque appel `.to_csv(...)`,
    même s'il s'étend sur plusieurs lignes, avec ses numéros de ligne."""
    for match in re.finditer(r"\.to_csv\(", content):
        start = match.start()
        # Trouver la parenthèse fermante en suivant l'imbrication
        depth = 1
        position = match.end()
        while position < len(content) and depth > 0:
            char = content[position]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            position += 1
        yield start, content[start:position]


def test_to_csv_called_with_index_false():
    # Given
    violations = []

    # When
    for filepath in sorted(PACKAGE_ROOT.rglob("*.py")):
        content = filepath.read_text(encoding="utf-8")
        for start, call_text in _extract_to_csv_calls(content):
            if not re.search(r"index\s*=\s*False\b", call_text):
                line_number = content.count("\n", 0, start) + 1
                violations.append(f"{filepath}:{line_number}")

    # Then
    assert not violations, (
        "Appels à `to_csv` sans `index=False` dans formation_mlops_2 :\n"
        + "\n".join(violations)
    )