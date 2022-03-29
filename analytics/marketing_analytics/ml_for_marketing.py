import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
# Import the function for splitting data to train and test
from sklearn.model_selection import train_test_split


telco_raw = pd.read_csv('telco.csv')

# PREPARING DATASET FOR ML
# Store customerID and Churn column names
custid = ['customerID']
target = ['Churn']

# Store categorical column names
categorical = telco_raw.nunique()[telco_raw.nunique() < 10].keys().tolist()

# Remove target from the list of categorical variables
categorical.remove(target[0])

# Store numerical column names
telco_raw['TotalCharges'] = telco_raw['TotalCharges'].replace(' ', np.nan)
numerical = [x for x in telco_raw.columns if x not in custid + target + categorical]

# DO ML
# Perform one-hot encoding to categorical variables
telco_raw = pd.get_dummies(data=telco_raw, columns=categorical, drop_first=True)

# Initialize StandardScaler instance
scaler = StandardScaler()

# Fit and transform the scaler on numerical columns
scaled_numerical = scaler.fit_transform(telco_raw[numerical])

# Build a DataFrame from scaled_numerical
scaled_numerical = pd.DataFrame(scaled_numerical, columns=numerical)


# Additional checks
def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


not_floats = telco_raw['TotalCharges'][telco_raw['TotalCharges'].apply(lambda x: not is_float(x))].unique()


# Churn:
#   Can be contractual (when customer explicitly cancel a service) and non-contractual
#       and voluntary (customer decided to stop using the product) or involuntary (renewal failed)

telcom = telco_raw
# Print the unique Churn values
print(set(telcom['Churn']))

# Calculate the ratio size of each churn group
telcom.groupby(['Churn']).size() / telcom.shape[0] * 100


# Split the data into train and test
train, test = train_test_split(telcom, test_size=0.25)

# Store column names from `telcom` excluding target variable and customer ID
cols = [col for col in telcom.columns if col not in custid + target]

# Extract training features
train_X = train[cols]

# Extract training target
train_Y = train[target]

# Extract testing features
test_X = test[cols]

# Extract testing target
test_Y = test[target]