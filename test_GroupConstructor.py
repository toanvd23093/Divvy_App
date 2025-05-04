from Group import Group
from User import User

import pytest # type: ignore

# coverage run -m pytest test_GroupAddExpenseWithSimplifyDebt.py test_GroupAddExpenseNoSimplifyDebt.py test_GroupConstructor.py test_GroupAddRemoveUsers.py test_User.py test_GroupAddExpenses_RealDataSet.py 
# coverage report -m
# coverage html

def test_GroupConstructor1(): #1
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    group1 = Group("Hawaii", [toan], False)

    assert group1.GroupName == "Hawaii"
    assert isinstance(group1.InitialGroupMembers, tuple) == True
    assert group1.InitialGroupMembers == (toan,)
    assert group1.MembersDB == {toan:{}}
    assert group1.SimplifyDebt == False

def test_GroupConstructor2(): #2
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    bich = User("beryl.tran@ey.com", "123456", "Bich", "Tran")
    group1 = Group("Hawaii.Honolulu112023", [toan, bich], True)

    assert group1.GroupName == "Hawaii.Honolulu112023"
    assert isinstance(group1.InitialGroupMembers, tuple) == True
    assert group1.InitialGroupMembers == (toan, bich)
    assert group1.MembersDB == {toan:{}, bich:{}}
    assert group1.SimplifyDebt == True

def test_GroupConstructor3(): #3
    group1 = Group("Hawaii.Honolulu112023", [], True)

    assert group1.GroupName == "Hawaii.Honolulu112023"
    assert isinstance(group1.InitialGroupMembers, tuple) == True
    assert group1.InitialGroupMembers == ()
    assert group1.MembersDB == {}
    assert group1.SimplifyDebt == True

def test_invalidGroupName1(): #4
    with pytest.raises(ValueError, match="Group Name should not contain special characters"):
        group1 = Group("Hawaii.Honolulu112023@", [], False)

def test_invalidGroupName2(): #5
    with pytest.raises(ValueError, match="Group Name should not contain special characters"):
        group1 = Group("Hawaii.Honolu@@lu112023", [], False)

def test_invalidGroupName3(): #6
    with pytest.raises(ValueError, match="Group Name should not contain special characters"):
        group1 = Group("Hawaii.Honolu lu112023", [], False)

def test_invalidGroupMembersType(): #7
    with pytest.raises(ValueError, match="Please specify a List of Group Members"):
        group1 = Group("Hawaii.Honolulu112023", {}, False)

def test_GroupMembersNotRecognized(): #8
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    group1 = Group("Hawaii", [toan], False)

    with pytest.raises(ValueError, match="User not recognized"):
        group1 = Group("Hawaii.Honolulu112023", [group1])

def test_InitialGroupMembersIsReadOnly(): #9
    group1 = Group("Hawaii.Honolulu112023", [], False)

    assert group1.GroupName == "Hawaii.Honolulu112023"
    assert group1.InitialGroupMembers == ()

    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    bich = User("beryl.tran@ey.com", "123456", "Bich", "Tran")
    
    with pytest.raises(ValueError, match=""):
        group1.InitialGroupMembers = (toan, bich)

    assert isinstance(group1.InitialGroupMembers, tuple) == True
    assert group1.InitialGroupMembers == ()

def test_InvalidSimplifyDebtFlag1(): #10
    with pytest.raises(ValueError, match="Simplify Debt option should be logical flag"):
        group1 = Group("Hawaii", [], "False")

def test_InvalidSimplifyDebtFlag2(): #11
    group1 = Group("Hawaii", [], True)
    with pytest.raises(ValueError, match="Simplify Debt option should be logical flag"):
        group1.SimplifyDebt = "False"