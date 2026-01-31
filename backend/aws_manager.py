import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

class AWSService:
    def __init__(self):
        # AWS Credentials loaded from environment or ~/.aws/credentials
        self.ec2 = boto3.client(
            'ec2',
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.s3 = boto3.client('s3')

    def get_instances(self):
        """List all EC2 instances and their status (Free Tier Friendly)"""
        try:
            response = self.ec2.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        "id": instance['InstanceId'],
                        "type": instance['InstanceType'],
                        "state": instance['State']['Name'],
                        "public_ip": instance.get('PublicIpAddress', 'N/A')
                    })
            return instances
        except ClientError as e:
            print(f"AWS Error: {e}")
            return []

    def start_instance(self, instance_id):
        """Start a stopped instance."""
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])
            return {"status": "starting", "instance_id": instance_id}
        except ClientError as e:
            return {"error": str(e)}

    def stop_instance(self, instance_id):
        """Stop a running instance."""
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            return {"status": "stopping", "instance_id": instance_id}
        except ClientError as e:
            return {"error": str(e)}

    def reboot_instance(self, instance_id):
        """Reboot an instance."""
        try:
            self.ec2.reboot_instances(InstanceIds=[instance_id])
            return {"status": "rebooting", "instance_id": instance_id}
        except ClientError as e:
            return {"error": str(e)}

    def terminate_instance(self, instance_id):
        """Terminate an instance."""
        try:
            self.ec2.terminate_instances(InstanceIds=[instance_id])
            return {"status": "terminating", "instance_id": instance_id}
        except ClientError as e:
            return {"error": str(e)}
