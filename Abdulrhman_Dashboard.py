import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine
from urllib.parse import quote_plus

#------------------------------------------------------------------------------------------------

# Database Connection and cacheing the data for 10 minutes

password = quote_plus("Abdulrhman2002@")
engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/course_db")

@st.cache_data(ttl = 600)
def data_sql():
   df = pd.read_sql("""select sa.total_amount, sa.quantity , sa.sale_date , ci.city_name , co.country_name 
    , pr.product_name , pr.category , pr.price , pc.cost , cu.customer_name , cu.gender , em.employee_name , em.department 
    from sales sa
    join product pr on sa.product_id = pr.product_id
    join product_cost pc on sa.product_id = pc.product_id
    join employee em on sa.employee_id = em.employee_id
    join customer cu on sa.customer_id = cu.customer_id
    join city ci on cu.city_id = ci.city_id
    join country co on ci.country_id = co.country_id""",engine)

#Date
   df["date"] = pd.to_datetime(df["sale_date"])
   df["year"] = df["date"].dt.year
   df["month"] = df["date"].dt.month
   return df

df= data_sql()

#----------------------------------------------------------------------------------------------------------
#KPIs Calculation
TotalSales = df["total_amount"].sum()
TotalQuantity = df["quantity"].sum()
TotalCost = df["cost"].sum()
TotalProfit = TotalSales - TotalCost
ProfitMargin = (TotalProfit / TotalSales) * 100
SalesAverage = TotalSales / TotalQuantity

df["profit"] = df["total_amount"] - df["cost"]

#-------------------------------------------------------------------------------------------------------
# Page Configuration

page_configration = st.set_page_config(page_title = "Abdulrhman Store",
                                    page_icon = "📊",
                                    layout = "wide")

# ---------------------------------------------------------------------------------------------------------
#Bottoms

st.sidebar.header("Pages")
buttons = st.sidebar.pills("Select Page",["Sales","Cost","Profit"] , default="Sales")

st.sidebar.markdown("---")
#--------------------------------------------------------------------------------------------------------
#filters
st.sidebar.header("Filters")

year = sorted(df["year"].unique())
year_filter = st.sidebar.multiselect("Year Filter",year,default= year)

country = sorted(df["country_name"].unique())
country_filter = st.sidebar.multiselect("Country Filter",country,default = country)

category = sorted(df["category"].unique())
category_filter = st.sidebar.multiselect("Category Filter",category,default = category)



#filter logic
df_filtered = df[df['year'].isin(year_filter)]
df_filtered = df_filtered[df_filtered['country_name'].isin(country_filter)]
df_filtered = df_filtered[df_filtered['category'].isin(category_filter)]




st.sidebar.markdown("---")

#--------------------------------------------------------------------------------------------

#count rows after filter
st.sidebar.write(f"{len(df_filtered)} Selected Rows")
st.sidebar.write(f"Out Of {len(df)} Rows")

#--------------------------------------------------------------------------------------------

st.title("📊 Abdulrhman Store Dashboard")

st.markdown("---")

#KPIs
st.subheader("🚩KPIs")

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
      st.metric("TotalSales",f"$ {TotalSales/1000:,.1f}K")
with kpi2:
    st.metric("Total Quantity",f"{TotalQuantity}")
with kpi3:
    st.metric("Total Cost",f"$ {TotalCost/1000:,.1f}K")

kpi4, kpi5, kpi6 = st.columns(3)
with kpi4:
    st.metric("Total Profit",f"$ {TotalProfit/1000:,.1f}K")
with kpi5:
    st.metric("Profit Margin",f"{ProfitMargin:.1f}%")
with kpi6:
    st.metric("Sales Average",f"$ {SalesAverage:,.1f}")

#---------------------------------------------------------------------------------------------

    #if error in filter
if df_filtered.empty:
   st.warning("please select a valid filter combination")

