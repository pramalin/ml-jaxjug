# Step 1. Open Jupyter Python Notebook. 
# Step 2. Load classes and data. Execute the first cell in the notebook to load the classes used for this exercise.
from pyspark.sql import SQLContext
from pyspark.sql import DataFrameNaFunctions
from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import Binarizer
from pyspark.ml.feature import VectorAssembler, StringIndexer, VectorIndexer

# Next, execute the second cell which loads the weather data into a DataFrame and prints the columns
sqlContext = SQLContext(sc)
df = sqlContext.read.load('file:///home/cloudera/Downloads/big-data-4/daily_weather.csv', 
                          format='com.databricks.spark.csv', 
                          header='true',inferSchema='true')
# df.columns
# Execute the third cell, which defines the columns in the weather data we will use for the decision tree classifier.
featureColumns = ['air_pressure_9am','air_temp_9am','avg_wind_direction_9am','avg_wind_speed_9am',
        'max_wind_direction_9am','max_wind_speed_9am','rain_accumulation_9am',
        'rain_duration_9am']

# Step 3. Drop unused and missing data. We do not need the number column in our data, so let's remove it from the DataFrame:
df = df.drop('number')
df = df.na.drop()
# df.count(), len(df.columns)

# Step 4. Create categorical variable. Let's create a categorical variable to denote if the humidity is not low. If the value is less than 25%, then we want the categorical value to be 0, otherwise the categorical value should be 1. We can create this categorical variable as a column in a DataFrame using Binarizer:
binarizer = Binarizer(threshold = 24.99999, inputCol="relative_humidity_3pm", outputCol="label")
binarizerDF = binarizer.transform(df)
# binarizerDF.select("relative_humidity_3pm", "label").show(4)

# Step 5. Aggregate features. Let's aggregate the features we will use to make predictions into a single column:
assembler = VectorAssembler(inputCols=featureColumns, outputCol="features")
assembled = assembler.transform(binarizerDF)

# Step 6. Split training and test data. We can split the data by calling randomSplit():
(trainingData, testData) = assembled.randomSplit([0.8, 0.2], seed = 13234)
# trainingData.count(), testData.count()

# Step 7. Create and train decision tree
dt = DecisionTreeClassifier(labelCol="label", featuresCol="features", maxDepth=5, minInstancesPerNode=20, impurity="gini")

# create model by executing the DT in Pipeline
pipeline = Pipeline(stages=[dt])
model = pipeline.fit(trainingData)

# make predictions
predictions = model.transform(testData)

# predictions.select("prediction", "label").show(10)

# Step 8. save results
predictions.select("prediction", "label").write.save(path="file:///home/cloudera/Downloads/big-data-4/predictions.csv", format="com.databricks.spark.csv", header='true')
