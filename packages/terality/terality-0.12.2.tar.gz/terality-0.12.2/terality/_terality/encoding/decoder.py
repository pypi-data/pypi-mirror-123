from typing import Any, Callable, Dict
from common_client_scheduler.requests_responses import AwsCredentials

import pandas as pd
from common_client_scheduler.structs import IndexType

from terality_serde import StructType
from common_client_scheduler import (
    Display,
    ExportResponse,
    StructRef,
    IndexColNames,
    PandasIndexMetadata,
    PandasSeriesMetadata,
    PandasDFMetadata,
    NDArrayMetadata,
)
from terality_serde.json_encoding import (
    DFParquetEncoding,
    decode_df_inplace,
)

from .. import DataTransfer, copy_to_user_s3_bucket
from ..utils.azure import test_for_azure_libs, parse_azure_filesystem
from .. import global_client


def _deserialize_display(
    aws_credentials: AwsCredentials, to_display: Display
):  # pylint: disable=unused-argument,useless-return
    # No need to force it in package dependencies, if it gets called it means we are in a Jupyter Notebook
    # and and this dependency is present
    # noinspection PyUnresolvedReferences
    from IPython.display import display, HTML

    display(HTML(to_display.value))


def _deserialize_export(aws_credentials: AwsCredentials, export: ExportResponse) -> None:
    path = export.path
    transfer_id = export.transfer_id
    if path.startswith("s3://"):
        copy_to_user_s3_bucket(aws_credentials, transfer_id, export.aws_region, path)
    elif path.startswith("abfs://") or path.startswith("az://"):
        test_for_azure_libs()
        from ..data_transfers.azure import copy_to_azure_datalake

        storage_account_name, container, path = parse_azure_filesystem(path, export.storage_options)
        copy_to_azure_datalake(
            aws_credentials=aws_credentials,
            transfer_id=transfer_id,
            aws_region=export.aws_region,
            storage_account_name=storage_account_name,
            container=container,
            path_template=path,
        )
    else:
        DataTransfer.download_to_local_files(
            global_client().get_download_config(),
            aws_credentials,
            transfer_id,
            path,
            export.is_folder,
        )


def _download_ndarray_from_metadata(
    aws_credentials: AwsCredentials, ndarray_metadata: NDArrayMetadata
):
    # noinspection PyTypeChecker
    # TODO use np.load, but we have to upload accordingly within scheduler ndarray_to_numpy_metadata.
    df = _download_df(
        aws_credentials=aws_credentials,
        transfer_id=ndarray_metadata.transfer_id,
        encoding=ndarray_metadata.encoding,
    )
    assert len(df.columns) == 1
    return df.iloc[:, 0].to_numpy()


def _download_df(
    aws_credentials: AwsCredentials, transfer_id: str, encoding: DFParquetEncoding
) -> pd.DataFrame:
    client = global_client().get_download_config()
    bytes_io = DataTransfer.download_to_bytes(client, aws_credentials, transfer_id)
    df = pd.read_parquet(bytes_io)
    decode_df_inplace(df, encoding)
    return df


def _rename_index(index: pd.Index, index_col_names: IndexColNames):
    if isinstance(index, pd.MultiIndex):
        index.names = index_col_names.names
    index.name = index_col_names.name


def _download_index_from_metadata(
    aws_credentials: AwsCredentials, index_metadata: PandasIndexMetadata
) -> pd.Index:
    """
    Download index data from S3, using index_metadata information retrieved from scheduler,
    and build the corresponding pandas index.
    """

    df = _download_df(aws_credentials, index_metadata.transfer_id, encoding=index_metadata.encoding)
    if len(df.columns) > 1:
        index = pd.MultiIndex.from_arrays([df.iloc[:, i] for i in range(len(df.columns))])
    elif index_metadata.type_ == IndexType.INT64_INDEX:
        index = pd.Int64Index(data=df.iloc[:, 0])
    elif index_metadata.type_ == IndexType.FLOAT64_INDEX:
        index = pd.Float64Index(data=df.iloc[:, 0])
    elif index_metadata.type_ == IndexType.DATETIME_INDEX:
        index = pd.DatetimeIndex(data=df.iloc[:, 0])
    elif index_metadata.type_ == IndexType.INDEX:
        index = pd.Index(data=df.iloc[:, 0])
    else:
        raise ValueError(f"Uknown index subclass {index_metadata.type_}")
    _rename_index(index, index_metadata.index_col_names)
    return index


def _download_series_from_metadata(
    aws_credentials: AwsCredentials, series_metadata: PandasSeriesMetadata
) -> pd.Series:
    df = _download_df(
        aws_credentials=aws_credentials,
        transfer_id=series_metadata.transfer_id,
        encoding=series_metadata.encoding,
    )
    series = df.iloc[:, 0]
    series.name = series_metadata.series_name
    _rename_index(series.index, series_metadata.index_col_names)
    return series


def _download_df_from_metadata(
    aws_credentials: AwsCredentials, df_metadata: PandasDFMetadata
) -> pd.DataFrame:
    df = _download_df(
        aws_credentials=aws_credentials,
        transfer_id=df_metadata.transfer_id,
        encoding=df_metadata.encoding,
    )
    df.columns = df_metadata.col_names
    df.columns.name = df_metadata.col_names_name  # type: ignore
    _rename_index(df.index, df_metadata.index_col_names)
    return df


_decoder: Dict[Any, Callable[[AwsCredentials, Any], Any]] = {
    NDArrayMetadata: _download_ndarray_from_metadata,
    PandasIndexMetadata: _download_index_from_metadata,
    PandasSeriesMetadata: _download_series_from_metadata,
    PandasDFMetadata: _download_df_from_metadata,
    Display: _deserialize_display,
    ExportResponse: _deserialize_export,
}


def decode(credentials_fetcher: AwsCredentials, obj):  # pylint: disable=invalid-name
    from terality import (
        NDArray,
        Index,
        Int64Index,
        Float64Index,
        DatetimeIndex,
        MultiIndex,
        Series,
        DataFrame,
    )  # To avoid circular dependencies
    from terality._terality.terality_structures import DataFrameGroupBy, SeriesGroupBy

    structs = {
        IndexType.INDEX: Index,
        IndexType.INT64_INDEX: Int64Index,
        IndexType.FLOAT64_INDEX: Float64Index,
        IndexType.DATETIME_INDEX: DatetimeIndex,
        IndexType.MULTI_INDEX: MultiIndex,
        StructType.NDARRAY: NDArray,
        StructType.SERIES: Series,
        StructType.DATAFRAME: DataFrame,
        StructType.SERIES_GROUPBY: SeriesGroupBy,
        StructType.DATAFRAME_GROUPBY: DataFrameGroupBy,
    }

    if isinstance(obj, StructRef):
        # noinspection PyProtectedMember
        # NOTE: hash(StrEnum.X) = hash(StrEnum.X.value)
        return structs[obj.type]._new(id_=obj.id)  # type: ignore
    if type(obj) in _decoder:
        return _decoder[type(obj)](credentials_fetcher, obj)
    return obj
