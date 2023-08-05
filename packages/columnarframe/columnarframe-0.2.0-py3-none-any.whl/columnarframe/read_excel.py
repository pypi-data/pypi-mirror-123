from openpyxl import load_workbook

from .frame import ColumnarFrame
from .utils import skip_footer
from .utils import make_key


def convert(cell, datefmt):
    if cell is not None and cell.value is None:
        return None

    if cell.data_type == 's':
        return str(cell.value)
    if cell.data_type == 'd':
        if datefmt is None:
            return str(cell.value)
        return cell.value.strftime(datefmt)
    if cell.data_type == 'n':
        return str(cell.value)
    if cell.data_type == 'b':
        return str(cell.value)

    raise RuntimeError('Unknown data type.')


def read_excel(
    filename,
    type='xlsx',
    sheet=None,
    skiprows=0,
    skipfooter=0,
    header=True,
    datefmt=None,
):
    wb = load_workbook(filename=filename)
    if sheet is None:
        ws = wb.active
    else:
        pass

    data = {}
    for idx, r in enumerate(ws.columns):
        if skiprows > 0:
            rit = iter(r[skiprows:])
        else:
            rit = iter(r)
        if header:
            key = make_key(idx, next(rit).value)
        else:
            key = str(idx)

        data[key] = [convert(c, datefmt) for c in rit]

    data = skip_footer(data, skipfooter)

    return ColumnarFrame(data)
