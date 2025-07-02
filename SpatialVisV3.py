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
"""
import reportlab.rl_config
reportlab.rl_config.renderPMBackend = 'rlPyCairo'  # Use rlPyCairo as the renderer
import pandas as pd # Library for readin and writing excel
import requests # Library to interact with and download URLs
import os # Library to talk to and manage the opperating system 
from lxml import etree # Library for reading xml files like SVGs
# import cairosvg # A graphics library for SVGs based on Cairo, fast but limited, See: touble-shooting cairo
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import json # Library to parse json files without error
from PIL import Image, ImageTk # Python Image Library, this is what imports and displays the attempts
import tkinter as tk # Tkinter is the standard library for GUI developement in python
from tkinter import ttk # An uppdated library of widgets for Tkinter
from tkinter import scrolledtext # Library to import scolled text boxes
from tkinter import messagebox # Library to show messages, used for confirm close
import ast # Library to parse pythonic grammer without error 
import subprocess
import os
import time

def convert_svg_to_png_inkscape(svg_path, png_path, width=None, height=None, x0=480, y0=480, x1=1120, y1=1120):
    inkscape_path = r"C:\Program Files\Inkscape\bin\inkscape.exe"
    
    cmd = [
        inkscape_path,
        svg_path,
        "--export-type=png",
        f"--export-filename={png_path}",  # ← COMMA MUST BE HERE
        f"--export-area={x0}:{y0}:{x1}:{y1}"
    ]
    
    # Add specific dimensions if needed
    if width and height:
        cmd.extend([f"--export-width={width}", f"--export-height={height}"])
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Successfully converted {svg_path} to {png_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {svg_path}: {e}")


def convert_svgs_to_pngs_inkscape(input_folder, output_folder, student=True):
    """Replace your existing convert_svgs_to_pngs function with this"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if student:
        for input_parent in os.listdir(input_folder):
            output_parent = os.path.join(output_folder, input_parent)
            if not os.path.exists(output_parent):
                os.makedirs(output_parent)
            input_parent_path = os.path.join(input_folder, input_parent)
            
            for filename in os.listdir(input_parent_path):
                if filename.endswith(".svg"):
                    svg_path = os.path.join(input_parent_path, filename)
                    png_filename = os.path.splitext(filename)[0] + ".png"
                    png_path = os.path.join(output_parent, png_filename)
                    convert_svg_to_png_inkscape(svg_path, png_path, width=320, height=320)



file_path = r".\SV_Students_SE3_2025_Python_Data.xlsx"
df = pd.read_excel(file_path)

def download_svg(url, output_path, retries=3, delay=5, timeout=30):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                with open(output_path, 'wb') as file:
                    file.write(response.content)
                print(f'Successfully downloaded {url} to {output_path}')
                return
            else:
                print(f"Failed to download {url} (status {response.status_code})")
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            print(f"Error on attempt {attempt+1}: {e}")
        time.sleep(delay * (attempt + 1))  # Exponential backoff
    print(f"Failed to download {url} after {retries} attempts.")

def batch_download(sheet_path, output_path, columns=('sketch_url', 'assignment_code', 'attempt', 'enrollment_id'), sheet_index=0, student=True, dashed=False):
    r"""
    A function that takes input and output paths and iterates through all URls in a certain column in an excel sheet.
        =====
        Inputs:
            sheet_path: A file path raw string to the excel sheet that you are downloading the images from.
            output_path: A file path raw string to a folder where you want the images saved (path created if it doesn't alreaydy exist).
            columns: A tuple with the name strings of column in order (url_column, name_column, attempt_column, SID_column), automatically initalized to match 'submissions_history'.
            sheet_index: The subsheet index you want, automatically initialized as 0. Can be an int or string.
            student: A booslean of that determines whether these are students submissions or not. Automatically set to True.
            dashed: A booolean argument of weather the images are the dsahed lines or not
        =====
        Example Usage:
            file_path = r'C:\Users\aaron\Documents\VERSA\VERSA Students.xlsx'
            output_path = r'C:\Users\aaron\Documents\Notebooks\VERSA'
            columns = ('sketch_url', 'assignment_code', 'index', 'enrollment_id')
            batch_download(file_path, output_path, columns=('sketch_url', 'assignment_code', 'attempt', 'enrollment_id'), sheet_index=0, student=True
    """
    # Read the Excel files
    df = pd.read_excel(sheet_path, sheet_name = sheet_index)
    url_column, name_column, attempt_column, SID_column = columns
    
    # Iterate through the URLs and save the SVG files for students
    if student:
        for index, row in df.iterrows():
            url = row[url_column]
            name = row[name_column]
            attempt = row[attempt_column]
            student = row[SID_column]
            output_dir = os.path.join(output_path, f'{student}_rsketches', f'{name}')
            # Make sure that the output folder exists and if it doesn't create it.
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            filename = os.path.join(output_dir, f"{attempt}.svg")
            download_svg(url, filename)
        # Student name convention ...\\Images\\(student id)\\(problem name)\\(attempt number)
        print(f"Raw sketches downloaded! Folder Name: '{student}_rsketches'")
    elif dashed:
        for index, row in df.iterrows():
            url = row[url_column]
            name = row[name_column]
            output_dir = os.path.join(output_path, 'dashes')
            # Make sure that the output folder exists and if it doesn't create it.
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            filename = os.path.join(output_dir, f"{name}.png")
            # Try statement to handle errors
            try:
                download_svg(url, filename)
            except:
                print(f'Failed to find dashed image for {name}')
        print("Dashed solutions downloaded! Folder Name: dashes")
    else:
        for index, row in df.iterrows():
            url = row[url_column]
            name = row[name_column]
            filename = os.path.join(output_path, "rsolutions", f"{name}.svg")
            download_svg(url, filename)
        print("Raw solutions downloaded! Folder Name: rsolutions")

def overlay_images(background_path, overlay_path, output_path, type, x=0, y=0):
    """Enhanced overlay function with better coordinate handling"""
    if type == 'svg':
        # Load and parse the background SVG
        with open(background_path, 'r') as f:
            background_svg = f.read()
        background_root = etree.fromstring(background_svg.encode('utf-8'))
        
        # Load and parse the overlay SVG
        with open(overlay_path, 'r') as f:
            overlay_svg = f.read()
        overlay_root = etree.fromstring(overlay_svg.encode('utf-8'))
        
        # Create a group for the overlay with proper positioning
        overlay_group = etree.Element('g')
        overlay_group.attrib['transform'] = f'translate({x},{y})'
        
        # Copy all children from overlay to the group
        for child in overlay_root:
            overlay_group.append(child)
        
        # Add the group to the background SVG
        background_root.append(overlay_group)
        
        # Ensure proper viewBox is set
        if 'viewBox' not in background_root.attrib:
            width = background_root.attrib.get('width', '800')
            height = background_root.attrib.get('height', '600')
            background_root.attrib['viewBox'] = f'0 0 {width} {height}'
        
        # Save the combined SVG
        combined_svg = etree.tostring(background_root, pretty_print=True).decode('utf-8')
        with open(output_path, 'w') as f:
            f.write(combined_svg)


