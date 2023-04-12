import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images=[
        ('LouisLi.jpg', 'Louis Li')
        # ('LouisLi2.jpg', 'Louis Li-2')
    ]

# Iterate through list to upload objects to S3  
# this will trigger s3 lambda 
for image in images:
    #rb = opens the file in binary format for reading
    file = open("./resources/" + image[0],'rb')
    object = s3.Object('analyst-photos', image[0])
    ret = object.put(Body=file, Metadata={
            "FullName": image[1]
        })