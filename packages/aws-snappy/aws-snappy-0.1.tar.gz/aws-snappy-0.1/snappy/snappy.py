import boto3
import  snappy.utils.constants as Consts
from snappy.instance import Instance
from snappy.utils import helper as Helper

class Snappy():

    def __init__(self, instances):

        # Create an empty list of instances
        self.instances = []

        # Create the boto3 EC2 client
        client = boto3.client('ec2')

        # Describe all instances
        response = client.describe_instances(
            Filters=Consts.filter_boto3_instance_retrieval(instances)
        )

        # Filter and append Instances
        for r in response['Reservations']:

            for i in r['Instances']:

                self.instances.append(Instance(i))
                
        # Verify if all instances were retrieved successfully
        if Helper.has_errors(instances, self.instances):
            
            # Retrieve the failing instances
            failed_instances = Helper.retrieve_failed_instances(instances, self.instances)
            
            # Raise the exception
            raise Exception(Consts.EXCEPTION_MESSAGE_INSTANCES_RETRIEVAL_FAILED.format(str(failed_instances)))
        
    def snap_roots(self, tags_specifications=None):
        
        # Make root snapshots for each instances and return the list of output
        return [instance.snap_root(tags_specifications) for instance in self.instances]