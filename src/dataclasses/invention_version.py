from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..misc.api_responses import CurrentVersion

class InventionVersion:
    invention_id: int
    replication_id: str
    version_number: int
    blob_name: str
    blob_hash: str
    instantiation_cost: int
    lights_cost: int
    chips_cost: int
    cloud_variables_cost: int

    def __init__(self, data: 'CurrentVersion') -> None:
        self.invention_id = data['InventionId']
        self.replication_id = data['ReplicationId']
        self.version_number = data['VersionNumber']
        self.blob_name = data['BlobName']
        self.blob_hash = data['BlobHash']
        self.instantiation_cost = data['InstantiationCost']
        self.lights_cost = data['LightsCost']
        self.chips_cost = data['ChipsCost']
        self.cloud_variables_cost = data['CloudVariablesCost']