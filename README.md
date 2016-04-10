# FileWatcher
FileWatcher is a script that checks if there has been an update to a remote file, e.g. list of trades published by 
a stock exchange. 

This script was originally written to be run as an *AWS Lambda* instance which stores version hash in an S3 bucket and 
publishes notifications using Amazon SNS. 

## Deployment
In order to deploy the script in AWS for your use case you need to:

1. Set ```FILE_URL``` to the url of the file your script will be watching
2. Set ```S3_BUCKET_NAME``` to the name of your bucket you want to use for storing hash of the current version of the 
document
3. Set ```S3_FILE_KEY``` to the key that will be used to identify the document in the bucket.
4. Set ```SNS_TOPIC_ARN``` to the ARN identifier of the SNS topic that will publish events on any update to the document
5. Set ```EMAIL_SUBJECT``` and ```EMAIL_BODY``` which will be used as subject and body of the SNS message, respectively.

## Additional Notes
* Make sure you create appropriate roles and policies to set up permissions for different AWS resources. All of it 
can be done quite easily from the console. 

