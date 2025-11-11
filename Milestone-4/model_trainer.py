# model_trainer.py (FIXED)
# Enhanced Model Training with CORRECT Target Variable (JobRole)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('final_high_accuracy_job_dataset.csv')

print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# ============================================
# 1. DATA CLEANING & PREPROCESSING
# ============================================

# Remove duplicates
df = df.drop_duplicates()
print(f"\nDataset after removing duplicates: {df.shape}")

# Strip whitespace from all string columns
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip()

# Handle missing values
print("\nMissing values:")
print(df.isnull().sum())

# Fill missing values appropriately
df['Certification'] = df['Certification'].fillna('None')
df['Internship'] = df['Internship'].fillna('No')

print("\nUnique Job Roles (Target Variable):")
print(df['JobRole'].value_counts())
print(f"Total unique roles: {df['JobRole'].nunique()}")

# ============================================
# 2. FEATURE ENGINEERING
# ============================================

# Create new features
df['SkillCount'] = 2  # We have Skill1 and Skill2

# Create Education Level (numeric)
degree_hierarchy = {
    'BCA': 1, 'B.Tech': 1,
    'MCA': 2, 'M.Tech': 2, 'MBA': 2
}
df['DegreeLevel'] = df['Degree'].map(degree_hierarchy)

# Create Experience Categories
def categorize_experience(years):
    if years == 0:
        return 'Fresher'
    elif years <= 2:
        return 'Junior'
    elif years <= 5:
        return 'Mid'
    else:
        return 'Senior'

df['ExperienceCategoryFeature'] = df['ExperienceYears'].apply(categorize_experience)

# Create Project Density (projects per year)
df['ProjectDensity'] = df['ProjectCount'] / (df['ExperienceYears'] + 1)

# Create a skill set combining both skills
df['SkillSet'] = df['Skill1'] + '_' + df['Skill2']

print("\nFeature Engineering Complete!")

# ============================================
# 3. ENCODING CATEGORICAL VARIABLES
# ============================================

# Dictionary to store encoders for later use
encoders = {}
label_columns = ['Degree', 'Major', 'Skill1', 'Skill2', 'Certification', 
                  'Internship', 'ExperienceLevel', 'ExperienceCategoryFeature']

# Encode categorical features
for col in label_columns:
    le = LabelEncoder()
    df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
    encoders[col] = le
    print(f"Encoded {col}: {len(le.classes_)} unique values")

# ✅ ENCODE TARGET VARIABLE CORRECTLY
print("\n" + "="*60)
print("ENCODING TARGET VARIABLE: JobRole")
print("="*60)
target_encoder = LabelEncoder()
df['JobRole_encoded'] = target_encoder.fit_transform(df['JobRole'])

print(f"\nTarget Classes (JobRole):")
for idx, role in enumerate(target_encoder.classes_):
    count = (df['JobRole'] == role).sum()
    print(f"  {idx}: {role} ({count} samples)")

# ============================================
# 4. SELECT FEATURES FOR MODEL
# ============================================

feature_columns = [
    'Degree_encoded', 'Major_encoded', 'Skill1_encoded', 'Skill2_encoded',
    'Certification_encoded', 'ExperienceYears', 'ProjectCount', 
    'Internship_encoded', 'ExperienceLevel_encoded', 'DegreeLevel',
    'ProjectDensity', 'ExperienceCategoryFeature_encoded'
]

X = df[feature_columns]
# ✅ USE JobRole AS TARGET (NOT ExperienceLevel!)
y = df['JobRole']

print(f"\nFeature matrix shape: {X.shape}")
print(f"Target variable: JobRole")
print(f"Target distribution:")
print(y.value_counts())

# ============================================
# 5. SCALE FEATURES
# ============================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=feature_columns)

print(f"\nFeatures scaled successfully!")

# ============================================
# 6. SPLIT DATA
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set size: {X_train.shape}")
print(f"Test set size: {X_test.shape}")
print(f"\nTraining set class distribution:")
print(y_train.value_counts())

