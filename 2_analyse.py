import streamlit as st

st.title('Analysis page')

import pandas as pd
import plotly.express as px


# prepare data
# load csv into master_df, drop unnecessary columns
master_AT = st.file_uploader('Upload master_AT here to begin analysis:')
if not master_AT:
    st.write('Analysis will start once a file is uploaded')
    st.stop()
master_df = pd.read_csv(master_AT)
master_df = master_df.drop(columns=['Account', 'Notes', 'Check #', 'Status'])
# print("master_df has {} items".format(len(master_df)))
# print(master_df.head().to_string())

# extract income transactions from master_df
income_df = master_df[master_df["Envelope"].isna()]
# print("\n\nincome_df has {} items.".format(len(income_df)))
# print(income_df.to_string())

# Make expenses_df
expenses_df = master_df[~master_df["Envelope"].isna()].copy()
# expenses_df.loc[0, 'Envelope'] = "Cat1"
expenses_df['Amount'] = expenses_df['Amount'].str.replace(',', '').astype(float) # $1,234 -> $1234
expenses_df['Amount'] = expenses_df['Amount'].multiply(-1)
# print("\n\nexpenses_df has {} items".format(len(expenses_df)))
# print(expenses_df.head().to_string())

# Split categories and subcategory in expenses_df and append as new columns
cat_subcat = expenses_df['Envelope'].str.split(":")
# print("\n\n", cat_subcat)
# print(cat_subcat.str[0])
expenses_df['Category'] = cat_subcat.str[0]
expenses_df['Subcategory'] = cat_subcat.str[1]
# print("\n\nexpenses_df with Category and Subcategory columns added:\n", expenses_df.head().to_string())

# Create cat_dict, a dictionary with Category as key, and value as list of Subcategories, or empty list if it is
# a main category.
cat_dict = {}  # links Categories to list of Subcategories,
for row in cat_subcat:
    if len(row) == 1 or row[0] == row[-1]:
        # this is a main category only
        cat_dict[row[0]] = []
    elif len(row) == 2 and not row[0] in cat_dict:
        # this is a Category:Subcategory, the Category doesn't exist in cat_dict yet, thus make new key
        cat_dict[row[0]] = [row[-1]]
    elif len(row) == 2 and row[0] in cat_dict:
        # this is a Category:Subcategory, the Category already exists in cat_dict, thus append Subcategory
        if row[-1] not in cat_dict[row[0]]:
            cat_dict[row[0]].append(row[-1])
    else:
        # print("\n\nI'm not sure what this is:", row)
        pass



# Make date_range1, a range of DateTimes representing each month in expenses_df between its earliest and latest
# month.
expenses_df['Date'] = pd.to_datetime(expenses_df['Date'], dayfirst=True)
start_month = min(expenses_df['Date']).replace(day=1)
end_month = max(expenses_df['Date']).replace(day=1)
# print("Dates between {} and {}".format(start_month, end_month))
month_range = pd.date_range(start=start_month, end=end_month, freq='MS')
# print('\nmonth_range = ', month_range)
year_range = pd.date_range(start=start_month, end=end_month, freq='YS')
# print('\nyear_range = ', year_range)


# archived code #1

# Create table that lists yearly/monthly spendings per category
cat_spendings_table = {'Year':[], 'Category':[], 'Yearly/YTD Spend':[]}
for year in year_range.year:
    for category in cat_dict:
        if cat_dict[category]: # if the category has subcategories
            cat_spendings_table['Year'].append(year)
            cat_spendings_table['Category'].append(category + " (total)")
            filtered_df2 = expenses_df[(expenses_df['Date'].dt.year == year) &
                                       (expenses_df['Category'] == category)]
            total_spend = filtered_df2['Amount'].sum()
            cat_spendings_table['Yearly/YTD Spend'].append(total_spend)

            for subcategory in cat_dict[category]:
                cat_spendings_table['Year'].append(year)
                cat_spendings_table['Category'].append(subcategory)
                filtered_df2 = expenses_df[(expenses_df['Date'].dt.year == year) &
                                           (expenses_df['Category'] == category) &
                                           (expenses_df['Subcategory'] == subcategory)]
                total_spend = filtered_df2['Amount'].sum()
                cat_spendings_table['Yearly/YTD Spend'].append(total_spend)
        else: # if the category has no subcategories
            cat_spendings_table['Year'].append(year)
            cat_spendings_table['Category'].append(category)
            filtered_df2 = expenses_df[(expenses_df['Date'].dt.year == year) &
                                       (expenses_df['Category'] == category)]
            total_spend = filtered_df2['Amount'].sum()
            cat_spendings_table['Yearly/YTD Spend'].append(total_spend)

        cat_spendings_table['Year'].append('')
        cat_spendings_table['Category'].append('')
        cat_spendings_table['Yearly/YTD Spend'].append('')

