import pandas as pd
orders=pd.read_csv("unclean_orders.csv")
customers=pd.read_csv("unclean_customers.csv")
print(orders.head())
print(customers.head())

print("norder missing values")
print(orders.isnull().sum())
print("ncustomer missing values")
print(customers.isnull().sum())

print("\norders duplicate")
print(orders.duplicated().sum())

print("\ncustomers duplicate")
print(customers.duplicated().sum())

print("\nduplicate orders")
print(orders[orders.duplicated()])

print("\nduplicate customers")
print(customers[customers.duplicated()])

print("\norder with missing value")
print(orders[orders.isnull().any(axis=1)])

print("\ncustomer with missing value")
print(customers[customers.isnull().any(axis=1)])

orders["Region"]=orders["Region"].str.strip()
orders["Region"]=orders["Region"].str.title()

print("\norders region values")
print(orders["Region"].unique())
print(orders["Region"].tolist())

print(customers[customers["Customer_ID"]=="C005"])
orders.loc[orders["Order_ID"]==1005,"Region"]="Chennai"
print(orders[orders["Order_ID"]==1007])

print(orders[orders["Order_ID"]==1008])
print(customers[customers["Customer_ID"]=="C011"])

orders=orders.drop_duplicates()
customers=customers.drop_duplicates()

print("\norders duplicate after cleaning")
print(orders.duplicated().sum())

print("\ncustomers duplicate after cleaning")
print(customers.duplicated().sum())

orders.to_csv("clean_orders.csv",index=False)
customers.to_csv("clean_customers.csv",index=False)