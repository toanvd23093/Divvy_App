from src.Group import Group
from src.User import User
import pytest

# coverage run -m pytest
# coverage report -m
# coverage html

# --- Setup Helper ---
def setup_users_and_group():
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    bich = User("beryl.tran@ey.com", "123456", "Bich", "Tran")
    eugene = User("eugene.vodai@harvard.com", "123456", "Eugene", "Vo-Dai")
    pho = User("phonuoc123@gmail.com", "123456", "Pho", "Pham")

    return toan, bich, eugene, pho

# --- Test Points ---
def test_calculateExpenses1(): #1
    # Create users and group
    toan, bich, eugene, pho = setup_users_and_group()
    bibibi = Group("23GrampianWay", [toan,bich,eugene], False)

    # Add expenses
    bibibi.addExpenseSinglePayer([toan, bich, eugene],120,toan,"planeTicket")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:40,eugene:40}

    bibibi.addExpenseSinglePayer([bich, toan, eugene],60,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:20,eugene:20}

    bibibi.addExpenseSinglePayer([toan, eugene, bich],15,eugene,"drink")
    assert bibibi.MembersDB[eugene] == {toan:5,eugene:0,bich:5}

    bibibi.addExpenseSinglePayer([bich, eugene, toan],90,toan,"hotel")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:70,eugene:70}

    bibibi.addExpenseSinglePayer([bich, eugene],20,toan,"water")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:80,eugene:80}

    bibibi.addExpenseSinglePayer([bich, toan, eugene],27,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:29,eugene:29}

    bibibi.addExpenseSinglePayer([bich, toan],16,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:37,eugene:29}

    bibibi.addExpenseSinglePayer([eugene, toan],14,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:44,eugene:36}

    bibibi.splitExpensesCalculation()

    assert bibibi.ResultsDB == {toan   : {toan:0,bich:36.0,eugene:75.0},
                                bich   : {toan:0,bich:0,eugene:31.0},
                                eugene : {toan:0,bich:0,eugene:0},
                                }
    
    bibibi.SimplifyDebt = True
    assert bibibi.ResultsDB == {toan   : {bich:5.0,eugene:106.0,toan:0},
                                bich   : {toan:0,bich:0,eugene:0},
                                eugene : {toan:0,bich:0,eugene:0}
                                }

    bibibi.SimplifyDebt = False
    assert bibibi.ResultsDB == {toan   : {toan:0,bich:36.0,eugene:75.0},
                                bich   : {toan:0,bich:0,eugene:31.0},
                                eugene : {toan:0,bich:0,eugene:0},
                                }
    
def test_calculateExpenses2(): #2
    # Create users and group
    toan, bich, eugene, pho = setup_users_and_group()
    bibibi = Group("23GrampianWay", [toan, bich,eugene], False)

    # Add expenses
    bibibi.addExpenseSinglePayer([toan,bich,eugene],90,toan,"planeTicket")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:30,eugene:30}

    bibibi.addExpenseSinglePayer([bich,toan,eugene],90,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:30,eugene:30}

    bibibi.addExpenseSinglePayer([toan,eugene,bich],120,eugene,"drink")
    assert bibibi.MembersDB[eugene] == {toan:40,eugene:0,bich:40}

    bibibi.addExpenseSinglePayer([bich,eugene,toan],30,toan,"hotel")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:40,eugene:40}

    bibibi.addExpenseSinglePayer([bich,toan,eugene],60,toan,"water")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:60,eugene:60}

    bibibi.addExpenseSinglePayer([bich,toan,eugene],210,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:100,eugene:100}

    bibibi.addExpenseSinglePayer([eugene,bich,toan],180,eugene,"dinner")
    assert bibibi.MembersDB[eugene] == {eugene:0,toan:100,bich:100}

    bibibi.addExpenseSinglePayer([eugene,toan,bich],240,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:180,eugene:180}

    bibibi.addExpenseSinglePayer([eugene,bich,toan],270,eugene,"dinner")
    assert bibibi.MembersDB[eugene] == {eugene:0,toan:190,bich:190}

    bibibi.addExpenseSinglePayer([toan,eugene,bich],360,toan,"dinner")
    assert bibibi.MembersDB[toan] == {eugene:180,toan:0,bich:180}

    bibibi.splitExpensesCalculation()
    
    assert bibibi.ResultsDB == {eugene: {toan:10.0, bich:10.0, eugene:0},
                                toan: {toan:0,bich:0,eugene:0},
                                bich: {toan:0,bich:0,eugene:0}
                                }
    
    bibibi.SimplifyDebt = True
    assert bibibi.ResultsDB == {eugene: {toan:10.0, bich:10.0, eugene:0},
                                toan: {toan:0,bich:0,eugene:0},
                                bich: {toan:0,bich:0,eugene:0}
                                }
    
