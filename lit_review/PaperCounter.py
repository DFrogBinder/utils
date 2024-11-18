import pandas as pd
import matplotlib.pyplot as plt

class PaperPlotter:
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initializes the analyzer with the provided dataframe.

        :param dataframe: A pandas DataFrame containing paper data, with a 'Year' column.
        """
        self.dataframe = dataframe
        self.papers_per_year = None

    def process_data(self):
        """
        Groups the dataframe by the 'Year' column and counts the number of papers per year.
        Stores the result in the 'papers_per_year' attribute.
        """
        self.papers_per_year = self.dataframe.groupby('Year').size()

    def plot_histogram(self, output_file: str = None):
        """
        Creates a histogram of the number of papers published per year.

        :param output_file: Optional. If provided, the plot will be saved to the specified file path.
        """
        if self.papers_per_year is None:
            raise ValueError("Data has not been processed. Please call 'process_data' first.")
        
        # Create the histogram
        plt.figure(figsize=(10, 6))
        plt.bar(self.papers_per_year.index, self.papers_per_year.values, color='skyblue', edgecolor='black')

        # Add titles and labels
        plt.title('Number of Papers Published per Year', fontsize=30, fontweight='bold')
        plt.xlabel('Year', fontsize=25)
        plt.ylabel('Number of Papers', fontsize=25)

        # Improve aesthetics
        plt.yticks(fontsize=20)
        plt.xticks(rotation=45,fontsize=20)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save or show the plot
        if output_file:
            plt.savefig(output_file, dpi=500)
        else:
            plt.show()