latest_year = year_range[-1].year  # Get the latest year
latest_year_months = len([date for date in month_range if date.year == latest_year])  # Count months in the latest year
# print(f'Assuming {latest_year_months} months have passed in current year {latest_year}')
# calculate monthly amounts
cat_spendings_table['Monthly Spend'] = []
for i in range(len(cat_spendings_table['Yearly/YTD Spend'])):
    year_amount = cat_spendings_table['Yearly/YTD Spend'][i]
    if cat_spendings_table['Year'] == latest_year: # calculate # of months passed if latest year
        months = latest_year_months
    else:
        months = 12
    if year_amount: # if not an empty line
        cat_spendings_table['Monthly Spend'].append(year_amount / months)
    else:
        cat_spendings_table['Monthly Spend'].append('')
cat_spendings_table_df = pd.DataFrame(cat_spendings_table)
cat_spendings_table_df = cat_spendings_table_df.round(2)
# print('cat_spendings_table_df =\n', cat_spendings_table_df)

st.write('{} transactions found between {} to {}'.format(len(expenses_df),
                                                           min(expenses_df['Date']).strftime('%d-%m-%y'),
                                                           max(expenses_df['Date']).strftime('%d-%m-%y')))

# Streamlit layout all below!

st.title('Personal expenses tracker')

# TODO: add stacked line chart showing total category expenses each year
# total expenses this year

st.header('Year analysis')

# year selector for category
selected_year = st.selectbox("Select a year to analyse", year_range.year)

# category graph, view/no view subcategories
view_subcat = st.checkbox('View subcategories?')
filtered_df1 = expenses_df[(expenses_df['Date'].dt.year == selected_year)]
# Aggregate total spending per category for the filtered data
if not view_subcat:
    cat_spending = filtered_df1.groupby('Category')['Amount'].sum().reset_index()
    cat_spending
    cat_spending_year_fig = px.pie(cat_spending, values='Amount', names='Category')
else:
    cat_spending = filtered_df1.groupby('Envelope')['Amount'].sum().reset_index()
    cat_spending['Category'] = [i.split(':')[0] for i in cat_spending['Envelope']]
    cat_spending['Subcategory'] = [i.split(':')[-1] for i in cat_spending['Envelope']]
    cat_spending
    cat_spending_year_fig = px.sunburst(cat_spending, path=['Category', 'Subcategory'], values='Amount')
    # TODO: add percentage label

# Create the pie chart
st.plotly_chart(cat_spending_year_fig)

st.write('Monthly/yearly spendings of expenses = cat_spendings_table_df')
st.dataframe(cat_spendings_table_df)

st.write('expenses_df')
st.dataframe(expenses_df)
# filter expenses_df by category

st.header('Month analysis (current YTD?)')
# filtered_df1
filtered_df1['Month'] = filtered_df1['Date'].dt.month
# filtered_df1
cat_spending_month = filtered_df1.groupby(['Envelope', 'Month'])['Amount'].sum().reset_index()
# cat_spending_month
cat_spendings_month_fig = px.area(cat_spending_month, x='Month', y='Amount', color='Envelope')
st.plotly_chart(cat_spendings_month_fig)

# TODO: expenses_df filtered by user selection for Envelope and month

print('\n script rerun')