def test_calculateExpenses3(): #3
    # Create users and group
    toan, bich, eugene, pho = setup_users_and_group()
    bibibi = Group("23GrampianWay", [toan,bich,eugene,pho], False)

    # Add expenses
    bibibi.addExpenseSinglePayer([toan,bich,eugene,pho],16,toan,"planeTicket")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:4,eugene:4,pho:4}

    bibibi.addExpenseSinglePayer([pho,bich,toan,eugene],20,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:5,eugene:5,pho:5}

    bibibi.addExpenseSinglePayer([toan,pho,eugene,bich],24,eugene,"drink")
    assert bibibi.MembersDB[eugene] == {toan:6,eugene:0,bich:6,pho:6}

    bibibi.addExpenseSinglePayer([bich,eugene,pho,toan],28,pho,"hotel")   
    assert bibibi.MembersDB[pho] == {toan:7,bich:7,eugene:7,pho:0}

    bibibi.addExpenseSinglePayer([bich,toan,pho,eugene],32,toan,"water")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:12,eugene:12,pho:12}

    bibibi.splitExpensesCalculation()
    
    assert bibibi.ResultsDB == {toan: {toan:0,bich:7.0,eugene:6.0,pho:5.0},
                                eugene: {toan:0,pho:0,eugene:0,bich:1.0},
                                pho: {bich:2, eugene:1,toan:0,pho:0},
                                bich:{toan:0,bich:0,eugene:0,pho:0}
                               }
    
    bibibi.SimplifyDebt = True
    assert bibibi.ResultsDB == {toan: {bich:10.0,eugene:6.0,pho:2.0,toan:0},
                                bich: {toan:0,bich:0,eugene:0,pho:0},
                                eugene: {toan:0,bich:0,eugene:0,pho:0},
                                pho: {toan:0,bich:0,eugene:0,pho:0}
                               }
    
    bibibi.SimplifyDebt = False
    assert bibibi.ResultsDB == {toan: {toan:0,bich:7.0,eugene:6.0,pho:5.0},
                                eugene: {toan:0,pho:0,eugene:0,bich:1.0},
                                pho: {bich:2, eugene:1,toan:0,pho:0},
                                bich:{toan:0,bich:0,eugene:0,pho:0}
                               }
    
def test_calculateExpenses4(): #4
    # Create users and group
    toan, bich, eugene, pho = setup_users_and_group()
    bibibi = Group("23GrampianWay", [toan,bich,eugene,pho], False)

    # Add expenses
    bibibi.addExpenseSinglePayer([pho,bich,toan,eugene],20,bich,"dinner")
    bibibi.addExpenseSinglePayer([bich,eugene,pho,toan],28,pho,"hotel")   
    bibibi.addExpenseSinglePayer([toan,bich,eugene,pho],16,toan,"planeTicket")   
    bibibi.addExpenseSinglePayer([toan,pho,eugene,bich],24,eugene,"drink")
    bibibi.addExpenseSinglePayer([bich,toan,pho,eugene],32,toan,"water")   

    bibibi.splitExpensesCalculation()
    
    assert bibibi.ResultsDB == {toan: {toan:0,bich:7.0,eugene:6.0,pho:5.0},
                                eugene: {toan:0,eugene:0,pho:0,bich:1.0},
                                pho: {bich:2,eugene:1,toan:0,pho:0},
                                bich: {toan:0,bich:0,eugene:0,pho:0}
                               }
    
    bibibi.SimplifyDebt = True

    assert bibibi.ResultsDB == {toan: {bich:10.0,eugene:6.0,pho:2.0,toan:0},
                                bich: {toan:0,bich:0,eugene:0,pho:0},
                                eugene: {toan:0,bich:0,eugene:0,pho:0},
                                pho: {toan:0,bich:0,eugene:0,pho:0}
                               }
    
    bibibi.SimplifyDebt = False

    assert bibibi.ResultsDB == {toan: {toan:0,bich:7.0,eugene:6.0,pho:5.0},
                                eugene: {toan:0,eugene:0,pho:0,bich:1.0},
                                pho: {bich:2,eugene:1,toan:0,pho:0},
                                bich: {toan:0,bich:0,eugene:0,pho:0}
                               }
    
