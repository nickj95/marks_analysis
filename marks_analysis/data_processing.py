import pandas as pd


def load_data(filenames, sheet_names):
    """
    Load data from multiple Excel files and sheets into pandas DataFrames.

    Parameters:
    filenames (list): List of file paths to Excel files.
    sheet_names (list): List of sheet names to read from each Excel file.

    Returns:
    list: List of pandas DataFrames containing the loaded data.
    """
    dataframes = []
    for filename, sheet_name in zip(filenames, sheet_names):
        for sheet in sheet_name:
            dataframes.append(pd.read_excel(filename, sheet_name=sheet))
    return dataframes


def preprocess_marker_data(df):
    """
    Preprocess marker data by dropping unnecessary columns and renaming columns.

    Parameters:
    df (pandas.DataFrame): DataFrame containing marker data.

    Returns:
    pandas.DataFrame: Preprocessed marker data.
    """
    df = df.drop('Unnamed: 0', axis=1)
    df = df.rename({
        'Exam Board Code': 'Exam Board',
        'Paper Name': 'Paper',
        'Candidate Number': 'CandNo',
        'Your Name': 'Examiner',
        'Overall Initial Mark ': 'Initial Mark',
    }, axis=1)
    df['CandNo'] = df['CandNo'].astype(str)
    df['Initial Mark'] = df['Initial Mark'].astype(float)
    return df


def preprocess_paper_data(df):
    """
    Preprocess paper data by dropping unnecessary columns and renaming columns.

    Parameters:
    df (pandas.DataFrame): DataFrame containing paper data.

    Returns:
    pandas.DataFrame: Preprocessed paper data.
    """
    df = df.drop('Unnamed: 0', axis=1)
    df = df.rename({
        'Exam Board Code': 'Exam Board',
        'Paper Name': 'Paper',
        'Candidate Number': 'CandNo'
    }, axis=1)
    df['CandNo'] = df['CandNo'].astype(str)
    return df