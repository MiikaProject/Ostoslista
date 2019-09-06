# User stories

## Browse possible purchases
 As User, I want there to be a itemlist which I can choose my items to my grocerylist quickly. If the itemlist does not include the item I am looking for, I would like to be able to add the item there myself.
 ### The SQL-queries related to this user story are:
 * List all items:  
 SELECT name,price FROM Item; 
 * Insert new item:  
 INSERT INTO Item (name,price)  
 VALUES (name,price);


## Manage items in grocerylist
As User, I want to add items from my itemlist to my grocerylist quickly. I also want to be able to remove item from the grocerylist easy without any hazzle. I also want to see how much items on my grocerylist cost.

 ### The SQL-queries related to this user story are:
 * Add item to grocerylist:  
 INSERT INTO Groceryitem (item_id,grocerylist_id)  
 VALUES (item_id,grocerylist_id);
 * Remove item from grocerylist:  
 DELETE FROM Groceryitem  
WHERE item_id=item_id AND grocerylist_id=grocerylist_id;
 * Calculate sum of groceries for certain account:  
 SELECT account_id,SUM(item.price) FROM Grocerylist  
 INNER JOIN groceryitem ON grocerylist_id=grocerylist.id  
 INNER JOIN item ON item_id=item.id
 GROUP BY grocerylist.id  
 HAVING account_id=account_id);



## Store purchases 
As User, I want to be able to keep track of my grocery purchases. I want to be able to quicky see how much money I have spent on groceries monthly. I would also like to be able to inspect item to see show many times I have purchased it and how much money I have spent being them.
 ### The SQL-queries related to this user story are:
 * List all previous purchases:  
SELECT * FROM Archive  
INNER JOIN Account ON account_id=account.id  
INNER JOIN ArchiveItem ON archive_id=archive.id  
WHERE account.id=account.id;

 * Calulated sum of purchases for archive:  
SELECT archive.id,SUM(item.price) from archive  
INNER JOIN archiveitem ON archive.id=archiveitem.archive_id  
INNER JOIN item ON archiveitem.item_id=item.id  
GROUP BY archive.id  
HAVING archive.id=:archive_id"


## Manage account
As User, I would like to be able to make a own account to the application easily and without spending a lot time doing it. I do not want to spend time filling endless forms. I would also like to be able to entirely delete my account if I wish to do so.
 ### The SQL-queries related to this user story are:
 * Register account:  
 INSERT INTO Account (username,name,password)  
 VALUES ('username','name','password')
 * Change password:  
 UPDATE Account  
 SET password='newpassword'  
 WHERE id=user.id;
 * Delete account:  
 DELETE FROM Account  
 WHERE account.id=user.id;

## Manage item list
As Admin, I would like to be able edit and possibly remove items 
 ### The SQL-queries related to this user story are:
* Remove item:  
DELETE FROM Item  
WHERE item.id='deleteditem.id';
* Edit item name and price:
UPDATE Item  
SET name='newname', price='newprice'  
WHERE item.id = 'updateditem.id';

## Manage accounts
As Admin, I would like to be able to see list of all registered accounts. I would also like to see last time they have logged in and possibly remove accounts.
 ### The SQL-queries related to this user story are:
 * List all accounts:  
 SELECT * FROM Account;
 * Get login information for accounts
 SELECT account.id,login_time FROM LoginTime  
 INNER JOIN Account ON account_id=account.id;
 * Remove account
 DELETE FROM Account  
 WHERE account.id=deletedaccount.id;


