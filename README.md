# Document AutoTagging Project

This project is the POC implementation of an autotagging algorithm written using the popular production NLP library called Spacy.

On your machine, you should have the following:
- A modern Python version (>= v3.9)
- A UNIX-like OS (highly recommend connecting WSL to VSCode, if you are trying to run the project on Windows)
- PIP package manager (it should come installed with Python on your machine)

Once have the project cloned, you can run the setup script found in the `scripts` directory
```bash
chmod +x ./scripts/setup-environment.sh
./scripts/setup-environment.sh
```

This wil install all the project dependencies, in a dedicated virtual environment created at the root directory of the project (it is called `venv`)

*Note: If the script doesn't work, you can manually run all the steps in there. Unix-based systems commonly use `python3` as the primary alias for calling the interprter, but you might need to adapt to `python`.*

The autotagging demo can be found in the `main.py` script. 
It takes in three CLI arguments in the following order:
1. File path for the document PDF (**sample documents can be located inside the documents directory**)
2. The predefined tags for the mock organization you are tested against, as a comma-seperated list (ex: tag1, tag2,etc)
3. The Spacy English model name (recommended to use en_core_web_lg, as it was installed in the setup bash script)

An example of calling this script is as follows:
```bash
python3 main.py ./documents/pdfs/demo2.pdf management,water,laws en_core_web_lg
```

