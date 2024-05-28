import pandas as pd
import camelot

def KotakstatementExtractor(filePath):

    # Extracts relevant tables from the bank statement and concatenates into one table
    tableData = tableDataExtractor(filePath)

    # Performs string and table operations to convert tableData into statement dataframe
    statement = tableDataToStatementConverter(tableData)

    return statement

def tableDataExtractor(filePath):

    # Extracts all possible tables from the PDF using camelot
    tableList = camelot.read_pdf(filePath, pages = '1-end', flavor = 'stream', row_tol = 10)

    # Extract DataFrames from tables excluding the first and last tables
    dfs_to_concat = [table.df for table in tableList[1:]]

    # Concatenate DataFrames
    df = pd.concat(dfs_to_concat, ignore_index=True)

    # Combines two Date column into one and deletes the extra column
    df[1] = df[1] + df[2]
    df.drop(columns = [2], inplace = True)

    return df

def tableDataToStatementConverter(tableData):
    df = tableData

    # Combining rows which has data spread across multiple rows
    statement = description_wrapper(df)

    return statement

def description_wrapper(dataframe):
    df = dataframe

    # Concatenates row values into topmost row of every transaction
    desc = df.iloc[1, 2]
    step = 1
    for i in range(2, df.shape[0]):
        if df.iloc[i, 1] != "":
            df.iloc[i - step, 2] = desc
            desc = df.iloc[i, 2]
            step = 1

        elif df.iloc[i, 1] == "":
            desc = desc + df.iloc[i, 2]
            step = step + 1
            if i == df.shape[0] - 1:
                df.iloc[i - step + 1, 2] = desc

    # Remove all the uneccessary rows
    mask = (df.iloc[:, 1] == "") | (df.iloc[:, 1] == "Date")  # Check for empty values or "Date" string in column 1
    filtered_df = df[~mask]  # Filter out rows with empty values or "Date" string in column 1
    result_df = filtered_df.drop_duplicates(subset = 0)  # Remove duplicate rows from the DataFrame
    result_df.reset_index(drop=True, inplace=True)  # Display the filtered DataFrame

    return result_df
