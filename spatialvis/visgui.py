import json


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