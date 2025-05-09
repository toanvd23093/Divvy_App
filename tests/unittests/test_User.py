from src.User import User
import pytest # type: ignore

# coverage run -m pytest test_GroupAddExpenseWithSimplifyDebt.py test_GroupAddExpenseNoSimplifyDebt.py test_GroupConstructor.py test_GroupAddRemoveUsers.py test_User.py test_GroupAddExpenses_RealDataSet.py 
# coverage report -m
# coverage html

def test_UserConstructor(): #1
    user1 = User(userEmail = "toanvd2309@gmail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")
    assert user1.userEmail == "toanvd2309@gmail.com"
    assert user1.userPassword == "123456"
    assert user1.userFirstName == "Toan"
    assert user1.userLastName == "Vo-Dai"
    assert str(user1) == "First Name: Toan. Last Name: Vo-Dai. Email: toanvd2309@gmail.com. Password: 123456"

def test_ValidEmail1(): #2
    user1 = User(userEmail = "toanvd.2309@gmail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")
    assert user1.userEmail == "toanvd.2309@gmail.com"

def test_ValidEmail2(): #3 
    user1 = User(userEmail = "toanvd_2309@gmail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")
    assert user1.userEmail == "toanvd_2309@gmail.com"

def test_ValidEmail3(): #4 
    user1 = User(userEmail = "toanvd-2309@gmail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")
    assert user1.userEmail == "toanvd-2309@gmail.com"

def test_ValidEmail4(): #5
    user1 = User(userEmail = "toan.VD-2309@gmail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")
    assert user1.userEmail == "toan.VD-2309@gmail.com"

def test_InvalidEmail1(): #6  
    with pytest.raises(ValueError, match = "Email Format is not valid. Valid format should be john-doe@gmail.com"):
        user1 = User(userEmail = "toanvd2309@@gmail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")

def test_InvalidEmail2(): #7   
    with pytest.raises(ValueError, match = "Email Format is not valid. Valid format should be john-doe@gmail.com"):
        user1 = User(userEmail = "toanvd2309@gmail..com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")

def test_InvalidEmail3(): #8
    with pytest.raises(ValueError, match = "Email Format is not valid. Valid format should be john-doe@gmail.com"):
        user1 = User(userEmail = "toanvd2309@g9ail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")

def test_InvalidEmail4(): #9   
    with pytest.raises(ValueError, match = "Email Format is not valid. Valid format should be john-doe@gmail.com"):
        user1 = User(userEmail = "toanvd2309@gmail.c1m", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")

def test_InvalidEmail5(): #10 
    with pytest.raises(ValueError, match = "Email Format is not valid. Valid format should be john-doe@gmail.com"):
        user1 = User(userEmail = "toanvd2309@gmail.12", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")

def test_InvalidEmail6(): #11    
    with pytest.raises(ValueError, match = "Email Format is not valid. Valid format should be john-doe@gmail.com"):
        user1 = User(userEmail = "toanvd{2309@gmail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")

def test_InvalidEmail7(): #12   
    with pytest.raises(ValueError, match = "Email Format is not valid. Valid format should be john-doe@gmail.com"):
        user1 = User(userEmail = "toanvd[2309]@gmail.com", userPassword = "123456", userFirstName="Toan", userLastName="Vo-Dai")

def test_InvalidPassword1(): #13
    with pytest.raises(ValueError, match = "Password should have more than 5 letters"):
        user1 = User(userEmail = "toanvd2309@gmail.com", userPassword = "12345", userFirstName="Toan", userLastName="Vo-Dai")

def test_ValidFirstName1(): #14
    user1 = User(userEmail = "30vodai@cua.edu", userPassword = "123456", userFirstName="John Doe", userLastName="Vo-Dai")
    assert user1.userFirstName == "John Doe"

def test_ValidFirstName2(): #15
    user1 = User(userEmail = "toanv@mathworks.com", userPassword = "123456", userFirstName="John - Doe", userLastName="Vo-Dai")
    assert user1.userFirstName == "John - Doe"

def test_ValidFirstName3(): #16
    user1 = User(userEmail = "beryl.tran@ey.com", userPassword = "123456", userFirstName="John-Doe", userLastName="Vo-Dai")
    assert user1.userFirstName == "John-Doe"

def test_InvalidFirstName1(): #17
    with pytest.raises(ValueError, match = "There should not be any special character in first name"):
        user1 = User(userEmail = "toanvd2309@gmail.com", userPassword = "123456", userFirstName="John  Doe", userLastName="Vo-Dai")

def test_InvalidFirstName2(): #18
    with pytest.raises(ValueError, match = "There should not be any special character in first name"):
        user1 = User(userEmail = "toanvd2309@gmail.com", userPassword = "123456", userFirstName="John ? Doe", userLastName="Vo-Dai")

def test_InvalidFirstName3(): #19
    with pytest.raises(ValueError, match = "There should not be any special character in first name"):
        user1 = User(userEmail = "toanvd2309@gmail.com", userPassword = "123456", userFirstName="John / Doe", userLastName="Vo-Dai")

def test_ValidLastName1(): #20
    user1 = User(userEmail = "30vodai@cua.edu", userPassword = "123456", userFirstName="John Doe", userLastName="Vo-Dai")
    assert user1.userLastName == "Vo-Dai"

def test_ValidLastName2(): #21
    user1 = User(userEmail = "toanv@mathworks.com", userPassword = "123456", userFirstName="John - Doe", userLastName="VODAI")
    assert user1.userLastName == "VODAI"

def test_ValidLastName3(): #22
    user1 = User(userEmail = "beryl.tran@ey.com", userPassword = "123456", userFirstName="John-Doe", userLastName="Vo - DAi")
    assert user1.userLastName == "Vo - DAi"

def test_InvalidLastName1(): #23
    with pytest.raises(ValueError, match = "There should not be any special character in last name"):
        user1 = User(userEmail = "toanvd2309@gmail.com", userPassword = "123456", userFirstName="John Doe", userLastName="Vo  Dai")

def test_InvalidLastName2(): #24
    with pytest.raises(ValueError, match = "There should not be any special character in last name"):
        user1 = User(userEmail = "toanvd2309@gmail.com", userPassword = "123456", userFirstName="John Doe", userLastName="Vo/Dai")

def test_InvalidLastName3(): #25
    with pytest.raises(ValueError, match = "There should not be any special character in last name"):
        user1 = User(userEmail = "toanvd2309@gmail.com", userPassword = "123456", userFirstName="John Doe", userLastName="Vo?Dai")