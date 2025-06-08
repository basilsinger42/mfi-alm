from mfi_alm.liabilities.liability import Liability
from mfi_alm.liabilities.mortality import MortalityTable

"""
TODO:

Create a class called AnnuityDue. It should inherit attributes the general Liability class.
It reads in a MortalityTable object and an interest rate i.
Example:
    annuity_due = AnnuityDue(mortality_table=mortality_table, i=i)
    apv = annuity_due.apv(n=n, x=x)
"""

class AnnuityDue(Liability):
    def __init__(self, mortality_table: MortalityTable, i: float):
        pass
