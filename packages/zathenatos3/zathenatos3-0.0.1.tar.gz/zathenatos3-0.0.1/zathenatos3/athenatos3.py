class athenatos3:

    def __init__(self, sqlquery, database, bucket_name, module_name, outputs3):
        self.sqlquery = sqlquery
        self.database = database
        self.bucket_name = bucket_name
        self.module_name = module_name
        self.outputs3 = outputs3


    def athenatos3(self):
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
                            QueryString = self.sqlquery,
                            QueryExecutionContext = {'Database': self.database}, 
                            ResultConfiguration = {'OutputLocation': f's3://{self.bucket_name}/{self.module_name}'}
                            )

        queryStart


        #executes query and waits 3 seconds
        queryId = queryStart['QueryExecutionId']


        #copies newly generated csv file with appropriate name
        #query result output location you mentioned in AWS Athena
        copy_source = {
            'Bucket': self.bucket_name,
            'Key': f"{self.module_name}/{queryId}.csv"
        }
        s3_client.copy(copy_source, self.bucket_name, f'{self.module_name}/{self.outputs3}')


        BUCKET = copy_source['Bucket']
        KEY = copy_source['Key']
        s3_client.delete_object(Bucket=BUCKET, Key=KEY)

        s3_client.delete_object(
            Bucket = self.bucket_name,
            Key = f"{self.module_name}/{queryId}.csv.metadata"
        )

        print('csv generated')
