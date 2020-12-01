"""Creates the Dataflow pipeline."""

def GenerateConfig(context):
    resources = [{
        'name': 'dataflow-iot-pipeline',
        'type': context.env["project"]+'/dataflow:dataflow.projects.locations.templates.launch',
        'properties': {
              'projectId': context.env["project"],
              'location': 'europe-west2',
              'gcsPath': 'gs://dataflow-templates-europe-west2/latest/Cloud_PubSub_to_Avro',
              'jobName': 'dataflow-iot-ingestion-pipeline',
              'environment': {
                'bypassTempDirValidation': False,
                'maxWorkers': 1,
                'numWorkers': 1,
                'machineType': 'n1-standard-1',
                'tempLocation': 'gs://$(ref.temporary-iot-ingestion-bucket.name)/temp',
                'ipConfiguration': 'WORKER_IP_UNSPECIFIED'
              },
              'parameters': {
                'inputTopic': 'projects/'+context.env["project"]+'/topics/'+context.properties["topic"],
                'outputDirectory': 'gs://$(ref.iot-ingestion-bucket.name)',
                'windowDuration': '10m',
                'avroTempDirectory': 'gs://$(ref.temporary-iot-ingestion-bucket.name)/avro'
              }
        }
    }]
    return {'resources': resources}
