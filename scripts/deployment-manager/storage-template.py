"""Creates the Cloud Storage bucket."""


def GenerateConfig(context):
    name = context.env['name']
    delete_after = context.properties['deleteAfter']
    resources = [{
        'name': name,
        'type': 'gcp-types/storage-v1:buckets',
        'properties': {
            'location': 'europe-west2',
            'storageClass': 'STANDARD',
            "lifecycle": {
                "rule": [
                    {
                        "action": {
                            "type": "Delete"
                        },
                        "condition": {
                            "age": delete_after,
                            # https://cloud.google.com/storage/docs/lifecycle#islive
                            "isLive": True
                        }
                    }
                ]
            }
        },
    }]
    return {'resources': resources}
