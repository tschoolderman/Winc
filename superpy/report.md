# Report of the SuperPy assignment
&nbsp;
*By Thomas Schoolderman*

&nbsp;
## Three technical elements of my code
&nbsp;
- inventory tracker
- pandas implementation
- matplotlib
  
---
&nbsp;
## Inventory tracker
To assist an easy access of the inventory tracking of the quantity is done in a seperate csv file.  
Tracking is done automatically when buying, selling or expiring products.  
The code below shows how the `csv.reader` is used to put the data into a list.  
Producing a list of sublists, which is then used to iterate over and find the item being sold.  
When said item has been found it takes the second value and calculates the new quantity.  
After the quantity has been calculated it is then changed in the list, whereafter the list is again written back to the csv file to create an updated inventory.  
```python
    lines = []  # Placeholder for rows in csv file
    for row in inv_reader:
        lines.append(row)  # Append all rows as list
    # Check if the sold product is available
    if any(sell.product in i for i in lines) is True:
        for i in lines:
            if i[0] == sell.product:
                # Decrease the product quantity when available
                x = int(i[1]) - sell.quantity
                i[1] = x
                if x >= 0:
                    with open(
                        INVENTORY_FILE_PATH, mode="w", newline=""
                    ) as inv_file:
                        inv_writer = csv.writer(
                            inv_file,
                            delimiter=",",
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL,
                        )
                        # Write the new quantity to csv
                        inv_writer.writerows(lines)
```
---
&nbsp;
## Pandas implementation
Pandas has been used to assist with certain data management.  
Such as creating the dataframes for showing which products are expiring between two dates;  
`old_date` and `new_date` of the `def changing_date()` function, which are acquired from the date.txt file.  
In the code snippet below; the csv file for bought_products is sorted based on the difference between the old and new date.  
A new copy of the dataframe is created to prevent the `settingswithcopywarning` error message.  
Afterwards the dataframe is presented as a table using the `tabulate` module.  
```python
    df = pd.read_csv("bought_products.csv", index_col="id")
    expired_df = df.loc[(df["expiration_date"] < get_date())].copy()
    mask = (expired_df["expiration_date"] >= old_date) & (
        expired_df["expiration_date"] < new_today
    )
    expired_df = expired_df.loc[mask]
    print(f'\n{tabulate(expired_df,headers=COLUMNS_BOUGHT,tablefmt="fancy_outline",)}')
```
<br/>

Pandas is also used for creating and merging three different dataframes from csv files as shown below.  
Since the merged dataframe contains `NaN`-values the pandas `interpolate` function is used to complete the missing date.  
```python
    df2 = pd.read_csv("bought_products.csv", index_col="id")
    df2 = df2.groupby("date", as_index=False)["cost"].sum().copy()

    df3 = pd.read_csv("sold_products.csv", index_col="id")
    df3 = df3.groupby("date", as_index=False)["income"].sum().copy()

    df4 = pd.read_csv("expired_products.csv", index_col="id")
    df4 = df4.groupby("date", as_index=False)["loss"].sum().copy()

    # Merge the dataframes into a single dataframe
    dfs = [df2, df3, df4]
    final_df = reduce(
        lambda left, right: pd.merge(left, right, on=["date"], how="outer"), dfs
    )
    final_df = final_df.sort_values(by=["date"])
    # Using interpolate to compensate for NaN values in the dataframe
    final_df = final_df.interpolate(method="linear", limit_direction="forward", axis=0)
    # Add a new column to the dataframe
    final_df["profit"] = final_df["income"] - (final_df["cost"] + final_df["loss"])
```
<br/>

Pandas is used, together with `openpyxl`, to export the date from a csv file to xslx format.  
```python
    if e.export == "bought":
        df = pd.read_csv(BOUGHT_FILE_PATH)
        df.to_excel("bought.xlsx")
        return f"The {e.export} file has been exported to Excel"
```
---
&nbsp;
## Matplotlib
The module `matplotlib` is used to present a graph of the cashflow from the very beginning.  
A window is created with the code below.  
```python
    # Define the window of the graph
    plt.style.use("dark_background")
    plt.rcParams["figure.figsize"] = [10, 4]
    plt.rcParams["figure.autolayout"] = True
```
<br/>

As mentioned in the "Pandas implementation"; the `NaN`-values have been interpolated.  
If this wasn't done, lines would have breaks in them.  
Lines have been defined as shown in the code in the snippet below.  
```python
    # Define the line for the loss
    plt.plot(
        final_df["date"],
        final_df["loss"],
        color="#FFCE30",
        lw=2,
        linestyle="dotted",
        marker="o",
        label="loss",
    )
```
<br/>

In the snippet below it is shown how the axis are labeled as well as a defined place for the legend.  
```python
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0.0)
    plt.title("Cash flow per date")
    plt.xlabel("Date")
    plt.ylabel("Cashflow in euro's")
    plt.show()
```