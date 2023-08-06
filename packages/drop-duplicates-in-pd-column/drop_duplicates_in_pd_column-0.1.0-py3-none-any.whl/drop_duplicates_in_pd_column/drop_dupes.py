import pandas as pd


def drop_column_duplicates(file,column_name):
  df = pd.read_csv(file)
  print("Old Size:",df[column_name].shape)
  df.drop_duplicates(subset = column_name, keep='first', inplace = True)
  print("New Size:",df[column_name].shape)
  return df
  
  
drop_column_duplicates('master_skus copy.csv','sku')
