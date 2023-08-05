import json
import os
import tempfile
from http import HTTPStatus
from typing import List
from uuid import UUID

import pyarrow as pa
import pyarrow.parquet as pq

import requests
from pydantic import parse_obj_as
from requests import HTTPError

from .catalog_session import CatalogSession
from .models import (
    Dataset,
    CreateDatasetRequest,
    ColumnGroup,
    ColumnGroupListItem,
    CreateColumnGroupRequest,
    CreateDatasetResponse,
)
from .exceptions import CatalogRequestError, ColumnGroupExists, FramesMetadataExists


def create_dataset(session: CatalogSession, dataset_name: str) -> Dataset:
    create_request = CreateDatasetRequest(name=dataset_name)
    r = session.post(f"datasets", json=create_request.dict())
    r.raise_for_status()
    dataset_info = CreateDatasetResponse.parse_obj(r.json())
    r = session.get(f"datasets/{dataset_info.id}")
    # TODO: Raise for status in CatalogSession
    r.raise_for_status()
    target_dataset = Dataset.parse_obj(r.json())
    return target_dataset


def delete_dataset(session: CatalogSession, dataset: Dataset):
    r = session.delete(f"/datasets/{dataset.id}")
    r.raise_for_status()


def fetch_or_create_dataset(session: CatalogSession, dataset_name: str) -> Dataset:
    r = session.get(f"datasets")
    r.raise_for_status()
    datasets = parse_obj_as(List[Dataset], r.json())
    # TODO(gunnar): Should be able to inject query through endpoint instead of this hack
    target_dataset = next((d for d in datasets if d.name == dataset_name), None)
    if target_dataset is None:
        target_dataset = create_dataset(session, dataset_name)
    return target_dataset


def upload_local_file_to_catalog(session: CatalogSession, dataset, pq_path, series_name):
    with open(pq_path, mode="rb") as file:
        try:
            r = session.post(
                f"/datasets/{dataset.id}/column_groups/import",
                files={"file": file},
                data={"name": series_name, "columns": json.dumps([{"name": series_name}]), "type": "timeseries"},
            )
            r.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == HTTPStatus.CONFLICT:
                raise ColumnGroupExists(e)
            else:
                raise CatalogRequestError(e)


def add_or_replace_column_group(
    session: CatalogSession, dataset: Dataset, create_request: CreateColumnGroupRequest
) -> UUID:
    try:
        return add_column_group(session, dataset, create_request)
    except ColumnGroupExists:
        delete_column_group(session, dataset, create_request.name)
        return add_column_group(session, dataset, create_request)


def fetch_column_groups(session: CatalogSession, dataset: Dataset) -> List[ColumnGroup]:
    r = session.get(f"datasets/{dataset.id}/column_groups")
    r.raise_for_status()
    return parse_obj_as(List[ColumnGroup], r.json())


def delet_frames_metadata(session: CatalogSession, dataset: Dataset):
    try:
        session.delete(f"/datasets/{dataset.id}/frames_metadata")
    except HTTPError as e:
        raise CatalogRequestError(e)


def add_frames_metadata(session: CatalogSession, dataset: Dataset, path: str):
    try:
        r = session.post(f"/datasets/{dataset.id}/frames_metadata", json={"path": path})
        r.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == HTTPStatus.CONFLICT:
            raise FramesMetadataExists(e)
        else:
            raise CatalogRequestError(e)


def add_or_replace_frames_metadata(session: CatalogSession, dataset: Dataset, cloud_path: str):
    try:
        add_frames_metadata(session, dataset, cloud_path)
    except FramesMetadataExists:
        delet_frames_metadata(session, dataset)
        add_frames_metadata(session, dataset, cloud_path)


# TODO: Get rid of method? This is painfully slow.
def upload_and_overwrite_frames_metadata(session: CatalogSession, dataset: Dataset, pq_path: str):
    """Uploads a parquet file via form upload (NOTE: Very slow!)

    Args:
        session: CatalogSession
        dataset: Dataset to upload to
        pq_path: Local parquet path to upload to server
    """
    try:
        upload_frame_references(session, dataset, pq_path)
    except FramesMetadataExists:
        delet_frames_metadata(session, dataset)
        upload_frame_references(session, dataset, pq_path)


def upload_frame_references(session: CatalogSession, dataset: Dataset, pq_path: str):
    with open(pq_path, mode="rb") as file:
        try:
            r = session.post(
                f"/datasets/{dataset.id}/frames_metadata/upload",
                files={"file": file},
            )
            r.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == HTTPStatus.CONFLICT:
                raise FramesMetadataExists(e)
            else:
                raise CatalogRequestError(e)


def add_column_group(session: CatalogSession, dataset: Dataset, create_request: CreateColumnGroupRequest):
    try:
        r = session.post(f"/datasets/{dataset.id}/column_groups", json=create_request.dict())
        r.raise_for_status()
        return UUID(r.json()["id"])
    except HTTPError as e:
        if e.response.status_code == HTTPStatus.CONFLICT:
            raise ColumnGroupExists(e)
        else:
            raise CatalogRequestError(e)


def import_table(session: CatalogSession, dataset: Dataset, pa_new: pa.Table, series_name: str):
    with tempfile.TemporaryDirectory() as new_dir:
        out_path = os.path.join(new_dir, f"{series_name}.parquet")
        pq.write_table(pa_new, out_path)

        try:
            upload_local_file_to_catalog(session, dataset, out_path, series_name)
        except HTTPError as e:
            if e.response.status_code == HTTPStatus.CONFLICT:
                # TODO: Handle versioning on other side. This conflict resolution needs fixing
                delete_column_group(session, dataset, series_name)
                upload_local_file_to_catalog(session, dataset, out_path, series_name)


def delete_column_group(session: CatalogSession, dataset: Dataset, column_group_name: str):
    r = session.get(f"/datasets/{dataset.id}/column_groups")
    r.raise_for_status()
    column_groups = parse_obj_as(List[ColumnGroupListItem], r.json())
    target_group = next((g for g in column_groups if g.name == column_group_name), None)
    # TODO: How do we do safe deleting? Have some grace period where things can be reverted?
    if target_group is not None:
        r = session.delete(f"/datasets/{dataset.id}/column_groups/{target_group.id}")
        r.raise_for_status()
    else:
        raise ValueError(
            f"Trying to delete non-existent column_group '{column_group_name}' in {dataset}. Candidates where {column_groups}"
        )
