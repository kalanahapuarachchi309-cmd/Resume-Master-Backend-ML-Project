# Machine Learning Model Evaluation Report

**Project:** AI Resume/CV Screening & Job Matching System  
**Prepared by:** Hiruna (ML Engineer) & Backend Team  
**Evaluation Date:** 2026-09-12  
**Target Variable:** `match_label` (1 = Suitable Match, 0 = Unsuitable Match)  

---

## 1. Dataset Characteristics & Summary

- **Total Samples:** 1680 resume-to-job matching pairs
- **Class Distribution:**
  - Class 1 (Suitable Match): 812 (48.3%)
  - Class 0 (Unsuitable Match): 868 (51.7%)
- **Data Splitting:** 80% Train (1344 pairs) / 20% Test (336 pairs) with stratified split to prevent data leakage.

---

## 2. Mandatory Feature Engineering Techniques (7 Features)

1. **TF-IDF Semantic Similarity:** Fitted on training text corpus; cosine similarity computed between candidate resume and job vacancy.
2. **Skill Overlap Ratio:** Jaccard-like intersection ratio: $|\text{Candidate Skills} \cap \text{Required Skills}| / |\text{Required Skills}|$.
3. **Skill Count:** Total count of overlapping required skills.
4. **Missing Skill Ratio:** Proportion of mandatory skills absent: $|\text{Missing Skills}| / |\text{Required Skills}|$.
5. **Experience Delta:** Candidate years minus required years, bounded within $[-3.0, +3.0]$.
6. **Experience Fit Binary:** Indicator variable (1 if candidate meets/exceeds requirement, 0 otherwise).
7. **Education Level Ordinal Encoding:** None=0, Diploma=1, Bachelor=2, Master=3, PhD=4.

---

## 3. Comparative Model Evaluation Results

| Model Name | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 93.45% | 93.75% | 92.59% | **93.17%** | 0.9875 |
| **Support Vector Machine (SVM)** | 94.05% | 93.83% | 93.83% | **93.83%** | 0.9912 |
| **Random Forest Classifier** | 99.11% | 98.18% | 100.00% | **99.08%** | 0.9992 |

---

## 4. Winning Model Selection

The **Random Forest Classifier** was selected for production inference because it achieved the highest **F1-Score of 99.08%**. In recruitment screening, F1-score is the optimal selection metric because it balances false positives (shortlisting unqualified candidates) and false negatives (rejecting qualified talent).

The serialized model is stored at `backend/app/ml/model.pkl` and directly integrated with the FastAPI ranking engine.
