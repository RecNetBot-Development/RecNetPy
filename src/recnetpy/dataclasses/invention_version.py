from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..misc.api_responses import CurrentVersion

class InventionVersion:
    """
    This object is an invention partial that represents a version of an invention.
    """

    #: This is the invention's unique identifier.
    invention_id: int
    replication_id: str
    #: This is an integer that represents a version of the invention.
    version_number: int
    blob_name: str
    blob_hash: str
    #: This is the precentage of ink an invention requires.
    instantiation_cost: float
    #: This is the light cost for the invention.
    lights_cost: int
    #: This is the CV2 cost for the invention.
    chips_cost: int
    #: This is the amount of clould variable resources required.
    cloud_variables_cost: int

    def __init__(self, data: 'CurrentVersion') -> None:
        self.invention_id = data['InventionId']
        self.replication_id = data['ReplicationId']
        self.version_number = data['VersionNumber']
        self.blob_name = data['BlobName']
        self.blob_hash = data['BlobHash']
        self.instantiation_cost = round(data['InstantiationCost'] / 300, 1) if data['InstantiationCost'] else 0
        self.lights_cost = data['LightsCost']
        self.chips_cost = data['ChipsCost']
        self.cloud_variables_cost = data['CloudVariablesCost']