def batch_overlay_images(background_folder, overlay_folder, output_folder, x=0, y=0, student=True, type = 'svg'):
    r"""
    This function takes a folder for the background, overlays, and output. It then itterates over all of the images in the overlay folder by matching them to the backgroun image and saving to the output file.
        =====
         Inputs:
            background_folder: A file path string to the folder of SVGs you want as the background.
            overlay_folder: A file path string to the the folder of SVGs you want as the overlay.
            output_folder: A file path string to the folder you want the SVGs saved to.
            x: The x coordinate on the background you want the to start the overlay.
            y: The y coordinate on the background you want the to start the overlay.
            type: The image type, automatically SVG. Supports SVG and PNG types.
        =====
        Example Usage:
            background_folder = r"C:\Users\aaron\Documents\Notebooks\VERSA\background_folder"
            overlay_folder = r"C:\Users\aaron\Documents\Notebooks\VERSA\Student_27959"
            output_folder = r"C:\Users\aaron\Documents\Notebooks\VERSA\27959_sketches_svg"
            batch_overlay_svgs(background_folder, overlay_folder, output_folder, x=480, y=480)
    """
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all SVG files in the background folder
    if type == 'svg':
        if student:
            for overlay_parent in os.listdir(overlay_folder):
                output_parent = os.path.join(output_folder, overlay_parent)
                if not os.path.exists(output_parent):
                    os.makedirs(output_parent)
                overlay_parent_path = os.path.join(overlay_folder, overlay_parent)
                for overlay_file in os.listdir(overlay_parent_path):
                    if overlay_file.endswith('.svg'):
                        background_path = os.path.join(background_folder, f'{overlay_parent}.svg')
                        overlay_path = os.path.join(overlay_folder, overlay_parent, overlay_file)
            
                        # Check if the corresponding background file exists
                        if os.path.exists(background_path):
                            output_path = os.path.join(output_parent, overlay_file)
                            overlay_images(background_path, overlay_path, output_path, type, x, y)
                        else:
                            print(f"Background file not found for: {background_file}")
        else:
            for overlay_file in os.listdir(overlay_folder):
                if overlay_file.endswith('.svg'):
                    background_path = os.path.join(background_folder, overlay_file)
                    overlay_path = os.path.join(overlay_folder, overlay_file)
        
                    # Check if the corresponding background file exists
                    if os.path.exists(background_path):
                        output_path = os.path.join(output_folder, overlay_file)
                        overlay_images(background_path, overlay_path, output_path, type, x, y)
                    else:
                        print(f"Background file not found for: {overlay_path}")
        print(f'Processing Complete! Saved to {output_folder}')
    elif type == 'png':
        if student:
            for overlay_parent in os.listdir(overlay_folder):
                output_parent = os.path.join(output_folder, overlay_parent)
                if not os.path.exists(output_parent):
                    os.makedirs(output_parent)
                overlay_parent_path = os.path.join(overlay_folder, overlay_parent)
                for overlay_file in os.listdir(overlay_parent_path):
                    if overlay_file.endswith('.png'):
                        background_path = os.path.join(background_folder, f'{overlay_parent}.png')
                        overlay_path = os.path.join(overlay_folder, overlay_parent, overlay_file)
            
                        # Check if the corresponding background file exists
                        if os.path.exists(background_path):
                            output_path = os.path.join(output_parent, overlay_file)
                            overlay_images(background_path, overlay_path, output_path, type, x, y)
                        else:
                            print(f"Background file not found for: {overlay_path}")

        else:
            for overlay_file in os.listdir(overlay_folder):
                if overlay_file.endswith('.png'):
                    background_path = os.path.join(background_folder, overlay_file)
                    overlay_path = os.path.join(overlay_folder, overlay_file)
        
                    # Check if the corresponding background file exists
                    if os.path.exists(background_path):
                        output_path = os.path.join(output_folder, overlay_file)
                        overlay_images(background_path, overlay_path, output_path, type, x, y)
                    else:
                        output_path = os.path.join(output_folder, overlay_file)
                        overlay = Image.open(overlay_path)
                        overlay.save(output_path)
        print(f'Processing Complete! Saved to {output_folder}')


def match_svg_viewbox_and_size(student_svg_path, solution_svg_path, output_svg_path):
    # Read solution SVG for reference
    with open(solution_svg_path, 'r') as f:
        sol_svg = f.read()
    sol_root = etree.fromstring(sol_svg.encode('utf-8'))
    sol_viewbox = sol_root.attrib.get('viewBox')
    sol_width = sol_root.attrib.get('width')
    sol_height = sol_root.attrib.get('height')

    # Read student SVG and update attributes
    with open(student_svg_path, 'r') as f:
        stu_svg = f.read()
    stu_root = etree.fromstring(stu_svg.encode('utf-8'))
    if sol_viewbox:
        stu_root.attrib['viewBox'] = sol_viewbox
    if sol_width:
        stu_root.attrib['width'] = sol_width
    if sol_height:
        stu_root.attrib['height'] = sol_height

    # Save updated SVG
    with open(output_svg_path, 'wb') as f:
        f.write(etree.tostring(stu_root, pretty_print=True))       

def convert_svgs_to_pngs(input_folder, output_folder, student=True):
    r"""
    This function take and input and output folder and it converts all the SVG files in the input and converts them to PNGs in the output. This code has a mjor limitation as it interprepts all past paths (even those which have been errased) as extant paths and causes a lot of confusion. Look at it's MATLAB counterpart, it is slower but it converts the SVGs correctly.
        =====
        Inputs: 
            input_folder: Folder where the input SVGs are.
            output_folder: Folder where the PNGs are saved. (Path created if doesn't already exist)
            student: A boolean value that dtermine whether or not this is a students submissions.
        =====
        Example Usage:
            input_dir = r"C:\Users\aaron\Documents\Notebooks\VERSA\27959_sketches_svg"
            output_dir = r"C:\Users\aaron\Documents\Notebooks\VERSA\27959_sketches_png"
            convert_svgs_to_pngs(input_dir, output_dir)
    """
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all SVG files in the input folder
    if student:
        for input_parent in os.listdir(input_folder):
            output_parent = os.path.join(output_folder, input_parent)
            if not os.path.exists(output_parent):
                os.makedirs(output_parent)
            input_parent_path = os.path.join(input_folder, input_parent)
            for filename in os.listdir(input_parent_path):
                if filename.endswith(".svg"):
                    svg_path = os.path.join(input_parent_path, filename)
                    png_filename = os.path.splitext(filename)[0] + ".png"
                    png_path = os.path.join(output_parent, png_filename)
                    
                    try:
                        # Convert SVG to PNG
                        # cairosvg.svg2png(url=svg_path, write_to=png_path, unsafe =  True)
                        drawing = svg2rlg(svg_path)
                        renderPM.drawToFile(drawing,png_path,fmt="PNG")
                    except Exception as e:
                        print(f"Failed to convert {svg_path} to PNG. Error: {e}")
    else:
        for filename in os.listdir(input_folder):
            if filename.endswith(".svg"):
                svg_path = os.path.join(input_folder, filename)
                png_filename = os.path.splitext(filename)[0] + ".png"
                png_path = os.path.join(output_folder, png_filename)
                
                try:
                    # Convert SVG to PNG
                    # cairosvg.svg2png(url=svg_path, write_to=png_path)
                    drawing = svg2rlg(svg_path)
                    renderPM.drawToFile(drawing,png_path,fmt="PNG")
                except Exception as e:
                    print(f"Failed to convert {svg_path} to PNG. Error: {e}")
    print(f'Processing Complete! Saved to {output_folder}')

