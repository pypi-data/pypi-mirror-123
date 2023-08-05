import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.models.measurement_rows import DepthMeasurementRows
from cognite.well_model.client.models.resource_list import DepthMeasurementDataList, DepthMeasurementList
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.client.utils._identifier_list import identifier_list
from cognite.well_model.client.utils.constants import DEFAULT_LIMIT
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import (
    DepthMeasurement,
    DepthMeasurementDataItems,
    DepthMeasurementDataRequest,
    DepthMeasurementDataRequestItems,
    DepthMeasurementFilter,
    DepthMeasurementFilterRequest,
    DepthMeasurementItems,
    DistanceRange,
)

logger = logging.getLogger(__name__)


class MeasurementsAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)

        @extend_class(DepthMeasurement)
        def data(
            this: DepthMeasurement,
            measured_depth: Optional[DistanceRange] = None,
        ):
            return self.list_data(
                [
                    DepthMeasurementDataRequest(
                        sequence_external_id=this.source.sequence_external_id,
                        measured_depth=measured_depth,
                        measurement_types=[x.measurement_type for x in this.columns],
                    )
                ]
            )[0]

    def ingest(self, measurements: List[DepthMeasurement]) -> DepthMeasurementList:
        """
        Ingests a list of measurements into WDL

        @param measurements: list of measurements to ingest
        @return: list of ingested measurements
        """
        path = self._get_path("/measurements/depth")
        json = DepthMeasurementItems(items=measurements).json()
        response: Response = self.client.post(path, json)
        return DepthMeasurementList(DepthMeasurementItems.parse_raw(response.text).items)

    def list(
        self,
        wellbore_asset_external_ids: Optional[List[str]] = None,
        wellbore_matching_ids: Optional[List[str]] = None,
        measurement_types: Optional[List[str]] = None,
        limit: Optional[int] = DEFAULT_LIMIT,
    ) -> DepthMeasurementList:
        def request(cursor, limit):
            identifiers = identifier_list(wellbore_asset_external_ids, wellbore_matching_ids)
            path = self._get_path("/measurements/depth/list")
            json = DepthMeasurementFilterRequest(
                filter=DepthMeasurementFilter(
                    wellbore_ids=identifiers,
                    measurement_types=measurement_types,
                ),
                limit=limit,
                cursor=cursor,
            ).json()
            response: Response = self.client.post(path, json)
            measurement_items = DepthMeasurementItems.parse_raw(response.text)
            return measurement_items

        items = cursor_multi_request(
            get_cursor=lambda x: x.next_cursor,
            get_items=lambda x: x.items,
            limit=limit,
            request=request,
        )
        return DepthMeasurementList(items)

    def list_data(self, measurement_data_request_list: List[DepthMeasurementDataRequest]) -> DepthMeasurementDataList:
        """
        Get multiple measurement data by a list of DepthMeasurementDataRequest

        @param measurement_data_request_list: list of DepthMeasurementDataRequest
        @return: list of MeasurementData objects
        """
        measurement_data_request_items = DepthMeasurementDataRequestItems(items=measurement_data_request_list)
        path = self._get_path("/measurements/depth/data")
        response: Response = self.client.post(url_path=path, json=measurement_data_request_items.json())
        items = DepthMeasurementDataItems.parse_raw(response.text).items
        items = [DepthMeasurementRows.from_measurement_data(x) for x in items]
        return DepthMeasurementDataList(items)
