import pandas as pd
import numpy
import matplotlib.pyplot as plt

class Admin_class:
    def __init__(self, subject):
        data=pd.read_csv('Python_Part/Questionbank.csv', encoding="ISO-8859-1")
        self.df=pd.DataFrame(data)
        self.subject = subject

    def GetTotalQA(self):
        column = self.subject + 'que'
        count = self.df[column].count()
        return count
    
    def View_que(self):
        questions = self.df[self.subject+'que'].values.flatten()
        questions = [q for q in questions if pd.notna(q)]  # Remove NaN values
        return questions
        
    def AddQA(self, que, op1, op2, op3, op4, ans):
        self.df.loc[self.GetTotalQA(),[(self.subject+'que'),(self.subject+'1'),(self.subject+'2'),(self.subject+'3'),(self.subject+'4'),(self.subject+'ans')]]=[que,op1,op2,op3,op4,ans]
        self.Data_Frame = self.df.loc[:,'Physicsque':]
        self.Data_Frame.to_csv('Python_Part/Questionbank.csv')
        return
    
    def swap(self,df,row1,row2):
        df.iloc[row1], df.iloc[row2] = df.iloc[row2].copy(), df.iloc[row1].copy()
        return df
    
    def Delete_QA(self, que):
        que_ID = self.df[self.df[self.subject+'que'] == que].index[0]
        total_que = self.df[self.subject+'que'].count()

        self.df.loc[:,(self.subject+'que'):(self.subject+'ans')] = self.swap(self.df.loc[:,(self.subject+'que'):(self.subject+'ans')], total_que-1, que_ID)
        
        self.df.loc[total_que-1, self.subject+'que':self.subject+'ans'] = numpy.nan

        self.Data_Frame = self.df.loc[:,'Physicsque':]
        self.Data_Frame.to_csv('Python_Part/Questionbank.csv')
    
        return
    
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