from pathlib import Path

# The Inkscape path is not resilient to custom install paths or other operating system installs.
# This may need to be modified in the future. 
PATH_INKSCAPE = Path(r"C:\Program Files\Inkscape\bin\inkscape.exe")

#### Project Directories ####
PATH_DATA = Path(".data")
PATH_DATA_IMAGES = PATH_DATA / "images"
PATH_DATA_BACKGROUNDS = PATH_DATA / "backgrounds"
PATH_DATA_IMAGES_PROBLEMS = PATH_DATA_IMAGES / "problems_png"
PATH_DATA_IMAGES_SOLUTIONS = PATH_DATA_IMAGES / "solns_png"
