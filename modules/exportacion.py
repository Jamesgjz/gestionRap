from io import BytesIO

from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell


def crear_excel(headers, rows):
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("Gestión RAP")
    sheet.append(headers)
    for row in rows:
        cells = []
        for value in row:
            if isinstance(value, str):
                cell = WriteOnlyCell(sheet, value=value)
                cell.data_type = "s"
                cells.append(cell)
            else:
                cells.append(value)
        sheet.append(cells)
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()
