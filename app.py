import json
import subprocess
import sys
from tempfile import NamedTemporaryFile

from flask import Flask, request


def xl2b64(xlsx_path: str) -> str:
    python = sys.executable
    command = [python, "./maquettes-xl2json/maquettes-xl2json.py", xlsx_path, "-b"]
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.stdout, result.stderr


app = Flask(__name__)


@app.get("/")
def index():
    return """
<html>
<head>
    <title>maquettes-xl2web</title>
</head>
<body>
    <h2>Convertir un tableau Excel en maquette Pégase</h2>
    <div>
        <label for="file">Fichier Excel (cliquer pour choisir le fichier Excel)</label>
    </div>
    <div style="margin-top: 0.5em;">
        <input name="file" type="file" accept=".xlsx">
    </div>
    <div style="margin-top: 1em;">
        <label for="result">Maquette Pégase (cliquer dans la boîte ci-dessous pour copier le contenu dans le presse-papier)</label>
    </div>
    <div style="margin-top: 0.5em;">
        <textarea id="result" name="result" cols="100" rows="30"></textarea>
    </div>
    <div style="margin-top: 1em;">
        <label for="result">Erreurs</label>
    </div>
    <div style="margin-top: 0.5em;">
        <textarea id="error" name="result" cols="100" rows="30" disabled></textarea>
    </div>
    <script>
        const inputFile = document.querySelector("input[type=file]");
        const textareaResult = document.querySelector("textarea#result");
        const textareaError = document.querySelector("textarea#error");
        inputFile.addEventListener("change", (x) => {
            textareaResult.disabled = true;
            textareaResult.value = "... génération en cours ...";
            textareaError.value = "";
            const file = x.target.files[0];
            const formData = new FormData();
            formData.append("file", file);
            fetch("/", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then((data) => {
                textareaResult.value = data.result;
                textareaResult.disabled = false;
                textareaError.value = data.error;
            });
        });
        textareaResult.addEventListener("click", async () => {
            if (!textareaResult.value || textareaResult.value === "") return;
            await navigator.clipboard.writeText(textareaResult.value);
            alert("Maquette copiée dans le presse-papier ! Vous pouvez la coller avec CTRL-V.");
        });
    </script>
</body>
</html>
"""


@app.post("/")
def generate():
    with NamedTemporaryFile(suffix=".xlsx") as temp_file:
        request.files["file"].save(temp_file.name)
        result, error = xl2b64(temp_file.name)
    return json.dumps({"result": result, "error": error})
