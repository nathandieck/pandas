#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)

purchase_data.head()


# In[2]:


## Player Count


# In[3]:


#nunique: https://www.geeksforgeeks.org/python-pandas-series-nunique/
players = purchase_data["SN"].nunique()

players_d = {"Total Players": [players]}

players_df = pd.DataFrame(players_d)

players_df


# In[4]:


## Purchasing Analysis (Total)


# In[5]:


unique_items = purchase_data["Item Name"].nunique()

average_price = purchase_data["Price"].mean()

num_purchases = purchase_data["Purchase ID"].count()

revenue = purchase_data["Price"].sum()

summary_d = {"Number of Unique Items": [unique_items], 
             "Average Price": [average_price], 
             "Number of Purchases": [num_purchases],
             "Total Revenue": [revenue]}

summary_df = pd.DataFrame(summary_d)

summary_df["Average Price"] = summary_df["Average Price"].map("${:.2f}".format)

summary_df["Total Revenue"] = summary_df["Total Revenue"].map("${:,.2f}".format)

summary_df.head()


# In[6]:


## Gender Demographics


# In[7]:


gen_f_df = purchase_data.loc[purchase_data["Gender"] == "Female", :]
gen_f = len(gen_f_df["SN"].unique())
gen_m_df = purchase_data.loc[purchase_data["Gender"] == "Male", :]
gen_m = len(gen_m_df["SN"].unique())
gen_o_df = purchase_data.loc[purchase_data["Gender"] == "Other / Non-Disclosed", :]
gen_o = len(gen_o_df["SN"].unique())
players = len(purchase_data["SN"].unique())

gender_demographics = {"Gender": ["Female", "Male", "Other / Non_Disclosed"],
                      "Total Count": [gen_f, gen_m, gen_o],
                      "Percentage of Players": [(gen_f/players*100), (gen_m/players*100), (gen_o/players*100)]}

gender_demographics_df = pd.DataFrame(gender_demographics)

gender_demographics_df["Percentage of Players"] = gender_demographics_df["Percentage of Players"].map("{:,.2f}%".format)

gender_demographics_df.head()


# In[8]:


## Purchasing Analysis (Gender)


purchasers = {"Gender": ["Female", "Male", "Other / Non-Disclosed"],
             "Players": [gen_f, gen_m, gen_o]}

purchasers = pd.DataFrame(purchasers)

purchasers = purchasers.groupby("Gender")["Players"].sum()

purchases_pd = purchase_data[["Gender", "Price"]]

purchases_df = pd.DataFrame(purchases_pd)

purchases_count = purchases_df.groupby("Gender")["Gender"].count()

purchases_count = pd.DataFrame(purchases_count)

purchases_count = purchases_count.rename(columns={"Gender": "Purchase Count"})

purchases_avg = purchases_df.groupby("Gender")["Price"].mean()

purchases_avg = pd.DataFrame(purchases_avg)

purchases_avg = purchases_avg.rename(columns={"Price": "Average Purchase Price"})

purchases_total = purchases_df.groupby("Gender")["Price"].sum()

purchases_tpc = purchases_total / purchasers

purchases_tpc = pd.DataFrame(purchases_tpc)

purchases_tpc.columns = ['Avg. Total Purchase per Person']

purchases_tpc.head()

purchases_total = pd. DataFrame(purchases_total)

purchases_total = purchases_total.rename(columns={"Price": "Total Purchase Value"})

purchases_1 = pd.merge(purchases_count, purchases_avg, on = "Gender")

purchases_2 = pd.merge(purchases_total, purchases_tpc, on = "Gender")

purchases = pd.merge(purchases_1, purchases_2, on = "Gender")

purchases.dtypes

purchases["Average Purchase Price"] = purchases["Average Purchase Price"].map("${:.2f}".format)

purchases["Total Purchase Value"] = purchases["Total Purchase Value"].map("${:.2f}".format)

purchases["Avg. Total Purchase per Person"] = purchases["Avg. Total Purchase per Person"].map("${:.2f}".format)

purchases.head()


# In[9]:


## Age Demographics


# In[10]:


bins = [-1, 9, 14, 19, 24, 29, 34, 39, 120]

demographics = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

purchase_data["Demographics"] = pd.cut(purchase_data["Age"], bins, labels=demographics)

age_groups = purchase_data.groupby("Demographics")["SN"].nunique()

age_groups_2 = pd.DataFrame(age_groups)

def age_percents(number, num_players):
    return (number / num_players * 100)

