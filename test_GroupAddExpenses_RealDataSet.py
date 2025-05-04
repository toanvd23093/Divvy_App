from User import User
from Group import Group
import pandas as pd
from DivvyNumericTester import DivvyNumericTester
import pytest # type: ignore

# To run code coverage:
# coverage run -m pytest test_GroupAddExpenseWithSimplifyDebt.py test_GroupAddExpenseNoSimplifyDebt.py test_GroupConstructor.py test_GroupAddRemoveUsers.py test_User.py test_GroupAddExpenses_RealDataSet.py 
# coverage report -m
# coverage html

testdata = ['TestCases_SmallDataSet_v1.xlsx',
            'TestCases_LargeDataSet.xlsx',
            'TestCases_LargeDataSet_v2.xlsx']

@pytest.mark.parametrize('fileName',testdata)
def test_GroupAddExpenses_RealDataSet_NoSimplifyDebt(fileName):
    divvyNumericTester = DivvyNumericTester(fileName)
    divvyNumericTester.createUserListFromDataFile()
    
    SimpliFyDebt = False
    actExpenseResult = divvyNumericTester.runExpensesCalculation(SimpliFyDebt)
    expExpenseResult = divvyNumericTester.createBaseLine()

    assert expExpenseResult.equals(actExpenseResult) == True