def test_calculateExpenses5(): #5
    # Create users and group
    toan, bich, eugene, pho = setup_users_and_group()
    bibibi = Group("23GrampianWay", [toan,bich,eugene], False)

    # Add expenses
    bibibi.addExpenseSinglePayer([bich,toan,eugene],90,toan,"dinner")
    bibibi.addExpenseSinglePayer([bich,eugene,toan],90,bich,"hotel")   
    bibibi.addExpenseSinglePayer([toan,bich,eugene],120,eugene,"planeTicket")   
    bibibi.addExpenseSinglePayer([toan,eugene,bich],30,toan,"drink")
    bibibi.addExpenseSinglePayer([bich,toan,eugene],60,toan,"water")   

    bibibi.splitExpensesCalculation()

    assert bibibi.ResultsDB == {toan: {bich:30.0,eugene:20.0,toan:0},
                                eugene: {bich:10.0,toan:0,eugene:0},
                                bich: {toan:0,bich:0,eugene:0}
                               }
    
    bibibi.SimplifyDebt = True
    assert bibibi.ResultsDB == {toan: {bich:40.0,eugene:10.0,toan:0},
                                bich: {toan:0,bich:0,eugene:0},
                                eugene: {toan:0,bich:0,eugene:0}
                               }
    
    bibibi.SimplifyDebt = False
    assert bibibi.ResultsDB == {toan: {bich:30.0,eugene:20.0,toan:0},
                                eugene: {bich:10.0,toan:0,eugene:0},
                                bich: {toan:0,bich:0,eugene:0}
                               }
    
    # Add Pho to group
    bibibi.addMemberToGroup(pho)

    assert bibibi.MembersDB == {toan: {bich:60.0,eugene:60.0,toan:0},
                                eugene: {bich:40.0,toan:40.0,eugene:0},
                                bich: {toan:30.0,bich:0,eugene:30.0},
                                pho:{}
                               }
    
    # Add expenses
    bibibi.addExpenseSinglePayer([bich,toan,eugene,pho],240,bich,"dinner")
    bibibi.addExpenseSinglePayer([pho,bich,eugene,toan],200,pho,"hotel")   
    bibibi.addExpenseSinglePayer([toan,pho,bich,eugene],320,eugene,"planeTicket")   
    bibibi.addExpenseSinglePayer([toan,eugene,pho,bich],280,pho,"drink")
    bibibi.addExpenseSinglePayer([bich,toan,eugene,pho],360,toan,"water") 

    assert bibibi.MembersDB == {toan: {bich:150.0,eugene:150.0,toan:0,pho:90.0},
                                eugene: {bich:120.0,toan:120.0,eugene:0,pho:80.0},
                                bich: {toan:90.0,bich:0,eugene:90.0,pho:60},
                                pho:{toan:120.0,bich:120.0,eugene:120.0,pho:0}
                               }
    
    bibibi.splitExpensesCalculation()

    assert bibibi.ResultsDB == {toan: {bich:60.0,eugene:30.0,toan:0,pho:0},
                                eugene: {bich:30.0,toan:0,pho:0,eugene:0},
                                pho: {toan:30.0,bich:60.0,eugene:40.0,pho:0},
                                bich: {toan:0,bich:0,pho:0,eugene:0}
                               }
    
    bibibi.SimplifyDebt = True

    assert bibibi.ResultsDB == {toan: {bich:60.0,pho:0,toan:0,eugene:0},
                                pho: {bich:90.0,eugene:40.0,toan:0,pho:0},
                                bich: {toan:0,bich:0,eugene:0,pho:0},
                                eugene: {toan:0,bich:0,eugene:0,pho:0}
                               }
    
    bibibi.SimplifyDebt = False

    assert bibibi.ResultsDB == {toan: {bich:60.0,eugene:30.0,toan:0,pho:0},
                                eugene: {bich:30.0,toan:0,pho:0,eugene:0},
                                pho: {toan:30.0,bich:60.0,eugene:40.0,pho:0},
                                bich: {toan:0,bich:0,pho:0,eugene:0}
                               }
    