# ============================================
# 7. TRAIN MULTIPLE MODELS
# ============================================

print("\n" + "="*60)
print("TRAINING MODELS")
print("="*60)

# Model 1: Random Forest
print("\n1. Training Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_split=3,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)
print(f"✓ Random Forest Accuracy: {rf_acc:.4f}")

# Model 2: Gradient Boosting
print("\n2. Training Gradient Boosting...")
gb_model = GradientBoostingClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    min_samples_split=3,
    min_samples_leaf=1,
    random_state=42,
    subsample=0.8
)
gb_model.fit(X_train, y_train)
gb_pred = gb_model.predict(X_test)
gb_acc = accuracy_score(y_test, gb_pred)
print(f"✓ Gradient Boosting Accuracy: {gb_acc:.4f}")

# ============================================
# 8. EVALUATE MODELS
# ============================================

print("\n" + "="*60)
print("MODEL EVALUATION - PREDICTING JobRole")
print("="*60)

print("\n--- RANDOM FOREST RESULTS ---")
print(f"Accuracy: {rf_acc:.4f} ({rf_acc*100:.2f}%)")
print(f"F1 Score (weighted): {f1_score(y_test, rf_pred, average='weighted'):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, rf_pred))

print("\n--- GRADIENT BOOSTING RESULTS ---")
print(f"Accuracy: {gb_acc:.4f} ({gb_acc*100:.2f}%)")
print(f"F1 Score (weighted): {f1_score(y_test, gb_pred, average='weighted'):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, gb_pred))

# Select best model
best_model = rf_model if rf_acc >= gb_acc else gb_model
best_acc = max(rf_acc, gb_acc)
best_name = 'Random Forest' if rf_acc >= gb_acc else 'Gradient Boosting'

print(f"\n{'='*60}")
print(f"✓ BEST MODEL: {best_name}")
print(f"✓ ACCURACY: {best_acc:.4f} ({best_acc*100:.2f}%)")
print(f"✓ TARGET VARIABLE: JobRole (Not ExperienceLevel!)")
print(f"{'='*60}")

# ============================================
# 9. FEATURE IMPORTANCE
# ============================================

print("\n" + "="*60)
print("FEATURE IMPORTANCE")
print("="*60)

feature_importance = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': best_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10).to_string(index=False))

# ============================================
# 10. SAVE MODEL AND ARTIFACTS
# ============================================

# Create comprehensive model package
model_package = {
    'model': best_model,
    'scaler': scaler,
    'feature_columns': feature_columns,
    'encoders': encoders,
    'target_encoder': target_encoder,
    'target_variable': 'JobRole',  # ✅ IMPORTANT!
    'feature_importance': feature_importance,
    'accuracy': best_acc,
    'model_type': best_name,
    'classes': target_encoder.classes_.tolist()
}

joblib.dump(model_package, 'best_model.pkl')
print("\n✓ Model saved as 'best_model.pkl'")

# Save model metadata for reference
metadata = {
    'accuracy': best_acc,
    'accuracy_percentage': f"{best_acc*100:.2f}%",
    'model_type': best_name,
    'target_variable': 'JobRole',
    'features_used': feature_columns,
    'num_features': len(feature_columns),
    'job_roles': target_encoder.classes_.tolist(),
    'num_classes': len(target_encoder.classes_),
    'feature_importance': feature_importance.to_dict('records')
}

joblib.dump(metadata, 'model_metadata.pkl')
print("✓ Metadata saved as 'model_metadata.pkl'")

# Save as readable JSON
import json
with open('model_info.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print("✓ Model info saved as 'model_info.json'")

print("\n" + "="*60)
print("✅ MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"\nYour model now predicts: {best_name}")
print(f"Target: JobRole (not ExperienceLevel)")
print(f"Accuracy: {best_acc*100:.2f}%")
print(f"Classes: {len(target_encoder.classes_)} job roles")
print("\nReady to use! Run your Streamlit app now!")
print("="*60)