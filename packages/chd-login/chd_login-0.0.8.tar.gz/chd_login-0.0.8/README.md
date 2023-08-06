## CHD Login Tool

The CHD login tool is used to simplify the simulated login when accessing the CHD portal. Just follow the steps below to
easily login with your username and password.

### Install Packages

We recommend that you use the latest version to avoid unknown login failures.

```bash
pip install chd_login
```

### Use this Tool

If you pass the `need_detail=True` parameter, when the login is successful, you can get the user's cookie.

If you pass the `need_session=True` parameter, when the login is successful, you can get the session, so you can direct use session to visit the site directly. Session is a requests.session() obj. 

```python
from chd_login import IDSClient

# uid & password should match with chd portal site.
client = IDSClient(login_url, need_detail=True, need_session=True)
result, detail, session = client.login(uid, password)

# login success
if result:
    pass
# login failed
else:
    print(detail)
```

### Warning

Multiple attempts to login with the same account in a short period of time will trigger a verification code. Please login manually on the CHD portal site to solve the problem.

The behavior of the problem is that when you are using correct uid and password login, it returns 401 and 'check your username or password'.

### Others

If you have other usage questions, please contact me directly by `oren_zhang@outlook.com`.







