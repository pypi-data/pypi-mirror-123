# xr.backends.BackendEntrypoint
import xarray as xr
import os
import pandas as pd

class IoapiBackendEntrypoint(xr.backends.BackendEntrypoint):
    available = 1
    def open_dataset(self,
                     filename_or_obj,
                     mask_and_scale=True,
                     decode_times=True,
                     concat_characters=True,
                     decode_coords=True,
                     drop_variables=None,
                     use_cftime=None,
                     decode_timedelta=None,
                     group=None,
                     mode='r',
                     format=None,
                     clobber=True,
                     diskless=False,
                     persist=False,
                     lock=None,
                     autoclose=False, ):

        if drop_variables is None:
            drop_variables = ["COL", "ROW"]

        store = xr.backends.NetCDF4DataStore.open(
            filename_or_obj,
            mode=mode,
            format=format,
            clobber=clobber,
            diskless=diskless,
            persist=persist,
            lock=lock,
            autoclose=autoclose,
        )

        store_entrypoint = xr.backends.store.StoreBackendEntrypoint()

        with xr.core.utils.close_on_error(store):
            dataset = store_entrypoint.open_dataset(
                store,
                mask_and_scale=mask_and_scale,
                decode_times=decode_times,
                concat_characters=concat_characters,
                decode_coords=decode_coords,
                drop_variables=drop_variables,
                use_cftime=use_cftime,
                decode_timedelta=decode_timedelta,
            )
        dataset = self._set_datatime_coords(dataset)
        return dataset

    def _set_datatime_coords(self, dataset):
        idims = len(dataset.TFLAG.dims)
        if idims == 2:
            tflag1 = pd.Series(dataset['TFLAG'][:, 0]).astype(str).str.zfill(7)
            tflag2 = pd.Series(dataset['TFLAG'][:, 1]).astype(str).str.zfill(6)
        else:
            tflag1 = pd.Series(dataset['TFLAG'][:, 0, 0]).astype(str).str.zfill(7)
            tflag2 = pd.Series(dataset['TFLAG'][:, 0, 1]).astype(str).str.zfill(6)
        date = pd.to_datetime(
            [i + j for i, j in zip(tflag1, tflag2)], format='%Y%j%H%M%S')
        indexdates = pd.Series(date).drop_duplicates(keep='last').index.values
        dataset = dataset.isel(TSTEP=indexdates)
        dataset['TSTEP'] = date[indexdates]
        return dataset
