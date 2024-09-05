import pandas as pd
from datetime import datetime

# Load the CSV files
try:
    # Read the CSV files
    df = pd.read_csv('data.csv', encoding='utf-8')
    list_from_drive = pd.read_csv('updated_from_drive.csv', encoding='utf-8')

    # Trim leading/trailing whitespaces in 'ko' columns of both dataframes
    df['ko'] = df['ko'].str.strip()
    list_from_drive['ko'] = list_from_drive['ko'].str.strip()

    # Merge the data based on 'ko' column
    merged_df = pd.merge(df, list_from_drive[['ko', 'tw']], on='ko', how='left')

    # Handle missing 'tw' values by replacing them with an empty string
    merged_df['tw'] = merged_df['tw'].fillna('')

    # Identify new words that are missing from updated_from_drive.csv
    merged_df['new_word'] = ~merged_df['ko'].isin(list_from_drive['ko'])
    merged_df['new_word'] = merged_df['new_word'].apply(lambda x: 'new' if x else 'existing')

    # Separate new words to append at the end
    new_words = merged_df[merged_df['new_word'] == 'new']

    # Move the new words to the end of the dataframe
    updated_list = pd.concat([merged_df[merged_df['new_word'] == 'existing'], new_words])

    # Create a new CSV filename with the current date
    current_date = datetime.now().strftime("%Y%m%d")
    new_csv_filename = f'updated_list_{current_date}.csv'

    # Save the updated list to a new CSV file
    updated_list.to_csv(new_csv_filename, index=False, encoding='utf-8')

    print(f"Updated list saved to {new_csv_filename}")

except Exception as e:
    print(f"Error processing CSV files: {e}")