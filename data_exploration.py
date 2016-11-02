import time
import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataframe_pickle = 'data/se-df.pkl'

# Column names:
#   - 'CommentCount'
#   - 'ViewCount'
#   - 'Score'
#   - 'Tags'
#   - 'AnswerCount'
#   - 'FavoriteCount'
#   - 'Reputation'
#   - 'UserAge'
#   - 'Month'
#   - 'Day'
#   - 'HasAccepted'
#   - 'Title'
#   - 'Body' 
#   - 'Closed'

def log_status(msg):
  timer = "[{:10.3f}s]".format(time.time() - start_time)
  print("{: <10} {}".format(timer, msg))

if __name__ == '__main__':
  start_time = time.time()
  log_status("Process started.")

  # Load the dataframe from file
  df = pd.read_pickle(dataframe_pickle)
  log_status("Dataframe loaded.")


  # View percentage of closed questions by day
  # closed_per_day = df.groupby('Day')['Closed'].sum()
  # total_per_day  = df.groupby('Day')['Closed'].count()
  # ratio_day = closed_per_day/total_per_day

  # ratio_day.plot(kind='bar')
  # plt.savefig('ratio_day.png')
  # plt.clf()

  # View percentage of closed questions by month 
  # closed_per_month = df.groupby('Month')['Closed'].sum()
  # total_per_month = df.groupby('Month')['Closed'].count()
  # ratio_month = closed_per_month/total_per_month

  # ratio_month.plot(kind='bar')
  # plt.savefig('ratio_month.png')
  # plt.clf()

  # View closed questions vs user age  
  sub_df = df[['UserAge', 'Closed']]
  df = None # Allow garbage collection
  sub_df = sub_df.sort_values('UserAge')
  sub_df = sub_df[sub_df['UserAge'] >= 0]
  sub_df['CumulativeClosed'] = sub_df.Closed.cumsum()
  sub_df = sub_df.reset_index()

  rows = sub_df.shape[0]
  sub_df['RowNum'] = np.arange(1, rows+1)

  sub_df['PercentClosed'] = sub_df['CumulativeClosed']/sub_df['RowNum']
  sub_df.plot(x='UserAge', y='PercentClosed', logx=True, style='o')
  plt.savefig('percentclosed_by_age.png')
  plt.show()
  
