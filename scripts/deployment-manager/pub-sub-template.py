"""Creates the PubSub iot-ingestion topic."""


def GenerateConfig(context):
    resources = [{
        'name': 'iot-ingestion-topic',
        'type': 'gcp-types/pubsub-v1:projects.topics',
        'properties': {
            'topic': 'iot-ingestion'
        },
    }]
    return {'resources': resources}
