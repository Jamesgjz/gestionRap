from io import BytesIO



def crear_excel(headers, rows):
    from openpyxl import Workbook
    from openpyxl.cell import WriteOnlyCell

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


def descarga_autorizada(generar):
    import streamlit as st

    from web_auth import COOKIE_NAME, cuentas, sesiones

    token = st.context.cookies.get(COOKIE_NAME)

    def descargar():
        if sesiones.validar(token, cuentas()) is None:
            raise PermissionError("La sesión terminó. Vuelve a iniciar sesión.")
        return generar()

    return descargar
