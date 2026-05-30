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

#bikin fuzzy set untuk setiap kolom
fuzzy_set = {
    "job_level": {
        "low" : ("trap", 1, 1, 1, 2),
        "medium" : ("tri", 1, 2, 3),
        "high" : ("trap", 2, 3, 3,3)
    },

    "experience_years": {
        "low" : ("trap",0,0,1,3),
        "medium" : ("tri",5,10,15),
        "high" : ("trap",10,15,20,20)
    },

    "education_num":{
        "low" : ("trap",1,1,1.5,2.5),
        "medium" : ("tri",2,3,4),
        "high" : ("trap",3.5,4.5,5,5)
    },

    "skills_count":{
        "low" : ("trap",1,1,4,8),
        "medium" : ("tri",6,10,14),
        "high" : ("trap",12,16,19,19)
    },

    "certifications":{
        "low" : ("trap",0,0,1,2.5),
        "medium" : ("tri",1.5,3,4.5),
        "high" : ("trap",3.5,5,5,5)
    },
}