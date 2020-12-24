"""Creates the Cloud Storage bucket."""


def GenerateConfig(context):
    name = context.env['name']
    description = context.properties.get('description', 'deployment manager generated')
    direction = context.properties.get('direction', 'INGRESS')
    priority = context.properties.get('priority', 1000)
    tag = context.properties['tag']
    ports = context.properties['ports']
    source_ranges = context.properties['source_ranges']

    resources = [{
        'name': name,
        'type': 'compute.v1.firewall',
        'properties': {
            'description': description,
            'direction': direction,
            'priority': priority,
            'targetTags': [tag],
            'allowed': [{
                'IPProtocol': 'tcp',
                'ports': ports
            }],
            'sourceRanges': source_ranges
        },
    }]
    return {'resources': resources}