#----------------------------------------------------------------------------------------------
#show and export data
st.subheader("Data Frame")
with st.expander("show Data Frame :-"):
     st.dataframe(df_filtered,use_container_width=True)

     csv = df_filtered.to_csv(index=False).encode("utf-8")
     st.download_button("Export Data",data=csv,file_name = "Exported_Data.csv",mime="text/csv")

st.markdown("---")


#sales figures prearation

top5_Product_by_sales = df_filtered.groupby("product_name")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False).head()

sales_monthly_trend = df_filtered.groupby(["year","month"])["total_amount"].sum().reset_index()

city_by_sales =  df_filtered.groupby("city_name")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False)

category_donut_sales = df_filtered.groupby("category")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False)

gender_pie_chart_sales = df_filtered.groupby("gender")["total_amount"].sum().reset_index().sort_values(by="total_amount", ascending=False)

Map_Country_by_Sales = df_filtered.groupby("country_name")["total_amount"].sum().reset_index()


#Sales Chart
st.header("📊 Charts")

if buttons == "Sales":

    st.subheader("📊 Sales Charts")
    fig1 , fig2 = st.columns(2)

    with fig1:
        chart1 = px.bar(top5_Product_by_sales,
                  x="product_name",
                 y="total_amount",
                  title="TOP 5 Product By Sales",
                 labels={"total_amount": "Total Sales","product_name":"Product"},
                 hover_name="product_name",
                 template="plotly_white",
                 text_auto=".2s",
                 height=530,
                 color_discrete_sequence=["#000DFF"])
        chart1.update_layout(title_x=0.5)
        st.plotly_chart(chart1,use_container_width=True)

    with fig2:
        chart2 = px.line(sales_monthly_trend,
                        x=(["year","month"]),
                        y="total_amount",
                        title="Monthly Sales Trend",
                        labels={"total_amount": "Total Sales","value": "Month"},
                        template="plotly_white",
                        color="year",
                        height=530,
                        markers=True,
                        )
        chart2.update_layout(title_x=0.5,
                            xaxis={"dtick" : 1})
        st.plotly_chart(chart2,use_container_width=True)


    fig3 , fig4 , fig5 = st.columns(3)
    with fig3:
                chart3 = px.bar(city_by_sales,
                          x="city_name",
                          y="total_amount",
                          title="Cities By Sales",
                          labels={"total_amount": "Total Sales","city_name":"Cities"},
                          hover_name="city_name",
                          template="plotly_white",
                          text_auto=".2s",
                          color_discrete_sequence=["#000DFF"])
                chart3.update_layout(title_x=0.5)
                st.plotly_chart(chart3,use_container_width=True)

    with fig4:
                chart4 = px.pie(category_donut_sales,
                            names="category",
                            values="total_amount",
                            title="Category By Sales Donut Chart",
                            labels={"total_amount": "Total Sale"},
                            hover_name="category",
                            template="plotly_white",
                            color_discrete_sequence=["#000DFF"],
                            hole=0.5)
                chart4.update_layout(title_x=0.1)
                st.plotly_chart(chart4,use_container_width=True)


    with fig5:
                chart5 = px.pie(gender_pie_chart_sales,
                            names="gender",
                            values="total_amount",
                            title="Gender By Sales Pie Chart",
                            labels={"total_amount": "Total Sale"},
                            hover_name="gender",
                            template="plotly_white",
                            color_discrete_sequence=["#000DFF"])
                chart5.update_layout(title_x=0.2)
                st.plotly_chart(chart5,use_container_width=True)

    st.markdown("---")
    st.header("📍🗺️ Map")
    chart6 = px.scatter_geo(Map_Country_by_Sales,
                            locations="country_name",
                            locationmode="country names",
                            size="total_amount",
                            color="total_amount",
                            hover_name="country_name",
                            title="Country Sales Map",
                            template="plotly_dark",
                            height=530)
    chart6.update_layout(title_x=0.4)
    st.plotly_chart(chart6,use_container_width=True)



