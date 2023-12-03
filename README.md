# GroupMeSpamBlocker

To deploy:
  0. Create GroupMe bot
  1. Put handler in lambda function
  2. Run sls deploy (this will require the serverless.yml file in the same directory)
  3. Set AWS secrets (token, botID) to what is listed in your GroupMe developer portal

Debugging:
Use CloudWatch to check if your Lambda function is being called (the URL endpoint should be in the configuration section of the function to insert into your groupme bot). Errors can be found in the CloudWatch Log Group for the Lambda Function.
