import pytest
from snappy.utils.helper import has_errors, retrieve_failed_instances


###########################
####### Test Models #######
###########################
class MyInstanceT:
    
    def __init__(self, private_ip) -> None:
        self.private_ip = private_ip
        
class TestHelper:
    
    testdata = [
        (["X","X","X"], ["X","X"], True),
        (["X"], [], True),
        ([], ["X"], True),
        (["X","X","X"], ["X","X","X"], False),
        (["X"], ["X"], False),
        ([], [], False),
    ]
    @pytest.mark.parametrize("previous_instances,retrieved_instances,expected_result", testdata)
    def test_has_errors(self, previous_instances, retrieved_instances, expected_result):
        
        # Arrange
        
        # Act
        result = has_errors(previous_instances, retrieved_instances)
        
        # Assert
        assert expected_result == result
    
    
    testdata = [
        (
            ["10.10.10.1", "10.10.10.2","10.10.10.3", "10.10.10.4"], 
            [MyInstanceT("10.10.10.1"), MyInstanceT("10.10.10.3")], 
            ["10.10.10.2", "10.10.10.4"]
        ),
        (
            ["10.10.10.1", "10.10.10.2","10.10.10.3","10.10.10.4"], 
            [MyInstanceT("10.10.10.1"), MyInstanceT("10.10.10.2"), MyInstanceT("10.10.10.3")], 
            ["10.10.10.4"]
        ),
        (
            ["10.10.10.1",], 
            [], 
            ["10.10.10.1"]
        ),
        (
            ["10.10.10.1", "10.10.10.2","10.10.10.3", "10.10.10.4"], 
            [MyInstanceT("10.10.10.1"), MyInstanceT("10.10.10.2"), MyInstanceT("10.10.10.3"), MyInstanceT("10.10.10.4")], 
            []
        ),
        (
            ["10.10.10.1", "10.10.10.2","10.10.10.3", "10.10.10.4"], 
            [], 
            ["10.10.10.1", "10.10.10.2","10.10.10.3", "10.10.10.4"]
        ),
    ]
    @pytest.mark.parametrize("previous_instances,retrieved_instances,expected_result", testdata)
    def test_retrieve_failed_instancess(self, previous_instances, retrieved_instances, expected_result):
        
        # Arrange
        
        # Act
        result = retrieve_failed_instances(previous_instances, retrieved_instances)
        
        # Assert
        assert expected_result == result