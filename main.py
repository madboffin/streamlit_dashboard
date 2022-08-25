import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:", 
    layout="wide"
    )

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io='./supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000
        )

    # add hour column to dataframe
    df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
df = get_data_from_excel()

######### SIDEBAR ###############
st.sidebar.header("Please filter here:")

city = st.sidebar.multiselect(
    "Select city",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select customer type",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

################# header ######################
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KIP-s
total_sales = int(df_selection.Total.sum())
average_rating = round(df_selection.Rating.mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sale_by_transaction = round(df_selection.Total.mean(),2)

# setting up the page layout
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average sales per transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")
st.dataframe(df_selection)

#########################  ############################
# sale by prduct line [bar chart]
sales_by_product_line = (
    df_selection.groupby(by="Product line").sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by product line</b",
    template =  "plotly_white"
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis={'showgrid':False}
)

######### SALES BY HOUR [chart bar] #########
sales_by_hour = df_selection.groupby(by=["Hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title = "<b>Sales by hour</b>",
    template="plotly"
)
fig_hourly_sales.update_layout(
    xaxis={'tickmode':'linear'},
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis={'showgrid':False}
)

left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_product_sales)
right_col.plotly_chart(fig_hourly_sales)

#### hide streamlit default style ####
# hides some elements in the dashboard that come by default
hide_st_style = """
    <style>
    # MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    # header {visibility: hidden;}
    </style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)