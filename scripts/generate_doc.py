import subprocess
import requests
import os
from gemini import generate_response

DOC_PATH = "docs/auto-doc.md"


def get_base_commit():
    """Pobierz commit przed zmianami (start)."""
    return os.environ.get("GITHUB_EVENT_BEFORE", "HEAD~1")

def get_changed_files(base_commit):
    """Pobierz listę zmienionych plików .kt między base_commit a HEAD."""
    output = subprocess.check_output(["git", "diff", "--name-status", base_commit, "HEAD"]).decode()
    changes = []
    for line in output.strip().split("\n"):
        status, path = line.split("\t", 1)
        if path.endswith(".kt"):
            changes.append((status, path))
    return changes

def get_file_content(revision, path):
    """Pobierz treść pliku z danego commita lub aktualną."""
    try:
        if revision == "WORKSPACE":
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return subprocess.check_output(["git", "show", f"{revision}:{path}"]).decode()
    except Exception:
        return None  # Plik może nie istnieć w tym commicie

def read_existing_docs():
    if os.path.exists(DOC_PATH):
        with open(DOC_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# 1. Przygotowanie commitów
base_commit = get_base_commit()
print(f"Porównujemy zmiany od {base_commit} do HEAD.")

# 2. Wykrycie zmian
changed_files = get_changed_files(base_commit)
print("Zmodyfikowane pliki .kt:")
print(changed_files)

if not changed_files:
    print("Brak zmian w plikach .kt, pomijam generowanie dokumentacji.")
    exit(0)



# 3. Przygotowanie sekcji zmienionych plików
code_parts = []
for status, path in changed_files:
    old_content = get_file_content(base_commit, path)
    new_content = get_file_content("WORKSPACE", path)  # aktualna wersja na dysku

    if old_content is None and new_content is None:
        continue  # Plik usunięty i brak nowej wersji? Pomijamy

    part = f"Plik: {path}\n"

    if old_content and new_content:
        part += f"--- STARY KOD ---\n```kotlin\n{old_content}\n```\n\n"
        part += f"--- NOWY KOD ---\n```kotlin\n{new_content}\n```"
    elif old_content and not new_content:
        part += f"--- USUNIĘTY PLIK ---\n```kotlin\n{old_content}\n```"
    elif new_content and not old_content:
        part += f"--- NOWY PLIK ---\n```kotlin\n{new_content}\n```"

    code_parts.append(part)

changed_code = "\n\n".join(code_parts)
existing_docs = read_existing_docs()

# 4. Przygotowanie prompta
prompt = f"""
Oto aktualna dokumentacja REST API:

--- BEGIN CURRENT DOCS ---
{existing_docs}
--- END CURRENT DOCS ---

Poniżej znajduje się porównanie zmienionych plików Kotlin.
Zaktualizuj dokumentację tak, aby uwzględniała **dodane, zmienione oraz usunięte elementy**.
Nie powielaj istniejących wpisów — popraw istniejące lub usuń je jeśli dotyczą usuniętego kodu.

--- BEGIN CHANGES ---
{changed_code}
--- END CHANGES ---

Zwróć kompletną, zaktualizowaną dokumentację (bez komentarzy ani wyjaśnień):
"""

print("Generuję prompt dla LLM...")
print(prompt)

# 5. Wywołanie LLM
result = generate_response(prompt)

# 6. Zapisz do pliku
os.makedirs("docs", exist_ok=True)
with open(DOC_PATH, "w") as f:
    f.write(result)

print(f"✅ Dokumentacja wygenerowana i zapisana w {DOC_PATH}")
