from src.Group import Group
from src.Group import User

import pytest # type: ignore

# coverage run -m pytest test_GroupAddExpenseWithSimplifyDebt.py test_GroupAddExpenseNoSimplifyDebt.py test_GroupConstructor.py test_GroupAddRemoveUsers.py test_User.py test_GroupAddExpenses_RealDataSet.py 
# coverage report -m
# coverage html

def test_addMemberToGroup(): #1
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    group1 = Group("Hawaii", [toan], False)

    assert group1.GroupName == "Hawaii"
    assert group1.InitialGroupMembers == (toan,)
    assert group1.MembersDB == {toan:{}}

    bich = User("beryl.tran@ey.com", "123456", "Bich", "Tran")
    group1.addMemberToGroup(bich)
    assert group1.MembersDB == {toan:{}, bich:{}}

    eugene = User("eugene.vo-dai@harvard.edu", "123456", "Eugene", "Vo-Dai")
    group1.addMemberToGroup(eugene)
    assert group1.MembersDB == {toan:{}, bich:{}, eugene:{}}

def test_addInvalidMember(): #2
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    group1 = Group("Hawaii", [toan], False)
    group2 = Group("Hawaii", [toan], False)

    with pytest.raises(ValueError, match="User not recognized"):
        group1.addMemberToGroup(group2)

def test_memberAlreadyExists1(): #3
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    group1 = Group("Hawaii", [toan], False)

    with pytest.raises(ValueError, match="This user was initially added to this group"):
        group1.addMemberToGroup(toan)

def test_memberAlreadyExists2(): #4
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    group1 = Group("Hawaii", [], False)

    assert group1.InitialGroupMembers == ()
    group1.addMemberToGroup(toan)
    assert group1.MembersDB == {toan:{}}

    with pytest.raises(ValueError, match="This user has already been added to this group"):
        group1.addMemberToGroup(toan)

def test_removeMemberFromGroup(): #5
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    group1 = Group("Hawaii", [toan], False)

    assert group1.GroupName == "Hawaii"
    assert group1.InitialGroupMembers == (toan,)
    assert group1.MembersDB == {toan:{}}

    group1.removeMemberFromGroup(toan)
    assert group1.MembersDB == {}

    bich = User("beryl.tran@ey.com", "123456", "Bich", "Tran")
    group1.addMemberToGroup(bich)
    assert group1.MembersDB == {bich:{}}

    eugene = User("eugene.vo-dai@harvard.edu", "123456", "Eugene", "Vo-Dai")
    group1.addMemberToGroup(eugene)
    assert group1.MembersDB == {bich:{}, eugene:{}}

    group1.removeMemberFromGroup(eugene)
    assert group1.MembersDB == {bich:{}}

    group1.removeMemberFromGroup(bich)
    assert group1.MembersDB == {}

def test_removeInvalidMemberFromGroup(): #6
    group1 = Group("Hawaii", [], False)
    group2 = Group("Hawaii", [], False)

    with pytest.raises(ValueError, match="User not recognized"):
        group1.removeMemberFromGroup(group2)

def test_removeNonExistingMemberFromGroup(): #7
    toan = User("toanv@mathworks.com", "123456", "Toan", "Vo-Dai")
    group1 = Group("Hawaii", [], False)

    with pytest.raises(ValueError, match="This user is not in this group"):
        group1.removeMemberFromGroup(toan)