#--------------------------------------------------------------------------------------------------------------------



#Cost figures prearation

top5_Product_by_cost = df_filtered.groupby("product_name")["cost"].sum().reset_index().sort_values(by="cost", ascending=False).head()

cost_monthly_trend = df_filtered.groupby(["year","month"])["cost"].sum().reset_index()

city_by_cost =  df_filtered.groupby("city_name")["cost"].sum().reset_index().sort_values(by="cost", ascending=False)

category_donut_cost = df_filtered.groupby("category")["cost"].sum().reset_index().sort_values(by="cost", ascending=False)

gender_pie_chart_cost = df_filtered.groupby("gender")["cost"].sum().reset_index().sort_values(by="cost", ascending=False)

Map_Country_by_cost = df_filtered.groupby("country_name")["cost"].sum().reset_index()


#Cost Chart
if buttons == "Cost":

    st.subheader("📊 Cost Charts")
    fig7 , fig8 = st.columns(2)

    with fig7:
        chart7 = px.bar(top5_Product_by_cost,
                  x="product_name",
                 y="cost",
                  title="TOP 5 Product By cost",
                 labels={"cost": "Total cost","product_name":"Product"},
                 template="plotly_white",
                 hover_name="product_name",
                 text_auto=".2s",
                 height=530,
                 color_discrete_sequence=["#B50000"])
        chart7.update_layout(title_x=0.5)
        st.plotly_chart(chart7,use_container_width=True)

    with fig8:
        chart8 = px.line(cost_monthly_trend,
                        x=(["year","month"]),
                        y="cost",
                        title="Monthly cost Trend",
                        labels={"cost": "Total Cost","value": "Month"},
                        template="plotly_white",
                        color="year",
                        height=530,
                        markers=True,
                        )
        chart8.update_layout(title_x=0.5,
                            xaxis={"dtick" : 1})
        st.plotly_chart(chart8,use_container_width=True)


    fig9 , fig10 , fig11 = st.columns(3)
    
    with fig9:
                chart9 = px.bar(city_by_cost,
                          x="city_name",
                          y="cost",
                          title="Cities By Cost",
                          labels={"cost": "Total Cost","city_name":"Cities"},
                          template="plotly_white",
                          hover_name="city_name",
                          text_auto=".2s",
                          color_discrete_sequence=["#B50000"])
                chart9.update_layout(title_x=0.5)
                st.plotly_chart(chart9,use_container_width=True)

    with fig10:
                chart10 = px.pie(category_donut_cost,
                            names="category",
                            values="cost",
                            title="Category By Cost Donut Chart",
                            labels={"cost": "Total Cost"},
                            hover_name="category",
                            template="plotly_white",
                            color_discrete_sequence=["#B50000"],
                            hole=0.5)
                chart10.update_layout(title_x=0.1)
                st.plotly_chart(chart10,use_container_width=True)


    with fig11:
                chart11 = px.pie(gender_pie_chart_cost,
                            names="gender",
                            values="cost",
                            title="Gender By Cost Pie Chart",
                            labels={"cost": "Total Cost"},
                            hover_name="gender",
                            template="plotly_white",
                            color_discrete_sequence=["#B50000"])
                chart11.update_layout(title_x=0.2)
                st.plotly_chart(chart11,use_container_width=True)

    st.markdown("---")
    st.header("📍🗺️ Map")
    chart12 = px.scatter_geo(Map_Country_by_cost,
                            locations="country_name",
                            locationmode="country names",
                            size="cost",
                            color="cost",
                            hover_name="country_name",
                            title="Country Cost Map",
                            template="plotly_dark",
                            height=530)
    chart12.update_layout(title_x=0.4)
    st.plotly_chart(chart12,use_container_width=True)



#-----------------------------------------------------------------------------------------------------------------

#Profit figures prearation


