# Milestone 2 - Data Preprocessing and Visualization

## 📘 Project Overview
This notebook focuses on the **data preprocessing and exploratory data analysis (EDA)** phase of the project **"Predicting Job Roles from Educational Background"**.  
The objective is to clean, preprocess, and visualize the dataset to prepare it for machine learning model development in the next milestone.

---

## 🎯 Objectives
- Load and inspect the dataset.
- Handle missing values and inconsistent data.
- Encode categorical variables for machine learning compatibility.
- Perform basic exploratory data analysis and visualizations.

---

## 🧰 Technologies Used
- **Python**
- **Google Colab**
- **Libraries:**
  - `pandas` – for data manipulation  
  - `numpy` – for numerical operations  
  - `matplotlib` & `seaborn` – for visualizations  
  - `scikit-learn` – for preprocessing and label encoding

---

## 📂 Steps Performed
1. **Importing Libraries**  
   Loaded all required Python libraries for data handling, visualization, and preprocessing.

2. **Dataset Loading**  
   Uploaded a CSV file using the Google Colab file upload feature and displayed the first few rows for inspection.

3. **Exploratory Data Analysis (EDA)**  
   - Checked dataset information and structure.  
   - Identified missing values and the distribution of the target variable (`job_role`).  
   - Visualized relationships between features using `matplotlib` and `seaborn`.

4. **Data Preprocessing**  
   - Replaced `"None"` values with `NaN`.  
   - Filled missing values in columns like `skills`, `qualification`, and `experience_level` with `"Unknown"`.  
   - Encoded categorical variables using `LabelEncoder` from scikit-learn.

---

## 📊 Example Visualizations
- Distribution of `job_role`
- Skill vs. Qualification analysis
- Experience level frequency plots

*(Note: Actual plots can be viewed inside the notebook.)*

---

## 🚀 How to Run the Notebook
1. Open the notebook in **Google Colab**.
2. Upload your dataset (`.csv` file) when prompted.
3. Execute each cell sequentially to perform:
   - Data loading  
   - Cleaning and preprocessing  
   - Visualizations  

---

## 📁 Output
After successful execution, the notebook produces:
- A **cleaned and preprocessed dataset (`df_processed`)** ready for model training.  
- Visualizations summarizing data distributions and relationships.

---

## 📌 Next Steps
- Perform feature selection and model building (Milestone 3).
- Evaluate model performance and tune hyperparameters.

---

## 👨‍💻 Author
**K. Giri Dhar**  
B.Tech – Computer Science and Engineering  
VEMU Institute of Technology  
