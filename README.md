Cyber-security project

Using the OWASP 2017 top ten list
Link:
https://github.com/Lindrax/Cs-project
Instructions:
Clone the repository to your own computer
go to /project
run python3 manage.py migrate
go to project/server
run sqlite3 db.sqlite3 < db.sql
go back to /project
run python3 manage.py runserver

Flaw 1, Injection:
https://github.com/Lindrax/Cs-project/blob/3883aaef7b501c0403b55f6ecde90b44a8d9a677/project/server/pages/views.py#L14
Starting from this line, there is a function that is used to transfer funds from one account to another, due to the way that transactions are handled through sql queries, and the input isn’t sanitized, it allows the user to input sql queries into the database. by inserting malicious queries into the bank transfer form in the place of the amount the user can manipulate the database. For example by inputting “0; DROP TABLE pages_account; – ” as the amount, the user could delete the table of users.
This flaw can be easily fixed, by using django’s ORM functionality to make and save changes to the models, or by sanitizing the sql inputs and using parametrized queries, which makes inserting the data straight into the actual query impossible. Also a good practice is to use use the command .execute instead of .executescript, which makes executing multiple queries at the same time be invalid, so inserting the extra query as a parameter wouldn’t work.
The fix:
In my code the problem is fixed, by using django’s ORM that user parametrized queries, which ensures that the input is properly sanitized
https://github.com/Lindrax/Cs-project/blob/3883aaef7b501c0403b55f6ecde90b44a8d9a677/project/server/pages/views.py#L25

Flaw 2, Broken authentication
https://github.com/Lindrax/Cs-project/blob/3883aaef7b501c0403b55f6ecde90b44a8d9a677/project/server/config/simplesession.py#L4
In this project, the session key, which is used as a authentication cookie, is generated in a very predictable way, and on a small scale, which makes obtaining a session cookie through brute force very easy. The code generates session key, by taking a random integer from a very small range, which makes it possible to iterate through possible combinations quite quickly. This would for example allow an attacker to use a loop to send transfer requests to the server until they guess the cookie right, which would make it possible to transfer funds from someone else’s account without knowing their user credentials, as long as the person has an active session
(script https://github.com/Lindrax/Cs-project/blob/main/project/src/stealmoney.py) . This can be fixed by using the django default session cookie management, or by generating the session keys in a more secure way, that makes them almost impossible to crack.
Fix:
In my code this has been fixed by generating 16 bytes of cryptographically secure random bytes, which is then converted to a hexadecimal string, which is the usual way to format session keys. The code also checks that the session key is unique, so the keys don’t accidentally get reused
https://github.com/Lindrax/Cs-project/blob/30e9578fef6f0d0549ef455c8c118edcb9778f8b/project/server/config/simplesession.py#L12

Flaw 3, broken access control
https://github.com/Lindrax/Cs-project/blob/646ca3d807da44017ce84686677c9c53af1bdd2b/project/server/pages/views.py#L46
In the application, there is a url that lists all the accounts in the database, this is supposed to be only visible to superusers, but because the application only checks that the user is logged in, anyone can access this page. this is a clear case of broken access control, where the application doesn’t properly check that the user has the required privileges for viewing sensitive information
Fix:
This is fixed by using the user_passes_test decorator, in this case it is used to verify that the user trying to access the page has the role of a superuser, and thus normal users won’t get access to everyones information.
https://github.com/Lindrax/Cs-project/blob/646ca3d807da44017ce84686677c9c53af1bdd2b/project/server/pages/views.py#L44

Flaw 4, sensitive data exposure.
https://github.com/Lindrax/Cs-project/blob/a206c5462b0c3a41742cffb37ab8307ec19e6289/project/server/pages/views.py#L38
In the project there is a page for viewing your own account. When accessing the account the application checks that the user is authenticated ( has a valid session cookie) but doesn’t check that the user is logged in. This means that in a situation where the session tokens are still valid, even if the user has logged out, someone can run a script that iterates through potential tokens, and when a token is valid it prints out that persons name and balance. (script https://github.com/Lindrax/Cs-project/blob/main/project/src/hijacksession.py )
Fix:
By adding the @login_required decorator, the application check that the user is logged in before showing the page, and thus just obtaining the session id doesn’t allow attackers to see users balances
https://github.com/Lindrax/Cs-project/blob/646ca3d807da44017ce84686677c9c53af1bdd2b/project/server/pages/views.py#L37

Flaw 5, security misconfiguration.
https://github.com/Lindrax/Cs-project/blob/a206c5462b0c3a41742cffb37ab8307ec19e6289/project/server/db.sql#L79
In the way that the database is set up, admin user gets created automatically with the default password “salainen” this is a good example of security misconfiguration due to using a default configuration. someone could easily access the admin panel by iterating through basic or most used passwords, and thus gain access to the admin panel, where you can find all the information on other accounts.
Fix:
This can be fixed by either not creating a superuser by default, or as i have done in this project you are forced to change the default admin password, so that only the person running the application would know it (in the case that the application would actually be in production). The security could be further enhanced by forcing the user to choose a actually good or complex password
https://github.com/Lindrax/Cs-project/blob/a206c5462b0c3a41742cffb37ab8307ec19e6289/project/manage.py#L13
