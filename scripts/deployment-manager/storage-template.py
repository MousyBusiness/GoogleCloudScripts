"""Creates the Cloud Storage buckets for iot-ingestion."""


def GenerateConfig(context):
    resources = [{
        'name': 'iot-ingestion-bucket',
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
                            "age": 90,
                            "isLive": True
                        }
                    }
                ]
            }
        },
    },{
        'name': 'temporary-iot-ingestion-bucket',
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
                            "age": 30,
                            "isLive": True
                        }
                    }
                ]
            }
        },
    }]
    return {'resources': resources}
