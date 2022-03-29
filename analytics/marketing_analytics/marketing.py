import pandas as pd
from matplotlib import pyplot as plt

# Importing CSV
marketing = pd.read_csv('marketing.csv', parse_dates=['date_served', 'date_subscribed', 'date_canceled'])


# Mapping for channels
channel_dict = {"House Ads": 1, "Instagram": 2,
                "Facebook": 3, "Email": 4, "Push": 5}
marketing['channel_id'] = marketing['subscribing_channel'].map(channel_dict)


# Parsing dates
marketing['DoW'] = marketing['date_subscribed'].dt.dayofweek


def conversion_rate(dataframe, column_names):
    # Total number of converted users
    column_conv = dataframe[dataframe['converted'] == True].groupby(column_names)['user_id'].nunique()

    # Total number users
    column_total = dataframe.groupby(column_names)['user_id'].nunique()

    # Conversion rate
    conversion_rate = column_conv / column_total

    # Fill missing values with 0
    conversion_rate = conversion_rate.fillna(0)
    return conversion_rate


# Calculate conversion rate by age_group
age_group_conv = conversion_rate(marketing, ['date_served', 'age_group'])
print(age_group_conv)
print("Average CR: ", round(age_group_conv.values.mean() * 100, 2), "%")


# Reset index to turn the results into a DataFrame
# This expression is out of context (from separate exercise)
daily_conversion_rate = pd.DataFrame(age_group_conv.reset_index())
# Unstack and create a DataFrame
age_group_df = pd.DataFrame(age_group_conv.unstack())


# Plot multiple elements separately
def plotting_conv(dataframe):
    for column in dataframe:
        # Plot column by dataframe's index
        plt.plot(dataframe.index, dataframe[column])
        plt.title('Daily ' + str(column) + ' conversion rate\n',
                  size = 16)
        plt.ylabel('Conversion rate', size = 14)
        plt.xlabel('Date', size = 14)
        plt.ylim(0)
        # Show plot
        plt.show()
        plt.clf()


# Visualize conversion by age_group
# plotting_conv(age_group_df)


# Plot all elements at once
age_group_df.plot()
plt.title('Conversion rate by age group\n', size = 16)
plt.ylabel('Conversion rate', size = 14)
plt.xlabel('Age group', size = 14)
plt.legend(loc='upper right',
           labels=age_group_df.columns.values)
# plt.show()
