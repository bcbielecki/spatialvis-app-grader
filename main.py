"""
    A module that contains the functions related Spatial Vis Analysis.  
    =====
    Contains the following functions:
        download_svg(url, output_path)
        batch_download(sheet_path, output_path, columns, sheet_index, student)
        overlay_svgs(background_path, overlay_path, output_path, x, y)
        batch_overlay_svgs(background_folder, overlay_folder, output_folder, x, y, student)
        convert_svgs_to_pngs(input_folder, output_folder, student)
        clean_data(source_file, student_ID)
        save_excel(data_frame, source_file, sheet_name, if_exists)
        result_message(grading_metrics)
        get_results(grading_metrics)
        run_analysis(image_folder, excel_file, start_index, sID, load_in, if_exists)

    To run the program:
        (1) Open a terminal in the root project directory
        (2) Run the command 'py SpatialVisV3.py [Excel file path] [Student ID]'
                - where [Excel file path] is the path to the excel file which you will use for analysis
                  Ex) 'BlankTemplate.xlsx' or 'C:/Users/Bob/BlankTemplate.xlsx'
                - where [Student ID] is the numeric ID of the student whose data you would like to analyze
"""
import reportlab.rl_config

from spatialvis.viscore import download_backgrounds, prepare_analysis, run_analysis
from spatialvis.viscache import StartupCache
reportlab.rl_config.renderPMBackend = 'rlPyCairo'  # Use rlPyCairo as the renderer
import pandas as pd # Library for readin and writing excel
# import cairosvg # A graphics library for SVGs based on Cairo, fast but limited, See: touble-shooting cairo
from pathlib import Path
import sys

if __name__ == '__main__':

    excel_file_path = None
    student_id = None

    if len(sys.argv) == 3:
        try:
            excel_file_path = Path(sys.argv[1])
        except:
            raise ValueError("Invalid Excel file path as second argument")
        
        try:
            student_id = str(sys.argv[2])
        except:
            raise ValueError("Invalid student ID as third argument")
    elif len(sys.argv) == 1:
        saved_excel_file_path, saved_student_id = StartupCache.load()
        while excel_file_path is None:
            input_file_path = input(f"Enter an Excel file path (ex. 'file.xlsx' or 'C:\\\\User\\Bob\\file.xlsx') without quotes ({saved_excel_file_path}): ")
            if input_file_path == "" and saved_excel_file_path is not None:
                excel_file_path = saved_excel_file_path
            else:
                try:
                    excel_file_path = Path(input_file_path)
                except:
                    print("Invalid Excel file path. Try again.")

        while student_id is None:
            input_student_id = input(f"Enter a numeric student ID ({saved_student_id}): ")
            if input_student_id == "" and saved_student_id is not None:
                    student_id = saved_student_id
            else:
                try:
                    student_id = str(input_student_id)
                except:
                    print("Invalid student ID. Try again.")
    else:
        raise ValueError("Invalid number of arguments. Expected command format is 'py SpatioalVisV3.py' OR 'py SpatialVisV3.py [Excel file path] [Student ID]' ")

    StartupCache.save(excel_file_path, student_id)
    Path("./images").mkdir(exist_ok=True)
    Path("./backgrounds").mkdir(exist_ok=True)

    if not Path("./images/problems_png").exists() or not Path("./images/solns_png").exists():
        raise FileNotFoundError("The master files for assignment problems and solutions are missing and must be placed in /images/problems_png and /images/solns_png before running the program.")

    file_path = str(excel_file_path)
    df = pd.read_excel(file_path)

    # 0. Download background images first
    background_folder = r".\backgrounds"
    download_backgrounds(
        sheet_path=str(excel_file_path),
        output_path=background_folder,
        columns=('grid_image_file_url', 'assignment_code'),
        sheet_index='assignments'
    )

    # 1. Prepare data and images
    prepare_analysis(
        excel_file=str(excel_file_path),
        image_folder=r".\images",
        sID=student_id,
        background_folder=background_folder  # Use the populated folder
    )

    # 2. Run the analysis GUI
    run_analysis(
        image_folder=r".\images",
        excel_file=str(excel_file_path),
        start_index=0,
        sID=student_id,
        load_in=True
    )

