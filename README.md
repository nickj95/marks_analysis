**README for `marks_analysis`**

**Marks Analysis Package**
`marks_analysis` is a Python package designed for analyzing exam marks data. It includes functions for preprocessing data, performing statistical analyses, generating visualizations, and saving results. The package ensures that the analysis is robust and adaptable to changes in the dataset, including the absence of specific examiners.

### Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)
-   [Functions](#functions)
    -   [Data Loading and Preprocessing](#data-loading-and-preprocessing)
    -   [Statistical Analysis and Visualization](#statistical-analysis-and-visualization)
-   [Statistics Explanation](#statistics-explanation)
-   [Graph Interpretation](#graph-interpretation)

### Installation

To keep this package-toolkit modular and easily editable, installing via Git or pip is unnecessary. Instead, simply use the provided folder structure and follow the guidelines in `example_usage.py`. This approach allows users to directly work with the provided code and make any necessary adjustments without the need for complex installation procedures or ongoing package maintenance.

However, if you prefer to install the package directly into Python, you can do so by following these steps:

1.  **Install Directly from GitHub**:
```pip install git+https://github.com/nickj95/marks_analysis.git```

### Usage

Here’s an example of how to use the package:

1.  **Load the data and import functions:**
```
    from data_processing import load_data, preprocess_marker_data, preprocess_paper_data
    from analysis import analyze_data, analyze_all_examiners
```
If installed from Github use the following import function: 
```
from marks_analysis import load_data, preprocess_marker_data, preprocess_paper_data, analyze_data, analyze_all_examiners
```
```
    filenames = ["data/{file1}.xlsx", "data/{file2}.xlsx"]  
    sheet_names = [[0, 1], [0, 1]]  
    dfs = load_data(filenames, sheet_names)
   ```
If you have several files, update ```sheet_names``` accordingly. The primary data is usually found within the first and second sheets within a workbook. If that ever changes update the ```sheet_names``` values]

2.  **Preprocess the data:**
```
    df_marker = preprocess_marker_data(dfs[0].append(dfs[2]))  
    df_paper = preprocess_paper_data(dfs[1].append(dfs[3]))
```
3.  **Analyze data by examiner and marks:**
```
	analyze_data(df_marker, 'Examiner', 'Initial Mark', boards=[None, 'DPPE', 'DMHP'])  
    analyze_data(df_marker, 'Examiner', 'Agreed Mark', boards=[None, 'DPPE', 'DMHP'])  
    analyze_data(df_paper, 'Paper', 'Agreed Mark', boards=[None, 'DPPE', 'DMHP'])
 ```
 Note: here you may add or remove different examination boards. 
 
 4.  **Analyze supplementary data by examiner:**
```
analyze_all_examiners(df_marker)
```
### Functions
#### Data Loading and Preprocessing

-   **`load_data(filenames, sheet_names)`**: Loads data from multiple Excel files.
    
    **Parameters:**
    
    -   `filenames` (list): List of file paths to the Excel files.
    -   `sheet_names` (list): List of sheet names to load from each file.
    
    **Returns:**
    
    -   `dfs` (list): List of DataFrames for each loaded sheet.
-   **`preprocess_marker_data(df)`**: Preprocesses the marker data.
    
    **Parameters:**
    
    -   `df` (DataFrame): The raw marker data.
    
    **Returns:**
    
    -   `df_marker` (DataFrame): The preprocessed marker data.
-   **`preprocess_paper_data(df)`**: Preprocesses the paper data.
    
    **Parameters:**
    
    -   `df` (DataFrame): The raw paper data.
    
    **Returns:**
    
    -   `df_paper` (DataFrame): The preprocessed paper data.

#### Statistical Analysis and Visualization

-   **`analyze_data(data, by, mark, boards=[None])`**: Analyzes data by grouping it according to the specified columns.
    
    **Parameters:**
    
    -   `data` (DataFrame): The data to analyze.
    -   `by` (str): The column to group by.
    -   `mark` (str): The column containing marks.
    -   `boards` (list): List of exam boards to filter by (optional).
-   **`analyze_all_examiners(df_marker)`**: Analyzes data for all examiners and generates visualizations.
    
    **Parameters:**
    
    -   `df_marker` (DataFrame): The marker data.
-   **`check_agreed_marks(df_marker)`**: Checks if agreed marks differ for candidates.
    
    **Parameters:**
    
    -   `df_marker` (DataFrame): The marker data.
    
    **Returns:**
    
    -   `value_counts` (Series): Counts of agreed and differing marks.
-   **`plot_mark_differences(df_marker)`**: Plots differences between initial and agreed marks.
    
    **Parameters:**
    
    -   `df_marker` (DataFrame): The marker data.
    
    **Returns:**
    
    -   `df_difference` (DataFrame): The DataFrame with calculated differences.
-   **`plot_absolute_mark_differences(df_marker)`**: Plots absolute differences between initial and agreed marks.
    
    **Parameters:**
    
    -   `df_marker` (DataFrame): The marker data.
    
    **Returns:**
    
    -   `df` (DataFrame): The DataFrame with absolute mark differences.
    
### Statistics Explanation

-   **Cands**: The number of candidates who were evaluated.
-   **>=70, >=60, >=50, >=40, >=30, <30**: These statistics represent the percentage of candidates whose scores fall within specific grading categories. For example, `>=70` indicates the percentage of candidates who scored 70 or above.
-   **Q1 (First Quartile)**: The score below which 25% of the data fall. It indicates the lower quartile and provides a measure of the lower end of the score distribution.
-   **Median**: The middle value of the score distribution. It separates the higher half from the lower half and is a robust measure of central tendency.
-   **Q3 (Third Quartile)**: The score below which 75% of the data fall. It indicates the upper quartile and provides a measure of the higher end of the score distribution.
-   **Mean**: The average score. It provides a measure of central tendency but can be affected by extreme values (outliers).
-   **St. Dev. (Standard Deviation)**: Measures the amount of variation or dispersion in the scores. A higher standard deviation indicates more spread out scores.
-   **Max**: The highest score among the candidates.
-   **Min**: The lowest score among the candidates.
-   **KS P**: The p-value from the Kolmogorov-Smirnov test, indicating the likelihood that two samples are drawn from the same distribution. Lower values suggest significant differences between distributions.

### Graph Interpretation
The package generates several types of graphs to visualize the data and results:

#### Marks Distribution by Category

-   **Graph Description**: These are the main graphs of the analysis. They show the distribution of marks for each category (e.g., examiner or paper) by exam board and in aggregate using box plots.
-   **Usage**: Helps to identify if any categories have significantly different marking patterns compared to others.
-   **Interpretation**:
    -   **Box Plot**: Each box plot shows the median, quartiles, and potential outliers for the marks within a category.
    -   **Color Coding (Hue)**: Categories are color-coded based on their KS p-value significance levels, indicating how likely the mark distribution of a category differs from others.
    -   **Annotations**: If enabled, annotations show the number of observations for each category, providing additional context on the sample size.
    -   **Axes**: The x-axis represents the marks, while the y-axis represents the categories. The plot's range and ticks are set to ensure all marks are visible.

#### Agreed Marks Distribution

-   **Graph Description**: This graph shows the distribution of agreed marks.
-   **Usage**: Used to assess the consistency and fairness in the agreed marks.
-   **Interpretation**: Consistency in the distribution of agreed marks with the average (e.g., a normal distribution without large tails) suggests fair and uniform marking practices. 

#### Difference Between Initial and Agreed Marks

-   **Graph Description**: This graph shows the differences between initial and agreed marks for all examiners.
-   **Usage**: Helps to understand the extent of changes made during the marking process.
-   **Interpretation**: A large spread in differences might indicate significant adjustments during the review process, potentially due to discrepancies in initial marking. Ideally, the graph should exhibit a normal distribution with most changes occurring between -1 and 1.

#### Absolute Mark Differences per Examiner

-   **Graph Description**: This bar plot displays the total absolute differences in marks for each examiner.
-   **Usage**: Identifies examiners with the highest discrepancies between initial and agreed marks.
-   **Interpretation**: Higher total absolute differences suggest more significant changes or corrections needed in an examiner’s marking. However, note that a higher spread in differences may simply reflect an examiner with many students. Therefore, always interpret these findings with caution and consider the context of the overall results.

###   Output Files and Their Usage

The `marks_analysis` package generates several output files during the analysis process. These files are organized into specific directories for easy access and use:

#### Figures

-   **Directory**: `figures/`
-   **File Types**: PNG
-   **Usage**: The figures directory contains visualizations generated by the analysis functions. These visualizations include:
    -   **Marks Distribution by Categories**: Shows the distribution of marks given by each category.
    -   **Agreed Marks Distribution**: Displays the distribution of agreed marks.
    -   **Difference Between Initial and Agreed Marks**: Illustrates the differences between initial and agreed marks for all examiners.
    -   **Absolute Mark Differences**: Bar plot showing the total absolute differences in marks for each examiner.

These figures are used to visually assess the marking patterns and identify any significant discrepancies or trends in the data. They provide a quick and intuitive way to interpret the statistical results.

#### Breakdown Tables

-   **Directory**: `files/`
-   **File Types**: CSV, HTML, LaTeX
-   **Usage**: The markdown_files directory contains detailed breakdown tables of the analysis results. These files include:
    -   **CSV**: Easily importable into spreadsheet software for further analysis or reporting.
    -   **HTML**: Suitable for viewing in web browsers or embedding into reports.
    -   **LaTeX**: Ideal for inclusion in presentations if needed.

These breakdown tables provide comprehensive statistical summaries for different categories (e.g., examiners, papers) and can be used for further analysis and documentation.

### Concluding Remarks

The `marks_analysis` package offers a robust toolkit for analyzing exam marks data, generating both statistical summaries and visual insights. By organizing the output files into dedicated directories, the package ensures that users can easily access and utilize the results for further analysis, reporting, and presentation.

By following the guidelines provided in this readme and `example_usage.py`, users can efficiently load, preprocess, and analyze their data, gaining quick insights into the marking process and ensuring consistency and fairness in evaluations.
