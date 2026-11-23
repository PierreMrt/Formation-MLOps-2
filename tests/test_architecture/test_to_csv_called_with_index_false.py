"""Architecture test.

Vérifie que tous les appels à `to_csv` faits dans le package
`formation_mlops_2` sont bien appelés avec l'argument `index=False`.

Cela évite d'écrire l'index du DataFrame dans les fichiers CSV générés
(données, prédictions, etc.).
"""

from pathlib import Path

PACKAGE_ROOT = Path(__file__).parents[2] / "formation_mlops_2"



def test_to_csv_called_with_index_false():
    # Given
    violations = []

    # When
    for filepath in sorted(PACKAGE_ROOT.rglob("*.py")):
        for line_number, line in enumerate(
            filepath.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if ".to_csv(" in line and "index=False" not in line:
                violations.append(f"{filepath}:{line_number}")

    # Then
    assert not violations, (
        "Appels à `to_csv` sans `index=False` dans formation_mlops_2 :\n"
        + "\n".join(violations)
    )
