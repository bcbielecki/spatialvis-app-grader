# Spatial Vis App Assignment Grading Tool

This is a graphical program for manually grading student submissions to the [Spatial Vis App](https://egrove.education/). The repository is forked from one made by researchers at UC San Diego, who are investigating methods for [improving student outcomes in STEM courses](https://jacobsschool.ucsd.edu/news/release/3324?id=3324).

Student submission data must be exported as an Excel file from the Spatial Vis App and imported into the grading tool for analysis. The repository does not provide this data.

This project is in active development with no planned release as of now. All installation and launch instructions are purely for developmental work. Licensing information is provided at the bottom of the readme file.

## Supported Systems

The project has been developed for and tested on a Windows 11, Intel x86-64 machine with Python 3.13.5.
No systems beyond the aforementioned are officially supported.

## Dependencies

- Inkscape v1.4.x or newer
- Third-party Python packages outlined in the repo's requirements.txt file
- QT is licensed under GPL version 3

## Installation Guide

1. Install [Python](https://www.python.org/downloads/) v3.13.X or newer
2. Install [Inkscape](https://inkscape.org/) v1.4.x or newer
3. Clone this repository to a local project directory
4. From the project root directory, create and activate [Python virtual environment](https://docs.python.org/3/library/venv.html) (highly recommended but not necessarily required)
   1. Run the command `python -m venv .venv` in the terminal from the project root directory to install the venv
   2. Activate the virtual environment by running the command `.venv/Scripts/activate.bat` (Windows cmd.exe) or `.venv/Scripts/Activate.ps1` (Windows PowerShell). For other systems, refer to the Python venv docs.
5. You're done! Refer to the Launch Guide for starting the program.

## Launch Guide

Use this guide only after completing all the installation steps.

1. In your terminal, with the virtual environment activated run `py main.py` from the root project directory.
2. You will be prompted for information before the program launches. Enter it.
3. Wait for preprocessing to complete... It may take several minutes to an hour depending on the data size.
4. A window will open for you to analyze the data.
5. Congrats! That's it.

## License

The repository from which this project is forked currently lacks licensing information, so **you may use this repository at your own risk, assuming all risks and damages incurred.**
