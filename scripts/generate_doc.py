import subprocess
import requests
import os
from gemini import generate_response

DOC_PATH = "docs/auto-doc.md"
PUML_PATH = "docs/diagram.puml"
PNG_PATH = "docs/diagram.png"
ACTIVITY_PUML_PATH = "docs/activity_diagram.puml"
ACTIVITY_PNG_PATH = "docs/activity_diagram.png"

def get_base_commit():
    """Pobierz commit przed zmianami (start)."""
    return os.environ.get("GITHUB_EVENT_BEFORE", "HEAD~1")

def get_changed_files(base_commit):
    """Pobierz listę zmienionych plików .kt między base_commit a HEAD."""
    output = subprocess.check_output(["git", "diff", "--name-status", base_commit, "HEAD"]).decode()
    changes = []
    for line in output.strip().split("\n"):
        parts = line.split("\t")
        status = parts[0]

        if status.startswith('R') or status.startswith('C'):
            # Rename lub Copy - 3 kolumny: status, stara_ścieżka, nowa_ścieżka
            old_path = parts[1]
            new_path = parts[2]

            if new_path.endswith(".kt"):
                changes.append(("renamed", old_path, new_path))
        elif status == 'M':
            # Modyfikacja
            path = parts[1]
            if path.endswith(".kt"):
                changes.append(("modified", path))
        elif status == 'A':
            # Nowy plik
            path = parts[1]
            if path.endswith(".kt"):
                changes.append(("added", path))
        elif status == 'D':
            # Usunięty plik
            path = parts[1]
            if path.endswith(".kt"):
                changes.append(("deleted", path))
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

def read_existing_diagram():
    if os.path.exists(PUML_PATH):
        with open(PUML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def read_existing_activity_diagram():
    if os.path.exists(ACTIVITY_PUML_PATH):
        with open(ACTIVITY_PUML_PATH, "r", encoding="utf-8") as f:
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
for change in changed_files:
    if change[0] == "renamed":
        old_path = change[1]
        new_path = change[2]
    else:
        old_path = change[1]
        new_path = change[1]

    old_content = get_file_content(base_commit, old_path)
    new_content = get_file_content("WORKSPACE", new_path)  # aktualna wersja na dysku

    if old_content is None and new_content is None:
        continue  # Plik usunięty i brak nowej wersji? Pomijamy

    part = f"Plik: {new_path}\n"

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

# 4. Przygotowanie prompta Markdown
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

print("Prompt dla Markdown:")
print(prompt)

# 5. Wywołanie LLM Markdown
print("Generuję dokumentację Markdown...")
result = generate_response(prompt)

# 6. Zapisz do pliku Markdown
os.makedirs("docs", exist_ok=True)
with open(DOC_PATH, "w") as f:
    f.write(result)

print(f"✅ Dokumentacja Markdown wygenerowana i zapisana w {DOC_PATH}")


# 7. Przygotowanie prompta SysML
existing_puml = read_existing_diagram()

prompt_puml = f"""
Oto aktualny diagram SysML (w formacie PlantUML):

--- BEGIN CURRENT DIAGRAM ---
{existing_puml}
--- END CURRENT DIAGRAM ---

Poniżej znajduje się porównanie zmienionych plików Kotlin.
Zaktualizuj diagram tak, aby uwzględniał **dodane, zmienione oraz usunięte klasy, interfejsy oraz ich relacje**.

--- BEGIN CHANGES ---
{changed_code}
--- END CHANGES ---

Uwagi:
- Zachowaj wszystkie istniejące poprawne elementy, ale usuń te, których już nie ma.
- Dodaj nowe klasy/interfejsy i relacje jeśli pojawiły się w zmianach.
- Używaj poprawnej składni PlantUML (otocz `@startuml` i `@enduml`).
- Nie pisz żadnych dodatkowych wyjaśnień ani opisów.
"""
# 8. Wywołanie LLM SysML
print("Generuję diagram PlantUML...")
result_puml = generate_response(prompt_puml)

# 9 Zapis do pliku SysML
os.makedirs("docs", exist_ok=True)
with open(PUML_PATH, "w", encoding="utf-8") as f:
    f.write(result_puml)

print(f"✅ Diagram PlantUML zapisany w {PUML_PATH}")


# 10. Wygeneruj PNG z PUML
def render_puml_to_png(input_path, output_path):
    try:
        subprocess.run(["plantuml", "-tpng", "-o", ".", input_path], check=True)
        print(f"✅ Diagram PNG wygenerowany w {output_path}")
    except Exception as e:
        print(f"❌ Błąd przy generowaniu diagramu PNG: {e}")

render_puml_to_png(PUML_PATH, PNG_PATH)


# ---- Diagram Aktywności ----
existing_activity = read_existing_activity_diagram()

prompt_activity = f"""
Wygeneruj diagram aktywności w formacie PlantUML dla funkcji/metod zawartych w kodzie Kotlin.
Skup się na metodach publicznych (np. kontrolerach REST).

--- BEGIN CURRENT DIAGRAM ---
{existing_activity}
--- END CURRENT DIAGRAM ---

--- BEGIN CHANGES ---
{changed_code}
--- END CHANGES ---

Zasady:
- Dla każdej funkcji/metody wygeneruj osobny diagram aktywności.
- Każdy diagram zaczynaj od @startuml i kończ @enduml.
- Używaj notacji activity diagramów w PlantUML (start -> akcje -> end).
- Jeśli metoda jest usunięta, usuń ją z diagramu.
- Nie pisz komentarzy, tylko czysty kod PlantUML.
"""

print("Generuję diagram aktywności (PlantUML)...")
activity_result = generate_response(prompt_activity)

with open(ACTIVITY_PUML_PATH, "w", encoding="utf-8") as f:
    f.write(activity_result)

print(f"✅ Diagram aktywności zapisany w {ACTIVITY_PUML_PATH}")
render_puml_to_png(ACTIVITY_PUML_PATH, ACTIVITY_PNG_PATH)