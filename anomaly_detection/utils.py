import re
import pandas as pd

# Define regex patterns
DATETIME_PATTERN = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})'
IP_PATTERN = r"'clientip':\s'([\d\.]+)'"
METHOD_PATTERN = r"'method':\s'(\w+)'"
ENDPOINT_PATTERN = r"'url':\s'([^']+)'"
RESPONSE_CODE_PATTERN = r"'status':\s(\d+)"

def extract_data(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else None

def preprocess_dataframe(data, window_size=30):
    pd.set_option('display.max_columns', None)
    # df = pd.DataFrame(df)
    # print(df.type)
    # print(df)
    # data_arr = []
    # for log in data:
    #     temp = []
    #     for item in log:
    #         temp.append(item[1])
    #     data_arr.append(temp)
    # print(data_arr)
    df = pd.DataFrame(data, columns=["Line"])
    # df = df[['Time''Line']]
    # print(df)
    # Extract necessary fields
    df['DateTime'] = df['Line'].apply(lambda x: extract_data(DATETIME_PATTERN, x))
    df['IP_Address'] = df['Line'].apply(lambda x: extract_data(IP_PATTERN, x))
    df['HTTP_Method'] = df['Line'].apply(lambda x: extract_data(METHOD_PATTERN, x))
    df['Endpoint'] = df['Line'].apply(lambda x: extract_data(ENDPOINT_PATTERN, x))
    df['Response_Code'] = df['Line'].apply(lambda x: extract_data(RESPONSE_CODE_PATTERN, x))
    
    # Drop unnecessary columns
    df = df.drop(['Line'], axis=1)
    # print("-----------", df)
    # Convert DateTime column to datetime type and sort values
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S,%f')
    df = df.sort_values(by='DateTime').reset_index(drop=True)
    
    # Drop unwanted columns post sorting
    df = df.drop(['DateTime', 'IP_Address', 'HTTP_Method'], axis=1)

    # Create sliding windows
    new_df = create_sliding_window_df(df, window_size)

    return new_df

def create_sliding_window_df(df, window_size):
    # Flatten the DataFrame into a single row
    flattened_data = df.values.flatten()
    
    # Create a new DataFrame from the flattened data
    new_df = pd.DataFrame([flattened_data])
    
    return new_df

def create_dummy(df):
    new_df = pd.DataFrame()
    
    for column_name, column_data in df.items():
        try:
            # Attempt to convert the column_name to an integer for the check.
            column_idx = int(column_name)
        except ValueError:
            # If conversion fails, continue to next column
            continue
        
        if column_idx % 2 == 0:
            new_col_name_forget_password = str(column_name) + "_/forget_password"
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
# Example usage:
# df = pd.read_csv('logfile.csv')
# new_df = preprocess_dataframe(df, window_size=30)
# print(new_df)