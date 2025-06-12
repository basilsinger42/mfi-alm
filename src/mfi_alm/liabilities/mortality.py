import pandas as pd
"""
TODO:

Create a class called MortalityTable.
It reads in a dataframe that has the columns x and lx.
Example:
    mortality_table = MortalityTable(df_mortality=df_mortality)
    tpx = mortality_table.tpx(t=5, x=10)
    tqx = mortality_table.tqx(t=5, x=10)
"""
class MortalityTable:
        def __init__(self, df_mortality: pd.DataFrame):
            if not {'x', 'lx'}.issubset(df_mortality.columns):
                raise ValueError("Mortality table must contain 'x' and 'lx' columns.")

            self.df = df_mortality.set_index('x').copy()
            self.df['qx'] = 1 - self.df['lx'].shift(-1) / self.df['lx']
            self.df['qx'] = self.df['qx'].fillna(1.0)

        def tpx(self, t: int, x: int) -> float:
            """
            _tp_x = l_{x+t} / l_x
            """
            if x not in self.df.index or x + t not in self.df.index:
                raise ValueError("Age or age+t out of range.")
            return self.df.loc[x + t, 'lx'] / self.df.loc[x, 'lx']

        def tqx(self, t: int, x: int) -> float:
            """
            _tq_x = 1 - _tp_x
            """
            return 1 - self.tpx(t, x)