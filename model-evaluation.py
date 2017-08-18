# coding: utf-8
# Step 2. Load predictions. Execute the first cell to load the classes used in this activity:
from pyspark.sql import SQLContext
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics

sqlContext = SQLContext(sc)
predictions = sqlContext.read.load('file:///home/cloudera/Downloads/big-data-4/predictions.csv', 
                          format='com.databricks.spark.csv', 
                          header='true',inferSchema='true')

# Step 3. Compute accuracy. Let's create an instance of MulticlassClassificationEvaluator to determine the accuracy of the predictions:
evaluator = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction", metricName="precision")
accuracy = evaluator.evaluate(predictions)
print("Accuracy = %g " % (accuracy))

# Step 4. Display confusion matrix. The MulticlassMetrics class can be used to generate a confusion matrix of our classifier model. However, unlike MulticlassClassificationEvaluator, MulticlassMetrics works with RDDs of numbers and not DataFrames, so we need to convert our predictions DataFrame into an RDD.
predictions.rdd.take(2)
predictions.rdd.map(tuple).take(2)
metrics = MulticlassMetrics(predictions.rdd.map(tuple))
metrics.confusionMatrix().toArray().transpose()

