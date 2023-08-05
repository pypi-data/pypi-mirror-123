import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.api.merge_rules.wells import WellMergeRulesAPI
from cognite.well_model.client.models.property_filter import DontCare, PropertyFilter, filter_to_model
from cognite.well_model.client.models.resource_list import WellList
from cognite.well_model.client.utils._identifier_list import identifier_items, identifier_items_single
from cognite.well_model.client.utils.constants import DEFAULT_LIMIT
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import (
    AssetSource,
    DateRange,
    DeleteWells,
    DistanceRange,
    IdentifierItems,
    PolygonFilter,
    Well,
    WellDepthMeasurementFilter,
    WellFilter,
    WellFilterRequest,
    WellIngestion,
    WellIngestionItems,
    WellItems,
    WellNdsFilter,
    WellNptFilter,
    WellSearch,
    WellTimeMeasurementFilter,
    WellTrajectoryFilter,
)

logger = logging.getLogger(__name__)


class WellsAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)
        self.merge_rules = WellMergeRulesAPI(client)

    def ingest(self, ingestions: List[WellIngestion]) -> WellList:
        path = self._get_path("/wells")
        json = WellIngestionItems(items=ingestions).json()
        response: Response = self.client.post(path, json)
        well_items: WellItems = WellItems.parse_obj(response.json())
        items: List[Well] = well_items.items
        return WellList(items)

    def delete(self, well_sources: List[AssetSource]):
        path = self._get_path("/wells/delete")
        json = DeleteWells(items=well_sources).json()
        self.client.post(path, json)

    # guranteed to be non-empty list
    def _retrieve_multiple(self, identifiers: IdentifierItems) -> List[Well]:
        path: str = self._get_path("/wells/byids")
        response: Response = self.client.post(url_path=path, json=identifiers.json())
        wells: List[Well] = WellItems.parse_raw(response.text).items
        return wells

    def retrieve(self, asset_external_id: Optional[str] = None, matching_id: Optional[str] = None) -> Well:
        """
        Get well by asset external id or matching id

        @param asset_external_id: Well asset external id
        @param matching_id: Well matching id
        @return: Well object
        """
        identifiers = identifier_items_single(asset_external_id, matching_id)
        return self._retrieve_multiple(identifiers)[0]

    def retrieve_multiple(
        self, asset_external_ids: Optional[List[str]] = None, matching_ids: Optional[List[str]] = None
    ) -> WellList:
        """
        Get wells by a list of asset external ids and matching ids

        @param asset_external_ids: list of well asset external ids
        @param matching_ids: List of well matching ids
        """
        identifiers = identifier_items(asset_external_ids, matching_ids)
        return WellList(self._retrieve_multiple(identifiers))

    def list(
        self,
        string_matching: Optional[str] = None,
        quadrants: PropertyFilter = DontCare,
        regions: PropertyFilter = DontCare,
        blocks: PropertyFilter = DontCare,
        fields: PropertyFilter = DontCare,
        operators: PropertyFilter = DontCare,
        sources: Optional[List[str]] = None,
        water_depth: Optional[DistanceRange] = None,
        spud_date: Optional[DateRange] = None,
        well_types: PropertyFilter = DontCare,
        licenses: PropertyFilter = DontCare,
        trajectories: Optional[WellTrajectoryFilter] = None,
        depth_measurements: Optional[WellDepthMeasurementFilter] = None,
        time_measurements: Optional[WellTimeMeasurementFilter] = None,
        npt: Optional[WellNptFilter] = None,
        nds: Optional[WellNdsFilter] = None,
        polygon: Optional[PolygonFilter] = None,
        output_crs: Optional[str] = None,
        limit: Optional[int] = DEFAULT_LIMIT,
    ) -> WellList:
        """
        Get wells that matches the filter

        @param string_matching - string to fuzzy match on description and name
        @param quadrants - list of quadrants to find wells within
        @param regions - list of regions to find wells within
        @param blocks - list of blocks to find wells within
        @param fields - list of fields to find wells within
        @param operators - list of well operators to filter on
        @param sources - list of source system names
        @param water_depth - list of water depths
        @param spud_date - list of spud dates
        @param licenses - list of well licenses
        @param well_types - list of well types, for example exploration
        @param trajectories - filter wells which have trajectory between certain depths
        @param measurements - filter wells which have measurements between certain depths in their logs
        @param npt - filter wells on Npt
        @param nds - filter wells on Nds
        @param polygon - geographic area to find wells within
        @param output_crs - crs for the returned well head
        @param limit - number of well objects to fetch
        @return: WellItems object
        """

        def request(cursor, limit):
            search = WellSearch(query=string_matching) if string_matching else None
            well_filter = WellFilterRequest(
                filter=WellFilter(
                    quadrant=filter_to_model(quadrants),
                    region=filter_to_model(regions),
                    block=filter_to_model(blocks),
                    field=filter_to_model(fields),
                    operator=filter_to_model(operators),
                    well_type=filter_to_model(well_types),
                    license=filter_to_model(licenses),
                    sources=sources,
                    water_depth=water_depth,
                    spud_date=spud_date,
                    trajectories=trajectories,
                    depth_measurements=depth_measurements,
                    time_measurements=time_measurements,
                    polygon=polygon,
                    npt=npt,
                    nds=nds,
                ),
                search=search,
                output_crs=output_crs,
                cursor=cursor,
                limit=limit,
            )
            path: str = self._get_path("/wells/list")
            response: Response = self.client.post(url_path=path, json=well_filter.json())
            well_items_data: WellItems = WellItems.parse_raw(response.text)
            return well_items_data

        items = cursor_multi_request(
            get_cursor=lambda x: x.next_cursor, get_items=lambda x: x.items, limit=limit, request=request
        )
        return WellList(items)