def clean_data(source_file, student_ID):
    r"""
    This is a function that takes a source file path and a student ID and it then goes into the appropriate sheet and removes any unidentifyable.
        =====
        Inputs:
            source_file: A string path to the desired Excel File
            student_ID: The enrollment ID you want to investigate as a  string
        =====
        Example Usage:
            source_file = r'C:\Users\aaron\Documents\VERSA\VERSA_Students.xlsx'
            student_ID = '27827'
            clean_data(source_file, student_ID)
    """
    # Read in sheet
    df = pd.read_excel(source_file, sheet_name=student_ID)
    # Remove any data that cant be analized
    df.dropna(subset = 'assignment_code', inplace = True)
    save_excel(df, source_file, student_ID)
    print('Data Cleaned!')

def save_excel(data_frame, source_file, subsheet_name, if_exists = 'replace'):
    """
    This is a function that takes a desired data frame and information about the desired location and saves it. Sheet needs to besaved and closed for proper permissions.
        =====
        Inputs:
            data_frame: The pandas.DataFrame variable that you want to savea an Excel sheet
            source_file: The location of the file you want to save to as a string path
            sheet_name: What you want to name the subsheet 
            if_exists: What to do if the sheet already exists, automatically set to 'replace'. Options:{‘error’, ‘new’, ‘replace’, ‘overlay’}
    """
    with pd.ExcelWriter(source_file, mode='a', if_sheet_exists=if_exists) as writer:
        data_frame.to_excel(writer, sheet_name = subsheet_name, index=False)
    print('Sheet Saved!')

def result_message(grading_metrics):
    """
    This is a function which takes the grading_metrics dictionary and determines what message was shown on the results screen
        =====
        Inputs: 
            grading_metrics: A python dictionary with the grading results for the associated drawing, converted from a json object
        Returns:
            message: The message as astring of characters that the students would see on the results screen.
    """
    solid_correct = grading_metrics['test_add_pix'] and grading_metrics['test_mis_solid_pix'] and grading_metrics['test_add_blob_len'] and grading_metrics['test_mis_solid_blob_len']
    dashed_correct = grading_metrics['test_dashed_blob_len'] and grading_metrics['test_gap_blob_len']
    if grading_metrics['pass_sketch']:
        return('Correct sketch')
    elif grading_metrics['missing_one_long_solid_blob']:
        return('You may be missing a line')
    elif grading_metrics['fh_add_one_long_solid_blob']:
        return('You may have too many line(s)')
    elif grading_metrics['fh_large_tol']:
        return('Close! Draw more carefully')
    elif solid_correct and not dashed_correct:
        return('Hidden line(s) incorrect')
    else:
        return('Try again')

def get_results(grading_metrics_string):
    r"""
    This is a function that takes the grading_metrics dictionary and parses the drawing results. 
        =====
        Inputs:
            grading_metrics_string: A python dictionary, as a string, with the grading results for the associated drawing, converted from a json object
        Returns:
            message: The string message shown to the students  
            correct_percent: Percent of correct pixels from normalized pixel counts
            missing_percent: Percent of missing pixels from normalized pixel counts
            additional_percent: Percent of additionl pixels from normalized pixel counts
        =====
        Example Usage-Loop:
            source_file = r"C:\Users\aaron\Documents\VERSA\VERSA_Students.xlsx"
            df = pd.read_excel(source_file)
            for ind in df.index:
                if type(df.at[ind,'grading_metrics']) is str: 
                    grading_metrics = json.loads(df.at[ind,'grading_metrics'])
                    df.at[ind,'minihint_metrics'] = get_results(grading_metrics)
                else:
                    pass
    """
    # The grading metrics data is not all formatted properly thus a try statement is needed
    try:
        grading_metrics = json.loads(grading_metrics_string)
        message = result_message(grading_metrics)
        correct_percent = grading_metrics['n_cor_combined_pix_norm']/grading_metrics['n_sol_combined_pix_norm']
        missing_percent = grading_metrics['n_mis_combined_pix_norm']/grading_metrics['n_sol_combined_pix_norm']
        additional_percent = grading_metrics['n_add_pix_norm']/grading_metrics['n_sol_combined_pix_norm']
    # If the json file cant be read it just returns a null
    except:
        return None, None, None, None 
    return message, correct_percent, missing_percent, additional_percent

def prepare_analysis(excel_file, image_folder, sID, background_folder):
    """Updated function using Inkscape for conversion"""
    # 1. Download student sketches
    batch_download(excel_file, image_folder, sheet_index=f'{sID}')
    
    # 2. Overlay sketches on backgrounds
    svg_output = os.path.join(image_folder, f'{sID}_svg')
    batch_overlay_images(
        background_folder,
        os.path.join(image_folder, f'{sID}_rsketches'),
        svg_output,
        x=480, y=480  # Try with 0,0 first instead of 480,480
    )
    
    # 3. Convert SVGs to PNGs using Inkscape
    png_output = os.path.join(image_folder, f'{sID}_png')
    convert_svgs_to_pngs_inkscape(  # Use Inkscape version
        input_folder=svg_output,
        output_folder=png_output,
        student=True
    )
    
    # 4. Clean Excel data
    clean_data(excel_file, f'{sID}')



#def prepare_analysis(excel_file, image_folder, sID, background_folder):
#    """
#    Functionn to run before starting the analysis of a new student, it downloads the images, overlays them on the backgrounds and cleans the excel sheet.
#        =====
#        Inputs:
#            excel_file: The parent file of the student data with the subsheets
#            image_folder: The parent Image folder
#            sID: The student id you are looking to investigate as an int
#            background_folder: The specific folder for the background images
#    """
#    batch_download(excel_file, image_folder, sheet_index = f'{sID}')
#    batch_overlay_images(background_folder, os.path.join(image_folder, f'{sID}_rsketches'), os.path.join(image_folder, f'{sID}_svg'), x=480, y=480)
#    clean_data(excel_file, f'{sID}')

