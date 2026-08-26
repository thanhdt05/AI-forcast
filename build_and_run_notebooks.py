import nbformat
from nbformat.v4 import new_notebook, new_code_cell
from nbclient import NotebookClient

def build_diabetes_notebook():
    nb = new_notebook()
    cells = [
        # Cell 1: Load Data & info (p. 271)
        """import numpy as np
import pandas as pd

df = pd.read_csv('diabetes.csv')
df.info()""",

        # Cell 2: Check for nulls (p. 271)
        """#---check for null values---
print("Nulls")
print("=====")
print(df.isnull().sum())""",

        # Cell 3: Check for 0s (p. 272)
        """#---check for 0s---
print("0s")
print("==")
print(df.eq(0).sum())""",

        # Cell 4: Replace 0 with NaN (p. 272)
        """df[['Glucose','BloodPressure','SkinThickness',
    'Insulin','BMI','DiabetesPedigreeFunction','Age']] = \\
    df[['Glucose','BloodPressure','SkinThickness',
    'Insulin','BMI','DiabetesPedigreeFunction','Age']].replace(0, np.nan)""",

        # Cell 5: Replace NaN with mean (p. 272)
        """df.fillna(df.mean(), inplace = True) # replace NaN with the mean""",

        # Cell 6: Verify 0s (p. 272-273)
        """print(df.eq(0).sum())""",

        # Cell 7: Examine correlation (p. 273)
        """corr = df.corr()
print(corr)""",

        # Cell 8: Matplotlib matshow correlation (p. 274-275)
        """%matplotlib inline
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 10))
cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0, len(df.columns), 1)
ax.set_xticks(ticks)
ax.set_xticklabels(df.columns, rotation=90)
ax.set_yticks(ticks)
ax.set_yticklabels(df.columns)

#---print the correlation factor---
for i in range(df.shape[1]):
    for j in range(df.shape[1]):
        text = ax.text(j, i, round(corr.iloc[i, j], 2),
                       ha="center", va="center", color="w")
plt.show()""",

        # Cell 9: Seaborn heatmap (p. 275)
        """import seaborn as sns

sns.heatmap(df.corr(), annot=True)

#---get a reference to the current figure and set its size---
fig = plt.gcf()
fig.set_size_inches(8, 8)
plt.show()""",

        # Cell 10: Top four features (p. 275)
        """#---get the top four features that has the highest correlation---
print(df.corr().nlargest(4, 'Outcome').index)""",

        # Cell 11: Top four correlation values (p. 276)
        """#---print the top 4 correlation values---
print(df.corr().nlargest(4, 'Outcome').values[:, 8])""",

        # Cell 12: Logistic Regression (p. 277)
        """from sklearn import linear_model
from sklearn.model_selection import cross_val_score

#---features---
X = df[['Glucose', 'BMI', 'Age']]

#---label---
y = df.iloc[:, 8]

log_regress = linear_model.LogisticRegression()
log_regress_score = cross_val_score(log_regress, X, y, cv=10, scoring='accuracy').mean()
print(log_regress_score)""",

        # Cell 13: Append score to result (p. 277)
        """result = []
result.append(log_regress_score)""",

        # Cell 14: K-Nearest Neighbors init (p. 277)
        """from sklearn.neighbors import KNeighborsClassifier

#---empty list that will hold cv (cross-validates) scores---
cv_scores = []""",

        # Cell 15: KNN Cross-validation & find optimal k (p. 278)
        """#---number of folds---
folds = 10

#---creating odd list of K for KNN---
ks = list(range(1, int(len(X) * ((folds - 1) / folds)), 2))

#---perform k-fold cross validation---
for k in ks:
    knn = KNeighborsClassifier(n_neighbors=k)
    score = cross_val_score(knn, X, y, cv=folds, scoring='accuracy').mean()
    cv_scores.append(score)

#---get the maximum score---
knn_score = max(cv_scores)

#---find the optimal k that gives the highest score---
optimal_k = ks[cv_scores.index(knn_score)]
print(f"The optimal number of neighbors is {optimal_k}")
print(knn_score)
result.append(knn_score)""",

        # Cell 16: SVM Linear (p. 278)
        """from sklearn import svm

linear_svm = svm.SVC(kernel='linear')
linear_svm_score = cross_val_score(linear_svm, X, y, cv=10, scoring='accuracy').mean()
print(linear_svm_score)
result.append(linear_svm_score)""",

        # Cell 17: SVM RBF (p. 278)
        """rbf = svm.SVC(kernel='rbf')
rbf_score = cross_val_score(rbf, X, y, cv=10, scoring='accuracy').mean()
print(rbf_score)
result.append(rbf_score)""",

        # Cell 18: Selecting the Best Performing Algorithm (p. 279)
        """algorithms = ["Logistic Regression", "K Nearest Neighbors", "SVM Linear Kernel", "SVM RBF Kernel"]
cv_mean = pd.DataFrame(result, index=algorithms)
cv_mean.columns = ["Accuracy"]
cv_mean.sort_values(by="Accuracy", ascending=False)""",

        # Cell 19: Train model with optimal k (p. 279)
        """knn = KNeighborsClassifier(n_neighbors=optimal_k)
knn.fit(X, y)""",

        # Cell 20: Save model to disk (p. 279)
        """import pickle

#---save the model to disk---
filename = 'diabetes.sav'

#---write to the file using write and binary mode---
pickle.dump(knn, open(filename, 'wb'))""",

        # Cell 21: Load model from disk (p. 279)
        """#---load the model from disk---
loaded_model = pickle.load(open(filename, 'rb'))""",

        # Cell 22: Sample prediction (p. 280)
        """Glucose = 65
BMI = 70
Age = 50

prediction = loaded_model.predict([[Glucose, BMI, Age]])
print(prediction)
if (prediction[0] == 0):
    print("Non-diabetic")
else:
    print("Diabetic")""",

        # Cell 23: Prediction probability & confidence (p. 280)
        """proba = loaded_model.predict_proba([[Glucose, BMI, Age]])
print(proba)
print("Confidence: " + str(round(np.amax(proba[0]) * 100, 2)) + "%")""",

        # Cell 24: Prediction helper / Client function test (p. 283)
        """def predict_diabetes(BMI, Age, Glucose):
    prediction = loaded_model.predict([[Glucose, BMI, Age]])[0]
    proba = loaded_model.predict_proba([[Glucose, BMI, Age]])[0]
    confidence = str(round(np.amax(proba) * 100, 2))
    return {"prediction": int(prediction), "confidence": confidence}

predictions = predict_diabetes(30, 40, 100)
print("Diabetic" if predictions["prediction"] == 1 else "Not Diabetic")
print("Confidence: " + predictions["confidence"] + "%")""",

        # Cell 25: Prediction test with second example (p. 284)
        """BMI = 55
Age = 29
Glucose = 120

predictions = predict_diabetes(BMI, Age, Glucose)
print("Diabetic" if predictions["prediction"] == 1 else "Not Diabetic")
print("Confidence: " + predictions["confidence"] + "%")"""
    ]

    for code in cells:
        nb.cells.append(new_code_cell(code))

    print("Executing chapter12_diabetes_demo.ipynb...")
    client = NotebookClient(nb, timeout=600, kernel_name='python3')
    client.execute()

    with open('chapter12_diabetes_demo.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Successfully built and executed chapter12_diabetes_demo.ipynb")


def build_house_price_notebook():
    nb = new_notebook()
    cells = [
        # Cell 1: Imports & System Diagram
        """%matplotlib inline
import os
import re
import math
import pickle
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error
)

warnings.filterwarnings('ignore')
os.makedirs('figures', exist_ok=True)
os.makedirs('results', exist_ok=True)

# System Architecture Diagram
fig, ax = plt.subplots(figsize=(12, 2.6))
ax.axis('off')
labels = [
    'User / Environment',
    'House input',
    'Feature representation',
    'Preprocessing',
    'Regression model',
    'Predicted price'
]
xs = [0.07, 0.24, 0.41, 0.58, 0.75, 0.92]
for x, label in zip(xs, labels):
    ax.text(x, 0.5, label, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.45', fc='white', ec='black'))
for x1, x2 in zip(xs[:-1], xs[1:]):
    ax.annotate('', xy=(x2-0.07, 0.5), xytext=(x1+0.07, 0.5),
                arrowprops=dict(arrowstyle='->'))
plt.tight_layout()
plt.savefig('figures/05_system_diagram.png', dpi=160, bbox_inches='tight')
plt.show()""",

        # Cell 2: Loading Data & info() (Chapter 12 page 271)
        """#---load data---
df = pd.read_csv('gia_nha.csv')
df.info()""",

        # Cell 3: First 5 rows
        """df.head()""",

        # Cell 4: Summary table of columns, types, missing, unique
        """summary = pd.DataFrame({
    'Type': df.dtypes.astype(str),
    'Missing': df.isnull().sum(),
    'Unique': df.nunique(dropna=True)
})
summary""",

        # Cell 5: Summary of Target (Price)
        """print('Target (Price) summary statistics:')
print(df['Price'].describe())""",

        # Cell 6: Check for nulls (Chapter 12 page 271)
        """#---check for null values---
print("Nulls")
print("=====")
print(df.isnull().sum())""",

        # Cell 7: Check for 0s (Chapter 12 page 272)
        """#---check for 0s---
print("0s")
print("==")
print(df.select_dtypes(include=np.number).eq(0).sum())""",

        # Cell 8: Data Cleansing - Filter positive Price and Area
        """# Price and Area are essential and must be positive
df = df[(df['Price'] > 0) & (df['Area'] > 0)].copy()
df.reset_index(drop=True, inplace=True)
print('Dataset shape after checking positive Price and Area:', df.shape)""",

        # Cell 9: Feature Representation & Location Extraction
        """#---extract location features from Address---
def extract_location(address):
    parts = [re.sub(r'[.\s]+$', '', p.strip()) for p in str(address).split(',')]
    province = parts[-1] if len(parts) >= 1 and parts[-1] and parts[-1].lower() != 'nan' else 'Unknown'
    district = parts[-2] if len(parts) >= 2 and parts[-2] else 'Unknown'
    return pd.Series([province, district])

df[['Province', 'District']] = df['Address'].apply(extract_location)

numeric_cols = ['Area', 'Frontage', 'Access Road', 'Floors', 'Bedrooms', 'Bathrooms']
categorical_cols = [
    'House direction', 'Balcony direction', 'Legal status',
    'Furniture state', 'Province', 'District'
]
feature_cols = numeric_cols + categorical_cols

X = df[feature_cols].copy()
y = df['Price'].copy()

feature_table = pd.DataFrame([
    ['Area', 'Numerical', 'Real value', 'House area (m²)'],
    ['Frontage', 'Numerical', 'Real value', 'Frontage width (m)'],
    ['Access Road', 'Numerical', 'Real value', 'Road/access width (m)'],
    ['Floors', 'Numerical', 'Real value', 'Number of floors'],
    ['Bedrooms', 'Numerical', 'Real value', 'Number of bedrooms'],
    ['Bathrooms', 'Numerical', 'Real value', 'Number of bathrooms'],
    ['House direction', 'Categorical', 'Ordinal encoded', 'House direction'],
    ['Balcony direction', 'Categorical', 'Ordinal encoded', 'Balcony direction'],
    ['Legal status', 'Categorical', 'Ordinal encoded', 'Legal status'],
    ['Furniture state', 'Categorical', 'Ordinal encoded', 'Furniture state'],
    ['Province', 'Categorical', 'Ordinal encoded', 'Province/city extracted from Address'],
    ['District', 'Categorical', 'Ordinal encoded', 'District extracted from Address'],
], columns=['Feature', 'Type', 'Representation', 'Meaning'])
feature_table""",

        # Cell 10: Price Distribution
        """plt.figure(figsize=(8, 4.5))
plt.hist(df['Price'].dropna(), bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of House Price')
plt.xlabel('Price (billion VND)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('figures/01_price_distribution.png', dpi=160)
plt.show()""",

        # Cell 11: Area Distribution
        """plt.figure(figsize=(8, 4.5))
plt.hist(df['Area'].dropna(), bins=30, color='salmon', edgecolor='black')
plt.title('Distribution of House Area')
plt.xlabel('Area (m²)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('figures/02_area_distribution.png', dpi=160)
plt.show()""",

        # Cell 12: Bedrooms Distribution
        """plt.figure(figsize=(8, 4.5))
plt.hist(df['Bedrooms'].dropna(), bins=20, color='lightgreen', edgecolor='black')
plt.title('Distribution of Bedrooms')
plt.xlabel('Number of bedrooms')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('figures/03_bedrooms_distribution.png', dpi=160)
plt.show()""",

        # Cell 13: Correlation between numerical features (Chapter 12 page 273)
        """#---examining the correlation between features---
correlation_cols = numeric_cols + ['Price']
corr = df[correlation_cols].corr()
print(corr)""",

        # Cell 14: Matplotlib matshow correlation (Chapter 12 page 274)
        """fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.matshow(corr, vmin=-1, vmax=1, cmap='coolwarm')
fig.colorbar(cax)
ticks = np.arange(len(correlation_cols))
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(correlation_cols, rotation=90)
ax.set_yticklabels(correlation_cols)
for i in range(len(correlation_cols)):
    for j in range(len(correlation_cols)):
        ax.text(j, i, round(corr.iloc[i, j], 2), ha='center', va='center', fontsize=8)
plt.title('Correlation Matrix of Numerical Features', pad=20)
plt.tight_layout()
plt.savefig('figures/04_correlation_matrix.png', dpi=160, bbox_inches='tight')
plt.show()""",

        # Cell 15: Seaborn heatmap (Chapter 12 page 275)
        """plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Seaborn Heatmap of Correlations')
plt.tight_layout()
plt.show()""",

        # Cell 16: Top correlated features with Price (Chapter 12 page 275-276)
        """#---get top features correlated with Price---
print(corr.nlargest(len(correlation_cols), 'Price')['Price'])""",

        # Cell 17: Train/Validation/Test Split
        """X_train_all, X_test, y_train_all, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_all, y_train_all, test_size=0.20, random_state=42
)

print('Training rows:', len(X_train))
print('Validation rows:', len(X_val))
print('Final test rows:', len(X_test))""",

        # Cell 18: Preprocessing pipeline setup and fitting
        """def make_preprocessor(cat_cols):
    numerical = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
    ])
    return ColumnTransformer([
        ('num', numerical, numeric_cols),
        ('cat', categorical, cat_cols)
    ])

preprocessor = make_preprocessor(categorical_cols)

# Fit preprocessing on TRAINING data only
X_train_ready = preprocessor.fit_transform(X_train)
X_val_ready = preprocessor.transform(X_val)
X_test_ready = preprocessor.transform(X_test)

print('Encoded training shape:', X_train_ready.shape)""",

        # Cell 19: Evaluation Function
        """def evaluate(y_true, prediction):
    mse = mean_squared_error(y_true, prediction)
    return {
        'MAE': mean_absolute_error(y_true, prediction),
        'MSE': mse,
        'RMSE': math.sqrt(mse),
        'R2': r2_score(y_true, prediction),
        'MAPE (%)': mean_absolute_percentage_error(y_true, prediction) * 100
    }""",

        # Cell 20: Baseline Reference Model
        """baseline = DummyRegressor(strategy='mean')
baseline.fit(X_train_ready, y_train)
baseline_prediction = baseline.predict(X_val_ready)
baseline_metrics = evaluate(y_val, baseline_prediction)
print('Baseline Metrics (Mean Predictor):')
print(baseline_metrics)""",

        # Cell 21: Model Comparison Definitions (Chapter 12 page 277-278)
        """models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=10.0, solver='lsqr'),
    'Decision Tree': DecisionTreeRegressor(
        max_depth=15, min_samples_leaf=3, random_state=42
    ),
    'Random Forest': RandomForestRegressor(
        n_estimators=50, max_depth=18, min_samples_leaf=2,
        random_state=42, n_jobs=-1
    ),
    'Extra Trees': ExtraTreesRegressor(
        n_estimators=50, max_depth=18, min_samples_leaf=2,
        random_state=42, n_jobs=-1
    )
}""",

        # Cell 22: Training 5 candidate models and ranking (Chapter 12 page 279)
        """rows = [['Baseline Mean', *baseline_metrics.values()]]
for name, model in models.items():
    print('Training:', name)
    model.fit(X_train_ready, y_train)
    prediction = model.predict(X_val_ready)
    metrics = evaluate(y_val, prediction)
    rows.append([name, *metrics.values()])
    print(metrics)

comparison = pd.DataFrame(
    rows,
    columns=['Model', 'MAE', 'MSE', 'RMSE', 'R2', 'MAPE (%)']
)
comparison = comparison.sort_values('R2', ascending=False).reset_index(drop=True)
comparison.to_csv('results/model_comparison.csv', index=False)
comparison""",

        # Cell 23: Plotting Model Comparison (Chapter 12 page 279)
        """plot_df = comparison[comparison['Model'] != 'Baseline Mean'].sort_values('R2')
plt.figure(figsize=(8, 4.5))
plt.barh(plot_df['Model'], plot_df['R2'], color='royalblue')
plt.xlabel('Validation R²')
plt.title('Model Comparison (Validation R²)')
plt.tight_layout()
plt.savefig('figures/06_model_comparison.png', dpi=160)
plt.show()""",

        # Cell 24: Selecting the Best Performing Model (Chapter 12 page 279)
        """best_row = comparison[comparison['Model'] != 'Baseline Mean'].iloc[0]
best_model_name = best_row['Model']
print('Best validation model:', best_model_name)
print(best_row)""",

        # Cell 25: Experiment 2 - Hyperparameter Tuning (n_estimators)
        """hyper_rows = []
for n in [10, 30, 50]:
    rf = RandomForestRegressor(
        n_estimators=n, max_depth=18, min_samples_leaf=2,
        random_state=42, n_jobs=-1
    )
    rf.fit(X_train_ready, y_train)
    pred = rf.predict(X_val_ready)
    m = evaluate(y_val, pred)
    hyper_rows.append([n, *m.values()])

hyper_df = pd.DataFrame(
    hyper_rows,
    columns=['n_estimators', 'MAE', 'MSE', 'RMSE', 'R2', 'MAPE (%)']
)
hyper_df.to_csv('results/hyperparameter_experiment.csv', index=False)
hyper_df""",

        # Cell 26: Hyperparameter Plot
        """plt.figure(figsize=(7, 4.5))
plt.plot(hyper_df['n_estimators'], hyper_df['R2'], marker='o', color='darkorange', linewidth=2)
plt.xlabel('n_estimators')
plt.ylabel('Validation R²')
plt.title('Random Forest Hyperparameter Experiment')
plt.grid(True)
plt.tight_layout()
plt.savefig('figures/07_hyperparameter.png', dpi=160)
plt.show()""",

        # Cell 27: Experiment 3 - Representation Investigation (Location Features)
        """base_cat_cols = ['House direction', 'Balcony direction', 'Legal status', 'Furniture state']
representation_rows = []

for label, cat_cols in [
    ('Without Province + District', base_cat_cols),
    ('With Province + District', categorical_cols)
]:
    cols = numeric_cols + cat_cols
    pre = make_preprocessor(cat_cols)
    train_ready = pre.fit_transform(X_train[cols])
    val_ready = pre.transform(X_val[cols])

    rf = RandomForestRegressor(
        n_estimators=50, max_depth=18, min_samples_leaf=2,
        random_state=42, n_jobs=-1
    )
    rf.fit(train_ready, y_train)
    pred = rf.predict(val_ready)
    m = evaluate(y_val, pred)
    representation_rows.append([label, *m.values()])

representation_df = pd.DataFrame(
    representation_rows,
    columns=['Representation', 'MAE', 'MSE', 'RMSE', 'R2', 'MAPE (%)']
)
representation_df.to_csv('results/representation_experiment.csv', index=False)
representation_df""",

        # Cell 28: Representation Plot
        """plt.figure(figsize=(8, 4.5))
plt.bar(representation_df['Representation'], representation_df['R2'], color=['teal', 'coral'])
plt.ylabel('Validation R²')
plt.title('Representation Experiment (Impact of Location Features)')
plt.tight_layout()
plt.savefig('figures/08_representation.png', dpi=160)
plt.show()""",

        # Cell 29: Training Final Model on All Training Data (Chapter 12 page 279)
        """#---train final model using full training set---
final_preprocessor = make_preprocessor(categorical_cols)
X_train_all_ready = final_preprocessor.fit_transform(X_train_all)
X_test_final_ready = final_preprocessor.transform(X_test)

final_model = RandomForestRegressor(
    n_estimators=50, max_depth=18, min_samples_leaf=2,
    random_state=42, n_jobs=-1
)
final_model.fit(X_train_all_ready, y_train_all)""",

        # Cell 30: Evaluating Final Model on Unseen Test Set
        """final_prediction = final_model.predict(X_test_final_ready)
final_metrics = evaluate(y_test, final_prediction)
print('Final unseen test metrics:')
print(final_metrics)
pd.DataFrame([final_metrics]).to_csv('results/final_test_metrics.csv', index=False)""",

        # Cell 31: Saving the Final Model to Disk (Chapter 12 page 279)
        """#---save the model to disk---
bundle = {
    'preprocessor': final_preprocessor,
    'model': final_model,
    'feature_cols': feature_cols,
    'numeric_cols': numeric_cols,
    'categorical_cols': categorical_cols
}
filename = 'house_price_model.pkl'
with open(filename, 'wb') as f:
    pickle.dump(bundle, f)

print(f"Saved: {filename}")""",

        # Cell 32: Loading the Saved Model from Disk (Chapter 12 page 279)
        """#---load the model from disk---
with open('house_price_model.pkl', 'rb') as f:
    loaded_bundle = pickle.load(f)

print("Model loaded successfully.")""",

        # Cell 33: Sample Predictions on Unseen House Profiles (Chapter 12 page 280)
        """examples = pd.DataFrame([
    {
        'Area': 50, 'Frontage': 5, 'Access Road': 6, 'Floors': 4,
        'Bedrooms': 4, 'Bathrooms': 3,
        'House direction': 'Tây', 'Balcony direction': 'Tây',
        'Legal status': 'Have certificate', 'Furniture state': 'Basic',
        'Province': 'Hồ Chí Minh', 'District': 'Bình Tân'
    },
    {
        'Area': 80, 'Frontage': 5, 'Access Road': 10, 'Floors': 5,
        'Bedrooms': 5, 'Bathrooms': 4,
        'House direction': 'Đông - Nam', 'Balcony direction': 'Đông - Nam',
        'Legal status': 'Have certificate', 'Furniture state': 'Full',
        'Province': 'Hà Nội', 'District': 'Cầu Giấy'
    },
    {
        'Area': 120, 'Frontage': 7, 'Access Road': 15, 'Floors': 3,
        'Bedrooms': 4, 'Bathrooms': 4,
        'House direction': 'Nam', 'Balcony direction': 'Nam',
        'Legal status': 'Sale contract', 'Furniture state': 'Basic',
        'Province': 'Đà Nẵng', 'District': 'Ngũ Hành Sơn'
    }
])

example_ready = loaded_bundle['preprocessor'].transform(
    examples[loaded_bundle['feature_cols']]
)
example_prices = loaded_bundle['model'].predict(example_ready)
examples['Predicted Price (billion VND)'] = np.round(example_prices, 2)
examples.to_csv('results/demo_predictions.csv', index=False)
examples""",

        # Cell 34: Client Prediction Function Test (Chapter 12 page 283-284)
        """#---client prediction simulation function---
def predict_house_price(house_dict):
    sample_df = pd.DataFrame([house_dict])
    ready = loaded_bundle['preprocessor'].transform(sample_df[loaded_bundle['feature_cols']])
    price = loaded_bundle['model'].predict(ready)[0]
    return round(price, 2)

test_house = {
    'Area': 65, 'Frontage': 4.5, 'Access Road': 8, 'Floors': 3,
    'Bedrooms': 3, 'Bathrooms': 2,
    'House direction': 'Nam', 'Balcony direction': 'Nam',
    'Legal status': 'Have certificate', 'Furniture state': 'Full',
    'Province': 'Hà Nội', 'District': 'Đống Đa'
}
predicted = predict_house_price(test_house)
print(f"Predicted price for test house: {predicted} billion VND")"""
    ]

    for code in cells:
        nb.cells.append(new_code_cell(code))

    print("Executing house_price_assignment.ipynb...")
    client = NotebookClient(nb, timeout=600, kernel_name='python3')
    client.execute()

    with open('house_price_assignment.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Successfully built and executed house_price_assignment.ipynb")

if __name__ == '__main__':
    build_diabetes_notebook()
    build_house_price_notebook()
    print("ALL NOTEBOOKS BUILT AND EXECUTED SUCCESSFULLY!")
