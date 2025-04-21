import subprocess
import requests
import os
from gemini import generate_response

DOC_PATH = "docs/auto-doc.md"


def get_changed_files():
    try:
        # Spróbuj HEAD~1
        subprocess.check_output(["git", "rev-parse", "HEAD~1"])
        base_commit = "HEAD~1"
    except subprocess.CalledProcessError:
        # Jeśli to pierwszy commit
        base_commit = subprocess.check_output(
            ["git", "rev-list", "--max-parents=0", "HEAD"]
        ).decode().strip()

    changed_files = subprocess.check_output(
        ["git", "diff", "--name-only", base_commit, "HEAD"]
    ).decode().splitlines()

    return [f for f in changed_files if f.endswith(".kt") and os.path.exists(f)]

def read_file_content(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def read_existing_docs():
    if os.path.exists(DOC_PATH):
        with open(DOC_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""


diff_files = get_changed_files()

# Filtrowanie po nazwie pliku
changed_files = diff_files
print("Changed files:")
print(changed_files)

if not changed_files:
    print("Brak zmian w plikach .kt, pomijam generowanie dokumentacji.")
    exit(0)

code_parts = []
for file in changed_files:
    content = read_file_content(file)
    code_parts.append(f"Plik: {file}\n```kotlin\n{content}\n```")

changed_code = "\n\n".join(code_parts)
existing_docs = read_existing_docs()

prompt = f"""
Oto aktualna dokumentacja REST API:

--- BEGIN CURRENT DOCS ---
{existing_docs}
--- END CURRENT DOCS ---

Poniżej znajduje się zmodyfikowany kod źródłowy.
Zaktualizuj powyższą dokumentację tak, aby uwzględniała **tylko zmiany związane z poniższymi plikami**.
Nie powielaj już istniejących wpisów – dodaj tylko nowe/zmienione lub zaktualizuj istniejące jeśli trzeba. Nie pisz nic poza tekstem dokumentacji.

--- BEGIN CHANGED CODE ---
{changed_code}
--- END CHANGED CODE ---

Zwróć kompletną dokumentację po aktualizacji:
"""

print(prompt)

result = "Tymczasowo puste" #generate_response(prompt)

# 6. Zapisz do pliku
os.makedirs("docs", exist_ok=True)
with open(DOC_PATH, "w") as f:
    f.write(result)

print("Dokumentacja zapisana w " + DOC_PATH)
