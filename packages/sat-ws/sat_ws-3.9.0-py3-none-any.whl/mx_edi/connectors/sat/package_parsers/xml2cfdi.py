from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Dict, List, Tuple
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from zipfile import ZipFile

from ....core import CFDI, Concepto
from .cfdi_parser import CFDIParser, MissingData
from .utils import get_attr

CFDI_NS = "{http://www.sat.gob.mx/cfd/3}"
TFD_NS = "{http://www.sat.gob.mx/TimbreFiscalDigital}"


class XML2CFDI(CFDIParser):
    root_elements: Dict[str, Callable] = {
        "Version": str,
        "Sello": str,
        "CondicionesDePago": str,
        "Folio": str,
        "Serie": str,
        "NoCertificado": str,
        "Certificado": str,
        "TipoDeComprobante": str,
        "Fecha": datetime.fromisoformat,
        "LugarExpedicion": str,
        "FormaPago": str,
        "MetodoPago": str,
        "Moneda": str,
        "TipoCambio": Decimal,
        "SubTotal": Decimal,
        "Total": Decimal,
    }

    @classmethod
    def _get_root_data(cls, xml: Element) -> Dict[str, Any]:
        return {
            field: caster(attr)
            for field, caster in cls.root_elements.items()
            if (attr := get_attr(xml, field)) is not None
        }

    @classmethod
    def _get_impuestos(cls, concepto) -> dict[str, float]:
        """Get the sum of the taxes in Concepto"""
        xml_impuestos = concepto.find(f"{CFDI_NS}Impuestos")
        if not xml_impuestos:
            return {"Traslado": 0, "Retencion": 0}
        xml_traslados = xml_impuestos.find(f"{CFDI_NS}Traslados")
        sum_traslado = (
            sum(
                float(get_attr(traslado, "Importe"))
                for traslado in xml_traslados.findall(f"{CFDI_NS}Traslado")
            )
            if xml_traslados
            else 0
        )
        xml_retenciones = xml_impuestos.find(f"{CFDI_NS}Retenciones")
        sum_retencion = (
            sum(
                float(get_attr(retencion, "Importe"))
                for retencion in xml_retenciones.findall(f"{CFDI_NS}Retencion")
            )
            if xml_retenciones
            else 0
        )
        return {"Traslado": sum_traslado, "Retencion": sum_retencion}

    @classmethod
    def _get_conceptos(cls, xml: Element) -> List[Concepto]:
        xml_conceptos = xml.find(f"{CFDI_NS}Conceptos")
        if not xml_conceptos:
            return []
        return [
            Concepto(
                Descripcion=get_attr(concepto, "Descripcion"),
                Cantidad=float(get_attr(concepto, "Cantidad")),
                ValorUnitario=float(get_attr(concepto, "ValorUnitario")),
                Importe=float(get_attr(concepto, "Importe")),
                Impuestos=cls._get_impuestos(concepto),
            )
            for concepto in xml_conceptos.findall(f"{CFDI_NS}Concepto")
        ]

    @classmethod
    def parse(cls, xml: Element, xml_string: str = None) -> CFDI:
        data = cls._get_root_data(xml)
        complemento = xml.find(f"{CFDI_NS}Complemento")
        if not complemento:
            raise MissingData(f"{CFDI_NS}Complemento")
        CfdiRelacionados = xml.find(f"{CFDI_NS}CfdiRelacionados")
        if CfdiRelacionados:
            data["CfdiRelacionados"] = {
                get_attr(cfdi_relacionado, "UUID")
                for cfdi_relacionado in CfdiRelacionados.findall(f"{CFDI_NS}CfdiRelacionado")
            }
        uuid = get_attr(
            complemento.find(f"{TFD_NS}TimbreFiscalDigital"),
            "UUID",
        )
        emisor = xml.find(f"{CFDI_NS}Emisor")
        receptor = xml.find(f"{CFDI_NS}Receptor")
        data["RfcEmisor"] = get_attr(emisor, "Rfc")
        data["NombreEmisor"] = get_attr(emisor, "Nombre")
        data["RegimenFiscalEmisor"] = get_attr(emisor, "RegimenFiscal")
        data["RfcReceptor"] = get_attr(receptor, "Rfc")
        data["NombreReceptor"] = get_attr(receptor, "Nombre")
        data["UsoCFDIReceptor"] = get_attr(receptor, "UsoCFDI")
        data["UUID"] = uuid
        data["Conceptos"] = cls._get_conceptos(xml)
        data["xml"] = xml_string

        return CFDI(**data)

    @classmethod
    def _get_xmls(cls, files: List[str]) -> List[Tuple[Element, str]]:
        return [(ElementTree.fromstring(xml_file), xml_file) for xml_file in files]

    @classmethod
    def parse_zip(cls, zipfile: ZipFile) -> List["CFDI"]:
        xml_files = cls._get_files(zipfile)
        xmls = cls._get_xmls(xml_files)
        return [cls.parse(xml[0], xml[1]) for xml in xmls]