top5_Product_by_Profit = df_filtered.groupby("product_name")["profit"].sum().reset_index().sort_values(by="profit", ascending=False).head()

profit_monthly_trend = df_filtered.groupby(["year","month"])["profit"].sum().reset_index()

city_by_profit =  df_filtered.groupby("city_name")["profit"].sum().reset_index().sort_values(by="profit", ascending=False)

category_donut_profit = df_filtered.groupby("category")["profit"].sum().reset_index().sort_values(by="profit", ascending=False)

gender_pie_chart_profit = df_filtered.groupby("gender")["profit"].sum().reset_index().sort_values(by="profit", ascending=False)

Map_Country_by_profit = df_filtered.groupby("country_name")["profit"].sum().reset_index()


#Cost Chart
if buttons == "Profit":

    st.subheader("📊 Profit Charts")
    fig13 , fig14 = st.columns(2)

    with fig13:
        chart13 = px.bar(top5_Product_by_Profit,
                  x="product_name",
                 y="profit",
                  title="TOP 5 Product By Profit",
                 labels={"profit": "Total Profit","product_name":"Product"},
                 template="plotly_white",
                 text_auto=".2s",
                 hover_name="product_name",
                 height=530,
                 color_discrete_sequence=["#00FFAA"])
        chart13.update_layout(title_x=0.5)
        st.plotly_chart(chart13,use_container_width=True)

    with fig14:
        chart14 = px.line(profit_monthly_trend,
                        x=(["year","month"]),
                        y="profit",
                        title="Monthly Profit Trend",
                        labels={"profit": "Total Profit","value": "Month"},
                        template="plotly_white",
                        color="year",
                        height=530,
                        markers=True,
                        )
        chart14.update_layout(title_x=0.5,
                            xaxis={"dtick" : 1})
        st.plotly_chart(chart14,use_container_width=True)


    fig15 , fig16 , fig17 = st.columns(3)

    with fig15:
                chart15 = px.bar(city_by_profit,
                          x="city_name",
                          y="profit",
                          title="Cities By Profit",
                          labels={"profit": "Total Profit","city_name":"Cities"},
                          template="plotly_white",
                          text_auto=".2s",
                          hover_name="city_name",
                          color_discrete_sequence=["#00FFAA"])
                chart15.update_layout(title_x=0.5)
                st.plotly_chart(chart15,use_container_width=True)

    with fig16:
                chart16 = px.pie(category_donut_profit,
                            names="category",
                            values="profit",
                            title="Category By Profit Donut Chart",
                            labels={"profit": "Total Profit"},
                            template="plotly_white",
                            hover_name="category",
                            color_discrete_sequence=["#00FFAA"],
                            hole=0.5)
                chart16.update_layout(title_x=0.1)
                st.plotly_chart(chart16,use_container_width=True)


    with fig17:
                chart17 = px.pie(gender_pie_chart_profit,
                            names="gender",
                            values="profit",
                            title="Gender By Profit Pie Chart",
                            labels={"profit": "Total Profit"},
                            hover_name="gender",
                            template="plotly_white",
                            color_discrete_sequence=["#00FFAA"])
                chart17.update_layout(title_x=0.2)
                st.plotly_chart(chart17,use_container_width=True)

    st.markdown("---")
    st.header("📍🗺️ Map")
    chart18 = px.scatter_geo(Map_Country_by_profit,
                            locations="country_name",
                            locationmode="country names",
                            size="profit",
                            color="profit",
                            hover_name="country_name",
                            title="Country Profit Map",
                            template="plotly_dark",
                            height=530,)
    chart18.update_layout(title_x=0.4)
    st.plotly_chart(chart18,use_container_width=True)



#-------------------------------------------------------------------------------------------------------
#Create by
st.sidebar.markdown("---")
st.sidebar.subheader("Created By")
st.sidebar.write(" \u00a9 2026 (Abdulrhman Alaqrouq)")



#The End