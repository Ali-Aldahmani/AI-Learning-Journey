import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn import metrics

# Load data
df = pd.read_csv('Assets/ADNOC_Stock_historical_Data.csv')

# Create previous day features
df['Prev_Close'] = df['Close'].shift(1)
df['Prev_Open'] = df['Open'].shift(1)
df['Prev_High'] = df['High'].shift(1)
df['Prev_Low'] = df['Low'].shift(1)
df['Prev_Volume'] = df['Volume'].shift(1)

features = ['Prev_Open','Prev_High','Prev_Low','Prev_Volume','Prev_Close']

# Drop only rows that matter
df = df.dropna(subset=features + ['Close'])

X = df[features]
Y = df['Close']

# Time-based split (correct for stocks)
split = int(len(df) * 0.6)
X_train, X_test = X.iloc[:split], X.iloc[split:]
Y_train, Y_test = Y.iloc[:split], Y.iloc[split:]

# Train model
lm = LinearRegression()
lm.fit(X_train, Y_train)

# Coefficients
cdf = pd.DataFrame(lm.coef_, X.columns, columns=['Coefficient'])
print(cdf)

# Prediction
predictions = lm.predict(X_test)

# Evaluation plots
plt.scatter(Y_test, predictions)
plt.xlabel("Actual Close Price")
plt.ylabel("Predicted Close Price")
plt.title("Actual vs Predicted Close Price")
plt.show()

sns.histplot((Y_test - predictions), kde=True)
plt.title("Residuals Distribution")
plt.show()

# Metrics
rmse = np.sqrt(metrics.mean_squared_error(Y_test, predictions))
r2 = metrics.r2_score(Y_test, predictions)

print("RMSE:", rmse)
print("R2 Score:", r2)