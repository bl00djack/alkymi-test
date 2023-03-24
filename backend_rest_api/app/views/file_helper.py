import io
import csv
import pandas


class FileTypeNotSupported(Exception):
    pass


class CSVReader:
    def __init__(self, f):
        self.file_data = io.StringIO(f.read().decode())

    def get_data(self, has_header_row=False):
        csv_reader = csv.reader(self.file_data)
        header = []
        rows = []
        for idx, row in enumerate(csv_reader):
            if has_header_row and idx == 0:
                header = row
            else:
                rows.append(row)
        return header, rows


class ExcelReader:
    def __init__(self, f):
        self.file_data = f.read()

    def get_data(self, has_header_row=False):
        pdheader = None if has_header_row is False else 0
        df = pandas.read_excel(self.file_data, header=pdheader)

        header = df.columns.values.tolist() if has_header_row else []
        rows = []

        buffer = io.StringIO()
        df.to_csv(buffer, index=False, header=pdheader)
        buffer.seek(0)
        csv_reader = csv.reader(buffer)
        for idx, row in enumerate(csv_reader):
            rows.append(row)
        return header, rows


class FileHelperFactory:
    file_readers = {
        "csv": CSVReader,
        "xls": ExcelReader,
        "xlsx": ExcelReader
    }

    @classmethod
    def get_reader(cls, f, file_extension):
        file_reader = cls.file_readers.get(file_extension)

        if file_reader is None:
            raise FileTypeNotSupported

        return file_reader(f)
