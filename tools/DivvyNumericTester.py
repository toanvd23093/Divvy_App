from src.User import User
from src.Group import Group
from tools.LoadDataFileHelper import get_data_file
import pandas as pd
import re

# Tester for Numeric Test
class DivvyNumericTester():
    def __init__(self,fileName):

        data_file = get_data_file(fileName)

        self.userList = []
        self.rawData = pd.read_excel(data_file, sheet_name="Data")
        self.expectedOutput = pd.read_excel(data_file, sheet_name="ExpResult")
        self.keyUserMapping = {}

    def createUserListFromDataFile(self):
        transaction_dict = self.rawData.iloc[0].to_dict()
        keyPattern = r'^([a-zA-Z]+)(\s+([a-zA-Z]+))?$'

        for key in transaction_dict.keys():
            if key not in ['Date', 'Description', 'Cost', 'Total', 'Index', 'Category','Currency']:

                match = re.match(keyPattern, key)

                if match:
                    firstName = match.group(1)
                    if match.group(3):
                        lastName = match.group(3)
                    else:
                        lastName = f"x"
                    
                    tmpUser = User(f"{firstName}{lastName}@gmail.com", "123456", firstName, lastName)
                    self.keyUserMapping.update({key:tmpUser})
                    self.userList.append(tmpUser)

    def createBaseLine(self):
        rows, cols = self.expectedOutput.shape

        tmpDict = {}
        for i in range(0,rows):
            transaction_dict = self.expectedOutput.iloc[i].to_dict()
            key = transaction_dict['Name']
            lender = self.keyUserMapping[key]
            tmpDict.update({f"{lender.userFirstName} {lender.userLastName}":{}})

            for borrowerKey in transaction_dict.keys():
                if borrowerKey == 'Name':
                    continue
                
                borrower = self.keyUserMapping[borrowerKey]
                tmpDict[f"{lender.userFirstName} {lender.userLastName}"].update({f"{borrower.userFirstName} {borrower.userLastName}":f"{transaction_dict[borrowerKey]:.2f}"})
 
        return pd.DataFrame(tmpDict).T
    
    def runExpensesCalculation(self,SimplifyDebt):        
        # Create group
        myGroup = Group("TesterGroup", self.userList, SimplifyDebt)

        rows, cols = self.rawData.shape

        for i in range(0,rows):
            transaction_dict = self.rawData.iloc[i].to_dict()
            TotalExpense = transaction_dict['Cost']
            MemberInvolvedInTheTransaction = []
            Shares = {}
            for member in self.keyUserMapping.keys():          
                if transaction_dict[member] > 0:
                    WhoPaid = self.keyUserMapping[member]

                    if transaction_dict[member] < TotalExpense:
                        MemberInvolvedInTheTransaction.append(self.keyUserMapping[member])
                        Shares.update({self.keyUserMapping[member]:(TotalExpense-transaction_dict[member])/TotalExpense})

                if transaction_dict[member] < 0:
                    MemberInvolvedInTheTransaction.append(self.keyUserMapping[member])
                    Shares.update({self.keyUserMapping[member]:-transaction_dict[member]/TotalExpense})

            min_value = min(Shares.values())
            for member in Shares.keys():
                Shares[member] /= min_value

            myGroup.addExpenseSinglePayer(MemberInvolvedInTheTransaction,TotalExpense,WhoPaid,Shares,transaction_dict['Description'])
    
        myGroup.splitExpensesCalculation()

        return myGroup.printOutResult()

def main():
    a = DivvyNumericTester('4704-expanded_2025-04-28_export.xlsx')
    # a = DivvyNumericTester('TestCases_LargeDataSet.xlsx')
    # a = DivvyNumericTester('TestCases_SmallDataSet_v1.xlsx')
    a.createUserListFromDataFile()
    
    actResult = a.runExpensesCalculation(False)
    expResult = a.createBaseLine()

    assert expResult.equals(actResult) == True

    print(actResult)
    print(expResult)

    # actResult.to_excel('ToanOutput.xlsx', index=True)  # index=False if you don't want row numbers

if __name__=="__main__":
    main()