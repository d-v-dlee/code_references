import time
import logging
import sys
import json
import pandas as pd

#################################### logging for Databricks ####################################
################################################################################################


###### run at top of databricks notebook ######
cluster_id = dbutils.notebook.entry_point.getDbutils().notebook().getContext().clusterId().get()
try:
  run_id = dbutils.notebook.entry_point.getDbutils().notebook().getContext().currentRunId().get()
  run_id = str(run_id).replace("RunId","").replace("(","").replace(")","")
except:
  run_id = "999"
log_folder = "/job_logs/" + str(run_id) + "/"
print(log_folder)

beginning_time = time.time()
 
logging_output = pd.DataFrame(columns=["time", "type", "text"])
dbutils.fs.mkdirs(log_folder)
 
###### helper functions ######

def output_log(log, log_type, text):
  df = pd.DataFrame({"time":str(datetime.now()), "type":log_type, "text":text}, index=[0])
  df = df[list(logging_output.columns)]
  return(log[list(logging_output.columns)].append(df, ignore_index=True))

def display_time(seconds):
    """
    accepts seconds and returns 
    """
    result = []
    for name, count in (('weeks', 604800),('days', 86400),('hours', 3600),('minutes', 60),('seconds', 1)):
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:2])

###### run in cells ######

logging_output = output_log(logging_output, "StdOut", "Reading 4 Main Input files")
logging_output.to_json("/dbfs/" + log_folder + "full_log.json", orient='records')

try:
    pass
except Exception as e:
  logging_output = output_log(logging_output, "StdErr", str(e))
  logging_output.to_json("/dbfs/" + log_folder + "full_log.json", orient='records')
  raise ValueError(e)