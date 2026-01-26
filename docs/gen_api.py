from pathlib import Path

import mkdocs_gen_files


PACKAGE = "jam"
SRC = Path("src") / PACKAGE
API_DIR = Path("api")

nav = mkdocs_gen_files.Nav()

# index.md для раздела API
with mkdocs_gen_files.open(API_DIR / "index.md", "w") as f:
    f.write("# API Reference\n")

for path in sorted(SRC.rglob("*.py")):
    if path.name.startswith("_"):
        continue
    if "tests" in path.parts:
        continue

    module = ".".join(path.relative_to("src").with_suffix("").parts)
    doc_path = API_DIR / path.relative_to(SRC).with_suffix(".md")

    nav[module] = doc_path.as_posix()

    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"::: {module}\n")

# SUMMARY.md для literate-nav
with mkdocs_gen_files.open(API_DIR / "SUMMARY.md", "w") as f:
    f.writelines(nav.build_literate_nav())
