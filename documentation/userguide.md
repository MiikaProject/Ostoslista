


# How to use the application

## How to install the application
Follow instructions speficied [here](./installation.md)

## Register
The first step to using the application is making a account by clicking on register. Enter your name, username and password into the fields. If your username is already taken, choose an another one. Once succesfull you will be redirected to the login page.

## Make user admin or superuser
Currently the only way to give account admin or superuser priviledges is inserting new role for the user directly into the database. This is done with following SQL commands. First find the account id you want to make admin or super by typing : SELECT account.id from account WHERE account.name = 'username'; where 'username' is the username of the account. Then use query INSERT INTO user_roles (user_id,role_id) VALUES (account.id,role.id). Into account.id insert the id you retrieved in earlier query. Into role.id insert the desired role (1=user, 2=admin, 3=super).


## Login 
Enter your username and password. After succesful login you will be redirected to the home page. 


## Basic functions


### Manage to itemlist
You can browse items you can add to your grocerylist on the itemlist-page. If item you would like to add to your grocerylist is not available there, you can easily add it to the itemlist on the same page. There is a form at the bottom of the page. Add the item's name and price to the form and click Add. This enters your item to the itemlist.
 
### Manage grocerylist



### Manage own account