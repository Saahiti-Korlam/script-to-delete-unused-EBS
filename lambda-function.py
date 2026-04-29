import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_snapshots(OwnerIds:'self')

instance_response = ec2.describe_instances(Filters[{'Name':'instance_name','Value':['running']}])
active_instance_ids = set()

for reservation in instance_response[Reservations]:
    for instance in reservation[Instances]:
        active_instance_ids.add(instance.['InstanceId'])

for snapshot in response['Snapshots']:
    snapshot_id=snapshot['SnapshotId']
    volume_id=snapshot.get('VolumeId')
    if not volume_id:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        print("Deleted Snapshot {snapshot_id} as it is no longer attached to any volume")
     else :
        #check if volume still exists
        try :
            volume_response = ec2.describe_volumes(VolumeId=[volume_id])
            if not in volume_response[Volumes][0][Attachments]:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print("Deleted EBS snapshot {snapshot_id} as it was taken from a volume not attached to any running instance.")
            except  ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound' :
                  ec2.delete_snapshot(SnapshotId=snapshot_id)
                  print(f"Deleted EBS snapshot {snapshot_id} as its associated volume was not found.")  