#https://chrisalbon.com/python/data_wrangling/pandas_make_new_columns_using_functions/

age_groups_2["Percentage of Players"] = age_percents(age_groups_2["SN"], players)

age_groups_2["Percentage of Players"] = age_groups_2["Percentage of Players"].map("{:,.2f}%".format)


age_groups_2


# In[11]:


## Purchasing Analysis (Age)


# In[12]:


pcount_age = purchase_data.groupby("Demographics")["SN"].count()

avg_age = purchase_data.groupby("Demographics")["Price"].mean()

total_age = purchase_data.groupby("Demographics")["Price"].sum()

uniq_players = purchase_data.groupby("Demographics")["SN"].nunique()

pc_age = total_age / uniq_players

summary_age = pd.DataFrame({
    "Purchase Count": pcount_age,
    "Average Purchase Price": avg_age,
    "Total Purchase Value": total_age,
    "Avg. Total Purchase Per Person": pc_age
})

summary_age["Total Purchase Value"] = summary_age["Total Purchase Value"].map("${:.2f}".format)
summary_age["Avg. Total Purchase Per Person"] = summary_age["Avg. Total Purchase Per Person"].map("${:.2f}".format)
summary_age["Average Purchase Price"] = summary_age["Average Purchase Price"].map("${:.2f}".format)

summary_age
#pcount_age = purchase_data.groupby(("Demographics")["Purchase ID"]).unique()


# In[13]:


## Top Spenders


# In[14]:


buyer_count = purchase_data.groupby("SN")["Purchase ID"].count()

buyer_average = purchase_data.groupby("SN")["Price"].mean()

buyer_total = purchase_data.groupby("SN")["Price"].sum()

summary_buyers = pd.DataFrame({
    "Purchase Count": buyer_count,
    "Average Purchase Price": buyer_average,
    "Total Purchase Value": buyer_total
})

#summary_buyers["Total Purchase Value"].astype(int)

summary_buyers_df = summary_buyers.sort_values("Total Purchase Value", ascending=False)

summary_buyers_df["Average Purchase Price"] = summary_buyers["Average Purchase Price"].map("${:.2f}".format)
summary_buyers_df["Total Purchase Value"] = summary_buyers["Total Purchase Value"].map("${:.2f}".format)

summary_buyers_df.head()


# In[15]:


## Most Popular Items


# In[35]:


#Ask TAs: How was I supposed to do this correctly? 

items = purchase_data[["Item ID", "Item Name", "Price"]]

item_counts = items.groupby("Item ID")["Item Name"].value_counts()

item_counts_df = pd.DataFrame(item_counts)

item_counts_df = item_counts_df.rename(columns={"Item Name": "Purchase Count"})

item_counts_merged = pd.merge(items, item_counts_df, on = "Item ID", how="left")


def purchase_counts(item_price, item_pcount):
    return (item_price*item_pcount)

#https://chrisalbon.com/python/data_wrangling/pandas_make_new_columns_using_functions/

item_counts_merged["Total Purchase Value"] = purchase_counts(item_counts_merged["Price"], item_counts_merged["Purchase Count"])

item_counts_sorted = item_counts_merged.sort_values(["Purchase Count", "Item ID"], ascending=False)

item_counts_sorted = item_counts_sorted.drop_duplicates("Item ID", keep = "first")

item_counts_sorted["Price"] =item_counts_sorted["Price"].map("${:.2f}".format)
item_counts_sorted["Total Purchase Value"] =item_counts_sorted["Total Purchase Value"].map("${:.2f}".format)
item_counts_sorted = item_counts_sorted.set_index("Item ID")
item_counts_sorted = item_counts_sorted[["Item Name", "Purchase Count", "Price", "Total Purchase Value"]]

item_counts_sorted


# In[37]:


## Most Profitable Items


# In[44]:


item_counts_resorted = item_counts_sorted = item_counts_merged.sort_values(["Total Purchase Value"], ascending=False)
item_counts_resorted = item_counts_resorted.drop_duplicates("Item ID", keep = "first")

item_counts_resorted["Price"] =item_counts_resorted["Price"].map("${:.2f}".format)
item_counts_resorted["Total Purchase Value"] =item_counts_resorted["Total Purchase Value"].map("${:.2f}".format)
item_counts_resorted = item_counts_resorted.set_index("Item ID")
item_counts_resorted = item_counts_resorted[["Item Name", "Purchase Count", "Price", "Total Purchase Value"]]

item_counts_resorted.head()


# In[ ]:




