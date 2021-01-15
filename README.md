# Issue tracker

It's a simple issue tracker developed with Flask and SQLite. Users have to create an account. Then they can create issues, comment on them or close them if necessary.

![Screen1](/images/Screen1.png)

![Screen2](/images/Screen2.png)
## Install

```bash
pip3 install flask, flask_login, flask_sqlalchemy
git clone https://github.com/psurkov/Issue-tracker.git
cd Issue-tracker
```

## Use

Type `flask run` to start application. You will see a link such as http://127.0.0.1:5000/ then follow it.

You need to sign up or sign in to create issues and comment on them. Two accounts have already been created. Alice's account `alice@gmail.com` with the password `qwerty` and Bob's `bob@gmail.com` with the password `12345`. You can sign in with one of them or create your own.

If you want to clear the database just delete `sqlite.db` from root and restart the application.
