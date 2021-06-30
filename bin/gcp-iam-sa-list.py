#!/usr/bin/env python
'''
..moduleauthor:: Mike Pietruszka <mike@mpietruszka.com>
..summary:: Display IAM roles and Service Account details
..note::
    - sys.argv[1]: GCP Project ID
'''

import googleapiclient.discovery
import sys

iam = googleapiclient.discovery.build('iam', 'v1')
project = sys.argv[1]
compute_url = "https://www.googleapis.com/compute/v1/projects/"

iam_roles = iam.projects().roles().list(parent=f"projects/{project}").execute()
print("IAM Roles:")
for role in iam_roles['roles']:
    print(role)

print("\nIAM Service Accounts:")
service_accounts = iam.projects().serviceAccounts().list(name=f"projects/{project}").execute()
for sa in service_accounts['accounts']:
    print(sa)
    key = iam.projects().serviceAccounts().keys().list(name=sa['name']).execute()
    print(key)

