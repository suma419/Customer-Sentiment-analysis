
import boto3

# 🔐 Paste your actual credentials here temporarily just to verify it works
aws_access_key_id = "AKIAxxxxxxxxxxxxxxxx"
aws_secret_access_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

try:
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-2"
    )

    sts = session.client("sts")
    identity = sts.get_caller_identity()
    print("✅ Credentials working! Account info:")
    print(identity)

except Exception as e:
    print("❌ Credentials failed:", str(e))
