from typing import List, Optional, Tuple
from uuid import UUID

from pydantic import BaseModel


class CreateDatasetRequest(BaseModel):
    name: str


class Dataset(BaseModel):
    name: str
    id: UUID
    size: int


class CreateDatasetResponse(BaseModel):
    id: UUID


class ColumnImport(BaseModel):
    name: str
    column: Optional[str] = None


class ColumnGroupListItem(BaseModel):
    id: UUID
    name: str


class Column(BaseModel):
    id: UUID
    name: str


class ColumnGroup(BaseModel):
    id: UUID
    name: str
    size: int
    type: str
    path: str
    columns: List[Column]


class TimeseriesImport(BaseModel):
    columns: List[ColumnImport]
    type: str = "timeseries"


class CreateColumnGroupRequest(BaseModel):
    """
    Attributes:
        name: Name of ColumnGroupListItem to create
        columns: List of columns to import (excluding id_column and timestamp_column)
        type: str or ColumnGroupType that is a valid enum
        from_path: Path to read in Parquet
        filter_statement: Optional filter statement to apply when reading in data. See pyarrow.ParquetDataset
        id_column: Column name that will form the recording_id column on the ColumnGroupListItem
        timestamp_columns: Name of column(s) to read timestamps from
    """

    name: str
    columns: List[ColumnImport]
    type: str
    from_path: str
    filter_statement: Optional[List[List[tuple]]] = None
    id_column: str
    timestamp_columns: List[str]
