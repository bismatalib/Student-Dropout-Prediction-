<div align="center">

# 🎓 Student Dropout Risk Prediction

**An end-to-end machine learning project that predicts a student's probability of dropping out, so institutions can offer support before it is too late.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Logistic%20Regression-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

### 🔗 [**Live Demo → ejkztte6aa5mnr9adhgkap.streamlit.app**](https://ejkztte6aa5mnr9adhgkap.streamlit.app/)

</div>

---

## 📌 Overview

Every year, many university students leave before finishing their degree. Catching the warning signs early gives advisors a chance to help.

This project uses real student records to train a **Logistic Regression** classifier that estimates each student's **dropout probability** and assigns a **risk level** (Low, Medium or High). The model is wrapped in an interactive **Streamlit web app** that also explains *why* a student received a given result.

Built as part of my **Machine Learning Internship at Big Brains**.

## ✨ Key Features

- 🔮 **Instant risk prediction** with a probability and a Low / Medium / High risk level
- 📊 **Explainable results**: shows which factors raise or lower a student's risk
- 📈 **Visual breakdown**: gauge chart, factor-effect chart and comparison with students who stayed vs. dropped out
- 🧪 **Example students** to explore the model quickly
- 🧰 **Complete ML workflow**: data collection, cleaning, EDA, modeling, evaluation and deployment

## 📂 Dataset

| Item | Details |
|---|---|
| **Name** | Predict Students' Dropout and Academic Success |
| **Source** | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success) (also available on Kaggle) |
| **Origin** | Polytechnic Institute of Portalegre, Portugal (Realinho et al., 2021) |
| **Records** | 4,424 students |
| **Features** | 34 (demographic, socioeconomic, enrollment, academic and economic indicators) |
| **Original target** | Dropout / Enrolled / Graduate |
| **Missing values** | None |

For this project the target was converted to **binary**: `1 = Dropout`, `0 = Not Dropout` (Enrolled or Graduate). About **32%** of students are dropouts, so the classes are moderately imbalanced.

> Please check the dataset page for its license and citation requirements.

## 🔬 Methodology

1. **Problem definition**: binary classification (Dropout vs. Not Dropout)
2. **Data collection and exploration**: shape, data types, target distribution
3. **Cleaning and preprocessing**
   - Checked missing values and duplicates (none found)
   - Fixed column names and converted the target to binary
   - Grouped rare categories (fewer than 50 students) into an "other" group
   - One-hot encoded the category-coded columns (Course, Application mode, parents' occupations, etc.), giving **94 features**
4. **Train/test split**: 80/20 stratified split (`random_state=42`)
5. **Scaling**: `StandardScaler` fitted on the training set only, to avoid data leakage
6. **Exploratory data analysis** on the training set only
7. **Modeling**: Logistic Regression
8. **Evaluation**: accuracy, precision, recall, F1-score, ROC-AUC and confusion matrix
9. **Deployment**: Streamlit app hosted on Streamlit Community Cloud

## 🔍 Key Insights from EDA

- 📉 **Academic results matter most.** Dropouts averaged a 1st-semester grade of about 7.3, compared with about 12.2 for other students.
- 🚫 **Passing no units is a major warning sign.** About 82% of students with zero approved units in the 2nd semester dropped out.
- 💳 **Unpaid tuition is a strong risk factor.** About 87% of students with unpaid tuition dropped out, compared with about 25% of those up to date.
- 🎓 **Scholarships help.** Scholarship holders dropped out at only about 12%, versus about 39% for non-holders.
- 🎂 **Age plays a role.** Dropout rises from about 21% (age 19 and under) to about 60% (ages 26-30).
- 🌍 **Economic indicators** (unemployment, inflation, GDP) showed little difference between groups.

## 📈 Model Performance

Evaluated on the held-out test set (885 students):

| Metric | Score |
|---|---|
| **Accuracy** | 0.887 |
| **Precision** | 0.871 |
| **Recall** | 0.761 |
| **F1-score** | 0.812 |
| **ROC-AUC** | 0.932 |

**Confusion matrix**

|  | Predicted: Not Dropout | Predicted: Dropout |
|---|---|---|
| **Actual: Not Dropout** | 569 | 32 |
| **Actual: Dropout** | 68 | 216 |

**What this means:** the model separates dropouts from non-dropouts very well (ROC-AUC 0.93). Missing a student who actually drops out (68 false negatives) is more costly than a false alarm (32 false positives), so recall is the metric to watch.

**Improving recall:** using `class_weight="balanced"` raised recall from **0.76 to 0.85** (F1 from 0.81 to 0.82), at the cost of lower precision (0.80). This is a useful trade-off when catching at-risk students matters most.

## 🖥️ The App

The app takes 9 key inputs: age, gender, tuition status, debt status, scholarship, and approved units and grades for both semesters. All other features use typical values from the training data.

**Risk levels**

| Probability | Risk level |
|---|---|
| Below 30% | 🟢 Low Risk |
| 30% to 60% | 🟡 Medium Risk |
| 60% or more | 🔴 High Risk |


## 🗂️ Project Structure

```
Student-Dropout-Prediction-/
├── app.py                                  # Streamlit web app
├── model.json                              # Trained model weights, scaler and defaults
├── requirements.txt                        # Dependencies for deployment
├── Student_Dropout_Prediction_Full.ipynb   # Full analysis and modeling notebook
└── README.md
```

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/bismatalib/Student-Dropout-Prediction-.git
cd Student-Dropout-Prediction-

# 2. Install the dependency
pip install streamlit

# 3. Start the app
python -m streamlit run app.py
```

To reproduce the full analysis, open `Student_Dropout_Prediction_Full.ipynb` in Jupyter, place the dataset CSV in the same folder, and use **Restart & Run All**.

## ⚠️ Limitations

- Trained on data from a single Portuguese institution, so results may not generalize to other universities without re-validation.
- The model uses 2nd-semester results, so it identifies risk **after the first year**, not at enrollment.
- The app uses 9 key inputs and fills the remaining features with typical values.
- This tool **supports** decisions. It is not a final judgement about any student, and a human should decide what support to offer.

## 🔮 Future Improvements

- Compare against Random Forest and XGBoost
- Add cross-validation and hyperparameter tuning
- Explore feature selection and SHAP-based explanations
- Build an early-warning version that uses only enrollment-time data
- Add batch prediction from an uploaded CSV file

## 🛠️ Tech Stack

Python · Pandas · NumPy · Scikit-learn · Matplotlib · Seaborn · Streamlit

## 👤 Author

**Bisma Talib**
Machine Learning Intern at Big Brains

[LinkedIn](https://www.linkedin.com/in/bisma-talib-077848362/) · [GitHub](https://github.com/bismatalib)

---

<div align="center">

If you found this project useful, please consider giving it a ⭐

</div>