def run_analysis(image_folder, excel_file, start_index, sID, load_in, if_exists = 'replace'):
    r"""
    This function contains the code that intailizes and runs the GUI. This function constructs and then fills a class object that reprrsents the actual interface. This interface is then populated with different widgets and functions that call the relivant data from a Pandas DataFrame. This DataFram and the corrasponding otput are run through Pandas' ability to read and write to excel files. The files are stored nd modifyed inside of lists of dictionaries where we can index into the proper data. 
        =====
        Steps:
            1. Read in data and saved analysis to fill empty dictonaries.
            2. Initalize Tkinter window inside of a class object.
            3. Populate this window with different widgets for each image, textbox, button, etcetera
            4. Define function that can control the index and updates the contents of the main frame.
            5. Define a function the updates the dictionaries with the relivant analysis.
            6. Define a save function to write an output file and a constructor dictionary.
            7. Call object if it is being called in the main name space.
        =====
        Inputs:
            image_folder: A string path to the desired parent image folder.
            excel_file: A string path to the excel file you want to read in.
            start_index: Index to initialize as an integer.
            sID: Student ID that you want to investigate as a string, reqires you have already done the previous data steps.
            load_in: A bool of whether you are loading in data that has been analized.
            if_exists: What to do if the sheet already exists, automatically set to 'replace'. Options:{‘error’, ‘new’, ‘replace’, ‘overlay’}
        =====
        Returns:
            Prints a confirm for sheet saving and the integer of the index you closed on.
        =====
        Example usage:
            SpatialVis.run_sv_analysis(
                image_folder = "C:\\Users\\aaron\\Documents\\VERSA_data\\Images", 
                excel_file = "C:\\Users\\aaron\\Documents\\VERSA_data\\VERSA_Students.xlsx", 
                start_index = 217, 
                sID = '27827'
                load_in = True)
    """
    # Variable assignment
    parent_image_folder = image_folder
    source_file = excel_file
    start_index = start_index

    # Read in the data frame and initalize empty lists
    df = pd.read_excel(source_file, sheet_name = sID)
    data = []
    analysis_list = []
    i = 0

    # Itterate down each row and save the data to the right index in the liss
    for index, row in df.iterrows():
        result_message, correct_per, missing_per, additional_per = get_results(df.loc[index, 'grading_metrics'])
        problem_name = row['assignment_code']
        student_ID = row['enrollment_id']
        attempt = row['attempt']
        row_dictionay = {
            'assignment_id' : row['id'],
            'assignment_code' : problem_name,
            'attempt' : attempt,
            'problem_description' : row['problem_description'],
            'is_required' : row['is_required'],
            'enrollment_id' : attempt,
            'results' : result_message,
            'correct_per' : correct_per,
            'missing_per' : missing_per,
            'additional_per' : additional_per,
            'hint_bool': row['did_look_at_hint'],
            'peak_bool': row['did_peek'],
            'sketch_path' : os.path.join(parent_image_folder, f'{student_ID}_png\\{problem_name}\\{attempt}.png'),
            'problem_path' : os.path.join(parent_image_folder, f'problems_png\\{problem_name}_problem.png'),
            'solution_path' : os.path.join(parent_image_folder, f'solns_png\\{problem_name}.png')
        }
        analysis_dic = {
            'assignment_id' : row['id'],
            'index' : i,
            'correctness': '[Not evaluated]',
            'grading': '[Not evaluated]',
            'mini_hints': '[Not evaluated]',
            'evidence': '[Not evaluated]',
            'first_attempt': "",
            'no_change': "",
            'clean_up_lines': "",
            'add_line': "",
            'remove_line': "",
            're_orienting': "",
            're_sizing': "",
            'other1': "",
            'no_mistakes': "",
            'extra_line': "",
            'extra_section': "",
            'extra_dashes': "",
            'missing_line': "",
            'missing_section': "",
            'missing_dashes': "",
            'wrong_size': "",
            'wrong_orientation': "",
            'wrong_location': "",
            'messy_lines': "",
            'f_not_r': "",
            'other2': "",
            'hint_comment': "",
            'evidence_comment': "",
            'action_comment': "",
            'mistakes_comment': "",
            'gen_comment': "",
        }
        i += 1
        data.append(row_dictionay)
        analysis_list.append(analysis_dic)

    # If loading in previous data this reads it to the correct list
    if load_in:
        af = pd.read_excel(source_file, sheet_name = (sID+'_output'))
        analysis_list = []
        i = 0
        for index, row in af.iterrows():
            construct_dict = ast.literal_eval(row['constructor_dict'])
            analysis_dic = {
                'assignment_id' : row['id'],
                'index' : i,
                'correctness': row['correctness'],
                'grading': row['grading_algorithm'],
                'mini_hints': row['best_minihint'],
                'evidence': row['learning_evidence'],
                'first_attempt': construct_dict['first_attempt'],
                'no_change': construct_dict['no_change'],
                'clean_up_lines': construct_dict['clean_up_lines'],
                'add_line': construct_dict['add_line'],
                'remove_line': construct_dict['remove_line'],
                're_orienting': construct_dict['re_orienting'],
                're_sizing': construct_dict['re_sizing'],
                'other1': construct_dict['other1'],
                'no_mistakes': construct_dict['no_mistakes'],
                'extra_line': construct_dict['extra_line'],
                'extra_section': construct_dict['extra_section'],
                'extra_dashes': construct_dict['extra_dashes'],
                'missing_line': construct_dict['missing_line'],
                'missing_section': construct_dict['missing_section'],
                'missing_dashes': construct_dict['missing_dashes'],
                'wrong_size': construct_dict['wrong_size'],
                'wrong_orientation': construct_dict['wrong_orientation'],
                'wrong_location': construct_dict['wrong_location'],
                'messy_lines': construct_dict['messy_lines'],
                'f_not_r': construct_dict['f_not_r'],
                'other2': construct_dict['other2'],
                'hint_comment': row['other_hint'],
                'evidence_comment': row['other_evidence'],
                'action_comment': row['other_action'],
                'mistakes_comment': row['other_mistakes'],
                'gen_comment': row['general_comment'],
            }
            i += 1
            analysis_list.append(analysis_dic)
    
    if len(analysis_list) != len(data):
                analysis_list = []  # Reset if mismatched
                for i, item in enumerate(data):
                    analysis_dic = {
                        'assignment_id': item['assignment_id'],
                        'index': i,
                        'correctness': '[Not evaluated]',
                        'grading': '[Not evaluated]',
                        'mini_hints': '[Not evaluated]',
                        'evidence': '[Not evaluated]',
                        # ... [other fields with default values] ...
                    }
                    analysis_list.append(analysis_dic)    

    # Class obect which contains the parent for the GUI
    class SpatialVisViewer(tk.Tk):
        # Initialize and populate GUI runs on function call
        def __init__(self, data, analysis_list, start_index):
            super().__init__()
            self.data = data
            self.analysis = analysis_list
            self.current_index = start_index
    
            # Set up the frame
            self.title("Spatial Vis Image Viewer")
            self.geometry("1400x700")
            self.columnconfigure(0, weight = 1)
            self.columnconfigure(1, weight = 4)
            self.rowconfigure(0, weight = 1)
            self.rowconfigure((1, 2), weight = 5)
            self.rowconfigure(3, weight = 1)

            # Binded events for the frame
            self.bind("<Control-s>", lambda event: self.save_to_ouput())
            self.protocol('WM_DELETE_WINDOW', self.confirm_exit)

            # Extra frame for greater levels of control (not implimented)
            self.control_frame = ttk.Frame(self, borderwidth = 10, relief = tk.GROOVE)
            self.control_frame.columnconfigure((0,1,2,3,4,5,6,7), weight = 1)
            self.control_frame.rowconfigure(0, weight = 1)
            self.control_frame.grid(row = 0, column = 0, columnspan = 2, sticky = 'news')

            # Frame which shows the problemand problem description
            self.problem_frame = ttk.Frame(self, borderwidth = 10, relief = tk.GROOVE)
            self.problem_frame.rowconfigure((0,1), weight = 1)
            self.problem_frame.columnconfigure(0, weight = 1, uniform = 'a')
            self.problem_frame.grid(row = 1, column = 0, rowspan = 2, sticky = 'news')

            # Frame which shows the solution and student attempt
            self.image_frame = ttk.Frame(self, borderwidth = 10, relief = tk.GROOVE)
            self.image_frame.columnconfigure((0,1,2), weight = 1, uniform = 'a')
            self.image_frame.rowconfigure(0, weight = 1, uniform = 'a')
            self.image_frame.grid(row = 1, column = 1, sticky = 'news')
            
            # Frame for interaction and data analysis
            self.selection_frame = ttk.Frame(self, borderwidth = 10, relief = tk.GROOVE)
            self.selection_frame.columnconfigure((0,1,2,3), weight = 1, uniform = 'a')
            self.selection_frame.grid(row = 2, column = 1, sticky = 'news')

            # Frame to control the shown problem and save the analysis
            self.function_frame = ttk.Frame(self, borderwidth = 10, relief = tk.GROOVE)
            self.function_frame.columnconfigure((0,1,2,3,4,5,6,7), weight = 1)
            self.function_frame.rowconfigure(0, weight = 1)
            self.function_frame.grid(row = 3, column = 0, columnspan = 2, sticky = 'news')

            # Subframes relating to attempt information
            self.data_frame = ttk.Frame(self.image_frame, borderwidth = 10, relief = tk.GROOVE)
            self.data_frame.grid(row = 0, column = 2, sticky = 'news')
            self.description_frame = ttk.Frame(self.problem_frame, borderwidth = 10, relief = tk.GROOVE)
            self.description_frame.grid(row = 1, column = 0, sticky = 'news')
            self.comments_frame = ttk.Frame(self.selection_frame)
            self.comments_frame.grid(row=2, column = 2, rowspan= 2, columnspan=2, sticky='news', padx = 5)
    
            ## Functionality
            # Descriptions of te attempts and problem
            self.attempt_label = ttk.Label(self.data_frame, text = "")
            self.message_label = ttk.Label(self.data_frame, text = "")
            self.correct_label = ttk.Label(self.data_frame, text = "")
            self.missing_label = ttk.Label(self.data_frame, text = "")
            self.additional_label = ttk.Label(self.data_frame, text = "")
            self.attempt_label.pack(pady = 5)
            self.message_label.pack(pady = 5)
            self.correct_label.pack(pady = 5)
            self.missing_label.pack(pady = 5)
            self.additional_label.pack(pady = 5)

            # Information about the previous attempt
            self.problem_label = ttk.Label(self.description_frame, text = "", wraplength = 280)
            self.prev_message_label = ttk.Label(self.description_frame, text = "")
            self.prev_correct_label = ttk.Label(self.description_frame, text = "")
            self.prev_missing_label = ttk.Label(self.description_frame, text = "")
            self.prev_additional_label = ttk.Label(self.description_frame, text = "")
            self.prev_hint_bool_label = ttk.Label(self.description_frame, text = "")
            self.prev_peek_bool_label = ttk.Label(self.description_frame, text = "")
            self.problem_label.pack(pady = 5)
            self.prev_message_label.pack()
            self.prev_correct_label.pack()
            self.prev_missing_label.pack()
            self.prev_additional_label.pack()
            self.prev_hint_bool_label.pack()
            self.prev_peek_bool_label.pack()
                    
            # Attempt Image
            self.attempt_image_label = tk.Label(self.image_frame, background = 'white')
            self.attempt_image_label.grid(row=0, column=1)
            self.attempt_image_label_label = tk.Label(self.image_frame, text = "Student attempt", background = 'white')
            self.attempt_image_label_label.grid(row=0, column=1, sticky = 's')
    
            # Solution Image
            self.solution_image_label = ttk.Label(self.image_frame, background = 'white')
            self.solution_image_label.grid(row=0, column=0)
            self.solution_image_label_label = ttk.Label(self.image_frame, text = "Solution", background = 'white')
            self.solution_image_label_label.grid(row=0, column=0, sticky = 's')
    
            # Problem Image
            self.problem_image_label = ttk.Label(self.problem_frame, background = 'white')
            self.problem_image_label.grid(row=0, column=0)
            self.solution_image_label_label = ttk.Label(self.problem_frame, text = "Problem", background = 'white')
            self.solution_image_label_label.grid(row=0, column=0, sticky = 's')
            
            # Next attempt button
            self.next_button = tk.Button(self.function_frame, text="Next attempt", command=self.next_image)
            self.next_button.grid(row=0, column=7, sticky = 'w', padx = 10)
    
            # Last attempt button
            self.last_button = tk.Button(self.function_frame, text="Previous attempt", command=self.last_image)
            self.last_button.grid(row=0, column=6, sticky = 'w', padx = 10)
    
            # Update analysis buttion
            self.update = tk.Button(self.function_frame, text="Update analysis", command=self.update_analysis)
            self.update.grid(row=0, column=4, sticky = 'w', padx = 10)
    
            # Save analysis button
            self.save = tk.Button(self.function_frame, text="Save analysis", command=self.save_to_ouput)
            self.save.grid(row=0, column=3, sticky = 'w', padx = 10)
            
            # Comboboxs (Drop down selections)
            # Correctness combobox
            self.correctness_string = tk.StringVar()
            self.correctness_label = ttk.Label(self.selection_frame, text = "Student correctness:")
            self.correctness_combo = ttk.Combobox(self.selection_frame, textvariable = self.correctness_string)
            self.correctness_combo['values'] = (
                '[Not evaluated]',
                'Correct',
                'Incorrect')
            self.correctness_label.grid(row=0, column = 0, sticky = 'n')
            self.correctness_combo.grid(row = 1, column = 0, sticky = 'new', padx = 5)

            # Grading combobox
            self.grading_string = tk.StringVar()
            self.grading_label = ttk.Label(self.selection_frame, text = "Grading algorithm:")
            self.grading_combo = ttk.Combobox(self.selection_frame, textvariable = self.grading_string)
            self.grading_combo['values'] = (
                '[Not evaluated]',
                'Graded properly', 
                'Too leaniant', 
                'Too strict')
            self.grading_label.grid(row = 0, column = 1, sticky = 'n')
            self.grading_combo.grid(row = 1, column = 1, sticky = 'new', padx = 5)

            # Hints combobox
            self.hints_string = tk.StringVar()
            self.hints_label = ttk.Label(self.selection_frame, text = "Best mini-hint")
            self.hints_combo = ttk.Combobox(self.selection_frame, textvariable = self.hints_string)
            self.hints_combo['values'] = (
                '[Not evaluated]',
                'Correct sketch', 
                'You may be missing a line',
                'You may have too many line(s)',
                'Close! Draw more carefully',
                'Hidden line(s) incorrect',
                'Try again',
                'Other')
            self.hints_label.grid(row=0, column = 2, sticky = 'n')
            self.hints_combo.grid(row = 1, column = 2, sticky = 'new', padx = 5)

            # Learning combobox
            self.learning_string = tk.StringVar()
            self.learning_label = ttk.Label(self.selection_frame, text = "Evidence of learning:")
            self.learning_combo = ttk.Combobox(self.selection_frame, textvariable = self.learning_string)
            self.learning_combo['values'] = (
                '[Not evaluated]',
                'Learninng from previous attempt', 
                'Learing from previous problem',
                'Correct: no evidence',
                'Incorrect: no evidence', 
                'Learning from mini-hints',
                'Learning from hints',
                'Small changes',
                'Repeated mistake',
                'Not learning from feedback',
                'Other')
            self.learning_label.grid(row = 0, column = 3, sticky = 'n')
            self.learning_combo.grid(row = 1, column = 3, sticky = 'new', padx = 5)

            # Student action check buttons
            self.action_frame = ttk.Frame(self.selection_frame)
            self.action_frame.grid(row = 2, column = 0, rowspan= 2, sticky = 'news')
            self.action_label = ttk.Label(self.action_frame, text = "Change from previous (choose multiple):")
            self.action_label.grid(row=0,column=0,columnspan=2)
            self.act_check1_var = tk.StringVar(value = "")
            self.act_check1 = ttk.Checkbutton(self.action_frame, text = 'First attempt', variable = self.act_check1_var, onvalue = "First attempt", offvalue = "")
            self.act_check1.grid(row=1,column=0)
            self.act_check2_var = tk.StringVar(value = "")
            self.act_check2 = ttk.Checkbutton(self.action_frame, text = 'No change', variable = self.act_check2_var, onvalue = "No change", offvalue = "")
            self.act_check2.grid(row=2,column=0)
            self.act_check3_var = tk.StringVar(value = "")
            self.act_check3 = ttk.Checkbutton(self.action_frame, text = 'Clean up lines', variable = self.act_check3_var, onvalue = "Clean up lines", offvalue = "")
            self.act_check3.grid(row=3,column=0)
            self.act_check4_var = tk.StringVar(value = "")
            self.act_check4 = ttk.Checkbutton(self.action_frame, text = 'Add line(s)', variable = self.act_check4_var, onvalue = "Add line(s)", offvalue = "")
            self.act_check4.grid(row=4,column=0)
            self.act_check5_var = tk.StringVar(value = "")
            self.act_check5 = ttk.Checkbutton(self.action_frame, text = 'Remove line(s)', variable = self.act_check5_var, onvalue = "Remove line(s)", offvalue = "")
            self.act_check5.grid(row=5,column=0)
            self.act_check6_var = tk.StringVar(value = "")
            self.act_check6 = ttk.Checkbutton(self.action_frame, text = 'Re-orienting', variable = self.act_check6_var, onvalue = "Re-orienting", offvalue = "")
            self.act_check6.grid(row=6,column=0)
            self.act_check7_var = tk.StringVar(value = "")
            self.act_check7 = ttk.Checkbutton(self.action_frame, text = 'Re-sizing', variable = self.act_check7_var, onvalue = "Re-sizing", offvalue = "")
            self.act_check7.grid(row=7,column=0)
            self.act_check8_var = tk.StringVar(value = "")
            self.act_check8 = ttk.Checkbutton(self.action_frame, text = 'Other', variable = self.act_check8_var, onvalue = "Other:", offvalue = "")
            self.act_check8.grid(row=8,column=0)

            # Student mistake check buttons
            self.mistakes_frame = ttk.Frame(self.selection_frame)
            self.mistakes_frame.grid(row = 2, column = 1, rowspan= 2, sticky = 'news')
            self.mistakes_label = ttk.Label(self.mistakes_frame, text = "Student mistakes (choose multiple):")
            self.mistakes_label.grid(row=0,column=0,columnspan=2)
            self.mis_check1_var = tk.StringVar(value = "")
            self.mis_check1 = ttk.Checkbutton(self.mistakes_frame, text = 'No mistakes', variable = self.mis_check1_var, onvalue = "No mistakes", offvalue = "")
            self.mis_check1.grid(row=1,column=0)
            self.mis_check2_var = tk.StringVar(value = "")
            self.mis_check2 = ttk.Checkbutton(self.mistakes_frame, text = 'Extra line', variable = self.mis_check2_var, onvalue = "Extra line", offvalue = "")
            self.mis_check2.grid(row=2,column=0)
            self.mis_check3_var = tk.StringVar(value = "")
            self.mis_check3 = ttk.Checkbutton(self.mistakes_frame, text = 'Extra section', variable = self.mis_check3_var, onvalue = "Extra Section", offvalue = "")
            self.mis_check3.grid(row=3,column=0)
            self.mis_check4_var = tk.StringVar(value = "")
            self.mis_check4 = ttk.Checkbutton(self.mistakes_frame, text = 'Extra dashes', variable = self.mis_check4_var, onvalue = "Extra dashes", offvalue = "")
            self.mis_check4.grid(row=4,column=0)
            self.mis_check5_var = tk.StringVar(value = "")
            self.mis_check5 = ttk.Checkbutton(self.mistakes_frame, text = 'Missing line', variable = self.mis_check5_var, onvalue = "Missing line", offvalue = "")
            self.mis_check5.grid(row=5,column=0)
            self.mis_check6_var = tk.StringVar(value = "")
            self.mis_check6 = ttk.Checkbutton(self.mistakes_frame, text = 'Missing section', variable = self.mis_check6_var, onvalue = "Missing section", offvalue = "")
            self.mis_check6.grid(row=6,column=0)
            self.mis_check7_var = tk.StringVar(value = "")
            self.mis_check7 = ttk.Checkbutton(self.mistakes_frame, text = 'Missing dashes', variable = self.mis_check7_var, onvalue = "Missing dashes", offvalue = "")
            self.mis_check7.grid(row=7,column=0)
            self.mis_check8_var = tk.StringVar(value = "")
            self.mis_check8 = ttk.Checkbutton(self.mistakes_frame, text = 'Wrong size', variable = self.mis_check8_var, onvalue = "Wrong size", offvalue = "")
            self.mis_check8.grid(row=8,column=0)
            self.mis_check9_var = tk.StringVar(value = "")
            self.mis_check9 = ttk.Checkbutton(self.mistakes_frame, text = 'Wrong orientation', variable = self.mis_check9_var, onvalue = "Wrong orientation", offvalue = "")
            self.mis_check9.grid(row=1,column=1)
            self.mis_check10_var = tk.StringVar(value = "")
            self.mis_check10 = ttk.Checkbutton(self.mistakes_frame, text = 'Wrong location', variable = self.mis_check10_var, onvalue = "Wrong location", offvalue = "")
            self.mis_check10.grid(row=2,column=1)
            self.mis_check11_var = tk.StringVar(value = "")
            self.mis_check11 = ttk.Checkbutton(self.mistakes_frame, text = 'Messy lines', variable = self.mis_check11_var, onvalue = "Messy lines", offvalue = "")
            self.mis_check11.grid(row=3,column=1)
            self.mis_check13_var = tk.StringVar(value = "")
            self.mis_check13 = ttk.Checkbutton(self.mistakes_frame, text = 'Flip, not rotate', variable = self.mis_check13_var, onvalue = "Flip, not rotate", offvalue = "")
            self.mis_check13.grid(row=4,column=1)
            self.mis_check12_var = tk.StringVar(value = "")
            self.mis_check12 = ttk.Checkbutton(self.mistakes_frame, text = 'Other', variable = self.mis_check12_var, onvalue = "Other", offvalue = "")
            self.mis_check12.grid(row=5,column=1)
            
            ## Comment boxs
            # Hint commets
            self.hint_comment_text = scrolledtext.ScrolledText(self.comments_frame, height = 2, width = 20)
            self.hint_comment_text.grid(row=1, column=0)
            self.hint_comment_label = ttk.Label(self.comments_frame, text = "Other hint:")
            self.hint_comment_label.grid(row=0,column=0)
            
            # Evidence comments
            self.evidence_comment_text = scrolledtext.ScrolledText(self.comments_frame, height = 2, width = 20)
            self.evidence_comment_text.grid(row=1, column=1)
            self.Evidence_comment_label = ttk.Label(self.comments_frame, text = "Other evidence:")
            self.Evidence_comment_label.grid(row=0,column=1)
    
            # Action comments
            self.change_comment_text = scrolledtext.ScrolledText(self.comments_frame, height = 2, width = 20)
            self.change_comment_text.grid(row=3, column=0)
            self.change_comment_label = ttk.Label(self.comments_frame, text = "Other change:")
            self.change_comment_label.grid(row=2,column=0)
    
            # Mistake comments
            self.mistake_comment_text = scrolledtext.ScrolledText(self.comments_frame, height = 2, width = 20)
            self.mistake_comment_text.grid(row=3, column=1)
            self.mistake_comment_label = ttk.Label(self.comments_frame, text = "Other mistake:")
            self.mistake_comment_label.grid(row=2,column=1)
    
            # General comments
            self.gen_comment_text = scrolledtext.ScrolledText(self.comments_frame, height = 2, width = 20)
            self.gen_comment_text.grid(row=5, column=0, columnspan = 2)
            self.gen_comment_label = ttk.Label(self.comments_frame, text = "General comments:")
            self.gen_comment_label.grid(row=4,column=0, columnspan = 2)

            # Gets the data
            self.update_content()

        # Function the reads the lists for the right data and updates the GUi
        def update_content(self):

        
            def safe_format(value):
                return f"{(value * 100):.0f}" if value is not None else "N/A"

    # ... rest of your existing code ...

            # Get the results for this attempt and the previous
            attempt_item = self.data[self.current_index]
            last_item = self.data[self.current_index - 1]
            analysis_item = self.analysis[self.current_index]
            attempt_image_path = attempt_item['sketch_path']
            solution_image_path = attempt_item['solution_path']
            problem_image_path = attempt_item['problem_path']
            attempt_description = f'{attempt_item["assignment_code"]} ({attempt_item["is_required"]}): {attempt_item["problem_description"]}'
            attempt = f'Attempt: {attempt_item["attempt"] + 1}'
            message = f'Displayed message: {attempt_item["results"]}'
            correct = f'Correct percent: {safe_format(attempt_item["correct_per"])}'
            missing = f'Missing percent: {safe_format(attempt_item["missing_per"])}'
            additional = f'Additional percent: {safe_format(attempt_item["additional_per"])}'

            last_correct = f'Previous correct percent: {safe_format(last_item["correct_per"])}'
            last_missing = f'Previous missing percent: {safe_format(last_item["missing_per"])}'
            last_additional = f'Previous additional percent: {safe_format(last_item["additional_per"])}'
            last_hint_bool = f'Did look at hint: {last_item["hint_bool"]}'
            last_peek_bool = f'Did peak: {last_item["peak_bool"]}'

            # Opens the attempt image 
            attempt_image = Image.open(attempt_image_path).resize((320, 320))
            attempt_photo = ImageTk.PhotoImage(attempt_image)

            # Opens the solution image 
            solution_image =  Image.open(solution_image_path).resize((320, 320))
            solution_photo = ImageTk.PhotoImage(solution_image)

            # Opens the problem image 
            problem_image = Image.open(problem_image_path)
            problem_photo = ImageTk.PhotoImage(problem_image)

            # Populates the labels with the relivant information
            self.attempt_image_label.config(image=attempt_photo)
            self.attempt_image_label.image = attempt_photo  # keep a reference to avoid garbage collection
            self.solution_image_label.config(image=solution_photo)
            self.solution_image_label.image = solution_photo
            self.problem_image_label.config(image=problem_photo)
            self.problem_image_label.image = problem_photo
            
            self.problem_label.config(text=attempt_description)
            self.attempt_label.config(text=attempt)
            self.message_label.config(text=message)
            self.correct_label.config(text=correct)
            self.missing_label.config(text=missing)
            self.additional_label.config(text=additional)

            # If relivant loads in the previous attempt data
            if attempt_item["attempt"] != 0:
                self.prev_message_label.config(text=last_message)
                self.prev_correct_label.config(text=last_correct)
                self.prev_missing_label.config(text=last_missing)
                self.prev_additional_label.config(text=last_additional)
                self.prev_hint_bool_label.config(text=last_hint_bool)
                self.prev_peek_bool_label.config(text=last_peek_bool)
            else:
                self.prev_message_label.config(text="")
                self.prev_correct_label.config(text="")
                self.prev_missing_label.config(text="")
                self.prev_additional_label.config(text="")
                self.prev_hint_bool_label.config(text="")
                self.prev_peek_bool_label.config(text="")
    
            # Sets the values of the comboboxes andcomments either to '[Not evaluated] or what was previously selected.'
            self.correctness_combo.set(analysis_item.get('correctness', '[Not evaluated]'))
            self.grading_combo.set(analysis_item.get('grading', '[Not evaluated]'))
            self.hints_combo.set(analysis_item.get('mini_hints', '[Not evaluated]'))
            self.learning_combo.set(analysis_item.get('evidence', '[Not evaluated]'))
            self.act_check1_var.set(analysis_item.get('first_attempt', ''))
            self.act_check2_var.set(analysis_item.get('no_change', ''))
            self.act_check3_var.set(analysis_item.get('clean_up_lines', ''))
            self.act_check4_var.set(analysis_item.get('add_line', ''))
            self.act_check5_var.set(analysis_item.get('remove_line', ''))
            self.act_check6_var.set(analysis_item.get('re_orienting', ''))
            self.act_check7_var.set(analysis_item.get('re_sizing', ''))
            self.act_check8_var.set(analysis_item.get('other1', ''))
            self.mis_check1_var.set(analysis_item.get('no_mistakes', ''))
            self.mis_check2_var.set(analysis_item.get('extra_line', ''))
            self.mis_check3_var.set(analysis_item.get('extra_section', ''))
            self.mis_check4_var.set(analysis_item.get('extra_dashes', ''))
            self.mis_check5_var.set(analysis_item.get('missing_line', ''))
            self.mis_check6_var.set(analysis_item.get('missing_section', ''))
            self.mis_check7_var.set(analysis_item.get('missing_dashes', ''))
            self.mis_check8_var.set(analysis_item.get('wrong_size', ''))
            self.mis_check9_var.set(analysis_item.get('wrong_orientation', ''))
            self.mis_check10_var.set(analysis_item.get('wrong_location', ''))
            self.mis_check11_var.set(analysis_item.get('messy_lines', ''))
            self.mis_check13_var.set(analysis_item.get('f_not_r', ''))
            self.mis_check12_var.set(analysis_item.get('other2', ''))
            self.hint_comment_text.delete('1.0', tk.END)
            self.hint_comment_text.insert('1.0', analysis_item.get('hint_comment', ''))
            self.evidence_comment_text.delete('1.0', tk.END)
            self.evidence_comment_text.insert('1.0', analysis_item.get('evidence_comment', ''))
            self.change_comment_text.delete('1.0', tk.END)
            self.change_comment_text.insert('1.0', analysis_item.get('action_comment', ''))
            self.mistake_comment_text.delete('1.0', tk.END)
            self.mistake_comment_text.insert('1.0', analysis_item.get('mistakes_comment', ''))
            self.gen_comment_text.delete('1.0', tk.END)
            self.gen_comment_text.insert('1.0', analysis_item.get('gen_comment', ''))

        # Function the saves the selections of the analizer
        def update_analysis(self):
            attempt_item = self.data[self.current_index]
            for item in self.analysis:
                if item['assignment_id'] == attempt_item['assignment_id']:
                    item['correctness'] = self.correctness_combo.get()
                    item['grading'] = self.grading_combo.get()
                    item['mini_hints'] = self.hints_combo.get()
                    item['evidence'] = self.learning_combo.get()
                    item['first_attempt'] = self.act_check1_var.get()
                    item['no_change'] = self.act_check2_var.get()
                    item['clean_up_lines'] = self.act_check3_var.get()
                    item['add_line'] = self.act_check4_var.get()
                    item['remove_line'] = self.act_check5_var.get()
                    item['re_orienting'] = self.act_check6_var.get()
                    item['re_sizing'] = self.act_check7_var.get()
                    item['other1'] = self.act_check8_var.get()
                    item['no_mistakes'] = self.mis_check1_var.get()
                    item['extra_line'] = self.mis_check2_var.get()
                    item['extra_section'] = self.mis_check3_var.get()
                    item['extra_dashes'] = self.mis_check4_var.get()
                    item['missing_line'] = self.mis_check5_var.get()
                    item['missing_section'] = self.mis_check6_var.get()
                    item['missing_dashes'] = self.mis_check7_var.get()
                    item['wrong_size'] = self.mis_check8_var.get()
                    item['wrong_orientation'] = self.mis_check9_var.get()
                    item['wrong_location'] = self.mis_check10_var.get()
                    item['messy_lines'] = self.mis_check11_var.get()
                    item['f_not_r'] = self.mis_check13_var.get()
                    item['other2'] = self.mis_check12_var.get()
                    item['hint_comment'] = self.hint_comment_text.get("1.0",tk.END)
                    item['evidence_comment'] = self.evidence_comment_text.get("1.0",tk.END)
                    item['action_comment'] = self.change_comment_text.get("1.0",tk.END)
                    item['mistakes_comment'] = self.mistake_comment_text.get("1.0",tk.END)
                    item['gen_comment'] = self.gen_comment_text.get("1.0",tk.END)
                    break

        # Function the advances the index and updates the GUI
        def next_image(self):
            self.update_analysis()
            if (self.current_index + 1) > (len(self.data) - 1):
                self.current_index = 0
            else:
                self.current_index = (self.current_index + 1)
            self.update_content()

        # Function the decreases the index and updates the GUI
        def last_image(self):
            self.update_analysis()
            self.current_index = (self.current_index - 1)
            self.update_content()

        # Function that calles save_to_excel and properly saves the data
        def save_to_ouput(self):
            self.update_analysis()
            output_list = []
            for item in self.analysis:
                # Turn the multiple select into a succinct string
                action_list = []
                if item['first_attempt'] != "":
                    action_list.append(item['first_attempt'])
                elif item['no_change'] != "":
                    action_list.append(item['no_change'])
                elif item['clean_up_lines'] != "":
                    action_list.append(item['clean_up_lines'])
                elif item['add_line'] != "":
                    action_list.append(item['add_line'])
                elif item['remove_line'] != "":
                    action_list.append(item['remove_line'])
                elif item['re_orienting'] != "":
                    action_list.append(item['re_orienting'])
                elif item['re_sizing'] != "":
                    action_list.append(item['re_sizing'])
                elif item['other1'] != "":
                    action_list.append(item['other1'])

                # Turn the multiple select into a succinct string
                mistakes_list = []
                if item['no_mistakes'] != "":
                    mistakes_list.append(item['no_mistakes'])
                elif item['extra_line'] != "":
                    mistakes_list.append(item['extra_line'])
                elif item['extra_section'] != "":
                    mistakes_list.append(item['extra_section'])
                elif item['extra_dashes'] != "":
                    mistakes_list.append(item['extra_dashes'])
                elif item['missing_line'] != "":
                    mistakes_list.append(item['missing_line'])
                elif item['missing_section'] != "":
                    mistakes_list.append(item['missing_section'])
                elif item['missing_dashes'] != "":
                    mistakes_list.append(item['missing_dashes'])
                elif item['wrong_size'] != "":
                    mistakes_list.append(item['wrong_size'])
                elif item['wrong_orientation'] != "":
                    mistakes_list.append(item['wrong_orientation'])
                elif item['wrong_location'] != "":
                    mistakes_list.append(item['wrong_location'])
                elif item['messy_lines'] != "":
                    mistakes_list.append(item['messy_lines'])
                elif item['f_not_r'] != "":
                    mistakes_list.append(item['f_not_r'])
                elif item['other2'] != "":
                    mistakes_list.append(item['other2'])

                # Constructor dictionary for multiple selects
                constructor_dict = {
                    'first_attempt': item['first_attempt'],
                    'no_change': item['no_change'],
                    'clean_up_lines': item['clean_up_lines'],
                    'add_line': item['add_line'],
                    'remove_line': item['remove_line'],
                    're_orienting': item['re_orienting'],
                    're_sizing': item['re_sizing'],
                    'other1': item['other1'],
                    'no_mistakes': item['no_mistakes'],
                    'extra_line': item['extra_line'],
                    'extra_section': item['extra_section'],
                    'extra_dashes': item['extra_dashes'],
                    'missing_line': item['missing_line'],
                    'missing_section': item['missing_section'],
                    'missing_dashes': item['missing_dashes'],
                    'wrong_size': item['wrong_size'],
                    'wrong_orientation': item['wrong_orientation'],
                    'wrong_location': item['wrong_location'],
                    'messy_lines': item['messy_lines'],
                    'f_not_r': item['f_not_r'],
                    'other2': item['other2'],
                }

                # Output dictionary that gets converted to an excel file
                output_dict = {
                    "id": item['assignment_id'],
                    "correctness": item['correctness'], 
                    "grading_algorithm": item['grading'],
                    "best_minihint": item['mini_hints'],
                    "learning_evidence": item['evidence'],
                    "student_action": f'{action_list}',
                    "student_mistakes": f'{mistakes_list}',
                    "other_hint": item['hint_comment'],
                    "other_evidence": item['evidence_comment'],
                    "other_action": item['action_comment'],
                    "other_mistakes": item['mistakes_comment'],
                    "general_comment": item['gen_comment'],
                    "constructor_dict": constructor_dict
                }
    
                output_list.append(output_dict)
    
    
            of = pd.DataFrame(output_list)
            save_excel(of, source_file, sID+'_output', if_exists = if_exists)

        # Function that propts the user to save before closing the app
        def confirm_exit(self):
            response = messagebox.askyesnocancel("Confirm Exit", "Want to save changes before exiting?")
            if response is None:
                # User clicked "Cancel"
                return
            elif response:
                # User clicked "Yes,"  
                self.save_to_ouput()
            # Close the application
            self.destroy()
            print(f"Closed at index: {self.current_index}")
            
    # Calls and runs the app
    app = SpatialVisViewer(data, analysis_list, start_index)
    app.mainloop()




   # Example of running functions in order

