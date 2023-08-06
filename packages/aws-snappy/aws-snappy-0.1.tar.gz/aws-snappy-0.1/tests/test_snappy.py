from snappy.snappy import Snappy

class TestSnappy:
    
    # Uncomment to perform snapshot test
    # def test_snappy_snap_roots(self):
        
    #     # Arrange
    #     instances = ["172.31.255.50", "172.31.255.20"]
    #     tags_specifications = [{
    #         "Key": "CreatorName",
    #         "Value": "mervin.hemaraju@checkout.com"
    #     }]
        
    #     # Act
    #     try:
    #         snappy = Snappy(instances)
            
    #         snapshots = snappy.snap_roots(tags_specifications)
            
    #         print(f"test_snappy_snap_roots: {snapshots}")
            
    #     except Exception as e:
    #         result = str(e)
            
    #         print(f"test_snappy_snap_roots: {result}")
            
    #     # Assert
    #     assert False
    
    def test_snappy_initialization_AbnormalData(self):
        
        # Arrange
        instances = ["172.31.255.50", "10.0.0.0"]
        expected_result = "The following instances could not be retrieved: ['10.0.0.0']"
        
        # Act
        try:
            snappy = Snappy(instances)
            
            result = "Failed"
        except Exception as e:
            result = str(e)
            
        # Assert
        assert result == expected_result
    
    def test_snappy_initialization_NormalData(self):
        
        # Arrange
        instances = ["172.31.255.50", "172.31.255.20"]
        expected_result = "Passed"
        
        # Act
        try:
            snappy = Snappy(instances)
            
            result = "Passed"
        except Exception as e:
            result = str(e)
            
        # Assert
        assert result == expected_result