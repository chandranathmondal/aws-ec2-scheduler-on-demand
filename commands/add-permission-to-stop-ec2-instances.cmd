aws lambda add-permission \
--function-name stop-ec2-instances \
--statement-id events-invoke-function \
--action lambda:InvokeFunction \
--principal events.amazonaws.com \
--source-arn arn:aws:events:<AWS_REGION>:<AWS_ACCOUNT_ID>:rule/*
