import time
import sqlite3
import pandas as pd

se_dump_db  = 'se-dump.db'
se_dump_pkl = 'se-df.pkl'

def log_status(msg):
  timer = "[{:10.3f}s]".format(time.time() - start_time)
  print("{: <10} {}".format(timer, msg))
  

# Gets all questions + asker information from the data dump
question_search_sql = '''
                        SELECT p.CommentCount,  p.ViewCount,   p.Score,            
                               p.Tags,          p.Title,       p.AnswerCount,  
                               p.FavoriteCount, u.Reputation,  
                               julianday(p.CreationDate) - julianday(u.CreationDate) as [UserAge],
                               CAST(strftime("%m", p.CreationDate) as integer) as [Month],
                               CAST(strftime("%w", p.CreationDate) as integer) as [Day],
                               p.AcceptedAnswerId IS NOT NULL as [HasAccepted], 
                               p.Title, p.Body, 
                               p.ClosedDate IS NOT NULL as [Closed]
                        FROM posts p
                        LEFT JOIN users u
                        ON   u.id = p.OwnerUserId
                        WHERE p.PostTypeId = 1 -- is question
                      '''

if __name__ == '__main__':
  start_time = time.time()
  # get all connected to our database dump
  log_status("Connecting to database...")
  db_connection = sqlite3.connect(se_dump_db)
  db_cursor = db_connection.cursor()

  # Run the sql query and create dataframe
  log_status("Running sql query and converting to dataframe...")
  sql_iterator = db_cursor.execute(question_search_sql)
  df = pd.DataFrame(db_cursor.fetchall())
  column_names = [t[0] for t in db_cursor.description]
  df.columns = column_names

  log_status("Dataframe created.")

  # Save the dataframe to file
  df.to_pickle(se_dump_pkl)

  log_status("Dataframe pickled.")
  log_status("Finished.")
