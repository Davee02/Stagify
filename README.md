# Stagify

Die produktive Version der Applikation kann unter der folgenden URL erreicht werden: <https://stagifyapp.azurewebsites.net/>. Da wir für das Frontend und Backend Azure App Services in der Preiskategorie "Free" benutzen, muss mit längeren Ladezeiten gerechnet werden.

## Entwicklung

Wir empfehlen die Verwendung des Code-Editors [Visual Studio Code](https://code.visualstudio.com/) für die Entwicklung und das Debugging von Stagify.
Nachdem der Root-Folder des Projekts in Visual Studio Code geöffnet wurde, sollen alle empfohlenen Extensions installiert werden. Es müssen keine zusätzlichen Einstellungen vorgenommen werden, da sonst die Standardeinstellungen verwendet werden.

Die folgenden Programme werden benötigt, um Stagify lokal auszuführen:

- [Python 3](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Danach muss die Postgres-Datenbank mit Docker Compose ausgeführt werden:

```shell
docker-compose up -d
```

Dann können alle Python-Pakete installiert, die Datenbank-Migrationen ausgeführt und den Dev-Server für das Backend gestartet werden:

```shell
cd ./stagifyapi
pip install -r anforderungen.txt
python manage.py migrieren
python manage.py runserver
```

Um das Frontend zu starten, müssen alle Node-Pakete wiederherstellt und der Dev-Server gestartet werden:

```Shell
cd ../stagifyfrontend
npm i
npm starten
```

Das Frontend ist nun auf `http://localhost:4200/` verfügbar, das Backend auf `http://localhost:8000/`.


Um sicherzustellen, dass alle Typescript- und Python-Dateien, die wir schreiben, identisch formatiert sind, verwenden wir die folgenden Tools:

- Typescript: [Prettier](https://prettier.io/) (ausgeführt mit `npx prettier --write ./stagifyfrontend`)
- Python: [Black](https://black.readthedocs.io/en/stable/) (ausgeführt mit `python -m black ./stagifyapi`)
