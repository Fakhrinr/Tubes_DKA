import pandas as pd
import numpy as np
import sklearn.metrics # type: ignore

# LOAD DATA
data = pd.read_excel('jobSalary_Kel_Meteor_classified.xlsx')
data = data[
    [
        "experience_years",
        "skills_count",
        "education_num",
        "salary"
    ]
]

# FUNGSI KEANGGOTAAN
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)

# EXPERIENCE
def exp_low(x):
    return triangular(x, 0, 0, 10)

def exp_med(x):
    return triangular(x, 5, 15, 25)

def exp_high(x):
    return triangular(x, 20, 35, 35)

# SKILLS
def skill_low(x):
    return triangular(x, 0, 0, 10)

def skill_med(x):
    return triangular(x, 5, 15, 25)

def skill_high(x):
    return triangular(x, 20, 30, 30)

# EDUCATION
def edu_low(x):
    return triangular(x, 0, 0, 2)

def edu_med(x):
    return triangular(x, 1, 3, 5)

def edu_high(x):
    return triangular(x, 4, 6, 6)

# OUTPUT SALARY
SALARY_LOW = 40000
SALARY_MED = 80000
SALARY_HIGH = 120000

# RULE BASE (15 RULE)
def rules(exp, skill, edu):

    r = []

    r.append((min(exp_high(exp), skill_high(skill), edu_high(edu)), SALARY_HIGH))
    r.append((min(exp_high(exp), skill_high(skill), edu_med(edu)), SALARY_HIGH))
    r.append((min(exp_high(exp), skill_med(skill), edu_high(edu)), SALARY_HIGH))
    r.append((min(exp_med(exp), skill_high(skill), edu_high(edu)), SALARY_HIGH))

    r.append((min(exp_med(exp), skill_med(skill), edu_high(edu)), SALARY_MED))
    r.append((min(exp_med(exp), skill_high(skill), edu_med(edu)), SALARY_MED))
    r.append((min(exp_high(exp), skill_low(skill), edu_high(edu)), SALARY_MED))
    r.append((min(exp_low(exp), skill_high(skill), edu_high(edu)), SALARY_MED))
    r.append((min(exp_med(exp), skill_med(skill), edu_med(edu)), SALARY_MED))

    r.append((min(exp_low(exp), skill_low(skill), edu_low(edu)), SALARY_LOW))
    r.append((min(exp_low(exp), skill_med(skill), edu_low(edu)), SALARY_LOW))
    r.append((min(exp_low(exp), skill_low(skill), edu_med(edu)), SALARY_LOW))
    r.append((min(exp_med(exp), skill_low(skill), edu_low(edu)), SALARY_LOW))
    r.append((min(exp_low(exp), skill_med(skill), edu_med(edu)), SALARY_LOW))
    r.append((min(exp_med(exp), skill_low(skill), edu_med(edu)), SALARY_LOW))

    return r

# SUGENO
def fuzzy_sugeno(exp, skill, edu):

    firing_strength = []
    output_value = []

    for alpha, z in rules(exp, skill, edu):
        firing_strength.append(alpha)
        output_value.append(z)

    if sum(firing_strength) == 0:
        return 0

    return np.sum(
        np.array(firing_strength) *
        np.array(output_value)
    ) / np.sum(firing_strength)

# MAMDANI
def fuzzy_mamdani(exp, skill, edu):

    salary_range = np.arange(20000, 150001, 1000)

    aggregated = np.zeros(len(salary_range))

    for alpha, z in rules(exp, skill, edu):

        if z == SALARY_LOW:
            mf = np.array([
                min(alpha,
                    triangular(s, 20000, 40000, 70000))
                for s in salary_range
            ])

        elif z == SALARY_MED:
            mf = np.array([
                min(alpha,
                    triangular(s, 50000, 80000, 110000))
                for s in salary_range
            ])

        else:
            mf = np.array([
                min(alpha,
                    triangular(s, 90000, 120000, 150000))
                for s in salary_range
            ])

        aggregated = np.maximum(aggregated, mf)

    if np.sum(aggregated) == 0:
        return 0

    return np.sum(
        salary_range * aggregated
    ) / np.sum(aggregated)

# PREDIKSI
pred_mamdani = []
pred_sugeno = []

for _, row in data.iterrows():

    exp = row["experience_years"]
    skill = row["skills_count"]
    edu = row["education_num"]

    pred_mamdani.append(
        fuzzy_mamdani(exp, skill, edu)
    )

    pred_sugeno.append(
        fuzzy_sugeno(exp, skill, edu)
    )

# EVALUASI
actual = data["salary"]

mae_mamdani = sklearn.metrics.mean_absolute_error(
    actual,
    pred_mamdani
)

mse_mamdani = sklearn.metrics.mean_squared_error(
    actual,
    pred_mamdani
)

mae_sugeno = sklearn.metrics.mean_absolute_error(
    actual,
    pred_sugeno
)

mse_sugeno = sklearn.metrics.mean_squared_error(
    actual,
    pred_sugeno
)

print("\n===== MAMDANI =====")
print("MAE :", mae_mamdani)
print("MSE :", mse_mamdani)

print("\n===== SUGENO =====")
print("MAE :", mae_sugeno)
print("MSE :", mse_sugeno)