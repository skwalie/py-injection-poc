import pandas


class DataFrameProvider(object):
    def get_frame(self, series):
        pass

    def save(self, data_frame, file_name: str, export_format: int):
        pass


def save_to_excel(data_frame, file_name: str):
    return data_frame.to_excel(file_name)


def save_to_csv(data_frame, file_name: str):
    return data_frame.to_csv(file_name)


ExportFormatMethod = {
    0: save_to_excel,
    1: save_to_csv
}

ExportFormatExtension = {
    0: ".xlsx",
    1: ".csv"
}


class CursorDataFrameProvider(DataFrameProvider):
    def __init__(self):
        self._pandas = pandas

    def get_frame(self, series):
        # series arg must/should be a cursor in order to call list() (?)
        return self._pandas.DataFrame(list(series))

    def save(self, data_frame, file_name: str, export_format: int):
        save_method = ExportFormatMethod[export_format]

        if file_name.endswith(ExportFormatExtension[export_format]):
            return save_method(data_frame, file_name)
        else:
            return save_method(data_frame, file_name + ExportFormatExtension[export_format])

