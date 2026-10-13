#######################
# CHIEF MASTER
# Herramientas y APIs
#######################

import requests


class IntermediateTools:

    def __init__(self):
        self.base_banco_mundial = (
            "https://api.worldbank.org/v2/country"
        )

    # ==========================================
    # TIPO DE CAMBIO
    # ==========================================

    def consultar_tipo_cambio_api(self, moneda: str):
        if not moneda:
            return {"error": "Se requiere el código de la moneda."}

        moneda = moneda.strip().upper()

        if len(moneda) != 3 or not moneda.isalpha():
            return {"error": "Utiliza un código de moneda de tres letras, por ejemplo USD."}

        url = f"https://open.er-api.com/v6/latest/{moneda}"

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            datos = response.json()

            if datos.get("result") != "success":
                return {"error": "La API no pudo consultar esa moneda."}

            tasas = datos.get("rates", {})
            tasa_gtq = tasas.get("GTQ")

            resultado = {
                "moneda_base": moneda,
                "tasa_a_quetzales": tasa_gtq,
                "fecha_actualizacion": datos.get("time_last_update_utc"),
                "fuente": "ExchangeRate-API"
            }

            if tasa_gtq:
                resultado["tasa_inversa"] = round(1 / tasa_gtq, 6)

            return resultado

        except Exception as e:
            return {
                "error": f"No se pudo consultar el tipo de cambio: {str(e)}"
            }

    # ==========================================
    # CONSULTA GENERAL AL BANCO MUNDIAL
    # ==========================================

    def _consultar_indicador(self, pais: str, indicador: str, nombre: str):
        if not pais:
            return {"error": "Se requiere el código del país, por ejemplo GT."}

        pais = pais.strip().upper()

        if len(pais) != 2 or not pais.isalpha():
            return {"error": "Utiliza el código ISO de dos letras, por ejemplo GT para Guatemala."}

        url = (
            f"{self.base_banco_mundial}/"
            f"{pais}/indicator/{indicador}"
        )

        try:
            response = requests.get(
                url,
                params={"format": "json", "per_page": 10, "mrv": 10},
                timeout=20
            )
            response.raise_for_status()
            datos = response.json()

            if not isinstance(datos, list) or len(datos) < 2:
                return {
                    "error": f"No se encontró información para {nombre}.",
                    "pais": pais
                }

            registros = datos[1]

            if not registros:
                return {
                    "pais": pais,
                    "indicador": nombre,
                    "observaciones": [],
                    "mensaje": "No hay datos disponibles."
                }

            observaciones = []

            for registro in registros:
                valor = registro.get("value")

                if valor is not None:
                    observaciones.append({
                        "anio": registro.get("date"),
                        "valor": valor,
                        "unidad": registro.get("unit") or None
                    })

            return {
                "pais": pais,
                "indicador": nombre,
                "observaciones": observaciones,
                "fuente": "Banco Mundial",
                "nota": (
                    "El dato más reciente disponible aparece primero. "
                    "El último año publicado puede no ser el actual."
                )
            }

        except Exception as e:
            return {
                "error": f"No se pudo consultar {nombre}: {str(e)}"
            }

    # ==========================================
    # INDICADORES ECONÓMICOS
    # ==========================================

    def consultar_pib_api(self, pais: str):
        return self._consultar_indicador(
            pais, "NY.GDP.MKTP.CD", "PIB en dólares corrientes"
        )

    def consultar_inflacion_api(self, pais: str):
        return self._consultar_indicador(
            pais, "FP.CPI.TOTL.ZG", "Inflación anual (%)"
        )

    def consultar_desempleo_api(self, pais: str):
        return self._consultar_indicador(
            pais, "SL.UEM.TOTL.ZS", "Desempleo (% de la fuerza laboral)"
        )

    def consultar_poblacion_api(self, pais: str):
        return self._consultar_indicador(
            pais, "SP.POP.TOTL", "Población total"
        )

    def consultar_pib_per_capita_api(self, pais: str):
        return self._consultar_indicador(
            pais, "NY.GDP.PCAP.CD", "PIB per cápita en dólares corrientes"
        )

    def consultar_exportaciones_api(self, pais: str):
        return self._consultar_indicador(
            pais, "NE.EXP.GNFS.ZS",
            "Exportaciones de bienes y servicios (% del PIB)"
        )

    def consultar_importaciones_api(self, pais: str):
        return self._consultar_indicador(
            pais, "NE.IMP.GNFS.ZS",
            "Importaciones de bienes y servicios (% del PIB)"
        )

    def consultar_deuda_externa_api(self, pais: str):
        return self._consultar_indicador(
            pais, "DT.DOD.DECT.CD", "Deuda externa total en dólares corrientes"
        )

    def consultar_inversion_extranjera_api(self, pais: str):
        return self._consultar_indicador(
            pais, "BX.KLT.DINV.CD.WD",
            "Inversión extranjera directa neta en dólares corrientes"
        )

    def consultar_consumo_hogares_api(self, pais: str):
        return self._consultar_indicador(
            pais, "NE.CON.PRVT.CD",
            "Consumo final de los hogares en dólares corrientes"
        )