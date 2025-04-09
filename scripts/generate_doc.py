import subprocess
import requests
import os


# Pobierz zmienione pliki z ostatniego commita
diff_files = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
).decode().splitlines()

# Filtrowanie po nazwie pliku
changed_files = [f for f in diff_files if f.endswith(".kt")]
print("Changed files:")
print(changed_files)

# 3. Pobierz diff treść tych plików
diff_text = subprocess.check_output(
    ["git", "diff", "HEAD~1", "HEAD", "--"] + changed_files
).decode()

if not diff_text.strip():
    print("Brak zmian w plikach .kt")
    exit(0)

# 4. Przygotuj prompt
prompt = f"""Na podstawie poniższego diff wygeneruj dokumentację REST API (OpenAPI-like):

{diff_text}
"""

print(prompt)

result = "Dokumentacja będzie tutaj"

# 6. Zapisz do pliku
os.makedirs("docs", exist_ok=True)
with open("docs/auto-doc.md", "w") as f:
    f.write(result)

print("Dokumentacja zapisana w docs/auto-doc.md")