def test_calculateExpenses6(): #6
    # Create users and group
    toan, bich, eugene, pho = setup_users_and_group()
    bibibi = Group("23GrampianWay", [toan,bich,eugene,pho], False)

    # Add expenses
    bibibi.addExpenseSinglePayer([bich,toan,eugene],90,toan,"dinner")
    bibibi.addExpenseSinglePayer([bich,eugene,toan],90,bich,"hotel")   
    bibibi.addExpenseSinglePayer([toan,bich,eugene],120,eugene,"planeTicket")   
    bibibi.addExpenseSinglePayer([toan,eugene,bich],30,toan,"drink")
    bibibi.addExpenseSinglePayer([bich,toan,eugene],60,toan,"water")   

    bibibi.splitExpensesCalculation()

    assert bibibi.ResultsDB == {toan: {bich:30.0,eugene:20.0,toan:0,pho:0},
                                eugene: {bich:10.0,toan:0,eugene:0,pho:0},
                                bich: {toan:0,bich:0,eugene:0,pho:0},
                                pho: {toan:0,pho:0,eugene:0,bich:0}
                               }
    
    bibibi.SimplifyDebt = True

    assert bibibi.ResultsDB == {toan: {bich:40.0,eugene:10.0,toan:0,pho:0},
                                bich: {toan:0,bich:0,eugene:0,pho:0},
                                eugene: {toan:0,bich:0,eugene:0,pho:0},
                                pho: {toan:0,bich:0,pho:0,eugene:0}
                               }
    
    # Add expenses
    bibibi.addExpenseSinglePayer([bich,toan,eugene,pho],240,bich,"dinner")
    bibibi.addExpenseSinglePayer([pho,bich,eugene,toan],200,pho,"hotel")   
    bibibi.addExpenseSinglePayer([toan,pho,bich,eugene],320,eugene,"planeTicket")   
    bibibi.addExpenseSinglePayer([toan,eugene,pho,bich],280,pho,"drink")
    bibibi.addExpenseSinglePayer([bich,toan,eugene,pho],360,toan,"water") 

    assert bibibi.MembersDB == {toan: {bich:150.0,eugene:150.0,toan:0,pho:90.0},
                                eugene: {bich:120.0,toan:120.0,eugene:0,pho:80.0},
                                bich: {toan:90.0,bich:0,eugene:90.0,pho:60},
                                pho:{toan:120.0,bich:120.0,eugene:120.0,pho:0}
                               }
    
    bibibi.splitExpensesCalculation()
    
    assert bibibi.ResultsDB == {toan: {bich:60.0,pho:0,toan:0,eugene:0},
                                pho: {bich:90.0,eugene:40.0,toan:0,pho:0},
                                bich: {toan:0,bich:0,eugene:0,pho:0},
                                eugene: {toan:0,bich:0,eugene:0,pho:0}
                               }
    
    bibibi.SimplifyDebt = False

    assert bibibi.ResultsDB == {toan: {bich:60.0,eugene:30.0,toan:0,pho:0},
                                eugene: {bich:30.0,toan:0,pho:0,eugene:0},
                                pho: {toan:30.0,bich:60.0,eugene:40.0,pho:0},
                                bich: {toan:0,bich:0,pho:0,eugene:0}
                               }  