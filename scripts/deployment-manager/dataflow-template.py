"""Creates the Dataflow pipeline."""


def GenerateConfig(context):
    name = context.env['name']
    job_name = context.properties['jobName']
    min_workers = context.properties.get('minWorkers', 1)
    max_workers = context.properties.get('maxWorkers', 1)
    machine_type = context.properties.get('machineType', 'n1-standard-1')
    window_duration = context.properties.get('windowDuration', '10m')
    template = context.properties.get('template', 'gs://dataflow-templates-europe-west2/latest/Cloud_PubSub_to_Avro')
    output_bucket = context.properties['outputBucket']
    temp_bucket = context.properties['tempBucket']

    resources = [{
        'name': name,
        'type': context.env["project"] + '/dataflow:dataflow.projects.locations.templates.launch',
        'properties': {
            'projectId': context.env['project'],
            'location': 'europe-west2',
            'gcsPath': template,
            'jobName': job_name,
            'environment': {
                'bypassTempDirValidation': False,
                'numWorkers': min_workers,
                'maxWorkers': max_workers,
                'machineType': machine_type,
                'tempLocation': '{}/temp'.format(temp_bucket),
                'ipConfiguration': 'WORKER_IP_UNSPECIFIED'
            },
            'parameters': {
                'inputTopic': 'projects/' + context.env['project'] + '/topics/' + context.properties["topic"],
                'outputDirectory': output_bucket,
                'windowDuration': window_duration,
                'avroTempDirectory': '{}/avro'.format(temp_bucket)
            }
        }
    }]
    return {'resources': resources}
