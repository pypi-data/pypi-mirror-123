
from dynaconf import Dynaconf, constants
from pathlib import Path

_settings = Dynaconf(
    envvar_prefix="MDPAPER",
    load_dotenv=True,
    warn_dynaconf_global_settings=True,
    environments=True,
    default_env="mdpaper",
    default_settings_paths=constants.DEFAULT_SETTINGS_FILES,
)

# Get list of index names
index = _settings.get("index", [])

# Reference file
references = _settings.get("references", "references.bib")

# Output file name
output = _settings.get("output")

# Pandoc binary
pandoc = _settings.get("pandoc", "pandoc")

# toc settings
toc = _settings.get("toc", True)
toc_depth = str(_settings.get("toc_depth", 2))

# Additional Filters
pandoc_filters = _settings.get("pandoc_filters", [])

# DOCX Settings
template_docx = _settings.get("template_docx", None)
if template_docx:
    template_docx = Path(template_docx).expanduser().resolve()

# PDF Settings
pdf_engine = _settings.get("pdf_engine", "xelatex")