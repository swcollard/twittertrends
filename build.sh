# /bin/sh

##
# Build script for project. Cleans, generates, and uploads build artifacts to AWS Lambda.
##

rm twittertrends.zip
zip -r twittertrends.zip *
aws lambda update-function-code --function-name TwitterTrends --zip-file fileb://twittertrends.zip 
