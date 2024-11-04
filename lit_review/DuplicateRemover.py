import pandas as pd
import numpy as np
import os
import logging

'''

Removes duplicate titles from the literature search results

'''
class Parser:
    def __init__(self, PathToFolder):
        self.DirPath = PathToFolder

        # Create a logger with a specified name
        self.logger = logging.getLogger('logger')
        
        # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
        self.logger.setLevel(logging.DEBUG)
        
        # Create a console handler and set its logging level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # Create a formatter to format log messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Attach the formatter to the console handler
        console_handler.setFormatter(formatter)
        
        # Add the console handler to the logger
        self.logger.addHandler(console_handler)
        
        # Log a message indicating initialization
        self.logger.info(f"{10*'+'}Parser has been initialized!{10*'+'}")

    def LoadData(self):

        # Get a list of all CSV files in the specified directory
        csv_files = [f for f in os.listdir(self.DirPath) if f.endswith('.xlsx')]

        self.logger.info(f"Files to be loaded: {csv_files}")

        # Load and concatenate all CSV files into a single DataFrame
        self.RawData = pd.concat(
            [pd.read_excel(os.path.join(self.DirPath, file)) for file in csv_files],
            ignore_index=True
        )

        self.logger.info(f"Data is loaded!")

    def FilterTitle(self,save_data=False):

        # Remove duplicates based on the 'Title' column, keeping the first occurrence
        self.FilteredData = self.RawData.drop_duplicates(subset='Title', keep='first')

        self.logger.info(f"{int(len(self.RawData.Title)) - int(len(self.FilteredData.Title))} Titles were removed from the dataset.")

        if save_data:
            self.SaveToCSV(self.FilteredData)
        
        return self.FilteredData

    def CheckResuts(self, data):
        num_nan = data['Year'].isna().sum()
        num_numeric = data['Year'].notna().sum()

        self.logger.info(f"Number of NaN entries: {num_nan}")
        self.logger.info(f"Number of numeric entries: {num_numeric}")
        
        return 1

    
    def SaveToCSV(self, dataset, path=None, filename='Output.csv'):

        if path is None:
            path = self.DirPath
        if not os.path.exists(path):
            os.makedirs(path)

        flag = self.CheckResuts(dataset)
        
        if flag:
            dataset.to_csv(os.path.join(path, filename), index=False)
        
        self.logger.info(f"Dataset was saved to {os.path.join(path, filename)}")
