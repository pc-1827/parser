import pandas as pd
import camelot

def HDFCstatementExtractor(filePath):

    # Extracts relevant tables from the bank statement and concatenates into one table
    tableData = tableDataExtractor(filePath)

    # Performs string and table operations to convert tableData into statement dataframe
    statement = tableDataToStatementConverter(tableData)

    return statement

def tableDataExtractor(filePath):

    # Extracts all possible tables from the PDF using camelot
    tableList = camelot.read_pdf(filePath, pages = '1-end', flavor = 'stream')

    dfs_to_concat = []

    for table in tableList:
        table_df = table.df

        # Check if the DataFrame has at least two columns

        if table_df.shape[1] > 1:
            if 'Statement of account' in table_df.iloc[:, 1].values and 'Nomination : Registered' in table_df.iloc[:, 0].values:
                # Find the index of the 'Statement of account' row
                index = table_df[table_df.iloc[:, 1] == 'Statement of account'].index

                if not index.empty:
                    # Extract rows from the next row onward
                    table_df = table_df.iloc[index[0] + 1:]
                    dfs_to_concat.append(table_df)

    df = pd.concat(dfs_to_concat, ignore_index=True)

    return df

def tableDataToStatementConverter(tableData):
    df = tableData

    # Insert new columns so that clustered data can be converted into individual columns
    df.insert(0, 'New1', "")
    df.insert(3, 'New2', "")
    df.insert(4, 'New3', "")

    # Splitting clustered data into new columns
    df = df.apply(process_row, axis=1)

    # Deleted unnecessary column
    df = df.iloc[:, :-1]

    # Combining rows which has data spread across multiple rows
    statement = description_wrapper(df)

    return statement


# Function to split text based on newline and assign to columns
def process_row(row):

    # Split column 2 based on newline
    col2_values = row[0].split('\n')
    if len(col2_values) > 1:
        row['New1'] = col2_values[0]  # Assign data before \n to column 1
        row[0] = col2_values[1]  # Assign data after \n to column 2

    # Split column 3 based on newline
    col3_values = row[1].split('\n')  # Split only once to handle multiple \n
    row[1] = col3_values[0]  # Assign data before first \n to column 3
    row['New2'] = col3_values[1] if len(col3_values) > 1 else ''  # Assign data after first \n to column 4 if available
    row['New3'] = col3_values[2] if len(col3_values) > 2 else ''  # Assign data after second \n to column 5 if available

    # Combines data in two columns into one
    if pd.notna(row[4]) and row[4] != "":
        if row[3] == "":
            row['New3'] = row[2]
            row[2] = ""
            row[3] = row[4]

        else:
            row[2] = row[3]
            row[3] = row[4]

    return row

# Function to wrap multiple spread rows into single row and delete unnecessary rows
def description_wrapper(dataframe):
    df = dataframe

    # Concatenates row values into topmost row of every transaction
    desc = df.iloc[1, 1]
    step = 1
    for i in range(2, df.shape[0]):
        if df.iloc[i, 0] != "":
            df.iloc[i - step, 1] = desc
            desc = df.iloc[i, 1]
            step = 1

        elif df.iloc[i, 0] == "":
            desc = desc + df.iloc[i, 1]
            step = step + 1
            if i == df.shape[0] - 1:
                df.iloc[i - step + 1, 1] = desc

    # Remove all the uneccessary rows
    mask = (df.iloc[:, 0] == "")  # Check for empty values in column 1
    filtered_df = df[~mask]  # Filter out rows with empty values in column 1
    result_df = filtered_df.drop_duplicates(subset = 0)  # Remove duplicate rows from the DataFrame
    result_df.reset_index(drop=True, inplace=True)  # Display the filtered DataFrame

    return result_df
