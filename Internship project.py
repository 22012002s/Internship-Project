#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as pt
import seaborn as sns


# # Data exploration and Cleaning

# In[2]:


p=pd.read_csv(r"C:\Users\shiva\Downloads\purchase_data.csv")
u=pd.read_csv(r"C:\Users\shiva\Downloads\user_interactions.csv")
w=pd.read_csv(r"C:\Users\shiva\Downloads\website_performance.csv")


# In[3]:


p.columns


# In[4]:


p.head()


# In[5]:


p.info()


# In[6]:


p.Purchase_Time=pd.to_datetime(p.Purchase_Time)


# In[7]:


p.shape


# In[8]:


p.isnull().any()


# In[9]:


u.head()


# In[10]:


u.info()


# In[11]:


u.isnull().any()


# In[12]:


u.columns


# In[13]:


u.info()


# In[14]:


u


# In[15]:


w.head()


# In[16]:


w.info()


# In[17]:


w.isnull().any()


# # User behaviour Analysis

# In[18]:


most_visited_page=u.Page_Viewed.value_counts()


# In[19]:


most_visited_page


# In[20]:


average_Time_perpage=u.groupby(by="Page_Viewed").Time_Spent_Seconds.mean()


# In[21]:


average_Time_perpage


# In[22]:


a=average_Time_perpage.reset_index()


# In[23]:


a


# # Data visualization

# In[24]:


pt.figure(figsize=(8,4))
pt.bar(x=a.Page_Viewed,height=a.Time_Spent_Seconds,color="r")
pt.xlabel("Pages Category")
pt.ylabel("Time per sec")
pt.title("Pages vs Time per sec")
pt.xticks(color="c")
pt.yticks(color="c")
pt.show()


# # Click through rate

# In[25]:


average_Time_perpage


# In[26]:


click_through_rate= average_Time_perpage/average_Time_perpage.sum()


# In[27]:


click_through_rate


# # Purchase Analysis

# In[28]:


Total_purchase=p.shape[0]
Total_interaction=u.shape[0]


# In[29]:


conversion_rate=(Total_purchase/Total_interaction)*100
print(f"Overall Conversion Rate: {conversion_rate:.2f}%")


# # Top selling products and category

# In[30]:


top_selling_products=p.Product_ID.value_counts().nlargest(10)
top_selling_products


# In[31]:


#we dont have product category column so i am assuming a product category is contained in product id.


# In[32]:


p["Product_Category"]=p.Product_ID.str[:3]


# In[33]:


top_selling_category=p.Product_Category.value_counts().nlargest(5)


# In[34]:


top_selling_category


# #  Relationship between Interactions and Likelihood of Purchase

# In[35]:


merge_pu= u.merge(p,on="User_ID",how="left")


# In[36]:


merge_pu.head()


# In[37]:


total_interaction_per_user=u.groupby(by="User_ID").size().reset_index(name="Total interaction")


# In[38]:


total_interaction_per_user.sort_values(by="Total interaction",ascending=False)


# In[39]:


Total_purchase_per_user = p.groupby(by="User_ID").size().reset_index(name="Total Purchase")


# In[40]:


Total_purchase_per_user.sort_values(by="Total Purchase",ascending=False)


# In[41]:


#Merge the total interactions and total purchases per user
merge_column=total_interaction_per_user.merge(Total_purchase_per_user,on="User_ID",how="left")
merge_column["Total Purchase"].fillna(0,inplace=True)
merge_column["Conversion rate"]=(merge_column["Total Purchase"]/merge_column["Total interaction"])*100
merge_column
print(merge_column.head())



# # Data Visualization

# In[42]:


x=merge_column["Total interaction"]
y=merge_column["Total Purchase"]


# In[43]:


pt.scatter(x,y,color="b")
pt.title("Relationship between interaction and Purchase")
pt.xlabel("Total interaction")
pt.ylabel("Total Purchase")
pt.show()


# # Cohort Analysis

# In[44]:


user=pd.read_csv(r"C:\Users\shiva\Downloads\user_interactions.csv")
## Convert the 'Time_spent' to a datetime format
user["Time_Spent_Seconds"]=pd.to_datetime(user.Time_Spent_Seconds)
## Find the first interaction date for each user
first_interaction=user.groupby(by="User_ID")["Time_Spent_Seconds"].min().reset_index()
first_interaction.rename(columns={"Time_Spent_Seconds":"First interaction"},inplace=True)
# Merge the first interaction date back to the u (u stand for user interaction data variable)
user=user.merge(first_interaction,on="User_ID",how="left")
user["Time Period"]=(user["Time_Spent_Seconds"]-user["First interaction"])


# In[45]:


user.columns


# In[46]:


cohort_metric=user.groupby(["First interaction" ,"Time Period"])["Time_Spent_Seconds"].mean().reset_index()
cohort_metric


# In[47]:


cohort_pivot = cohort_metric.pivot_table(index="First interaction", columns="Time Period", values="Time_Spent_Seconds")
pt.figure(figsize=(10, 6))
sns.lineplot(data=cohort_metric, x='Time Period', y='Time_Spent_Seconds', hue='First interaction')
pt.title('Cohort Analysis - Average Time Spent (seconds)')
pt.xlabel('Time Period (Months)')
pt.ylabel('Average Time Spent (seconds)')
pt.legend(title='First interaction', loc='upper right', bbox_to_anchor=(1.35, 1))
pt.show()


# # Website Performance Optimization

# In[49]:


website=pd.read_csv(r"C:\Users\shiva\Downloads\website_performance.csv")


# In[50]:


# Calculate the overall bounce rate and conversion rate:
overall_bounce_rate=website["Bounce_Rate"].mean()
overall_bounce_rate=website["Conversion_Rate"].mean()


# In[51]:


pt.figure(figsize=(10, 6))
sns.barplot(data=website, x='Month', y='Conversion_Rate')
pt.title('Conversion Rate Over Time')
pt.xlabel('Month')
pt.ylabel('Conversion Rate')
pt.xticks(rotation=45)
pt.show()


# In[ ]:




