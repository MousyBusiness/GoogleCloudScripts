"""Creates Compute Instance Template."""


def GenerateConfig(context):
    name = context.env['name']
    description = context.properties.get('description', 'deployment manager generated')
    source_image = context.properties['sourceImage']
    machine_type = context.properties.get('machineType', 'f1-micro')
    service_account = context.properties.get('serviceAccount', 'default')
    startup_script = context.properties.get('startupScript')
    shutdown_script = context.properties.get('shutdownScript')
    preemptible = context.properties.get('preemptible', False)
    network_tags = context.properties.get('networkTags', [])

    vm = {
        'name': name,
        'type': 'compute.v1.instanceTemplate',
        'properties': {
            'properties': {
                'description': description,
                'machineType': machine_type,
                'canIpForward': False,
                'scheduling':
                    {
                        'preemptible': preemptible,
                        'onHostMaintenance': 'TERMINATE' if preemptible else 'MIGRATE',
                        'automaticRestart': False if preemptible else True,
                    },
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': source_image
                    }
                }],
                'serviceAccounts': [{
                    'email': service_account,
                    'scopes': ['https://www.googleapis.com/auth/cloud-platform'],
                }],
                'networkInterfaces': [{
                    'network': 'projects/{}/global/networks/default'.format(context.env['project']),
                    'accessConfigs': [{
                        'name': 'External NAT',
                        'type': 'ONE_TO_ONE_NAT'
                    }],
                }],
                'metadata': {
                    'items': []
                },
                'tags': {
                    'items': network_tags,
                },
            },
        }
    }

    if startup_script:
        vm['properties']['properties']['metadata']['items'].append({
            'key': 'startup-script',
            'value': startup_script,
        })

    if shutdown_script:
        vm['properties']['properties']['metadata']['items'].append({
            'key': 'shutdown-script',
            'value': shutdown_script,
        })

    return {'resources': [vm]}
