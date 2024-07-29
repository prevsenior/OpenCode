# %%
import pandas as pd
import gzip
import os

# Name of the folder where the files are located
folder_name = '01_Requested 2023 Plan'

# Full path to the folder
folder_path = os.path.join(os.getcwd(), folder_name)

# List of files to be read
gzip_files = [
    'Investment Attribute.gz',
    'Investment Total Value.gz',
    'Investment Yearly Value.gz',
    'Portfolio Attribute.gz',
    'Portfolio Constraint.gz',
    'Portfolio Investment.gz',
    'Scenario Attribute.gz'
]

# Dictionary to store the DataFrames
dataframes = {}

# Check if the folder exists
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Loop to read each gzip file and store the corresponding DataFrame
    for file in gzip_files:
        file_path = os.path.join(folder_path, file)
        try:
            with gzip.open(file_path, 'rt') as f:
                # Reading the CSV with schema inference, header in the first line, and comma separator
                df = pd.read_csv(f, header=0, sep=',')
                # DataFrame name is the file name without the .gz extension
                df_name = os.path.splitext(file)[0]
                dataframes[df_name] = df
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
else:
    print(f"The folder {folder_path} was not found or is not a directory.")

# Now you have a dictionary of DataFrames, where the keys are the file names (without the .gz extension)
# You can access each DataFrame individually using dataframes['Investment Attribute'], dataframes['Investment Total Value'], etc.

# Example of how to access and visualize the content of the DataFrames
for df_name, df in dataframes.items():
    print(f"\nContent of DataFrame '{df_name}':")
    print(df.head())  # Prints the first few lines of the DataFrame


# %%
dataframes['Scenario Attribute'].info()
# %%
# Perform the joins to create a single DataFrame
if all(key in dataframes for key in ['Investment Attribute', 'Investment Total Value', 'Portfolio Investment', 'Portfolio Attribute', 'Scenario Attribute']):
    # Join Investment Attribute with Investment Total Value
    merged_df = pd.merge(dataframes['Investment Attribute'], dataframes['Investment Total Value'],
                         on=['Investment Id', 'Scenario Id'], how='inner')
    
    # Join the result with Portfolio Investment
    merged_df = pd.merge(merged_df, dataframes['Portfolio Investment'],
                         on=['Investment Id', 'Scenario Id'], how='inner')
    
    # Join the result with Portfolio Attribute
    merged_df = pd.merge(merged_df, dataframes['Portfolio Attribute'],
                         on=['Portfolio Id', 'Scenario Id'], how='inner')
    
    # Join the result with Scenario Attribute
    merged_df = pd.merge(merged_df, dataframes['Scenario Attribute'],
                         on=['Scenario Id'], how='inner')
    
    print("\nSchema of the merged DataFrame:")
    merged_df.info()
    
    print("\nContent of the merged DataFrame:")
    print(merged_df.head())
    
    # Save the merged DataFrame as a CSV file
    csv_file_path = os.path.join(folder_path, f"{folder_name}.csv")
    merged_df.to_csv(csv_file_path, index=False)
    print(f"Merged DataFrame saved as CSV file at: {csv_file_path}")

    # Save the merged DataFrame as a Parquet file
    parquet_file_path = os.path.join(folder_path, f"{folder_name}.parquet")
    merged_df.to_parquet(parquet_file_path, index=False)
    print(f"\nMerged DataFrame saved as Parquet file at: {parquet_file_path}")
else:
    print("One or more required DataFrames are missing.")

# %%
merged_df.info()
# %%
import pandas as pd

# Paths to the Parquet files
parquet_file_1 = '01_Requested 2023 Plan/01_Requested 2023 Plan.parquet'
parquet_file_2 = '03_Executing Plan/03_Executing Plan.parquet'

# Load the Parquet files into separate DataFrames
df1 = pd.read_parquet(parquet_file_1)
df2 = pd.read_parquet(parquet_file_2)

# Function to create a pivot table
def create_pivot_table(df, value_column='Total Value', index_column='Portfolio Name', columns_column='Scenario Name'):
    pivot_table = pd.pivot_table(
        df,
        values=value_column,
        index=index_column,
        columns=columns_column,
        aggfunc='sum',
        fill_value=0  # Fill missing values with 0 in the pivot table creation
    )
    return pivot_table

# Create pivot tables for each DataFrame
pivot_table_1 = create_pivot_table(df1)
pivot_table_2 = create_pivot_table(df2)

# Fill NaN values with 0 in the pivot tables
pivot_table_1 = pivot_table_1.fillna(0)
pivot_table_2 = pivot_table_2.fillna(0)

# Perform a full join on the pivot tables based on Portfolio Name
full_join_table = pd.merge(
    pivot_table_1,
    pivot_table_2,
    how='outer',
    on='Portfolio Name',
    suffixes=('_df1', '_df2')
)
full_join_table = full_join_table.fillna(0)

# Calculate the differences between the corresponding columns
full_join_table['Difference'] = full_join_table.iloc[:, 1] - full_join_table.iloc[:, 0]

# Format the values with 2 decimal places
full_join_table = full_join_table.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

# Display the full join table with differences
print("\nFull Join Table with Differences:")
print(full_join_table)

# %%
full_join_table
