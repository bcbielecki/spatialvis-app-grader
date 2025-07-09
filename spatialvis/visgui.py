
from spatialvis.viscache import StartupCache
from spatialvis.viscore import download_backgrounds, prepare_analysis, run_analysis, run_analysis2
from spatialvis import globals
import sys
import random
from pathlib import Path
from PySide6 import QtCore, QtWidgets, QtGui

import os

# QT Designer: https://realpython.com/qt-designer-python/
# QT Designer download: https://www.qt.io/download-qt-installer
# QT Designer manual: https://doc.qt.io/qt-6/qtdesigner-manual.html
# Use `pyuic6 input.ui -o output.py` to convert .ui files to .py files
# PySide6 docs: https://doc.qt.io/qtforpython-6/



class SpatialVisViewer(QtWidgets.QWidget):
    def __init__(self, data, analysis_list, start_index):
        super().__init__()
        self.data = data
        self.analysis = analysis_list
        self.current_index = start_index

        self.setWindowTitle("Spatial Vis Image Viewer")
        self.resize(1400, 700)

        # Layouts
        main_layout = QtWidgets.QGridLayout(self)
        control_layout = QtWidgets.QHBoxLayout()
        problem_layout = QtWidgets.QVBoxLayout()
        image_layout = QtWidgets.QGridLayout()
        selection_layout = QtWidgets.QGridLayout()
        function_layout = QtWidgets.QHBoxLayout()
        comments_layout = QtWidgets.QGridLayout()

        # Control Frame (top)
        # ... add buttons, etc. as needed ...

        # Problem Frame (left)
        self.problem_image_label = QtWidgets.QLabel()
        self.problem_image_label.setFixedSize(320, 320)
        self.problem_label = QtWidgets.QLabel()
        self.problem_label.setWordWrap(True)
        problem_layout.addWidget(self.problem_image_label)
        problem_layout.addWidget(self.problem_label)

        # Image Frame (center)
        self.solution_image_label = QtWidgets.QLabel()
        self.solution_image_label.setFixedSize(320, 320)
        self.attempt_image_label = QtWidgets.QLabel()
        self.attempt_image_label.setFixedSize(320, 320)
        image_layout.addWidget(self.solution_image_label, 0, 0)
        image_layout.addWidget(self.attempt_image_label, 0, 1)

        # Data Frame (right of images)
        self.attempt_label = QtWidgets.QLabel()
        self.message_label = QtWidgets.QLabel()
        self.correct_label = QtWidgets.QLabel()
        self.missing_label = QtWidgets.QLabel()
        self.additional_label = QtWidgets.QLabel()
        data_vbox = QtWidgets.QVBoxLayout()
        for w in [self.attempt_label, self.message_label, self.correct_label, self.missing_label, self.additional_label]:
            data_vbox.addWidget(w)
        image_layout.addLayout(data_vbox, 0, 2)

        # Selection Frame (bottom)
        self.correctness_combo = QtWidgets.QComboBox()
        self.correctness_combo.addItems([
            '[Not evaluated]', 'Correct', 'Incorrect'
        ])
        self.grading_combo = QtWidgets.QComboBox()
        self.grading_combo.addItems([
            '[Not evaluated]', 'Graded properly', 'Too leaniant', 'Too strict'
        ])
        self.hints_combo = QtWidgets.QComboBox()
        self.hints_combo.addItems([
            '[Not evaluated]', 'Correct sketch', 'You may be missing a line',
            'You may have too many line(s)', 'Close! Draw more carefully',
            'Hidden line(s) incorrect', 'Try again', 'Other'
        ])
        self.learning_combo = QtWidgets.QComboBox()
        self.learning_combo.addItems([
            '[Not evaluated]', 'Learninng from previous attempt', 'Learing from previous problem',
            'Correct: no evidence', 'Incorrect: no evidence', 'Learning from mini-hints',
            'Learning from hints', 'Small changes', 'Repeated mistake', 'Not learning from feedback', 'Other'
        ])
        selection_layout.addWidget(QtWidgets.QLabel("Student correctness:"), 0, 0)
        selection_layout.addWidget(self.correctness_combo, 1, 0)
        selection_layout.addWidget(QtWidgets.QLabel("Grading algorithm:"), 0, 1)
        selection_layout.addWidget(self.grading_combo, 1, 1)
        selection_layout.addWidget(QtWidgets.QLabel("Best mini-hint:"), 0, 2)
        selection_layout.addWidget(self.hints_combo, 1, 2)
        selection_layout.addWidget(QtWidgets.QLabel("Evidence of learning:"), 0, 3)
        selection_layout.addWidget(self.learning_combo, 1, 3)

        # Action and Mistake Checkboxes (left and right)
        self.action_checks = [QtWidgets.QCheckBox(text) for text in [
            'First attempt', 'No change', 'Clean up lines', 'Add line(s)', 'Remove line(s)', 'Re-orienting', 'Re-sizing', 'Other'
        ]]
        action_vbox = QtWidgets.QVBoxLayout()
        action_vbox.addWidget(QtWidgets.QLabel("Change from previous (choose multiple):"))
        for cb in self.action_checks:
            action_vbox.addWidget(cb)
        selection_layout.addLayout(action_vbox, 2, 0, 2, 1)

        self.mistake_checks = [QtWidgets.QCheckBox(text) for text in [
            'No mistakes', 'Extra line', 'Extra section', 'Extra dashes', 'Missing line', 'Missing section',
            'Missing dashes', 'Wrong size', 'Wrong orientation', 'Wrong location', 'Messy lines', 'Flip, not rotate', 'Other'
        ]]
        mistake_vbox = QtWidgets.QVBoxLayout()
        mistake_vbox.addWidget(QtWidgets.QLabel("Student mistakes (choose multiple):"))
        for cb in self.mistake_checks:
            mistake_vbox.addWidget(cb)
        selection_layout.addLayout(mistake_vbox, 2, 1, 2, 1)

        # Comments
        self.hint_comment_text = QtWidgets.QTextEdit()
        self.evidence_comment_text = QtWidgets.QTextEdit()
        self.change_comment_text = QtWidgets.QTextEdit()
        self.mistake_comment_text = QtWidgets.QTextEdit()
        self.gen_comment_text = QtWidgets.QTextEdit()
        comments_layout.addWidget(QtWidgets.QLabel("Other hint:"), 0, 0)
        comments_layout.addWidget(self.hint_comment_text, 1, 0)
        comments_layout.addWidget(QtWidgets.QLabel("Other evidence:"), 0, 1)
        comments_layout.addWidget(self.evidence_comment_text, 1, 1)
        comments_layout.addWidget(QtWidgets.QLabel("Other change:"), 2, 0)
        comments_layout.addWidget(self.change_comment_text, 3, 0)
        comments_layout.addWidget(QtWidgets.QLabel("Other mistake:"), 2, 1)
        comments_layout.addWidget(self.mistake_comment_text, 3, 1)
        comments_layout.addWidget(QtWidgets.QLabel("General comments:"), 4, 0, 1, 2)
        comments_layout.addWidget(self.gen_comment_text, 5, 0, 1, 2)
        selection_layout.addLayout(comments_layout, 2, 2, 2, 2)

        # Function Frame (bottom)
        self.prev_button = QtWidgets.QPushButton("Previous attempt")
        self.next_button = QtWidgets.QPushButton("Next attempt")
        self.update_button = QtWidgets.QPushButton("Update analysis")
        self.save_button = QtWidgets.QPushButton("Save analysis")
        function_layout.addWidget(self.save_button)
        function_layout.addWidget(self.update_button)
        function_layout.addWidget(self.prev_button)
        function_layout.addWidget(self.next_button)

        # Add layouts to main layout
        main_layout.addLayout(control_layout, 0, 0, 1, 2)
        main_layout.addLayout(problem_layout, 1, 0, 2, 1)
        main_layout.addLayout(image_layout, 1, 1)
        main_layout.addLayout(selection_layout, 2, 1)
        main_layout.addLayout(function_layout, 3, 0, 1, 2)

        # Connect signals
        self.next_button.clicked.connect(self.next_image)
        self.prev_button.clicked.connect(self.prev_image)
        self.update_button.clicked.connect(self.update_analysis)
        self.save_button.clicked.connect(self.save_to_output)

        # Load initial content
        self.update_content()

    def update_content(self):
        # Load images and update labels
        item = self.data[self.current_index]
        def load_image(path):
            if os.path.exists(path):
                pixmap = QtGui.QPixmap(path)
                return pixmap.scaled(320, 320, QtCore.Qt.KeepAspectRatio)
            else:
                return QtGui.QPixmap(320, 320)
        self.problem_image_label.setPixmap(load_image(item['problem_path']))
        self.solution_image_label.setPixmap(load_image(item['solution_path']))
        self.attempt_image_label.setPixmap(load_image(item['sketch_path']))
        self.problem_label.setText(item.get('problem_description', ''))

        self.attempt_label.setText(f"Attempt: {item.get('attempt', 0)+1}")
        self.message_label.setText(f"Displayed message: {item.get('results', '')}")
        self.correct_label.setText(f"Correct percent: {item.get('correct_per', 'N/A')}")
        self.missing_label.setText(f"Missing percent: {item.get('missing_per', 'N/A')}")
        self.additional_label.setText(f"Additional percent: {item.get('additional_per', 'N/A')}")

        # Set comboboxes and checkboxes from analysis
        analysis_item = self.analysis[self.current_index]
        self.correctness_combo.setCurrentText(analysis_item.get('correctness', '[Not evaluated]'))
        self.grading_combo.setCurrentText(analysis_item.get('grading', '[Not evaluated]'))
        self.hints_combo.setCurrentText(analysis_item.get('mini_hints', '[Not evaluated]'))
        self.learning_combo.setCurrentText(analysis_item.get('evidence', '[Not evaluated]'))

        # Set checkboxes
        for i, key in enumerate(['first_attempt', 'no_change', 'clean_up_lines', 'add_line', 'remove_line', 're_orienting', 're_sizing', 'other1']):
            self.action_checks[i].setChecked(bool(analysis_item.get(key, '')))
        for i, key in enumerate(['no_mistakes', 'extra_line', 'extra_section', 'extra_dashes', 'missing_line', 'missing_section', 'missing_dashes', 'wrong_size', 'wrong_orientation', 'wrong_location', 'messy_lines', 'f_not_r', 'other2']):
            self.mistake_checks[i].setChecked(bool(analysis_item.get(key, '')))

        # Set comments
        self.hint_comment_text.setPlainText(analysis_item.get('hint_comment', ''))
        self.evidence_comment_text.setPlainText(analysis_item.get('evidence_comment', ''))
        self.change_comment_text.setPlainText(analysis_item.get('action_comment', ''))
        self.mistake_comment_text.setPlainText(analysis_item.get('mistakes_comment', ''))
        self.gen_comment_text.setPlainText(analysis_item.get('gen_comment', ''))

    def update_analysis(self):
        # Save current selections to analysis
        item = self.data[self.current_index]
        analysis_item = self.analysis[self.current_index]
        analysis_item['correctness'] = self.correctness_combo.currentText()
        analysis_item['grading'] = self.grading_combo.currentText()
        analysis_item['mini_hints'] = self.hints_combo.currentText()
        analysis_item['evidence'] = self.learning_combo.currentText()
        for i, key in enumerate(['first_attempt', 'no_change', 'clean_up_lines', 'add_line', 'remove_line', 're_orienting', 're_sizing', 'other1']):
            analysis_item[key] = self.action_checks[i].isChecked()
        for i, key in enumerate(['no_mistakes', 'extra_line', 'extra_section', 'extra_dashes', 'missing_line', 'missing_section', 'missing_dashes', 'wrong_size', 'wrong_orientation', 'wrong_location', 'messy_lines', 'f_not_r', 'other2']):
            analysis_item[key] = self.mistake_checks[i].isChecked()
        analysis_item['hint_comment'] = self.hint_comment_text.toPlainText()
        analysis_item['evidence_comment'] = self.evidence_comment_text.toPlainText()
        analysis_item['action_comment'] = self.change_comment_text.toPlainText()
        analysis_item['mistakes_comment'] = self.mistake_comment_text.toPlainText()
        analysis_item['gen_comment'] = self.gen_comment_text.toPlainText()

    def next_image(self):
        self.update_analysis()
        self.current_index = (self.current_index + 1) % len(self.data)
        self.update_content()

    def prev_image(self):
        self.update_analysis()
        self.current_index = (self.current_index - 1) % len(self.data)
        self.update_content()

    def save_to_output(self):
        self.update_analysis()
        # Implement your save logic here (e.g., write to Excel)
        QtWidgets.QMessageBox.information(self, "Save", "Analysis saved!")



def launch_gui():
    app = QtWidgets.QApplication([])
    viewer = SpatialVisViewer([1], [], 0)
    viewer.show()

    sys.exit(app.exec())

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
    background_folder = globals.PATH_DATA_BACKGROUNDS
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
    data, analysis_list, start_index = run_analysis2(
        image_folder=globals.PATH_DATA_IMAGES,
        excel_file=str(excel_file_path),
        start_index=0,
        sID=student_id,
        load_in=True
    )

    app = QtWidgets.QApplication([])
    viewer = SpatialVisViewer(data, analysis_list, start_index)
    viewer.show()

    sys.exit(app.exec())