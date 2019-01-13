# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 10:59:19 2018

@author: serap aydogdu
"""
#%%
def problem1(datafile="WA_Fn-UseC_-Telco-Customer-Churn.csv"):
    import pandas as pd
    
    data=pd.read_csv(datafile)
    data.head()
    return print((data.groupby(['Churn', 'gender']).mean()['MonthlyCharges'].unstack()))
    
#%%
def problem2(datafile="WA_Fn-UseC_-Telco-Customer-Churn.csv"): 
    import pandas as pd
    
    data=pd.read_csv(datafile)   #Reading the data
    data.head()
    
    #Defining year_tenure basis on tenure months
    data.loc[data['tenure'] < 12, 'year_tenure' ] =0; 
    data.loc[(data['tenure'] >=12) & (data['tenure'] < 24) , 'year_tenure' ] =1;
    data.loc[(data['tenure'] >=24) & (data['tenure'] < 36) , 'year_tenure' ] =2;
    data.loc[(data['tenure'] >=36) & (data['tenure'] < 48) , 'year_tenure' ] =3;
    data.loc[(data['tenure'] >=48) & (data['tenure'] < 60) , 'year_tenure' ] =4;
    data.loc[(data['tenure'] >=60) & (data['tenure'] < 72) , 'year_tenure' ] =5;
    data.loc[(data['tenure'] >=72) & (data['tenure'] < 84) , 'year_tenure' ] =6;
    
    data["Count"]=1;  #For counting the number of data points, defining a new column named "Count".   
    data.head()
    
    df= data.groupby(['year_tenure','Churn']).agg({'Count': sum})   #Grouping year_tenure and Churn and summing data points
    df['Percent'] = df.groupby(['year_tenure']).apply(lambda x: 100 * x / float(x.sum()))   #Calculating percentage of the "Yes" and "No" in the coumn Churn.
    df=df.groupby(["year_tenure"]).agg({'Count':'sum','Percent':'min'});   #Selecting the "Yes" Churn and Count of the data points.
    df= df[["Percent","Count"]];   #Reorganize the columns' order in the dataframe.
    return print("\r\n",df)
    
#%%
def problem3(datafile=""): 
    import pandas as pd
    
    #Reading the datasets
    order_data=pd.read_csv(datafile+"olist_order_items_dataset.csv");order_data.head()
    products_data=pd.read_csv(datafile+"olist_products_dataset.csv"); products_data.head()
    category_data=pd.read_csv(datafile+"product_category_name_translation.csv"); category_data.head()
    
    #Merged these 3 datasets into one dataframe
    merged_data=pd.merge(order_data, products_data, how="left", on="product_id");merged_data.head()
    merged_data=pd.merge(merged_data,category_data, how="left", on="product_category_name"); merged_data.head()
    
    #First Calculate the percentage of the freight (delivery) cost to the total cost. The total cost is the sum of freight value and the price.
    merged_data["total_cost"]=merged_data.apply(lambda x: x['price'] + x['freight_value'],axis=1)   #create a new column as total_cost and sum the price and freight_value.
    merged_data["freight_percent"]= merged_data.apply(lambda x: 100* x['freight_value'] / x['total_cost'],axis=1)   #then calculate the percentage of freight_value 

    #And then calculate the average freight_percent for each product category.
    df=merged_data.groupby(["product_category_name_english"]).mean()["freight_percent"]
    df=pd.DataFrame(df); df.head()
    
    #Finally, show the top-10 and bottom-10 freight percentage of the data.
    print("\r\ntop_10\r\n",df.sort_values(by="freight_percent",ascending=False).head(10))
    print("\r\nbottom_10\r\n",df.sort_values(by="freight_percent",ascending=True).head(10))
            
#%%    
def problem4(datafile="BreadBasket_DMS.csv"): 
    import pandas as pd    
    
    data=pd.read_csv(datafile)   #Reading the data
    
    data.Date=pd.to_datetime(data.Date,format="%Y-%m-%d")                       # formatting the "Date" column
    data.Date.head()                                                            # see "Date" column as date formatted
    data.set_index(keys="Date",inplace=True); data.head()                       # set "Date" column as index.
    
    data["count"]=1; data.head()      #For counting the number of data points, defining a new column named "count".        
                      
    df=data.groupby(["Item"]).resample("M").agg({"count":"sum"}); df.head()     #calculate monthly sales quantity of each items.
    df.reset_index(level="Item", inplace=True); df.head()                       #breaking multiindexing, leave only "Date" column as an index.
    
    df=df[(df["Item"]=="Tea") | (df["Item"]=="Coffee")];                        # select only "Tea" and "Coffee" items among all items.
    df=(df.groupby(['Date', 'Item']).sum()['count'].unstack());                 #reshaping the dataframe.
    df.index=df.index.strftime("%Y-%B");                                        # reformatting "Date" column as Monthname_year.
    print("\r\n",df)
    
#%%    
    
    
    
    
    
    
    
    
    