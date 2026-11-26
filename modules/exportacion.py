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
    from time import monotonic

    import streamlit as st

    from local_auth import current_account
    from sesion_navegador import cuentas_activas, sesiones

    identificador = st.session_state.get("rap_id")
    sesion_local = st.session_state.get("rap_session")

    def descargar():
        cuentas = cuentas_activas()
        if identificador is not None:
            autorizada = sesiones.validar(identificador, cuentas) is not None
        else:
            autorizada = current_account(sesion_local, cuentas, monotonic()) is not None
        if not autorizada:
            raise PermissionError("La sesión terminó. Vuelve a iniciar sesión.")
        return generar()

    return descargar

