import re
import pandas as pd
from sklearn.utils import shuffle

# Define regex patterns
DATETIME_PATTERN = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})'
IP_PATTERN = r"'clientip':\s'([\d\.]+)'"
METHOD_PATTERN = r"'method':\s'(\w+)'"
ENDPOINT_PATTERN = r"'url':\s'([^']+)'"
RESPONSE_CODE_PATTERN = r"'status':\s(\d+)"

def create_dummies(df):
    # This is to create dummies for test set
    new_df = pd.DataFrame()

    for column_name, column_data in df.items():
        try:
            # Attempt to convert the column_name to an integer for the check.
            column_idx = int(column_name)
        except ValueError:
            # If conversion fails, continue to next column
            continue

        if column_idx % 2 == 0:
            new_col_name_forget_password = str(
                column_name) + "_/forget_password"
            new_col_name_login = str(column_name) + "_/login"

            # Create new columns with appropriate Boolean values
            new_df[new_col_name_forget_password] = column_data != "/login"
            new_df[new_col_name_login] = column_data == "/login"
        else:
            new_col_name_200 = str(column_name) + "_200"
            new_col_name_401 = str(column_name) + "_401"

            # Create new columns with appropriate Boolean values
            new_df[new_col_name_200] = column_data != 200
            new_df[new_col_name_401] = column_data == 400
    return new_df

def extract_data(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else None


def preprocess_dataframe(df, window_size=30):
    df = df[['Time', 'Line']]
    # Extract necessary fields
    df['DateTime'] = df['Line'].apply(
        lambda x: extract_data(DATETIME_PATTERN, x))
    df['IP_Address'] = df['Line'].apply(lambda x: extract_data(IP_PATTERN, x))
    df['HTTP_Method'] = df['Line'].apply(
        lambda x: extract_data(METHOD_PATTERN, x))
    df['Endpoint'] = df['Line'].apply(
        lambda x: extract_data(ENDPOINT_PATTERN, x))
    df['Response_Code'] = df['Line'].apply(
        lambda x: extract_data(RESPONSE_CODE_PATTERN, x))

    # Drop unnecessary columns
    df = df.drop(['Line', 'Time'], axis=1)

    # Convert DateTime column to datetime type and sort values
    df['DateTime'] = pd.to_datetime(
        df['DateTime'], format='%Y-%m-%d %H:%M:%S,%f')
    df = df.sort_values(by='DateTime').reset_index(drop=True)

    # Drop unwanted columns post sorting
    df = df.drop(['DateTime', 'IP_Address', 'HTTP_Method'], axis=1)

    # Create sliding windows
    new_df = create_sliding_window_df(df, window_size)

    return new_df


def create_sliding_window_df(df, window_size):
    row_count = len(df)
    windows = []

    for i in range(row_count - window_size + 1):
        window_data = df.iloc[i:i + window_size].values.flatten()
        windows.append(window_data)

    # Create a new DataFrame from the list of windows
    new_df = pd.DataFrame(windows)

    return new_df


def mix_dataset(df1, df2):
    df1 = preprocess_dataframe(df1)
    df2 = preprocess_dataframe(df2)
    df1['gold truth'] = 1
    df2['gold truth'] = 0
    # Combine the two DataFrames
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Shuffle the combined DataFrame
    shuffled_df = shuffle(combined_df).reset_index(drop=True)

    # Save or display the final DataFrame
    shuffled_df.to_csv("test_combined.csv", index=False)





# mix_dataset(pd.read_csv("test_normal.csv"), pd.read_csv("test_abnormal.csv"))
