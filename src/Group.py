from src.User import User
import re
import pandas as pd

# Object to create Group Expenses
# Copyright 2025

class Group():
    __slots__ = (
        '_GroupName',
        '_InitialGroupMembers',
        '_SimplifyDebt',
        'MembersDB',
        'ResultsDB',
        'ResultsDBNoSimplifyDebt',
        'ResultsDBWithSimplifyDebt',
    )

    def __init__(self,GroupName,InitialGroupMembers,SimplifyDebt=False):
        self.GroupName = GroupName
        self.InitialGroupMembers = InitialGroupMembers
        self.MembersDB = {}       
        self.ResultsDB = {}
        self.ResultsDBNoSimplifyDebt = {}
        self.ResultsDBWithSimplifyDebt = {}
        self.SimplifyDebt = SimplifyDebt

        if len(self.InitialGroupMembers) != 0:
            for i in range (0,len(self.InitialGroupMembers)):
                self.MembersDB.update({self.InitialGroupMembers[i]:{}})

    @property
    def GroupName(self):
        return self._GroupName

    @GroupName.setter
    def GroupName(self,GroupName):
        pattern = r'[a-zA-Z0-9_\.\-]+$'

        if not re.match(pattern,GroupName):
            raise ValueError("Group Name should not contain special characters")
        
        self._GroupName = GroupName

    @property
    def InitialGroupMembers(self):
        return tuple(self._InitialGroupMembers)
    
    @InitialGroupMembers.setter
    def InitialGroupMembers(self,InitialGroupMembers):
        if not isinstance(InitialGroupMembers, list):
            raise ValueError("Please specify a List of Group Members")
        
        if len(InitialGroupMembers) != 0:
            for member in InitialGroupMembers:
                if not isinstance(member, User):
                    raise ValueError("User not recognized")

        self._InitialGroupMembers = InitialGroupMembers

    @property 
    def SimplifyDebt(self):
        return self._SimplifyDebt
    
    @SimplifyDebt.setter
    def SimplifyDebt(self,SimplifyDebt):
        if not isinstance(SimplifyDebt, bool):
            raise ValueError("Simplify Debt option should be logical flag")
        
        self._SimplifyDebt = SimplifyDebt
        
        # Update ResultsDB accordingly based on SimplifyDebt flag
        if self._SimplifyDebt:
            self.ResultsDB = self.ResultsDBWithSimplifyDebt           
        else:
            self.ResultsDB = self.ResultsDBNoSimplifyDebt
    
    def addMemberToGroup(self,member):
        if not isinstance(member, User):
            raise ValueError("User not recognized")
        
        if member in self.InitialGroupMembers:
            raise ValueError("This user was initially added to this group")
        
        if member in self.MembersDB:
            raise ValueError("This user has already been added to this group")

        self.MembersDB.update({member:{}})

    def removeMemberFromGroup(self,member):
        if not isinstance(member, User):
            raise ValueError("User not recognized")
        
        if member not in self.MembersDB:
            raise ValueError("This user is not in this group")
        
        del self.MembersDB[member]

    # In case there is only one single payer
    def addExpenseSinglePayer(self,*args):
        if len(args) == 5: 
            MemberInvolvedInTheTransaction,TotalExpense,WhoPaid,Shares,Description = args
        elif len(args) == 4: 
            MemberInvolvedInTheTransaction,TotalExpense,WhoPaid,Description = args
            Shares = {}
            for borrower in MemberInvolvedInTheTransaction:
                Shares.update({borrower:1})

        if not isinstance(WhoPaid, User):
            raise ValueError("User not recognized")
        
        if not isinstance(TotalExpense, (int,float)):
            raise ValueError("Total expense is not valid. Must be an integer or a float number")
        
        if TotalExpense <= 0:
            raise ValueError("Total expense must be positive")

        borrowerDict = self.MembersDB[WhoPaid]
    
        for borrower in MemberInvolvedInTheTransaction:
            if borrower == WhoPaid:
                if borrower not in borrowerDict:
                    borrowerDict.update({borrower:0})
                else:
                    continue
            else:
                if borrower not in borrowerDict:
                    borrowerDict.update({borrower:Shares[borrower]*TotalExpense/sum(Shares.values())})
                else:
                    borrowerDict[borrower] += Shares[borrower]*TotalExpense/sum(Shares.values())

        self.MembersDB[WhoPaid] = borrowerDict

    # In case there are multiple payers
    def addExpenseMultiplePayers(self,*args):
        
        TotalExpense,WhoPaid,MemberInvolvedInTheTransaction,Description = args
        
        if not isinstance(WhoPaid,dict):
            raise ValueError(r"List of Payers is not valid. Should be a Dict with format {Lender:AmountPaid}")
        
        AmountPaid = []
        for lender in WhoPaid.keys():
            if not isinstance(lender, User):
                raise ValueError("User not recognized")

            AmountPaid.append(WhoPaid[lender])

        if not isinstance(MemberInvolvedInTheTransaction,dict):
            raise ValueError(r"List of Borrowers is not valid. Should be a Dict with format {Borrower:AmountBorrowed}")
        
        AmountBorrowed = []
        for borrower in MemberInvolvedInTheTransaction.keys():
            if not isinstance(borrower, User):
                raise ValueError("User not recognized")

            AmountBorrowed.append(MemberInvolvedInTheTransaction[borrower])

        if not isinstance(TotalExpense, (int,float)):
            raise ValueError("Total expense is not valid. Must be an integer or a float number")
        
        if TotalExpense <= 0:
            raise ValueError("Total expense must be positive")
        
        if sum(AmountPaid) < TotalExpense:
            raise ValueError(f"The payment values do not add up to the total cost of ${TotalExpense:.2f}. You are short by ${TotalExpense-sum(AmountPaid):.2f}")
        
        if sum(AmountPaid) > TotalExpense:
            raise ValueError(f"The payment values do not add up to the total cost of ${TotalExpense:.2f}. You are over by ${sum(AmountPaid)-TotalExpense:.2f}")
        
        if sum(AmountBorrowed) < TotalExpense:
            raise ValueError(f"The borrowed values do not add up to the total cost of ${TotalExpense:.2f}. You are short by ${TotalExpense-sum(AmountBorrowed):.2f}")
        
        if sum(AmountBorrowed) > TotalExpense:
            raise ValueError(f"The borrowed values do not add up to the total cost of ${TotalExpense:.2f}. You are over by ${sum(AmountBorrowed)-TotalExpense:.2f}")
        
        # Preprocess lenders' expenses, if a lender paid and also is involved to an expense, we offset that expense from the total amount the lender paid
        for lender in WhoPaid.keys():
            if lender in MemberInvolvedInTheTransaction:
                if WhoPaid[lender] >= MemberInvolvedInTheTransaction[lender]:
                    WhoPaid[lender] -= MemberInvolvedInTheTransaction[lender]
                    MemberInvolvedInTheTransaction[lender] = 0
                else:
                    MemberInvolvedInTheTransaction[lender] -= WhoPaid[lender] 
                    WhoPaid[lender] = 0

        # Distribute remaining expenses to the borrower
        for lender in WhoPaid.keys():
            borrowerDict = self.MembersDB[lender]
            
            for borrower in MemberInvolvedInTheTransaction.keys():
                if borrower == lender:
                    borrowerDict.update({borrower:0})
                
                if borrower != lender:
                    if MemberInvolvedInTheTransaction[borrower] <= WhoPaid[lender]:
                        if borrower not in borrowerDict:
                            borrowerDict[borrower] = MemberInvolvedInTheTransaction[borrower]
                        else:
                            borrowerDict[borrower] += MemberInvolvedInTheTransaction[borrower]
                                               
                        WhoPaid[lender] -= MemberInvolvedInTheTransaction[borrower]
                        MemberInvolvedInTheTransaction[borrower] = 0
                    else:
                        if borrower not in borrowerDict:
                            borrowerDict[borrower] = WhoPaid[lender]
                        else:
                            borrowerDict[borrower] += WhoPaid[lender]

                        MemberInvolvedInTheTransaction[borrower]-=WhoPaid[lender]
                        WhoPaid[lender] = 0
                            
            self.MembersDB[lender] = borrowerDict


    def splitExpensesCalculation(self):
        allMembers = self.MembersDB.keys()
        
        # Map member into integer index. 
        # For example, Toan is #0, Bich is #1, Eugene is #2, etc.
        i = 0
        mapUserObjectToIntegerDict = {} 
        for member in allMembers:
            mapUserObjectToIntegerDict[member] = i
            i += 1

        # Create a 2D table to store lender/borrower information.
        # Row indicate lenders and column indicate borrowers
        # For example, row 1 in below table, if Toan paid $90 for 
        # an expense and split equally, Bich and Eugene each owes 
        # Toan $30. Toan "owes" himself $30 but it should be written 
        # off as $0 for simplification.
        #          Toan     Bich     Eugene
        # Toan       0        30        30
        # Bich      20         0        20
        # Eugene     5         5         0
        
        lender_borrower_table = []
        
        for _ in range(len(allMembers)):
            lender_borrower_table.append([0]*len(allMembers))

        for lender in allMembers:
            for borrower in allMembers:
                r = mapUserObjectToIntegerDict[lender]
                c = mapUserObjectToIntegerDict[borrower]

                if borrower not in self.MembersDB[lender]:
                    lender_borrower_table[r][c] = 0
                else:
                    lender_borrower_table[r][c] = self.MembersDB[lender][borrower]                   
                        
        
        # Reduce the table above by comparing each pairs of lender-borrower.
        # For example, in row 1, Bich owes Toan $30, but in row 2, Toan owes
        # Bich $20. Thus, it should be reduced to Bich owes Toan #10. Simplified 
        # table from the example above is showned below:
        #          Toan     Bich     Eugene
        # Toan       0        10        25
        # Bich       0         0        15
        # Eugene     0         0         0

        for r in range(0,len(allMembers)):
            for c in range(0,len(allMembers)):
                if r == c:
                    continue
                else:
                    if lender_borrower_table[r][c] > lender_borrower_table[c][r]:
                        lender_borrower_table[r][c]-=lender_borrower_table[c][r]
                        lender_borrower_table[c][r] = 0
                    elif lender_borrower_table[r][c] < lender_borrower_table[c][r]:
                        lender_borrower_table[c][r]-=lender_borrower_table[r][c]
                        lender_borrower_table[r][c] = 0
                    elif lender_borrower_table[r][c] == lender_borrower_table[c][r]:
                        lender_borrower_table[r][c] = 0
                        lender_borrower_table[c][r] = 0

        # Now store the info from the simplified table into a dict{dict}
        # for easy access the result
        # Format: 
        # {
        #   lender1:{borrower #1:amount owed, borrower #2:amount owed, etc.},
        #   lender2:{borrower #1:amount owed, borrower #2:amount owed, etc.}
        # }

        self.ResultsDBNoSimplifyDebt = self.__createResultsDB(mapUserObjectToIntegerDict,lender_borrower_table)

        # Further simplify Debt if flag SimplifyDebt = True
        #          Toan      Bich      Eugene
        # Toan       0         0         35
        # Bich       0         0          5
        # Eugene     0         0          0
        lender_borrower_table_simplifyDebt = lender_borrower_table.copy()

        for r in range(0,len(allMembers)):
            for c in range(0,len(allMembers)):
                if r == c:
                    continue

                if lender_borrower_table_simplifyDebt[r][c] == 0:
                    continue
                    
                for c1 in range(0,len(allMembers)):
                    if c == c1:
                        continue
                        
                    if lender_borrower_table_simplifyDebt[c][c1] == 0:
                        continue
                        
                    if lender_borrower_table_simplifyDebt[r][c] > lender_borrower_table_simplifyDebt[c][c1]:
                        lender_borrower_table_simplifyDebt[r][c]-=lender_borrower_table_simplifyDebt[c][c1]
                        lender_borrower_table_simplifyDebt[r][c1]+=lender_borrower_table_simplifyDebt[c][c1]
                        lender_borrower_table_simplifyDebt[c][c1] = 0
                    elif lender_borrower_table_simplifyDebt[r][c] < lender_borrower_table_simplifyDebt[c][c1]:
                        lender_borrower_table_simplifyDebt[c][c1]-=lender_borrower_table_simplifyDebt[r][c]
                        lender_borrower_table_simplifyDebt[r][c1]+=lender_borrower_table_simplifyDebt[r][c]
                        lender_borrower_table_simplifyDebt[r][c] = 0
                    elif lender_borrower_table_simplifyDebt[r][c] == lender_borrower_table_simplifyDebt[c][c1]:
                        lender_borrower_table_simplifyDebt[r][c1]+=lender_borrower_table_simplifyDebt[c][c1]
                        lender_borrower_table_simplifyDebt[r][c] = 0
                        lender_borrower_table_simplifyDebt[c][c1] = 0

        # Now store the info from the simplified table into a dict{dict}
        # for easy access the result
        # Format: 
        # {
        #   lender1:{borrower #1:amount owed, borrower #2:amount owed, etc.},
        #   lender2:{borrower #1:amount owed, borrower #2:amount owed, etc.}
        # }
        self.ResultsDBWithSimplifyDebt = self.__createResultsDB(mapUserObjectToIntegerDict,lender_borrower_table_simplifyDebt)
        
        # Assign the appropriate results DB
        if self.SimplifyDebt:
            self.ResultsDB = self.ResultsDBWithSimplifyDebt           
        else:
            self.ResultsDB = self.ResultsDBNoSimplifyDebt

    def __createResultsDB(self, mapUserObjectToIntegerDict,costMatrix): # Use __ to indicate this method is private and wont allow external use
        resultsDBTmp = {}
        allMembers = mapUserObjectToIntegerDict.keys()

        for lender in allMembers:
            for borrower in allMembers:
                r = mapUserObjectToIntegerDict[lender]
                c = mapUserObjectToIntegerDict[borrower]

                if lender not in resultsDBTmp:
                    resultsDBTmp.update({lender:{borrower:costMatrix[r][c]}})
                else:
                    resultsDBTmp[lender].update({borrower:costMatrix[r][c]})

        return resultsDBTmp
    
    def printOutResult(self):
        # Print out the final result for who is the lender and who are the borrowers 
        # within the group
        tmpDict = {}
        for lender in self.ResultsDB.keys():
            tmpDict.update({f"{lender.userFirstName} {lender.userLastName}":{}})
            for borrower in self.ResultsDB[lender].keys():
                tmpDict[f"{lender.userFirstName} {lender.userLastName}"].update({f"{borrower.userFirstName} {borrower.userLastName}":f"{self.ResultsDB[lender][borrower]:.2f}"})
 
        return pd.DataFrame(tmpDict).T

