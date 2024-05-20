# file_uploader.py MinIO Python SDK example
from minio import Minio
from minio.error import S3Error
import urllib3
def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.

    client = Minio(
        "116.63.35.72:9000",
        access_key="cLuAvJjxwX7PJs7IUzRL",
        secret_key="80pT8fpk4DAtWqRSK4tEu5hyU5ho7EQQTAcpXag8",
        secure=False
    )
    bucket_name = "imagebucket"
    print(client.list_buckets())
    objects = client.list_objects("imagebucket",prefix='test2017/')
    for obj in objects:
        url = client.presigned_get_object(bucket_name,obj.object_name)
        print(url)
    # # The file to upload, change this path if needed
    # source_file = "/tmp/test-steven-file.txt"
    #
    # # The destination bucket and filename on the MinIO server
    # bucket_name = "python-test-bucket"
    # destination_file = "my-test-file.txt"
    #
    # # Make the bucket if it doesn't exist.
    # found = client.bucket_exists(bucket_name)
    # if not found:
    #     client.make_bucket(bucket_name)
    #     print("Created bucket", bucket_name)
    # else:
    #     print("Bucket", bucket_name, "already exists")
    #
    # # Upload the file, renaming it in the process
    # client.fput_object(
    #     bucket_name, destination_file, source_file,
    # )
    # print(
    #     source_file, "successfully uploaded as object",
    #     destination_file, "to bucket", bucket_name,
    # )

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)