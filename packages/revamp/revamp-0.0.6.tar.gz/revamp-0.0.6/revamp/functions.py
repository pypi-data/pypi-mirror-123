from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
import pandas as pd
import numpy as np
scaler_mm = MinMaxScaler()
le = LabelEncoder()
enc = OneHotEncoder(handle_unknown='ignore')

class report:
    
    def __init__(self, df):
        self.df = df

    def summary(self):
      Q1=self.df.quantile(0.25)
      Q3=self.df.quantile(0.75)
      IQR = self.df.quantile(0.75)-self.df.quantile(0.25)
      x=((self.df < (Q1 - 1.5 * IQR)) | (self.df > (Q3 + 1.5 * IQR))).sum().reset_index()
      corr_matrix = self.df.corr().abs()
      upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

      print("1. Dimension : ", self.df.shape)
      print("\n2. Categorical : ",[i for i in self.df.columns if self.df.dtypes[i]=='object'])
      print("\n3. Numerical : ",[i for i in self.df.columns if ( self.df.dtypes[i]=='float64' or  self.df.dtypes[i]=='int64')])
      if self.df.isnull().values.any()==True:
        print('\n4. Missing Value Fields : ',self.df.columns[self.df.isna().any()].tolist())
      else:
        print('\n4. Missing Value Imputation : NO')
      if ((self.df < (Q1 - 1.5 * IQR)) | (self.df > (Q3 + 1.5 * IQR))).sum().sum()>0:
        print("\n5. Outliers : ",x[x[0]>0]["index"].tolist())
      else:
        print("\n5. Outliers : NO")
      if self.df.duplicated(keep='first').sum() >0:
        print("\n6. Duplicates : YES")
      else:
        print("\n6. Duplicates : NO")
      if (0 not in self.df.mean() and 1 not in self.df.std()):
        print("\n7. Scaled : NO")
      else:
        print("\n7. Scaled : YES")
      if len([i for i in self.df.columns if self.df.dtypes[i]=='object'])>0:
        print("\n8. Label Encoded : NO")
      else:
        print("\n8. Label Encoded : YES")

      if len([column for column in upper.columns if any(upper[column] > 0.70)])==0:
        print("\n9. Correlation: NO \n")
      else:
        print("\n9. Correlated Fields :" ,[column for column in upper.columns if any(upper[column] > 0.70)] )

    def descriptive_analysis(self):
          means=self.df.mean().reset_index()
          means.rename(columns={"index":"Fields",0:"Mean"},inplace=True)

          median=self.df.median().reset_index()
          median.rename(columns={"index":"Fields",0:"Median"},inplace=True)

          mod=self.df.mode().iloc[0].reset_index()
          mod.rename(columns={"index":"Fields",0:"Mode"},inplace=True)

          skew=self.df.skew().reset_index()
          skew.rename(columns={"index":"Fields",0:"Skewness"},inplace=True)

          kurt=self.df.kurtosis().reset_index()
          kurt.rename(columns={"index":"Fields",0:"Kurtosis"},inplace=True)

          min=self.df[[i for i in self.df.columns if ( self.df.dtypes[i]=='float64' or  self.df.dtypes[i]=='int64')]].min().reset_index()
          min.rename(columns={"index":"Fields",0:"Min"},inplace=True)

          max=self.df[[i for i in self.df.columns if ( self.df.dtypes[i]=='float64' or  self.df.dtypes[i]=='int64')]].max().reset_index()
          max.rename(columns={"index":"Fields",0:"Max"},inplace=True)
        
          std=self.df.std().reset_index()
          std.rename(columns={"index":"Fields",0:"std"},inplace=True)

          count=self.df.count().reset_index()
          count.rename(columns={"index":"Fields",0:"Count"},inplace=True)

          uniq=self.df.nunique().reset_index()
          uniq.rename(columns={"index":"Fields",0:"Unique"},inplace=True)

          quant=self.df.quantile([0.25,0.5,0.75]).T.reset_index()
          quant.rename(columns={"index":"Fields",0.25:"Q1",0.5:"Q2",0.75:"Q3"},inplace=True)

          final_stats=means.merge(median,how="left",on="Fields")
          final_stats=final_stats.merge(mod,how="right",on="Fields")
          final_stats=final_stats.merge(skew,how="left",on="Fields")
          final_stats=final_stats.merge(kurt,how="left",on="Fields")
          final_stats=final_stats.merge(min,how="left",on="Fields")
          final_stats=final_stats.merge(max,how="left",on="Fields")
          final_stats=final_stats.merge(std,how="left",on="Fields")
          final_stats=final_stats.merge(count,how="right",on="Fields")
          final_stats=final_stats.merge(uniq,how="left",on="Fields")
          final_stats=final_stats.merge(quant,how="left",on="Fields")
          final_stats["IQR"]=final_stats["Q3"]-final_stats["Q1"]
          final_stats["Range"]=final_stats["Max"]-final_stats["Min"]

          return final_stats

          