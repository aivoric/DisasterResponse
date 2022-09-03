import pandas as pd
from sqlalchemy import create_engine

class ETLPipeline():
    """
    Class for getting the disaster response data, cleaning it up and preparing
    it for the machine learning step.
    """
    def __init__(self, message_location: str, category_location: str, 
            database: str, output_table: str) -> None:
        self.message_location = message_location
        self.category_location = category_location
        self.database = database
        self.output_table = output_table

    def load_data(self) -> None:
        try:
            self.messages = pd.read_csv(self.message_location)
            self.categories = pd.read_csv(self.category_location)
        except:
            raise Exception("Could not read messages or categories.")

    def clean_data(self) -> None:
        # Create a single df with messages and categories
        merged_df = self.messages.merge(self.categories, how="left")
        # Split the categories column into a new df with many columns
        categories_df = merged_df.categories.str.split(pat=";", expand=True)
        # Use the first row of the categories_df to create column headers
        categories_df.columns = categories_df.iloc[0].apply(lambda row: row[:-2])
        # In each cell of the categories_df only leave the number, e.g. aid_related-1 -> 1
        categories_df = categories_df.applymap(lambda cell: int(cell[-1:]))
        # In the merged df drop the old categories column
        merged_df.drop(columns=['categories'], inplace=True)
        # Create a new final df with the new categories and the old message data
        self.df = pd.concat([merged_df, categories_df], axis=1)
        # Remove any duplicates
        self.df.drop_duplicates(inplace=True)

    def save_data(self) -> None:
        try: 
            engine = create_engine(self.database)
            self.df.to_sql(self.output_table, engine, index=False, if_exists='replace')
        except:
            raise Exception("Could not save df to database.")

def main():
    """
    Create an ETLPipeline object and run the methods for the ETL flow:
    1) load_data()
    2) clean_data()
    3) save_data()

    The final result is a SQLlite database prepared for the ML step.
    """
    message_location = "data/messages.csv"
    category_location = "data/categories.csv"
    database = "sqlite:///data/DisasterResponse.db"
    output_table = "disaster_messages"
    etl_pipeline = ETLPipeline(message_location, category_location, database, output_table)
    etl_pipeline.load_data()
    etl_pipeline.clean_data()
    etl_pipeline.save_data()

if __name__ == '__main__':
    main()