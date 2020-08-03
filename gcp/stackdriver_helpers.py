from google.cloud import monitoring_v3
import time
import numpy as np

def create_metric(project_name, name, description):
    """
    Function for creating a metric to track in stackdriver. 
    NOTE: should only have to be run once. Needs credentials to GCP project.

    inputs
    -----
    project_name: name of project
    name: str, name of metric; example 'accuracy_metric', this becomes the descriptor.name
    description: str, description of metric
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(project_name)
    descriptor = monitoring_v3.types.MetricDescriptor()
    descriptor.type = 'custom.googleapis.com/' + name
    descriptor.metric_kind = (
        monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE)
    descriptor.value_type = (
        monitoring_v3.enums.MetricDescriptor.ValueType.DOUBLE)
    descriptor.description = description
    descriptor = client.create_metric_descriptor(project_name, descriptor)
    
    print(f'Created {descriptor.name}.')


def delete_metric(descriptor_name):
    """
    Function to delete metric.

    inputs
    -----
    descriptor_name: name of metric, ex 'projects/my-project-name/metricsDescriptors/custom.googleapis.com/test1'
    """
    client = monitoring_v3.MetricServiceClient()
    client.delete_metric_descriptor(descriptor_name)
    print('Deleted metric descriptor {}.'.format(descriptor_name))

def add_metric_point(project_name, metric_name, metric_value):
    """
    Function for adding data point for dashboard.

    inputs
    ------
    metric_name: name of metric, will be appended to beginning of series.metric.type, ex 'custom.googleapis.com/' + test_metric_1105'
    metric_value: numeric value to be added

    returns
    ------
    none, value added.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(project_name)
    series = monitoring_v3.types.TimeSeries()
    series.metric.type = 'custom.googleapis.com/' + metric_name
    series.resource.type = 'global'
    # series.resource.labels['project_id'] = project
    # series.resource.labels['zone'] = 'us-central1-a'
    # series.resource.labels['cluster_name'] = 'heavy-hitters'
    point = series.points.add()
    point.value.double_value = metric_value
    now = time.time()
    point.interval.end_time.seconds = int(now)
    point.interval.end_time.nanos = int(
        (now - point.interval.end_time.seconds) * 10**9)
    client.create_time_series(project_name, [series])

def write_to_stackdriver(project_name, metric_dict):
    """
    Uses a dictionary where the k = Stackdriver metric_name and v = Stackdriver metric to
    write to Stackdriver.

    ex. {'metric_name1': metric_value1,
        'metric_name2': metric_value2 }
    """
    for k, v in metric_dict.items():
        print(f'Writing metric_name {k} to Stackdriver.')  # this could be replaced by logger instead.
        add_metric_point(project_name, k, v)