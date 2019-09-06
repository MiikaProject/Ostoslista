


# How to use the application

## How to install the application
Follow instructions speficied [here](./installation.md)

## Register
The first step to using the application is making a account by clicking on register. Enter your name, username and password into the fields. If your username is already taken, choose an another one. Once succesfull you will be redirected to the login page.

## Login 
Enter your username and password. After succesful login you will be redirected to the home page. 


## Basic functions


### Manage to itemlist
You can browse items you can add to your grocerylist on the itemlist-page. If item you would like to add to your grocerylist is not available there, you can easily add it to the itemlist on the same page. There is a form at the bottom of the page. Add the item's name and price to the form and click Add. This enters your item to the itemlist.
 
### Manage grocerylist
Go to the groceries page by clicking "Groceries" in the navigation bar. Then scroll down to "Possible purschases". Click on "Add" button next to item name to add it to your grocery list. In the upper portion of the groceries page you can remove item from your grocery list by pressing "Remove". This removes the item from grocery list and does not add it to your purchase archive. Buy pressing "Buy" item is marked bought and it is removed from your grocery list and put into the archive.

### Manage archive
Enter the archive by clicking "Archive" in the navigation bar. In the archive you can see all your purchases. You can change the date you made the purchase by clicking on "Edit". You can also completely remove item from archive by pressing "Remove".

### Manage own account
You can manage your account on the account page. To get there click on "Account" on navigation bar. You can change your password there by entering your password and then entering your desired new password twice in the form. You can also remove your account from the application there.


## Admin functions

### Make user admin or superuser
Currently the only way to give account admin or superuser priviledges is inserting new role for the user directly into the database. This is done with following SQL commands:  
First find the account id you want to make admin or super by typing :  
SELECT account.id from account WHERE account.name = 'username'; where 'username' is the username of the account.  
Then use query:  
INSERT INTO user_roles (user_id,role_id)  
VALUES (account.id,role.id).  
Into account.id insert the id you retrieved in earlier query. Into role.id insert the desired role (1=user, 2=admin, 3=super).


### Admin page
Users with admin priviledge see Admin button on their navigation bar. By clicking on that they move into the admin page. On the admin page they see see how many times user has logged in and when was the last login. Admins can also remove user level accounts from the application.