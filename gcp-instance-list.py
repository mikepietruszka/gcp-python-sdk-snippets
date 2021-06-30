#!/usr/bin/env python
'''
..moduleauthor:: Mike Pietruszka <mike@mpietruszka.com>
..summary:: List GCP Compute Engine instances
..note::
    - sys.argv[1]: GCP Project ID
    - sys.argv[2]: Compute Engine Region
'''

import googleapiclient.discovery
import sys

compute = googleapiclient.discovery.build('compute', 'v1')
project = sys.argv[1]
region = sys.argv[2]
compute_url = "https://www.googleapis.com/compute/v1/projects/"

zones = compute.zones().list(project=project).execute()
our_zones = []
for zone in zones['items']:
    if "us-central1" in zone['region']:
        our_zones.append(zone['name'])

print("Live instances:")
for zone in our_zones:
    result = compute.instances().list(project=project, zone=zone).execute()
    if result.get('items'):
        for result in result['items'] if 'items' in result else None:
            print(result['name'],
                  result['networkInterfaces'][0]['networkIP'],
                  result['networkInterfaces'][0]['accessConfigs'][0]['natIP'],
                  result['tags']
                  )
    else:
        print(f"WARN: Did not find any instances in zone: {zone}")

instance_ops_request = compute.zoneOperations().list(project=project, zone=zone)
while instance_ops_request is not None:
    print("\nInstance operations:")
    instance_ops_result = instance_ops_request.execute()

    for result in instance_ops_result['items'] \
            if 'items' in instance_ops_result else None:
        print(result['name'],
              result['operationType'],
              result['targetLink'].replace(
                  f"{compute_url}{project}/", ''),
              result['status'],
              result['progress']
              )
    instance_ops_request = compute.zoneOperations().list_next(
        previous_request=instance_ops_request,
        previous_response=instance_ops_result
    )
