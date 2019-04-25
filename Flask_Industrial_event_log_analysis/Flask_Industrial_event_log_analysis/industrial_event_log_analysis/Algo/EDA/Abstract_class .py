from abc import ABC, abstractmethod
class Run_EDA(ABC):



    @abstractmethod
    def sample(self,df:DataFrame)-> DataFrame:
        """
        input values_dataframes
        always return data frame

        """
        pass

    @abstractmethod
    def train(self,df:DataFrame)-> pkl:
        """
        input dataframe
        always return pickle
        """
        pass

    @abstractmethod
    def score(self,modal_df:pkl,intial_df:DataFrame) -> DataFrame::
        """
        input pickle

        always return data frame
        """
        pass

    @abstractmethod
    def visualize(df:DataFrame) -> dict:
        """

        input dataframe and always return dictionary
        eg. dict(type="heatmap",z=ht,x=df.columns, y=df.columns)
        """
        pass