def main():
    # Create users
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    bich = User("beryl.tran@ey.com", "123456", "Bich", "Tran")
    eugene = User("eugene.vodai@harvard.com", "123456", "Eugene", "Vo-Dai")
    
    # Create group
    bibibi = Group("23GrampianWay", [toan,bich,eugene], False)

    # Add expenses
    bibibi.addExpenseSinglePayer([toan, bich,eugene],120,toan,"planeTicket")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:40,eugene:40}

    bibibi.addExpenseSinglePayer([bich, toan, eugene],60,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:20,eugene:20}

    bibibi.addExpenseSinglePayer([toan,eugene, bich],15,eugene,"drink")
    assert bibibi.MembersDB[eugene] == {toan:5,eugene:0,bich:5}

    bibibi.addExpenseSinglePayer([bich,eugene,toan],90,toan,"hotel")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:70,eugene:70}

    bibibi.addExpenseSinglePayer([bich,eugene],20,toan,"water")   
    assert bibibi.MembersDB[toan] == {toan:0,bich:80,eugene:80}

    bibibi.addExpenseSinglePayer([bich, toan, eugene],27,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:29,eugene:29}

    bibibi.addExpenseSinglePayer([bich, toan],16,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:37,eugene:29}

    bibibi.addExpenseSinglePayer([eugene, toan],14,bich,"dinner")
    assert bibibi.MembersDB[bich] == {bich:0,toan:44,eugene:36}

    bibibi.splitExpensesCalculation()

    print("---------------------NO SIMPLIFY--------------------------------")
    print(bibibi.ResultsDB)
    
    assert bibibi.ResultsDB == {toan   : {toan:0,bich:36.0,eugene:75.0},
                                bich   : {toan:0,bich:0,eugene:31.0},
                                eugene : {toan:0,bich:0,eugene:0},
                                }
    
    bibibi.SimplifyDebt = True
    print("----------------------WITH SIMPLIFY-------------------------------")
    print(bibibi.ResultsDB)

    assert bibibi.ResultsDB == {toan   : {toan:0,bich:5.0,eugene:106.0},
                                bich   : {toan:0,bich:0,eugene:0.0},
                                eugene : {toan:0,bich:0,eugene:0},
                                }

    bibibi.SimplifyDebt = False
    print("---------------------NO SIMPLIFY--------------------------------")
    print(bibibi.ResultsDB)
    
    assert bibibi.ResultsDB == {toan   : {toan:0,bich:36.0,eugene:75.0},
                                bich   : {toan:0,bich:0,eugene:31.0},
                                eugene : {toan:0,bich:0,eugene:0},
                                }
    

if __name__=="__main__":
    main()

        
        

                               
