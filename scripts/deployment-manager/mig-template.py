"""Creates Managed Instance Group with Healthcheck."""


def GenerateConfig(context):
    name = context.env['name']
    zone = context.properties['zone']
    min_instances = context.properties['minInstances']
    max_instances = context.properties['maxInstances']
    preemptible = context.properties.get('preemptible', False)
    service_account = context.properties.get('serviceAccount', 'default')
    cmds = context.properties.get('cmds', [])


#/var/log/daemon.log - debugging startup script

    startup_script = '''                
#!/bin/bash
# install logging agent
curl -sSO https://dl.google.com/cloudagents/add-logging-agent-repo.sh
sudo bash add-logging-agent-repo.sh
sudo apt-get update
sudo apt-get install -y google-fluentd
sudo apt-get install -y google-fluentd-catch-all-config
sudo service google-fluentd start
# install monitoring agent
curl -sSO https://dl.google.com/cloudagents/add-monitoring-agent-repo.sh
sudo bash add-monitoring-agent-repo.sh
sudo apt-get update
sudo apt-get install -y stackdriver-agent
sudo service stackdriver-agent start
'''

    for cmd in cmds:
        startup_script+=cmd+"\n"

    shutdown_script = '''        
#!/bin/bash
echo "shutting down"
'''

    resources = [{
        'name': 'healthcheck',
        'type': 'firewall-rule-template.py',
        'properties': {
            'description': 'allow http traffic for managed instance and load balancer health checks',
            'tag': 'healthcheck',
            'ports': [80],
            'source_ranges': ['35.191.0.0/16', '130.211.0.0/22'],
        },
    }, {
        'name': '{}-vm'.format(name),
        'type': 'compute-template.py',
        'properties': {
            'description': 'webscraper',
            'sourceImage': 'https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/ubuntu-minimal-1804-bionic-v20201216',
            'preemptible': preemptible,
            'networkTags': ['healthcheck'],
            'serviceAccount': service_account,
            'startupScript': startup_script,
            'shutdownScript': shutdown_script,
        },
    }, {
        'name': '{}-mig'.format(name),
        'type': 'compute.v1.instanceGroupManagers',
        'properties': {
            'baseInstanceName': name,
            'instanceTemplate': '$(ref.{}-vm.selfLink)'.format(name),
            'targetSize': min_instances,
            'autoHealingPolicies': [{
                'initialDelaySec': 60
            }],
            'zone': zone
        },
    }, {
        'name': '{}-as'.format(name),
        'type': 'compute.v1.autoscaler',
        'properties': {
            'target': '$(ref.{}-mig.selfLink)'.format(name),
            'autoscalingPolicy': {
                'minNumReplicas': min_instances,
                'maxNumReplicas': max_instances,
                'cpuUtilization': {
                    'utilizationTarget': 0.8
                },
                'coolDownPeriodSec': 180
            },
            'zone': zone
        },
    }]
    return {'resources': resources}
