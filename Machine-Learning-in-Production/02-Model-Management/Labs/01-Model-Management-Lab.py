# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # Lab: Adding Pre and Post-Processing Logic
# MAGIC 
# MAGIC ## ![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) In this lab you:<br>
# MAGIC  - Import data and train a random forest model
# MAGIC  - Defining pre-processing steps
# MAGIC  - Adding post-processing steps

# COMMAND ----------

# MAGIC %run ../../Includes/Classroom-Setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Data and Train Random Forest

# COMMAND ----------

import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_parquet("/dbfs/mnt/training/airbnb/sf-listings/airbnb-cleaned-mlflow.parquet")
X_train, X_test, y_train, y_test = train_test_split(df.drop(["price"], axis=1), df["price"], random_state=42)
X_train.head()

# COMMAND ----------

# MAGIC %md
# MAGIC Load the random forest model logged with mlflow from the demo notebook.

# COMMAND ----------

# TODO
import mlflow

# FILL_IN

# COMMAND ----------

# MAGIC %md
# MAGIC ## Adding Pre-Processing Steps
# MAGIC 
# MAGIC We trained our `rf2` model using a pre-processed training set that has one extra column (`review_scores_sum`) than the unprocessed `X_train` and `X_test` DataFrames.  The `rf2` model is expecting to have `review_scores_sum` as an input column as well. Even if `X_test` had the same number of columns as the processed data we trained on, the line above will still error since it does not have our custom truncated `trunc_lat` and `trunc_long` columns.
# MAGIC 
# MAGIC To fix this, we could manually re-apply the same pre-processing logic to the `X_test` set each time we wish to use our model. 
# MAGIC 
# MAGIC However, there is a cleaner and more streamlined way to account for our pre-processing steps. We can define a custom model class that automatically pre-processes the raw input it receives before passing that input into the trained model's `.predict()` function. This way, in future applications of our model, we will no longer have to worry about remembering to pre-process every batch of data beforehand.
# MAGIC 
# MAGIC Complete the `preprocess_input(self, model_input)` helper function of the custom `RFWithPreprocess` class so that the random forest model is always predicting off of a DataFrame with the correct column names and the appropriate number of columns.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Adding Pre-Processing and Post-Processing Steps
# MAGIC In the demo notebook, we built a custom `RFWithPreprocess` model class that uses a `preprocess_input(self, model_input)` helper function to automatically pre-processes the raw input it receives before passing that input into the trained model's `.predict()` function.
# MAGIC 
# MAGIC Now suppose we are not as interested in a numerical prediction as we are in a categorical label of `Expensive` and `Not Expensive` where the cut-off is above a price of $100. Instead of retraining an entirely new classification model, we can simply add on a post-processing step to our custom model so it returns the predicted label instead of numerical price.
# MAGIC 
# MAGIC Complete the following model class with **both the previous preprocess steps and the new `postprocess_result(self, result)`** function such that passing in `X_test` into our model will return an `Expensive` or `Not Expensive` label for each row.

# COMMAND ----------

# TODO
# Define the model class
class RFWithPostprocess(mlflow.pyfunc.PythonModel):

    def __init__(self, trained_rf):
        self.rf = trained_rf

    def preprocess_input(self, model_input):
        '''return pre-processed model_input'''
        # FILL_IN
        return 
      
    def postprocess_result(self, results):
        '''return post-processed results
        Expensive: predicted price > 100
        Not Expensive: predicted price <= 100'''
        # FILL_IN
        return 
    
    def predict(self, context, model_input):
        processed_model_input = self.preprocess_input(model_input.copy())
        results = self.rf.predict(processed_model_input)
        return self.postprocess_result(results)

# COMMAND ----------

# MAGIC %md
# MAGIC Create, save, and apply the model to `X_test`.

# COMMAND ----------

# Construct and save the model
model_path =  f"{working_dir}/RFWithPostprocess/"

try:
  shutil.rmtree(model_path.replace("dbfs:", "/dbfs")) # remove folder if already exists
except:
  None

rf_postprocess_model = RFWithPostprocess(trained_rf = rf2)
mlflow.pyfunc.save_model(path=model_path.replace("dbfs:", "/dbfs"), python_model=rf_postprocess_model)

# Load the model in `python_function` format
loaded_postprocess_model = mlflow.pyfunc.load_model(model_path.replace("dbfs:", "/dbfs"))

# Apply the model
loaded_postprocess_model.predict(X_test)

# COMMAND ----------

# MAGIC %md
# MAGIC Given any unmodified raw data, our model can perform the pre-processing steps, apply the trained model, and follow the post-processing step all in one `.predict` function call!
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/icon_note_24.png"/> See the solutions folder for an example solution to this lab.

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC <h2><img src="https://files.training.databricks.com/images/105/logo_spark_tiny.png"> Next Steps</h2>
# MAGIC 
# MAGIC Head to the next lesson, [Model Registry]($../02-Model-Registry).

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2021 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>