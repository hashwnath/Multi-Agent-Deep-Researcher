import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def test_s3_connection():
    """Test S3 connection and list files in your bucket"""
    
    # Get credentials from environment or AWS config
    session = boto3.Session(region_name='us-east-2')
    s3_client = session.client('s3')
    
    bucket_name = 'athena-output-spotify11'
    prefix = 'Unsaved/2025/05/28/'
    
    try:
        print(f"🔍 Testing S3 connection to bucket: {bucket_name}")
        print(f"📍 Region: us-east-2")
        print(f"📁 Prefix: {prefix}")
        print("-" * 50)
        
        # List objects in your bucket
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=10
        )
        
        if 'Contents' in response:
            print(f"✅ Found {len(response['Contents'])} files:")
            for obj in response['Contents']:
                print(f"   📄 {obj['Key']}")
                print(f"      Size: {obj['Size']} bytes")
                print(f"      Last Modified: {obj['LastModified']}")
                print()
        else:
            print("⚠️ No files found in the specified prefix")
            
        print("✅ S3 connection successful!")
        
    except Exception as e:
        print(f"❌ S3 connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your AWS credentials")
        print("2. Verify bucket name and region")
        print("3. Ensure you have read permissions")

if __name__ == "__main__":
    test_s3_connection() 