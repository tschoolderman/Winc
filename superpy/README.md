# Superpy

Using a supermarket application by using the CLI.  
<br/>

Table of Contents
---
- [Superpy](#superpy)
  - [Table of Contents](#table-of-contents)
  - [General info](#general-info)
  - [Setting the date](#setting-the-date)
  - [Buying products](#buying-products)
  - [Selling products](#selling-products)
  - [Expring products](#expring-products)
  - [View inventory](#view-inventory)
  - [View expired](#view-expired)
  - [Search inventory](#search-inventory)
  - [Revenue](#revenue)
  - [Export to excel](#export-to-excel)
  - [Profits](#profits)
  - [Show graph](#show-graph)
---
<br/>

## General info
---
To use this application, please make sure you are in the right directory before issueing commands.  
If needed change directory to `./superpy/`.  
In this guide parts of the code is shown in curly brackets '{}'.  
Arguments are passed in place of the curly brackets based on user input without the brackets.  
  
To use the help function enter the following code in de CLI:  
> ` python main.py -h`  
  
To gain access to a command specific help, use the following code:
> ` python main.py buy -h`  

To view the help of other commands, replace 'buy' with:  
sell, expire, inventory, view-expired, search, date, revenue, profit, export or graph.

<br/>

## Setting the date
---
Set the date of the program, which is perceived as 'today' by executing the following commands:  
  
When no arguments are given, set the date for the real-time today:
> $ `python main.py date`  

<br/>

Change the date which is perceived as the current 'today' by adding arguments.  
The arguments are given as a number. The number indicates the amount of days to increase the current 'today':  
> $ `python main.py date -a {days}`  

<br/>

## Buying products  
---
To buy products using the CLI enter the following command:  
> $ `python main.py buy -p {product} -q {product quantity} -m {product buy price} -e {expiration date in YYYY-MM-DD}`  

After executing this code the product is written to a csv file at the date set for today.

<br/>

## Selling products 
--- 
To sell products using the CLI enter the following command:  
> $ `python main.py sell -p {product} -q {product quantity} -m {product sell price}`  

After executing this code the product is written to a csv file at the date set for today.

<br/>  

## Expring products 
--- 
To expire products using the CLI enter the following command:  
> $ `python main.py expire -p {product} -q {product quantity} -m {product buy price}`  

After executing this code the product is written to a csv file at the date set for today.

<br/>  

## View inventory 
--- 
To view the current inventory using the CLI enter the following command:  
> $ `python main.py inventory`  

This shows a table of the total inventory of available products in store. 

<br/>  

## View expired 
--- 
To view all expired products using the CLI enter the following command:  
> $ `python main.py view-expired`  

This shows a table of all the expired products. 

<br/>  

## Search inventory 
--- 
To search the inventory for a specific product using the CLI enter the following command:  
> $ `python main.py search -s {product}`  

This shows the current stock of the searched item. 

<br/>  

## Revenue 
--- 
To show the revenue of a certain period using the CLI enter the following command:  
> $ `python main.py revenue -r {days}`  

Set the day to '0' to get the revenue for today.  
To get the revenue from yesterday until today enter '1'.  
To get the revenue from last month until today enter '30'.  
To get the revenue from last year until today enter '365'.  
This shows the revenue by the amount of days in the past specified by the user.  

<br/>  

## Export to excel 
--- 
To export files to an excel format using the CLI enter the following command:  
> $ `python main.py export -e {choice}`  

There are 4 choices of files to be exported to excel format: bought, sold, expired or inventory.  
The chosen file is exported to excel format in the current directory.   

<br/>  

## Profits 
--- 
To view the profits made using the CLI enter the following command:  
> $ `python main.py profit -p {days}`  

Set the day to '0' to get the revenue for today.  
To get the revenue from yesterday until today enter '1'.  
To get the revenue from last month until today enter '30'.  
To get the revenue from last year until today enter '365'.  
This shows the revenue by the amount of days in the past specified by the user.  

<br/>  

## Show graph 
--- 
To view a graph of the cash flow from start-up until now using the CLI enter the following command:  
> $ `python main.py graph`  

This will pop-up a new window showing a graph of the cash flow.  
This will show the income, loss, cost and profits over time.
