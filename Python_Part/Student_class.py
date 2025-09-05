import pandas as pd
import matplotlib.pyplot as plt
import random

class Student_class:
    def __init__(self, subject):
        data=pd.read_csv('Python_Part/Questionbank.csv', encoding="ISO-8859-1", dtype=str)
        self.df=pd.DataFrame(data)
        
        self.subject = subject
    
    def get_max_question(self):
        column = self.subject + 'que'
        return self.df[column].count()
 
    
    def get_subject_performance(self, name):
        if (name.upper()+self.subject) not in self.df.columns:
            return [], []
        
        student_df = self.df[name.upper()+self.subject]
        student_df = student_df.dropna()

        index = student_df.index
        attempts = []
        for i in index:
            attempts.append(i+1)

        percentages = student_df.tolist()

        return attempts, percentages
    
    def get_question_from_number(self, number):
        question_no_list = random.sample(range(self.df[self.subject + "que"].count()), number)

        questions = []
        for i in question_no_list:
            questions.append(self.df.loc[i, (self.subject + "que") : (self.subject + "ans")].tolist())
        return questions
    
    def set_result(self, name, percentage):
        name = name.upper()
        nameSubject = name+self.subject
        if (nameSubject not in self.df.columns):
            self.df[nameSubject] = pd.Series([None] * len(self.df))
        
        self.df.loc[self.df[nameSubject].count(), nameSubject] = percentage

        self.Data_Frame = self.df.loc[:,'Physicsque':]
        self.Data_Frame.to_csv('Python_Part/Questionbank.csv')

        return
