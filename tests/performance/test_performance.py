import pytest
from src.Group import Group
from src.User import User

# Benchmark performance of the app
# Copyright 2025

# coverage run -m pytest
# coverage report -m
# python -m pytest -m splitExpense_ThreePerson -v -s
# python -m pytest --trace-config   

def setup_users_and_group():
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    bich = User("beryl.tran@ey.com", "123456", "Bich", "Tran")
    eugene = User("eugene.vodai@harvard.com", "123456", "Eugene", "Vo-Dai")
    pho = User("phonuoc123@gmail.com", "123456", "Pho", "Pham")

    return toan, bich, eugene, pho

@pytest.mark.splitExpense_ThreePerson  
def test_calculateExpenses1(benchmark):  
    # Create users and group
    toan, bich, eugene, pho = setup_users_and_group()
    bibibi = Group("23GrampianWay", [toan, bich,eugene], False)

    # Add expenses
    bibibi.addExpenseSinglePayer([toan, bich,eugene],120,toan,"planeTicket")   
    bibibi.addExpenseSinglePayer([bich, toan, eugene],60,bich,"dinner")
    bibibi.addExpenseSinglePayer([toan,eugene, bich],15,eugene,"drink")
    bibibi.addExpenseSinglePayer([bich,eugene,toan],90,toan,"hotel")   
    bibibi.addExpenseSinglePayer([bich,eugene],20,toan,"water")   
    bibibi.addExpenseSinglePayer([bich, toan, eugene],27,bich,"dinner")
    bibibi.addExpenseSinglePayer([bich, toan],16,bich,"dinner")
    bibibi.addExpenseSinglePayer([eugene, toan],14,bich,"dinner")

    # Benchmark the expense calculation
    benchmark(bibibi.splitExpensesCalculation)

    # Validate the result
    assert bibibi.ResultsDB == {
        toan  :{toan:0,bich:36.0,eugene:75.0},
        bich  :{toan:0,bich:0,eugene:31.0},
        eugene  :{toan:0,bich:0,eugene:0},
    }