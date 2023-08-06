from unittest.mock import patch
import os
import pytest
import json
from compose.db2.users import UserManager, NoUserExistsException, PasswordInvalidException, UserAlreadyExistsException, IAMUserAlreadyExistsException, IBMIDInvalidException, InvalidUserGroupException
from compose.db2.configuration import Configuration
from compose.tests.mocks import kubernetes_mocks

@pytest.fixture
def usermanager(tmpdir):
    fd = tmpdir.mkdir("test").join("users.json") 
    data = {
        "iamusers": {
            "iam-ServiceId-test":"ucmon"
        },
        "policies": {
            "default": {
            "lock_duration": "60",
            "max_attempts": "5"
            }
        },
        "groups": {
            "BLUUSERS": {
            "desc": "Non-Admin Group"
            },
            "DB2IADM1": {
            "desc": "SYSADM group"
            },
            "BLUADMIN": {
            "desc": "Admin Group"
            }
        },
        "users": {
            "ucmon": {
                "username": "ucmon",
                "locked": False,
                "group": "bluadmin",
                "locked_count": 0,
                "locked_time": 0,
                "policyname": "default",
                "email": "",
                "password": "{SSHA}RjFvcFExNE9SOGx4eExKKzEwcElrYkMzZWU4aCtrUDg="
            },
            "mock-user": {
                "username": "mock-user",
                "locked": False,
                "group": "bluadmin",
                "locked_count": 0,
                "locked_time": 0,
                "policyname": "default",
                "email": "",
                "password": "{SSHA}RjFvcFExNE9SOGx4eExKKzEwcElrYkMzZWU4aCtrUDg="
            }
        },  
        "rev": 0
    }

    fd.write(json.dumps(data))

    conf = {
        'db2_user_file': fd,
        'cos_region': 'test',
        'cos_endpoint': 'localhost',
        'cos_access_key': 'test',
        'cos_secret_access_key': 'test',
        'cos_bucket': 'CSYS.TEST',
        'id': 'test',
        'fqdn': 'test.local',
        'repo_type': 's3',
        'db_name': 'bludb',
        'cosdisabled': True,
        'db2disabled': True
    }
    yield UserManager(conf)

def test_user_create(usermanager):
    um = usermanager
    data= '{"username":"test123","password":"temp1234"}'
    um.create_user(data)
    user = um.get_user(data)
    assert(user['username']=="test123")
    assert(user['group']=="bluusers")
    assert(user['email']=="")
    assert(user['locked']==False)

def test_user_create_ibmid_serviceid(usermanager):
    um = usermanager
    data= '{"username":"test123","group":"bluadmin","ibmid":"iam-ServiceId-test2"}'
    um.create_user(data)
    user = um.get_user(data)
    assert(user['username']=="test123")
    assert(user['group']=="bluadmin")
    assert(um.json_data["users"]["test123"]["locked"]==False)
    assert(um.json_data["users"]["test123"]["password"]!="")

def test_user_create_ibmid(usermanager):
    um = usermanager
    data= '{"username":"iamtest2","group":"bluadmin","ibmid":"IBMid-test1234"}'
    um.create_user(data)
    user = um.get_user(data)
    assert(user['username']=="iamtest2")
    assert(user['group']=="bluadmin")
    assert(um.json_data["users"]["iamtest2"]["locked"]==False)
    assert(um.json_data["users"]["iamtest2"]["password"]!="")

def test_user_create_alreadyexists(usermanager):
    um = usermanager
    data= '{"username":"ucmon","group":"bluadmin","hash":"fiefjoiejf"}'
    pytest.raises(UserAlreadyExistsException,um.create_user,data)

def test_user_create_iamalreadyexists(usermanager):
    um = usermanager
    data = '{"username":"test123","group":"bluadmin","ibmid":"iam-ServiceId-test"}'
    pytest.raises(IAMUserAlreadyExistsException,um.create_user,data)

def test_user_create_invalid_iam(usermanager):
    um = usermanager
    data= '{"username":"iamtest1","group":"bluadmin","ibmid":"iam-Test48484"}'
    pytest.raises(IBMIDInvalidException, um.create_user, data)

def test_restricted_user(usermanager):
    um = usermanager
    data= '{"username":"ucmon","email":"test123@email.com"}'
    pytest.raises(NoUserExistsException, um.modify_user, data)

def test_modify_user(usermanager):
    um = usermanager
    data= '{"username":"mock-user","email":"test123@email.com"}'
    um.modify_user(data)
    user = um.get_user(data)
    assert(user['email'] == "test123@email.com")
    assert(user['group'] == "bluadmin")

def test_user_delete(usermanager):
    um = usermanager
    data= '{"username":"user1", "password":"test12345"}'
    um.create_user(data)
    #should not fail
    user = um.get_user(data)
    #delete user and then check if it exists
    um.delete_user(data)
    pytest.raises(NoUserExistsException, um.get_user, data)

def test_iamuser_delete(usermanager):
    um = usermanager
    data= '{"username":"iamtestuser1","email":"test123@email.com","ibmid":"iam-ServiceId-testdelete","group":"bluadmin"}'
    um.create_user(data)
    user = um.get_user(data)
    um.delete_user(data)
    print(um.json_data['iamusers'])
    assert('iam-ServiceId-testdelete' not in um.json_data["iamusers"])
    pytest.raises(NoUserExistsException, um.get_user, data)

def test_lock_user(usermanager):
    um = usermanager
    data= '{"username":"mock-user"}'
    um.lock_user(data)
    assert(um.json_data["users"]["mock-user"]["locked"]==True)
    um.unlock_user(data)
    assert(um.json_data["users"]["mock-user"]["locked"]==False)

def test_user_changepassword(usermanager):
    um = usermanager
    data= '{"username":"mock-user", "hash":"{SSHA}RjFvcFExNE9SOGx4eExKKzEwcElrYkMzZWU4aCtrUDf="}'
    um.change_password(data)
    assert(um.json_data["users"]["mock-user"]["password"]!="{SSHA}RjFvcFExNE9SOGx4eExKKzEwcElrYkMzZWU4aCtrUDg=")

def test_user_bluuserchangepassword(usermanager):
    um = usermanager
    data= '{"username":"test123","password":"temp1234"}'
    um.create_user(data)
    data= '{"username":"test123","oldpassword":"temp22","newhash":"{SSHA}RjFvcFExNE9SOGx4eExKKzEwcElrYkMzZWU4aCtrUDg="}'
    pytest.raises(PasswordInvalidException, um.change_password_bluuser, data)
    data= '{"username":"test123","oldpassword":"temp1234","newhash":"{SSHA}RjFvcFExNE9SOGx4eExKKzEwcElrYkMzZWU4aCtrUDf="}'
    um.change_password_bluuser(data)

def test_create_invalidgroup(usermanager):
    um = usermanager
    data= '{"username":"testbadgroup","password":"temp1234","group":"test"}'
    pytest.raises(InvalidUserGroupException, um.create_user, data)


