# Hyper


In this section, we provide a wrapper to use Hyper. 


Simple usage is 

```
resp = Hyper().up(
    name="mnist",
    docker="pytorch/pytorch:latest", 
    pu='k80', 
    command=['python examples/mnist/main.py']
)
```

Example output
```
resp = {'ID': 'nukvsa-ff0fe92d-c8aa-41b4-bd9c-08219328b633', 
        'Name': 'ingest-', 
        'State': 'created', 
        'IPs': [], 
        'Nodes': [], 
        'Tasks': [
        {'ExperimentId': 'nukvsa-ff0fe92d-c8aa-41b4-bd9c-08219328b633', 
        'Commands': ['python3 /hub/dataset/ingest.py --bucket_in=intelinair-processing-agmri \
            --bucket_out=snark-intelinair-export --csv_path=intelinair/ingest/test_v023003/annotations.csv \
            --dataset=intelinair/ingest/test_v023003 --field_start=0 --field_end=10 --max_field_size=51200 \
            --workers=4'], 
        'Container': 'snarkai/hub:latest-production', 
        'ContainerPrivate': True, 
        'State': 'created', 
        'TaskId': 'xpopye-0a680505-d407-4459-95d3-f268c5b30e07', 
        'Timestamp': '1582028220.3952734', 
        'AssignedNode': 'None', 
        'ClusterId': 'hoqpgg-3d6ee359-4ff6-44ab-9a32-c2148537ae33', 
        'StatusSnapshot': 
            {'timestamp': [0], 'docker_logs': [''], 'cpu_util': ['NaN'], 'cpu_ram_util': ['NaN'], 'gpu_util': ['NaN'], 'gpu_ram_util': ['NaN']}, 
            'mount': {'gepkrvqy': '/snark'}}], 
        'Clusters': [{'UserId': 'davit', 'ExperimentId': 'nukvsa-ff0fe92d-c8aa-41b4-bd9c-08219328b633', 'Machine': {'type': 'm5.4xlarge', 'price': '0.8', 'spot_price': '0.768', 'spot': False}, 
        'Credentials': {}, 'Workers': 1, 'State': 'provisioning', 'ClusterId': 'hoqpgg-3d6ee359-4ff6-44ab-9a32-c2148537ae33', 'Timestamp': '1582028220.3631854', 'EndTimestamp': ' '}], 
        'Configs': {'name': 'ingest-', 'docker_url': 'snarkai/hub:latest-production', 'container_private': True, 
        'command': ['python3 /hub/dataset/ingest.py --bucket_in=intelinair-processing-agmri --bucket_out=snark-intelinair-export --csv_path=intelinair/ingest/test_v023003/annotations.csv --dataset=intelinair/ingest/test_v023003 --field_start=0 --field_end=10 --max_field_size=51200 --workers=4'], 
        'params': {}, 'samples': 1, 'credentials': {'access_key': None, 'secret_key': None, 'region': None, 'zone': None}, 'workers': 1, 'hardware': {'type': 'm5.4xlarge', 'price': '0.8', 'spot_price': '0.768', 'spot': False}, 'recovery': False, 'volumes': {}, 'mounts': {'gepkrvqy': '/snark'}}}]

```
