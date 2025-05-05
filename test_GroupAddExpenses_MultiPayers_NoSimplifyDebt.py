from Group import Group
from User import User

import pytest

# --- Setup Helper ---
def setup_users_and_group():
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    bich = User("beryl.tran@ey.com", "123456", "Bich", "Tran")
    eugene = User("eugene.vodai@harvard.com", "123456", "Eugene", "Vo-Dai")
    pho = User("phonuoc123@gmail.com", "123456", "Pho", "Pham")

    bibibi = Group("23GrampianWay", [toan, bich, eugene, pho], False)

    return toan, bich, eugene, pho, bibibi

# --- Test Points ---
def test_AddExpenses_InvalidPayerList(): #1

    toan, bich, eugene, pho, bibibi = setup_users_and_group()

    # Add expenses
    TotalExpense = 120
    WhoPaid = toan
    MemberInvolvedInTheTransaction = {toan:12, bich:28, pho:65, eugene:15}

    with pytest.raises(ValueError,match="List of Payers is not valid. Should be a Dict with format {Lender:AmountPaid}"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    WhoPaid = {toan:100,bich:20}
    MemberInvolvedInTheTransaction = [toan,bich,eugene,pho] 

    with pytest.raises(ValueError,match="List of Borrowers is not valid. Should be a Dict with format {Borrower:AmountBorrowed}"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

def test_AddExpenses_UnrecognizedPayer(): #2

    toan, bich, eugene, pho, bibibi = setup_users_and_group()
    bibibi2 = Group("23GrampianWay", [toan,bich,eugene,pho], False)

    # Add expenses
    TotalExpense = 120
    WhoPaid = {bibibi2:100,toan:20}
    MemberInvolvedInTheTransaction = {toan:12, bich:28, pho:65, eugene:15}

    with pytest.raises(ValueError,match="User not recognized"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    WhoPaid = {bich:100,toan:20}
    MemberInvolvedInTheTransaction = {bibibi2:12, bich:28, pho:65, eugene:15}

    with pytest.raises(ValueError,match="User not recognized"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

def test_AddExpenses_MultiPayer_InvalidTotalExpense(): #3

    toan, bich, eugene, pho, bibibi = setup_users_and_group()
    
    # Add expenses
    TotalExpense = "120"
    WhoPaid = {bich:100,toan:20}
    MemberInvolvedInTheTransaction = {toan:12, bich:28, pho:65, eugene:15}

    with pytest.raises(ValueError,match="Total expense is not valid. Must be an integer or a float number"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    TotalExpense = -120

    with pytest.raises(ValueError,match="Total expense must be positive"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")
   
def test_AddExpenses_MultiPayer_InvalidExpensesInput(): #4

    toan, bich, eugene, pho, bibibi = setup_users_and_group()
    
    # Add expenses
    TotalExpense = 120
    WhoPaid = {bich:10,toan:20}
    MemberInvolvedInTheTransaction = {toan:12, bich:28, pho:65, eugene:15}

    with pytest.raises(ValueError,match=r"The payment values do not add up to the total cost of \$120\.00\. You are short by \$90\.00"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")
    

    WhoPaid = {bich:100,toan:30}

    with pytest.raises(ValueError,match=r"The payment values do not add up to the total cost of \$120\.00\. You are over by \$10\.00"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    
    WhoPaid = {bich:100,toan:20}
    MemberInvolvedInTheTransaction = {toan:10, bich:10, pho:10, eugene:10}

    with pytest.raises(ValueError,match=r"The borrowed values do not add up to the total cost of \$120\.00\. You are short by \$80\.00"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    
    MemberInvolvedInTheTransaction = {toan:10, bich:10, pho:10, eugene:120}
    
    with pytest.raises(ValueError,match=r"The borrowed values do not add up to the total cost of \$120\.00\. You are over by \$30\.00"):
        bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")


def test_AddExpenses_MultiPayer_Case1(): #5

    toan, bich, eugene, pho, bibibi = setup_users_and_group()

    # Add expenses
    TotalExpense = 120
    WhoPaid = {toan:80, bich:40}
    MemberInvolvedInTheTransaction = {toan:12, bich:28, pho:65, eugene:15}
    bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    Exp_Members_DB = {toan:{toan:0.0,bich:0.0,pho:65,eugene:3},
                      bich:{toan:0.0,bich:0.0,pho:0,eugene:12},
                      pho:{},
                      eugene:{}}
    
    assert Exp_Members_DB == bibibi.MembersDB

    bibibi.splitExpensesCalculation()

    Exp_Results_DB = {toan  : {toan:0.0,bich:0.0,pho:65,eugene:3},
                      bich  : {toan:0.0,bich:0.0,pho:0,eugene:12},
                      pho   : {toan:0.0,bich:0.0,pho:0,eugene:0},
                      eugene: {toan:0.0,bich:0.0,pho:0,eugene:0}}
    
    assert Exp_Results_DB == bibibi.ResultsDB


def test_AddExpenses_MultiPayer_Case2(): #6

    toan, bich, eugene, pho, bibibi = setup_users_and_group()

    TotalExpense = 120

    # Add expenses #2 
    WhoPaid = {toan:16, bich:24, eugene: 15, pho: 65}
    MemberInvolvedInTheTransaction = {toan:9, bich:28, pho:51, eugene:32}
    bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    Exp_Members_DB = {toan  : {toan:0,bich:4,pho:0,eugene:3},
                      bich  : {toan:0,bich:0,pho:0,eugene:0},
                      pho   : {toan:0,bich:0,pho:0,eugene:14},
                      eugene: {toan:0,bich:0,pho:0,eugene:0}}
    
    assert Exp_Members_DB == bibibi.MembersDB

    bibibi.splitExpensesCalculation()

    Exp_Results_DB = {toan  : {toan:0,bich:4,pho:0,eugene:3},
                      bich  : {toan:0,bich:0,pho:0,eugene:0},
                      pho   : {toan:0,bich:0,pho:0,eugene:14},
                      eugene: {toan:0,bich:0,pho:0,eugene:0}}
    
    assert Exp_Results_DB == bibibi.ResultsDB


def test_AddExpenses_MultiPayer_Case3(): #3

    toan, bich, eugene, pho, bibibi = setup_users_and_group()

    TotalExpense = 120

    # Add expenses #1
    WhoPaid = {toan:80, bich:40}
    MemberInvolvedInTheTransaction = {toan:12, bich:28, pho:65, eugene:15}
    bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    bibibi.splitExpensesCalculation()

    Exp_Results_DB = {toan  : {toan:0.0,bich:0.0,pho:65,eugene:3},
                      bich  : {toan:0.0,bich:0.0,pho:0,eugene:12},
                      pho   : {toan:0.0,bich:0.0,pho:0,eugene:0},
                      eugene: {toan:0.0,bich:0.0,pho:0,eugene:0}}
    
    assert Exp_Results_DB == bibibi.ResultsDB

    # Add expenses #2 
    WhoPaid = {toan:16, bich:24, eugene: 15, pho: 65}
    MemberInvolvedInTheTransaction = {toan:9, bich:28, pho:51, eugene:32}
    bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    bibibi.splitExpensesCalculation()

    Exp_Results_DB = {toan  : {toan:0,bich:4,pho:65.0,eugene:6},
                      bich  : {toan:0,bich:0,pho:0,eugene:12.0},
                      pho   : {toan:0,bich:0,pho:0,eugene:14},
                      eugene: {toan:0,bich:0,pho:0,eugene:0}}
    
    assert Exp_Results_DB == bibibi.ResultsDB

    bibibi.SimplifyDebt = True

    Exp_Results_DB = {toan  : {toan:0,bich:0,pho:51.0,eugene:24},
                      bich  : {toan:0,bich:0,pho:0,eugene:8.0},
                      pho   : {toan:0,bich:0,pho:0,eugene:0},
                      eugene: {toan:0,bich:0,pho:0,eugene:0}}
    
    assert Exp_Results_DB == bibibi.ResultsDB

    # Add expenses #3
    TotalExpense = 300
    WhoPaid = {toan:115, bich:75, eugene:30, pho:80}
    MemberInvolvedInTheTransaction = {toan:75, bich:75, pho:75, eugene:75}
    bibibi.addExpenseMultiplePayers(TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,"dinner")

    bibibi.splitExpensesCalculation()

    Exp_Results_DB = {toan  : {toan:0,bich:0,pho:46,eugene:69},
                      bich  : {toan:0,bich:0,pho:0,eugene:8},
                      pho   : {toan:0,bich:0,pho:0,eugene:0},
                      eugene: {toan:0,bich:0,pho:0,eugene:0}}
    
    assert Exp_Results_DB == bibibi.ResultsDB

    bibibi.SimplifyDebt = False

    Exp_Results_DB = {toan  : {toan:0,bich:4,pho:65,eugene:46},
                      bich  : {toan:0,bich:0,pho:0,eugene:12},
                      pho   : {toan:0,bich:0,pho:0,eugene:19},
                      eugene: {toan:0,bich:0,pho:0,eugene:0}}
    
    assert Exp_Results_DB == bibibi.ResultsDB

