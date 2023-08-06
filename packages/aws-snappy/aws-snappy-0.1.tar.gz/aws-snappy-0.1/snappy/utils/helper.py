

def has_errors(previous_instances, retrieved_instances):
    
    # Check if some instances were not retrieved
    return len(previous_instances) != len(retrieved_instances)

def retrieve_failed_instances(previous_instances, retrieved_instances):
    
    # Retrieve the private IPs to manipulate
    retrieved_instances_ip = [instance.private_ip for instance in retrieved_instances]
    
    # Return all ip addresses not located in the retrieved instances
    return [ip for ip in previous_instances if ip not in retrieved_instances_ip]