def validate_svg(svg_path):
    """Check if SVG file is valid and get its dimensions"""
    try:
        with open(svg_path, 'r') as f:
            content = f.read()
        root = etree.fromstring(content.encode('utf-8'))
        
        width = root.attrib.get('width', 'Unknown')
        height = root.attrib.get('height', 'Unknown')
        viewBox = root.attrib.get('viewBox', 'Not set')
        
        print(f"SVG: {svg_path}")
        print(f"  Width: {width}, Height: {height}")
        print(f"  ViewBox: {viewBox}")
        
        return True
    except Exception as e:
        print(f"Invalid SVG {svg_path}: {e}")
        return False


def download_backgrounds(sheet_path, output_path, columns=('grid_image_file_url', 'assignment_code'), sheet_index='assignments'):
    """
    Downloads background images from Excel sheet and saves to specified folder.
    Inputs:
        sheet_path: Path to Excel file
        output_path: Folder to save background images
        columns: Tuple (url_column, name_column)
        sheet_index: Name/index of sheet containing backgrounds
    """
    df = pd.read_excel(sheet_path, sheet_name=sheet_index)
    url_column, name_column = columns
    
    # Create output directory if needed
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for index, row in df.iterrows():
        url = row[url_column]
        name = row[name_column]
        filename = os.path.join(output_path, f"{name}.svg")
        download_svg(url, filename)
    print(f"Background images downloaded to {output_path}!")

# 0. Download background images first
background_folder = r".\backgrounds"
download_backgrounds(
    sheet_path=r".\SV_Students_SE3_2025_Python_Data.xlsx",
    output_path=background_folder,
    columns=('grid_image_file_url', 'assignment_code'),
    sheet_index='assignments'
)

# 1. Prepare data and images
prepare_analysis(
    excel_file=r".\SV_Students_SE3_2025_Python_Data.xlsx",
    image_folder=r".\images",
    sID='36232',
    background_folder=background_folder  # Use the populated folder
)

# 2. Run the analysis GUI
run_analysis(
    image_folder=r".\images",
    excel_file= r".\SV_Students_SE3_2025_Python_Data.xlsx",
    start_index=0,
    sID='36232',
    load_in=True
)
