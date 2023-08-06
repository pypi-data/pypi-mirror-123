def athenatos3(sqlquery, database, bucket_name, module_name, outputs3):
    import boto3, time

    athena_client = boto3.client('athena', 
                          aws_access_key_id="AKIAQKI62VBAQ6LZPNW3", 
                          aws_secret_access_key="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", 
                          region_name="ap-southeast-1"
                          )


    s3_client = boto3.client('s3', 
                          aws_access_key_id="AKIAQKI62VBAQ6LZPNW3", 
                          aws_secret_access_key="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", 
                          region_name="ap-southeast-1"
                          )


    queryStart = athena_client.start_query_execution(
                        QueryString = sqlquery,
                        QueryExecutionContext = {'Database': database}, 
                        ResultConfiguration = {'OutputLocation': f's3://{bucket_name}/{module_name}'}
                        )

    queryStart


    #executes query and waits 3 seconds
    queryId = queryStart['QueryExecutionId']


    #copies newly generated csv file with appropriate name
    #query result output location you mentioned in AWS Athena
    queryLoc = f"{bucket_name}/{module_name}/{queryId}.csv"

    copy_source = {
        'Bucket': bucket_name,
        'Key': f"{module_name}/{queryId}.csv"
     }
    s3_client.copy(copy_source, bucket_name, f'{module_name}/{outputs3}')


    BUCKET = copy_source['Bucket']
    KEY = copy_source['Key']
    response = s3_client.delete_object(Bucket=BUCKET, Key=KEY)

    response = s3_client.delete_object(
        Bucket = bucket_name,
        Key = f"{module_name}/{queryId}.csv.metadata"
    )

    print('csv generated')