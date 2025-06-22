# Databricks notebook source
# DBTITLE 1,Path Of Files


 /FileStore/tables/sales_csv.txt



 /FileStore/tables/menu_csv.txt

# COMMAND ----------

# DBTITLE 1,Sales Dataframe
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,DateType

schema=StructType([
    StructField("product_id",IntegerType(),True),
    StructField("customer_id",StringType(),True),
    StructField("order_date",DateType(),True),
    StructField("location",StringType(),True),
    StructField("source_order",StringType(),True),

])

sales_df=spark.read.format("csv").option("inferschema","true").schema(schema).load("/FileStore/tables/sales_csv.txt")
display(sales_df)

# COMMAND ----------

# DBTITLE 1,Deriving Year,  Month,  Quarter
from pyspark.sql.functions import month,year,quarter

sales_df=sales_df.withColumn("order_year",year(sales_df.order_date))
display(sales_df)

# COMMAND ----------

sales_df=sales_df.withColumn("order_month",month(sales_df.order_date))
sales_df=sales_df.withColumn("order_quarter",quarter(sales_df.order_date))
display(sales_df)

# COMMAND ----------

# DBTITLE 1,Menu Dataframe
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,DateType

schema=StructType([
    StructField("product_id",IntegerType(),True),
    StructField("product_name",StringType(),True),
    StructField("price",StringType(),True),
    

])

menu_df=spark.read.format("csv").option("inferschema","true").schema(schema).load("/FileStore/tables/menu_csv.txt")
display(menu_df)

# COMMAND ----------

# DBTITLE 1,Total Amount Spent By Each Customer
total_amount_spent = (sales_df.join(menu_df,'product_id').groupBy('customer_id').agg({'price':'sum'})
                      .orderBy('customer_id'))
display(total_amount_spent)                      

# COMMAND ----------

# DBTITLE 1,Total Amount Spent By Each Food Category
total_amount_spent = (sales_df.join(menu_df,'product_id').groupBy('product_name').agg({'price':'sum'})
                      .orderBy('product_name'))
display(total_amount_spent)       

# COMMAND ----------

# DBTITLE 1,Total Amount Of Sales In Each Month
df1 = (sales_df.join(menu_df,'product_id').groupBy('order_month').agg({'price':'sum'})
       .orderBy('order_month'))
display(df1)     

# COMMAND ----------

# DBTITLE 1,Yearly Sales
df2 = (sales_df.join(menu_df,'product_id').groupBy('order_year').agg({'price':'sum'})
       .orderBy('order_year'))
display(df2)     

# COMMAND ----------

# DBTITLE 1,Quarterly Sales
df3 = (sales_df.join(menu_df,'product_id').groupBy('order_quarter').agg({'price':'sum'})
       .orderBy('order_quarter'))
display(df3)   

# COMMAND ----------

# DBTITLE 1,How Many Times Each Product Purchased
from pyspark.sql.functions import count

most_df=(sales_df.join(menu_df,'product_id').groupBy('product_id','product_name')
         .agg(count('product_id').alias('product_count')).orderBy('product_count',ascending=0)
         .drop('product_id'))

display(most_df)

# COMMAND ----------

# DBTITLE 1,Top 5 Ordered Items
from pyspark.sql.functions import count

most_df=(sales_df.join(menu_df,'product_id').groupBy('product_id','product_name')
         .agg(count('product_id').alias('product_count')).orderBy('product_count',ascending=0)
         .drop('product_id').limit(5))

display(most_df)

# COMMAND ----------

# DBTITLE 1,Top Ordered Items
from pyspark.sql.functions import count

most_df=(sales_df.join(menu_df,'product_id').groupBy('product_id','product_name')
         .agg(count('product_id').alias('product_count')).orderBy('product_count',ascending=0)
         .drop('product_id').limit(1))

display(most_df)

# COMMAND ----------

# DBTITLE 1,Frequency Of Customer Visited To Restaurant
from pyspark.sql.functions import countDistinct

df=(sales_df.filter(sales_df.source_order=='Restaurant').groupBy('customer_id').agg(countDistinct('order_date')))

display(df)

# COMMAND ----------

# DBTITLE 1,Total Sales By Each Country
total_amount_spent = (sales_df.join(menu_df,'product_id').groupBy('location').agg({'price':'sum'}))
display(total_amount_spent)    

# COMMAND ----------

# DBTITLE 1,Total Sales By  order_source
total_amount_spent = (sales_df.join(menu_df,'product_id').groupBy('source_order').agg({'price':'sum'}))
display(total_amount_spent)    