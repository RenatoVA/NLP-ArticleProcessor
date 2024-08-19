import pandas as pd
data = pd.read_csv('train.csv',index_col=False)
new_df = pd.DataFrame()
new_df['text'] = data['comment_text']
new_df['labels'] = data.iloc[:, 1:].values.tolist()
print(data.info())