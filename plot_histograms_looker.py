#need to create an API key to authenticate to the instance
!pip install looker_sdk
import looker_sdk
import os
import json
import io
import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

#Initialize connectivity variables:
os.environ['LOOKERSDK_BASE_URL'] = 'https://abcdefg.cloud.looker.com'
os.environ['LOOKERSDK_CLIENT_ID'] = 'xxxxxx'
os.environ['LOOKERSDK_CLIENT_SECRET'] = 'yyyyyy'

#Initialize the SDK and get data
sdk = looker_sdk.init40()

# Query to extract data from Looker
explore = sdk.lookml_model_explore("model_name", "view_name")
dimensions = explore.fields.dimensions
measures = explore.fields.measures
all_fields = dimensions + measures
query = {
  "model": "model_name",  # Replace with your LookML model name
  "view": "view_name",    # Replace with your LookML view name
  "fields": [all_field.name for all_field in all_fields]   # Replace with the fields you want to select
}
result_format = "json"

# Run the query and get the JSON result
result = sdk.run_inline_query(result_format, query)
df_result = pd.read_json(io.StringIO(result))

# Convert the JSON result to a Pandas DataFrame
df = pd.read_json(io.StringIO(result))

print("DataFrame size:", df.shape)
df.describe(include = 'all').T

numeric_vars = df.select_dtypes(include=np.number).columns.tolist()
print("Numeric variables:")
print(numeric_vars)
#in case there are string type columns
X = df.drop('view_name.column', axis=1)
y = df['view_name.column']

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)

print("Dimensions of X_train:", X_train.shape)
print("Dimensions of X_val:", X_val.shape)
print("Dimensions of X_test:", X_test.shape)
print("Dimensions of y_train:", y_train.shape)
print("Dimensions of y_val:", y_val.shape)
print("Dimensions of y_test:", y_test.shape)

encoder = LabelEncoder()

y_train = encoder.fit_transform(y_train)

y_val = encoder.transform(y_val)
y_test = encoder.transform(y_test)

class_counts = pd.Series(y_train).value_counts(normalize=True)

print(class_counts)

numeric_vars = X_train.select_dtypes(include=np.number).columns.tolist()
numeric_cols = X_train[numeric_vars]

# Create histograms for each numeric variable
fig, axes = plt.subplots(nrows=len(numeric_cols.columns), ncols=1, figsize=(10, 5 * len(numeric_cols.columns)))
for col, ax in zip(numeric_cols.columns, axes.flatten()):
    if not np.all(np.isnan(X_train[col])): # Check if all values are NaN
        ax.hist(X_train[col], bins=30, color='blue', alpha=0.7)
        ax.set_title(f'Histogram for column: {col}')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frecuency')

plt.tight_layout()
plt.show()

# a) Relationship between "columnA" y "valueX"
plt.figure(figsize=(10, 6))
sns.boxplot(x='view_name.columnA', y='view_name.valueX', data=df)
plt.title('Relationship between columnA and valueX')
plt.xlabel('columnA')
plt.ylabel('valueX')
plt.show()

# b) Relationship between "columnB" y "valueX"
plt.figure(figsize=(10, 6))
sns.countplot(x='view_name.columnB', hue='view_name.valueX', data=df)
plt.title('Relationship between columnB and valueX')
plt.xlabel('columnB')
plt.ylabel('valueX')
plt.xticks(rotation=45)
plt.show()

# c) Relationship between "columnC" y "valueX"
plt.figure(figsize=(10, 6))
sns.countplot(x='view_name.columnC', hue='view_name.valueX', data=df)
plt.title('Relationship between columnC and valueX')
plt.show()

