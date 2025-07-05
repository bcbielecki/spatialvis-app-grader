
from spatialvis.viscache import StartupCache
from spatialvis.viscore import download_backgrounds, prepare_analysis, run_analysis
from spatialvis import globals
import sys
from pathlib import Path


def launch_nogui():
    excel_file_path = None
    student_id = None

    # For now, we will support two non-gui methods of launching the program:
    # Method 1:
    #    (1) Open a terminal in the root project directory
    #    (2) Run the command 'py SpatialVisV3.py [Excel file path] [Student ID]'
    #            - where [Excel file path] is the path to the excel file which you will use for analysis
    #                Ex) 'BlankTemplate.xlsx' or 'C:/Users/Bob/BlankTemplate.xlsx'
    #            - where [Student ID] is the numeric ID of the student whose data you would like to analyze
    # Method 2:
    #    (1) Open a terminal in the root project directory
    #    (2) Run the command 'py SpatialVisV3.py'
    #    (3) Provide information via interactive prompts

    # Launch Method 1
    if len(sys.argv) == 3:
        try:
            excel_file_path = Path(sys.argv[1])
        except:
            raise ValueError("Invalid Excel file path as second argument")

        try:
            student_id = str(sys.argv[2])
        except:
            raise ValueError("Invalid student ID as third argument")

    # Launch Method 2
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
        raise ValueError("Invalid number of arguments. Expected command format is 'py SpatialVisV3.py' OR 'py SpatialVisV3.py [Excel file path] [Student ID]' ")


    # Save the user-provided excel file and student id. These can be used during the next launch to save time.
    StartupCache.save(excel_file_path, student_id)

    # Create any missing directories. No need to blow up.
    # TODO: These directories should be converted into global variables
    globals.PATH_DATA.mkdir(exist_ok=True)
    globals.PATH_DATA_IMAGES.mkdir(exist_ok=True)
    globals.PATH_DATA_BACKGROUNDS.mkdir(exist_ok=True)

    # There's no way for us to download the problem and solution pngs automatically, so it will be the 
    # responsibility of the user to do so. Keep in mind, this is a basic check; if the folders exist, but their
    # contents are missing, the program will blow up later.
    if not globals.PATH_DATA_IMAGES_PROBLEMS.exists() or not globals.PATH_DATA_IMAGES_SOLUTIONS.exists():
        raise FileNotFoundError("The master files for assignment problems and solutions are missing and must be placed in /images/problems_png and /images/solns_png before running the program.")


    #### Execute Download, Data Processing, then the Main Analysis GUI ####

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
        image_folder=globals.PATH_DATA_IMAGES,
        sID=student_id,
        background_folder=background_folder  # Use the populated folder
    )

    # 2. Run the analysis GUI
    run_analysis(
        image_folder=globals.PATH_DATA_IMAGES,
        excel_file=str(excel_file_path),
        start_index=0,
        sID=student_id,
        load_in=True
    )