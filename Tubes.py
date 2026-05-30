import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel('jobSalary_Kel_Meteor_classified.xlsx')
kolom_dipakai = [
    "job_level",
    "experience_years",
    "education_num",
    "skills_count",
    "certifications",
    "salary"
]
data = data[kolom_dipakai]
print(data.head())
print(data.describe())
print("\n Rentang nilai tiap kolom : ")
for kolom in kolom_dipakai:
    print("\nKolom:", kolom)
    print("Min:", data[kolom].min())
    print("Max:", data[kolom].max())
    print("Mean:", data[kolom].mean())