from __future__ import annotations

from typing import Optional

from .exceptions import APIKeyNotSuppliedError
from .api_handles import APIObject
from .processing_request_base import (JSONProcessingRequest,
                                      FieldZonationBase, ObservationBase)


def auth(api_key: Optional[str] = None) -> User:
    """Autheticates user with an API key.

    Args:
        api_key (str): API key to use DynaCrop services. You can acquire one
            at https://dynacrop.space/.

    Raises:
        APIKeyNotSuppliedError: If API key is not supplied.

    Returns:
        User: User endpoint. Information about a user associated with
            the API key.
    """

    if not api_key:
        raise APIKeyNotSuppliedError()
    return User()


class User(APIObject):
    """User endpoint object"""
    editable_attrs: Optional[set] = {}
    endpoint: str = 'user'

    def __init__(self):
        """Creates User endpoint object"""
        super(User, self).__init__('')


class Polygon(APIObject):
    """Polygon endpoint object"""
    editable_attrs: Optional[set] = {
        'max_mean_cloud_cover',
        'label',
        'smi_enabled'}
    endpoint: str = 'polygons'

    @classmethod
    def create(cls,
               geometry: str,
               label: Optional[str] = None,
               max_mean_cloud_cover: Optional[str] = None,
               smi_enabled: bool = False) -> APIObject:
        """Creates Polygon endpoint object.

        Args:
            geometry (str): Valid polygon shape in
                Well Known Text (WKT) representation
                (see: https://bit.ly/2WDzRym).
            label (Optional[str], optional): Description to the Polygon
                (user field). Defaults to None.
            max_mean_cloud_cover (Optional[str], optional): Maximum mean cloud
                coverage in decimal percentage (i.e. 0.3). Defaults to None.
            smi_enabled (bool, optional): To enable Soil Moisture Index
                pre-computation. Defaults to False.

        Returns:
            APIObject: APIObject instantiated into Polygon child.
        """
        return super(Polygon, cls). \
            create(
                geometry=geometry,
                label=label,
                max_mean_cloud_cover=max_mean_cloud_cover,
                smi_enabled=smi_enabled)


class TimeSeries(JSONProcessingRequest):
    """Time series endpoint object. Time series is the service of
DynaCrop API."""
    rendering_type = 'time_series'

    @classmethod
    def create(cls,
               polygon: Polygon,
               layer: str,
               date_from: str,
               date_to: str) -> APIObject:
        """Creates Time series endpoint object.

        Args:
            polygon (Polygon): Polygon endpoint object.
            layer (str): Should be Layer enumration. One of the DynaCrop API
                layers. See https://bit.ly/3D779ph for further information.
            date_from (str): Date to record time series from.
            date_to (str): Date to record time series to.

        Returns:
            APIObject: APIObject instatiated into TimeSeries child.
        """
        return super(TimeSeries, cls).create(polygon_id=polygon.id,
                                             rendering_type=cls.rendering_type,
                                             layer=layer.value,
                                             date_from=date_from,
                                             date_to=date_to)


class Observation(ObservationBase):
    """Observation endpoint object. Observation is the service of
DynaCrop API."""
    rendering_type = 'observation'

    @classmethod
    def create(cls,
               polygon: Polygon,
               layer: str,
               date_from: str,
               date_to: str) -> APIObject:
        """Creates Observation endpoint object.

        Args:
            polygon (Polygon): Polygon endpoint object.
            layer (str): Should be Layer enumration. One of the DynaCrop API
                layers. See https://bit.ly/3D779ph for further information.
            date_from (str): Date to watch for observation from.
            date_to (str): Date to watch for observation to.

        Returns:
            APIObject: APIObject instatiated into Observation child.
        """
        return super(Observation, cls). \
            create(
                polygon_id=polygon.id,
                rendering_type=cls.rendering_type,
                layer=layer.value,
                date_from=date_from,
                date_to=date_to)


class FieldZonation(FieldZonationBase):
    """Field zonation endpoint object. Field zonation is the service of
    DynaCrop API."""
    rendering_type = 'field_zonation'

    @classmethod
    def create(cls,
               polygon: Polygon,
               layer: str,
               date_from: str,
               date_to: str,
               number_of_zones: int = Optional[None]) -> APIObject:
        """Creates Field zonation endpoint object.

        Args:
            polygon (Polygon): Polygon endpoint object.
            layer (str): Should be Layer enumration. One of the DynaCrop API
                layers. See https://bit.ly/3D779ph for further information.
            date_from (str): Date to compute field zonation from.
            date_to (str): Date to compute field zonation to.
            number_of_zones (int): Number of zones to separate the field to.
                The number of thresholds must be one of 3, 5, 10, 20, 255.

        Returns:
            APIObject: APIObject instatiated into FieldZonation child.
        """
        return super(FieldZonation, cls). \
            create(
                polygon_id=polygon.id,
                rendering_type=cls.rendering_type,
                layer=layer.value,
                date_from=date_from,
                date_to=date_to,
                number_of_zones=str(number_of_zones))


class FieldZonationByMedian(FieldZonationBase):
    """Field zonation by median endpoint object. Field zonation by median
is the service of DynaCrop API."""
    rendering_type = 'field_zonation_by_median'

    @classmethod
    def create(cls,
               polygon: Polygon,
               layer: str,
               date_from: str,
               date_to: str,
               thresholds: list = Optional[None]) -> APIObject:
        """Creates Field zonation by median endpoint object.

        Args:
            polygon (Polygon): Polygon endpoint object.
            layer (str): Should be Layer enumration. One of the DynaCrop API
                layers. See https://bit.ly/3D779ph for further information.
            date_from (str): Date to compute field zonation by median from.
            date_to (str): Date to compute field zonation by median to.
            thresholds (int): Thresholds to zone the field in between.
                The number of thresholds must be one of 2, 4, 9, 19, 254.

        Returns:
            APIObject: APIObject instatiated into FieldZonationByMedian child.
        """
        return super(FieldZonationByMedian, cls).\
            create(
                polygon_id=polygon.id,
                rendering_type=cls.rendering_type,
                layer=layer.value,
                date_from=date_from,
                date_to=date_to,
                thresholds=thresholds)
