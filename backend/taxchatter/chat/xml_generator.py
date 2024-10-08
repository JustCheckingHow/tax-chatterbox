import datetime
import logging
import tempfile
import xml.etree.ElementTree as ET

from loguru import logger

class OsobaFizyczna:
    def __init__(
        self,
        pesel=None,
        imie=None,
        nazwisko=None,
        data_urodzenia=None,
        imie_ojca=None,
        imie_matki=None,
    ):
        self.pesel = pesel
        self.imie = imie
        self.nazwisko = nazwisko
        self.data_urodzenia = data_urodzenia
        self.imie_ojca = imie_ojca
        self.imie_matki = imie_matki

    @staticmethod
    def get_schema(suffix=None):
        suffix = "" if suffix is None else f"_{suffix}"
        return [
            {
                f"Pesel{suffix}": {
                    "description": "Numer Pesel",
                    "label": "Pesel",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{11}$",
                }
            },
            {
                f"Imie{suffix}": {
                    "description": "Imię",
                    "label": "Imię",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"Nazwisko{suffix}": {
                    "description": "Nazwisko",
                    "label": "Nazwisko",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"ImieOjca{suffix}": {
                    "description": "Imię ojca",
                    "label": "Imię ojca",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"ImieMatki{suffix}": {
                    "description": "Imię matki",
                    "label": "Imię matki",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"Obywatelstwo{suffix}": {
                    "description": "Obywatelstwo",
                    "label": "Obywatelstwo",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
        ]

    def parse_validate(self):
        self.pesel = self.validate_pesel(self.pesel)
        self.data_urodzenia = self.get_data_urodzenia(self.pesel)

        return {
            "pesel": self.pesel,
            "imie": self.imie,
            "nazwisko": self.nazwisko,
            "imie_ojca": self.imie_ojca,
            "imie_matki": self.imie_matki,
            "data_urodzenia": self.data_urodzenia,
        }

    def validate_pesel(self, pesel):
        if pesel is None:
            return None

        if len(pesel) != 11:
            raise ValueError("Invalid PESEL length")

        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3, 1]
        sum = 0
        try:
            for i in range(len(pesel) - 1):
                sum += int(pesel[i]) * weights[i]
        except ValueError:
            raise ValueError("Invalid PESEL")  # noqa: B904

        control_sum = 10 - (sum % 10)
        if control_sum == 10:
            control_sum = 0

        if control_sum != int(pesel[-1]):
            raise ValueError("Invalid PESEL control sum")

        return pesel

    def get_data_urodzenia(self, pesel):
        if pesel is None:
            return None

        day = int(pesel[4:6])
        month = int(pesel[2:4])
        year = int(pesel[:2])

        if month <= 92 and month >= 81:
            year = year + 1800
        elif month <= 32 and month >= 21:
            year = year + 2000
        elif month <= 52 and month >= 41:
            year = year + 2100
        elif month <= 72 and month >= 61:
            year = year + 2200
        else:
            year = year + 1900

        return datetime.datetime(year, month, day)


class AdresZamieszkania:
    def __init__(
        self,
        kod_kraju=None,
        wojewodztwo=None,
        powiat=None,
        gmina=None,
        miejscowosc=None,
        ulica=None,
        nr_domu=None,
        nr_lokalu=None,
        kod_pocztowy=None,
    ):
        self.kod_kraju = kod_kraju
        self.wojewodztwo = wojewodztwo
        self.powiat = powiat
        self.gmina = gmina
        self.miejscowosc = miejscowosc
        self.ulica = ulica
        self.nr_domu = nr_domu
        self.nr_lokalu = nr_lokalu
        self.kod_pocztowy = kod_pocztowy

    def get_schema(suffix=None):
        suffix = "" if suffix is None else f"_{suffix}"
        return [
            {
                f"KodPocztowy{suffix}": {
                    "description": "Kod pocztowy",
                    "label": "Kod pocztowy",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{2}-[0-9]{3}$",
                }
            },
            {
                f"Miejscowosc{suffix}": {
                    "description": "Miejscowość",
                    "label": "Miejscowość",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"KodKraju{suffix}": {
                    "description": "Kod kraju",
                    "label": "Kod kraju",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"Wojewodztwo{suffix}": {
                    "description": "Województwo",
                    "label": "Województwo",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"Powiat{suffix}": {
                    "description": "Powiat",
                    "label": "Powiat",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"Gmina{suffix}": {
                    "description": "Gmina",
                    "label": "Gmina",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"Ulica{suffix}": {
                    "description": "Ulica",
                    "label": "Ulica",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                f"NrDomu{suffix}": {
                    "description": "Numer domu",
                    "label": "Numer domu",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{1,10}$",
                }
            },
            {
                f"NrLokalu{suffix}": {
                    "description": "Numer lokalu",
                    "label": "Numer lokalu",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{1,10}$",
                }
            },
        ]

    def parse_validate(self):
        # TODO auto generate lacking data

        # TODO validate address using GMAPS

        return {
            "kod_kraju": self.kod_kraju,
            "wojewodztwo": self.wojewodztwo,
            "powiat": self.powiat,
            "gmina": self.gmina,
            "miejscowosc": self.miejscowosc,
            "ulica": self.ulica,
            "nr_domu": self.nr_domu,
            "nr_lokalu": self.nr_lokalu,
            "kod_pocztowy": self.kod_pocztowy,
        }


class PCC3_6_Schema:
    def __init__(
        self,
        declaration_date=None,
        transaction_date=None,
        kod_urzedu=None,
        osoba_fizyczna=None,
        adres_zamieszkania=None,
        P_6=None,
        P_7=None,
        P_20=None,
        P_21=None,
        P_22=None,
        P_23=None,
        P_26=None,
        P_62=None,
        stawka_podatku=2,
    ):
        self.declaration_date = declaration_date
        self.transaction_date = transaction_date
        self.kod_urzedu = kod_urzedu
        self.osoba_fizyczna = osoba_fizyczna
        self.adres_zamieszkania = adres_zamieszkania
        self.P_6 = P_6
        self.P_7 = P_7
        self.P_20 = P_20
        self.P_21 = P_21
        self.P_22 = P_22
        self.P_23 = P_23
        self.P_26 = P_26
        self.P_62 = P_62
        self.stawka_podatku = stawka_podatku

    def get_schema():
        return [
            {
                "section": {
                    "label": "Daty",
                    "content": [
                        {
                            "P_4": {
                                "description": "Data Dokonania czynności",
                                "label": "Data Dokonania czynności",
                                "required": True,
                                "type": "date",
                                "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                            }
                        },
                        {
                            "DataZlozeniaDeklaracji": {
                                "description": "Data złożenia deklaracji",
                                "label": "Data złożenia deklaracji",
                                "required": False,
                                "type": "date",
                                "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                            }
                        },
                    ],
                }
            },
            {
                "section": {
                    "label": "Dane osobowe",
                    "content": [
                        *OsobaFizyczna.get_schema(),
                    ],
                }
            },
            {
                "section": {
                    "label": "Adres zamieszkania",
                    "content": [
                        *AdresZamieszkania.get_schema(),
                    ],
                }
            },
            {
                "section": {
                    "label": "Inne dane",
                    "content": [
                        {
                            "UrzadSkarbowy": {
                                "description": "Kod Urzędu Skarbowego",
                                "label": "Kod Urzędu Skarbowego",
                                "required": True,
                                "type": "string",
                                "pattern": "^[0-9]{4}$",
                                "visible": False,
                            }
                        },
                        {
                            "P_6": {
                                "description": "Cel złożenia deklaracji",
                                "label": "Cel złożenia deklaracji",
                                "required": False,
                                "type": "string",
                                "pattern": "^[0-9]{1}$",
                                "visible": False,
                            }
                        },
                        {
                            "P_7": {
                                "description": "Podmiot składający deklarację 1 - podmiot zobowiązany solidarnie do zapłaty podatku, 5 - inny podmiot",  # noqa: E501
                                "label": "Podmiot składający deklarację",
                                "required": True,
                                "type": "string",
                                "pattern": "^[0-9]{1}$",
                            }
                        },
                        {
                            "P_20": {
                                "description": "Przedmiot opodatkowania 1 - umowa",
                                "label": "Przedmiot opodatkowania",
                                "required": True,
                                "type": "string",
                                "pattern": "^[0-9]{1}$",
                                "visible": False,
                            }
                        },
                        {
                            "P_21": {
                                "description": "Miejsce położenia rzeczy 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa",  # noqa: E501
                                "label": "Miejsce położenia rzeczy",
                                "required": False,
                                "type": "string",
                                "pattern": "^[0-9]{1}$",
                            }
                        },
                        {
                            "P_22": {
                                "description": "Miejsce położenia CWC 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa",  # noqa: E501
                                "label": "Miejsce położenia CWC",
                                "required": False,
                                "type": "string",
                                "pattern": "^[0-9]{1}$",
                            }
                        },
                        {"P_23": {"description": "Opis", "label": "Opis", "required": True, "type": "string"}},
                        {
                            "P_26": {
                                "description": "Podstawa opodatkowania określona zgodnie z art. 6 ustawy (po zaokrągleniu do pełnych złotych)",  # noqa: E501
                                "label": "Podstawa opodatkowania",
                                "required": True,
                                "type": "number",
                                "minimum": 1000,
                            }
                        },
                        {
                            "P_62": {
                                "description": "Liczba osób",
                                "label": "Liczba osób",
                                "required": True,
                                "type": "string",
                                "pattern": "^[0-9]{1,3}$",
                            }
                        },
                    ],
                }
            },
        ]

    def parse_validate(self):
        self.declaration_date = self.parse_validate_declaration_date()
        self.transaction_date = self.parse_validate_transaction_date()

        self.P_6 = self.parse_validate_P6()
        self.P_7 = self.parse_validate_P7()
        self.P_20 = self.parse_validate_P20()
        self.P_21 = self.parse_validate_P21()
        self.P_22 = self.parse_validate_P22()
        self.P_26 = self.parse_validate_P26()
        self.P_62 = self.parse_validate_P62()
        self.stawka_podatku = self.parse_stawka_podatku()

        return {
            "transaction_date": self.transaction_date,
            "declaration_date": self.declaration_date,
            "kod_urzedu": self.kod_urzedu,
            "P_6": self.P_6,
            "P_7": self.P_7,
            "P_20": self.P_20,
            "P_21": self.P_21,
            "P_22": self.P_22,
            "P_23": self.P_23,
            "P_26": self.P_26,
            "P_62": self.P_62,
            "stawka_podatku": self.stawka_podatku,
        }

    def parse_stawka_podatku(self):
        try:
            if "%" in str(self.stawka_podatku):
                self.stawka_podatku = float(self.stawka_podatku.replace("%", "").replace(",", "."))
            else:
                self.stawka_podatku = float(self.stawka_podatku)
        except ValueError as err:
            logger.exception(err)
            raise ValueError("Invalid tax rate") from err

        accepted_values = (1, 2, 0.1, 0.5, 0.2, 0.0)
        if self.stawka_podatku not in accepted_values:
            raise ValueError(f"Invalid tax rate (must be im {accepted_values})")
        
        return self.stawka_podatku

    def parse_validate_transaction_date(
        self,
    ):
        if self.transaction_date is None:
            return None
        try:
            self.transaction_date = datetime.datetime.strptime(self.transaction_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid transaction date")  # noqa: B904

        if self.transaction_date < datetime.datetime(2024, 1, 1):
            raise ValueError("Invalid transaction date (before 2024-01-01)")

        if self.transaction_date >= self.declaration_date:
            raise ValueError("Transaction date must be before declaration date")

        return self.transaction_date

    def parse_validate_declaration_date(self):
        if self.declaration_date is None:
            return None
        try:
            self.declaration_date = datetime.datetime.strptime(self.declaration_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid declaration date")  # noqa: B904

        if self.declaration_date < datetime.datetime(2024, 1, 1):
            raise ValueError("Invalid declaration date (before 2024-01-01)")

        return self.declaration_date

    def parse_validate_P6(self):
        if self.P_6 is None:
            return None
        try:
            self.P_6 = int(self.P_6)
        except ValueError:
            raise ValueError("Invalid declaration purpose")  # noqa: B904
        if self.P_6 in [1]:
            return self.P_6
        raise ValueError("Invalid declaration purpose")

    def parse_validate_P7(self):
        if self.P_7 is None:
            return None
        try:
            self.P_7 = int(self.P_7)
        except ValueError:
            raise ValueError("Invalid declarant")  # noqa: B904
        if self.P_7 in [1, 5]:
            return self.P_7
        raise ValueError("Invalid declarant (must be 1 or 5)")

    def parse_validate_P20(self):
        if self.P_20 is None:
            return None
        try:
            self.P_20 = int(self.P_20)
        except ValueError:
            raise ValueError("Invalid taxable subject")  # noqa: B904
        if self.P_20 in [1]:
            return self.P_20
        raise ValueError("Invalid taxable subject (must be 1)")

    def parse_validate_P21(self):
        if self.P_21 is None:
            return None
        accepted_values = [0, 1, 2]

        try:
            self.P_21 = int(self.P_21)
        except ValueError:
            raise ValueError("Invalid location of the asset")  # noqa: B904
        if self.P_21 in accepted_values:
            return self.P_21
        raise ValueError("Invalid location of the asset (must be 0, 1 or 2)")

    def parse_validate_P22(self):
        if self.P_22 is None:
            return None
        accepted_values = [0, 1, 2]

        try:
            self.P_22 = int(self.P_22)
        except ValueError:
            raise ValueError("Invalid location of the asset")  # noqa: B904
        if self.P_22 in accepted_values:
            return self.P_22
        raise ValueError("Invalid location of the asset (must be 0, 1 or 2)")

    def parse_validate_P26(self):
        if self.P_26 is None:
            return None
        try:
            self.P_26 = float(self.P_26)
        except ValueError:
            raise ValueError("Invalid taxation base")  # noqa: B904

        if self.P_26 < 1000:
            raise ValueError("Invalid taxation base (must be greater than 1000)")

        return round(self.P_26, 0)

    def parse_validate_P62(self):
        if self.P_62 is None:
            return None
        try:
            self.P_62 = int(self.P_62)
        except ValueError:
            raise ValueError("Invalid number of attachment")  # noqa: B904

        if self.P_62 < 1 and self.P_7 == 1:
            raise ValueError("Invalid number of attachment (must be greater than 0)")

        return self.P_62


class SDZ2_6_Schema:
    def __init__(
        self,
        P4=None,
        P_40=None,
        P_45=None,
        P_46=None,
        P_47=None,
        P_48=None,
        P_49=None,
        P_50=None,
        P_51=None,
        P_52=None,
        P_80=None,
        P_81=None,
        P_82=None,
        P_87=None,
        P_88=None,
        P_89=None,
        P_90=None,
        P_91=None,
        P_92=None,
        P_93=None,
        declaration_date=None,
        transaction_date=None,
        osoba_fizyczna_1=None,
        osoba_fizyczna_2=None,
        adres_zamieszkania_1=None,
        adres_zamieszkania_2=None,
        kod_urzedu=None,
    ):
        # P_4 - data złożenia deklaracji
        self.P4 = P4
        # P_40 - podstawa opodatkowania określona zgodnie z art. 6 ustawy (po zaokrągleniu do pełnych złotych)
        # - opodatkowana wg stawki podatku 0,1 %
        self.P_40 = P_40
        # P_45 - obliczony należny podatek od czynności cywilnoprawnej (po zaokrągleniu do pełnych złotych)
        self.P_45 = P_45

        # P_46 - kwota należnego podatku
        self.P_46 = P_46
        # P_47 - typ spółki: 1 - spółka osobowa, 2 - spółka kapitałowa
        self.P_47 = P_47
        # P_48 - Podstawa opodatkowania dotyczy: 1 - zawarcia umowy spółki, 2 - zwiększenia majątku spółki albo
        # podwyższenia kapitału zakładowego,
        # 3 - dopłaty,
        # 4 - pożyczki udzielonej spółce osobowej przez wspólnika,
        # 5 - oddania spółce rzeczy lub praw majątkowych do nieodpłatnego używania,
        # 6 - przekształcenia spółek,
        # 7 - łączenia spółek,
        # 8 - przeniesienia na terytorium Rzeczypospolitej Polskiej
        # rzeczywistego ośrodka zarządzania spółki kapitałowej lub jej siedziby
        self.P_48 = P_48
        # P_49 - podstawa opodatkowania - określona zgodnie z art. 6 ust. 1 pkt 8 ustawy
        # (po zaokrągleniu do pełnych złotych)
        self.P_49 = P_49
        # P_50 - Opłaty i koszty związane z zawarciem umowy spółki lub jej zmiany - na podstawie art. 6 ust. 9 ustawy
        self.P_50 = P_50
        # P_51 - Podstawa obliczenia podatku
        self.P_51 = P_51
        # P_52 - Kwota należnego podatku (po zaokrągleniu do pełnych złotych)
        self.P_52 = P_52
        # P_80 -ułamek do jakiegoś tam
        self.P_80 = P_80
        # P_81 - Miejsce nabycia środków
        self.P_81 = P_81
        # P_82 - wartość rynkowa
        self.P_82 = P_82
        # P_87 - wartość rynkowa ta sama jak w P_82
        self.P_87 = P_87

        # P_88 - stosunek pokrewieństwa
        # 1 - małżonkowie,
        # 2 - zstępny,
        # 3 - wstępny,
        # 4 - rodzeństwo,
        # 5 - pasierb,
        # 6 - ojczym,
        # 7 - macocha
        self.P_88 = P_88

        # sposób przekazania pieniędzy

        # P_89 - rachunek bankowy
        self.P_89 = P_89
        # P_90 - rachunek SKOK
        self.P_90 = P_90
        # P_91 - rachunek inny niz w banku lub SKOK
        self.P_91 = P_91
        # P_92 - przekaz pocztowy
        self.P_92 = P_92

        self.declaration_date = declaration_date
        self.transaction_date = transaction_date
        self.osoba_fizyczna_1 = osoba_fizyczna_1
        self.osoba_fizyczna_2 = osoba_fizyczna_2
        self.adres_zamieszkania_1 = adres_zamieszkania_1
        self.adres_zamieszkania_2 = adres_zamieszkania_2
        self.kod_urzedu = kod_urzedu

    def parse_validate(self):
        return {
            "P_4": self.parse_validate_P4(),
            "P_40": self.parse_validate_P40(),
            "P_45": self.parse_validate_P45(),
            "P_46": self.parse_validate_P46(),
            "P_47": self.parse_validate_P47(),
            "P_48": self.parse_validate_P48(),
            "P_49": self.parse_validate_P49(),
            "P_50": self.parse_validate_P50(),
            "P_51": self.parse_validate_P51(),
            "P_52": self.parse_validate_P52(),
            "P_80": self.parse_validate_P80(),
            "P_81": self.parse_validate_P81(),
            "P_82": self.parse_validate_P82(),
            "P_87": self.parse_validate_P87(),
            "P_88": self.parse_validate_P88(),
            "P_89": self.parse_validate_P89(),
            "P_90": self.parse_validate_P90(),
            "P_91": self.parse_validate_P91(),
            "P_92": self.parse_validate_P92(),
            "declaration_date": self.parse_validate_declaration_date(),
            "transaction_date": self.parse_validate_transaction_date(),
            "osoba_fizyczna_1": self.parse_validate_osoba_fizyczna_1(),
            "osoba_fizyczna_2": self.parse_validate_osoba_fizyczna_2(),
            "adres_zamieszkania_1": self.parse_validate_adres_zamieszkania_1(),
            "adres_zamieszkania_2": self.parse_validate_adres_zamieszkania_2(),
            "kod_urzedu": self.parse_validate_kod_urzedu(),
        }

    def get_schema():
        return [
            {
                "section": {
                    "label": "Daty",
                    "content": [
                        {
                            "P_4": {
                                "description": "Data Dokonania czynności",
                                "label": "Data Dokonania czynności",
                                "required": True,
                                "type": "date",
                                "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                            }
                        },
                        {
                            "DataZlozeniaDeklaracji": {
                                "description": "Data złożenia deklaracji",
                                "label": "Data złożenia deklaracji",
                                "required": False,
                                "type": "date",
                                "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                            }
                        },
                    ],
                }
            },
            {
                "section": {
                    "label": "Dane osobowe osoba 1.",
                    "content": [
                        *OsobaFizyczna.get_schema(suffix="1"),
                    ],
                }
            },
            {
                "section": {
                    "label": "Dane osobowe osoba 2.",
                    "content": [
                        *OsobaFizyczna.get_schema(suffix="2"),
                    ],
                }
            },
            {
                "section": {
                    "label": "Adres zamieszkania osoba 1.",
                    "content": [
                        *AdresZamieszkania.get_schema(suffix="1"),
                    ],
                }
            },
            {
                "section": {
                    "label": "Adres zamieszkania osoba 2.",
                    "content": [
                        *AdresZamieszkania.get_schema(suffix="2"),
                    ],
                }
            },
            {
                "section": {
                    "label": "Inne dane",
                    "content": [
                        {
                            "UrzadSkarbowy": {
                                "description": "Kod Urzędu Skarbowego",
                                "label": "Kod Urzędu Skarbowego",
                                "required": True,
                                "type": "string",
                                "pattern": "^[0-9]{4}$",
                                "visible": False,
                            },
                        },
                        {
                            "P_40": {
                                "description": "Podstawa opodatkowania",
                                "label": "Podstawa opodatkowania",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_45": {
                                "description": "Obliczony należny podatek",
                                "label": "Obliczony należny podatek",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_46": {
                                "description": "Kwota należnego podatku",
                                "label": "Kwota należnego podatku",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_47": {
                                "description": "Typ spółki 1 spółka osobowa, 2 spółka kapitałowa",
                                "label": "Typ spółki",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_48": {
                                "description": "Podstawa opodatkowania dotyczy: \
                                1 - zawarcia umowy spółki, \
                                2 - zwiększenia majątku spółki albo podwyższenia kapitału zakładowego, \
                                3 - dopłaty, \
                                4 - pożyczki udzielonej spółce osobowej przez wspólnika, \
                                5 - oddania spółce rzeczy lub praw majątkowych do nieodpłatnego używania, \
                                6 - przekształcenia spółek, \
                                7 - łączenia spółek, \
                                8 - przeniesienia na terytorium Rzeczypospolitej Polskiej rzeczywistego ośrodka\
zarządzania spółki kapitałowej lub jej siedziby, rzeczywistego ośrodka zarządzania spółki kapitałowej lub jej siedziby",
                                "label": "Podstawa opodatkowania dotyczy",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_49": {
                                "description": "Podstawa opodatkowania - określona zgodnie z art. 6 ust. 1 pkt 8 ustawy",
                                "label": "Podstawa opodatkowania",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_50": {
                                "description": "Opłaty i koszty związane z zawarciem umowy spółki lub jej zmiany - na podstawie art. 6 ust. 9 ustawy",
                                "label": "Opłaty i koszty związane z zawarciem umowy spółki lub jej zmiany",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_51": {
                                "description": "Podstawa obliczenia podatku",
                                "label": "Podstawa obliczenia podatku",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_52": {
                                "description": "Kwota należnego podatku (po zaokrągleniu do pełnych złotych)",
                                "label": "Kwota należnego podatku",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_80": {
                                "description": "Ułamek do jakiegoś tam",
                                "label": "Ułamek do jakiegoś tam",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_81": {
                                "description": "Miejsce nabycia środków",
                                "label": "Miejsce nabycia środków",
                                "required": True,
                                "type": "string",
                                "visible": False,
                            },
                        },
                        {
                            "P_82": {
                                "description": "Wartość rynkowa",
                                "label": "Wartość rynkowa",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_87": {
                                "description": "Wartość rynkowa ta sama jak w P_82",
                                "label": "Wartość rynkowa ta sama jak w P_82",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_88": {
                                "description": "Stosunek pokrewieństwa",
                                "label": "Stosunek pokrewieństwa",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_89": {
                                "description": "Sposób przekazania pieniędzy",
                                "label": "Sposób przekazania pieniędzy",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_90": {
                                "description": "Sposób przekazania pieniędzy",
                                "label": "Sposób przekazania pieniędzy",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_91": {
                                "description": "Sposób przekazania pieniędzy",
                                "label": "Sposób przekazania pieniędzy",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                        {
                            "P_92": {
                                "description": "Sposób przekazania pieniędzy",
                                "label": "Sposób przekazania pieniędzy",
                                "required": True,
                                "type": "number",
                                "visible": False,
                            },
                        },
                    ],
                }
            },

        ]

    def parse_validate_P4(self):
        try:
            self.P4 = datetime.datetime.strptime(self.P4, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid declaration date")  # noqa: B904

        return self.P4

    def parse_validate_P40(self):
        try:
            self.P_40 = float(self.P_40)
        except ValueError:
            raise ValueError("Invalid taxation base")  # noqa: B904

        return round(self.P_40, 0)

    def parse_validate_P47(self):
        accepted_values = [1, 2]

        try:
            self.P_47 = int(self.P_47)
        except ValueError:
            raise ValueError("Invalid company type")  # noqa: B904

        if self.P_47 in accepted_values:
            return self.P_47
        raise ValueError("Invalid company type (must be 1 or 2)")

    def parse_validate_P48(self):
        accepted_values = [1, 2, 3, 4, 5, 6, 7, 8]

        try:
            self.P_48 = int(self.P_48)
        except ValueError:
            raise ValueError("Invalid taxation base")  # noqa: B904

        if self.P_48 in accepted_values:
            return self.P_48
        raise ValueError("Invalid taxation base (must be 1, 2, 3, 4, 5, 6, 7 or 8)")

    def parse_validate_P49(self):
        try:
            self.P_49 = float(self.P_49)
        except ValueError:
            raise ValueError("Invalid taxation base")  # noqa: B904

        return round(self.P_49, 0)

    def parse_validate_P50(self):
        try:
            self.P_50 = float(self.P_50)
        except ValueError:
            raise ValueError("Invalid taxation base")  # noqa: B904

        return round(self.P_50, 0)

    def parse_validate_P51(self):
        try:
            self.P_51 = float(self.P_51)
        except ValueError:
            raise ValueError("Invalid taxation base")  # noqa: B904

        return round(self.P_51, 0)

    def parse_validate_P52(self):
        try:
            self.P_52 = float(self.P_52)
        except ValueError:
            raise ValueError("Invalid taxation base")  # noqa: B904

        return round(self.P_52, 0)

    def parse_validate_P80(self):
        # ulamek w formacie 1/3

        try:
            self.P_80 = self.P_80.split("/")
            self.P_80 = [int(self.P_80[0]), int(self.P_80[1])]
        except ValueError:
            raise ValueError("Invalid fraction")  # noqa: B904

        if self.P_80[0] < 1 or self.P_80[1] < 1:
            raise ValueError("Invalid fraction (must be greater than 0)")

        return self.P_80[0] / self.P_80[1]

    def parse_validate_P81(self):
        return self.P_81

    def parse_validate_P82(self):
        try:
            self.P_82 = float(self.P_82)
        except ValueError:
            raise ValueError("Invalid market value")  # noqa: B904

        return self.P_82

    def parse_validate_P87(self):
        return self.P_87


def validate_json_pcc3(json_data):
    # person data:
    osoba_fizyczna = OsobaFizyczna(
        pesel=json_data.get("Pesel", None),
        imie=json_data.get("Imie", None),
        nazwisko=json_data.get("Nazwisko", None),
        imie_ojca=json_data.get("ImieOjca", None),
        imie_matki=json_data.get("ImieMatki", None),
    ).parse_validate()
    
    # Address data:
    adres_zamieszkania = AdresZamieszkania(
        kod_kraju=json_data.get("KodKraju", None),
        wojewodztwo=json_data.get("Wojewodztwo", None),
        powiat=json_data.get("Powiat", None),
        gmina=json_data.get("Gmina", None),
        miejscowosc=json_data.get("Miejscowosc", None),
        ulica=json_data.get("Ulica", None),
        nr_domu=json_data.get("NrDomu", None),
        nr_lokalu=json_data.get("NrLokalu", None),
        kod_pocztowy=json_data.get("KodPocztowy", None),
    ).parse_validate()

    pcc_schema = PCC3_6_Schema(
        transaction_date=json_data.get("P_4", None),
        declaration_date=json_data.get("DataZlozeniaDeklaracji", None),
        kod_urzedu=json_data.get("KodUrzedu", None),
        osoba_fizyczna=osoba_fizyczna,
        adres_zamieszkania=adres_zamieszkania,
        P_6=json_data.get("P_6", None),
        P_7=json_data.get("P_7", None),
        P_20=json_data.get("P_20", None),
        P_21=json_data.get("P_21", None),
        P_22=json_data.get("P_22", None),
        P_23=json_data.get("P_23", None),
        P_26=json_data.get("P_26", None),
        P_62=json_data.get("P_62", None),
        stawka_podatku=json_data.get("stawka_podatku", 2),
    ).parse_validate()

    out = {}

    for key in pcc_schema:
        out[key] = pcc_schema[key]

    for key in osoba_fizyczna:
        out[key] = osoba_fizyczna[key]

    for key in adres_zamieszkania:
        out[key] = adres_zamieszkania[key]

    return out


def validate_json_sdz2(json_data):
    out = {}

    osoba_fizyczna1 = OsobaFizyczna(
        pesel=json_data.get("Pesel_1"),
        imie=json_data.get("Imie_1"),
        nazwisko=json_data.get("Nazwisko_1"),
        imie_ojca=json_data.get("ImieOjca_1"),
        imie_matki=json_data.get("ImieMatki_1"),
    ).parse_validate()

    adres_zamieszkania1 = AdresZamieszkania(
        kod_kraju=json_data.get("KodKraju_1"),
        wojewodztwo=json_data.get("Wojewodztwo_1"),
        powiat=json_data.get("Powiat_1"),
        gmina=json_data.get("Gmina_1"),
        miejscowosc=json_data.get("Miejscowosc_1"),
        ulica=json_data.get("Ulica_1"),
        nr_domu=json_data.get("NrDomu_1"),
        nr_lokalu=json_data.get("NrLokalu_1"),
        kod_pocztowy=json_data.get("KodPocztowy_1"),
    ).parse_validate()

    osoba_fizyczna2 = OsobaFizyczna(
        pesel=json_data.get("Pesel_2"),
        imie=json_data.get("Imie_2"),
        nazwisko=json_data.get("Nazwisko_2"),
        imie_ojca=json_data.get("ImieOjca_2"),
        imie_matki=json_data.get("ImieMatki_2"),
    ).parse_validate()

    adres_zamieszkania2 = AdresZamieszkania(
        kod_kraju=json_data.get("KodKraju_2"),
        wojewodztwo=json_data.get("Wojewodztwo_2"),
        powiat=json_data.get("Powiat_2"),
        gmina=json_data.get("Gmina_2"),
        miejscowosc=json_data.get("Miejscowosc_2"),
        ulica=json_data.get("Ulica_2"),
        nr_domu=json_data.get("NrDomu_2"),
        nr_lokalu=json_data.get("NrLokalu_2"),
        kod_pocztowy=json_data.get("KodPocztowy_2"),
    ).parse_validate()

    sdz2_schema = SDZ2_6_Schema(
        P_4=json_data.get("P_4"),
        P_40=json_data.get("P_40"),
        P_45=json_data.get("P_45"),
        P_46=json_data.get("P_46"),
        P_47=json_data.get("P_47"),
        P_48=json_data.get("P_48"),
        P_49=json_data.get("P_49"),
        P_50=json_data.get("P_50"),
        P_51=json_data.get("P_51"),
        P_52=json_data.get("P_52"),
        P_80=json_data.get("P_80"),
        P_81=json_data.get("P_81"),
        P_82=json_data.get("P_82"),
        P_87=json_data.get("P_87"),
        P_88=json_data.get("P_88"),
        P_89=json_data.get("P_89"),
        P_90=json_data.get("P_90"),
        P_91=json_data.get("P_91"),
        P_92=json_data.get("P_92"),
        declaration_date=json_data.get("DataZlozeniaDeklaracji"),
        transaction_date=json_data.get("P_4"),
        osoba_fizyczna_1=osoba_fizyczna1,
        osoba_fizyczna_2=osoba_fizyczna2,
        adres_zamieszkania_1=adres_zamieszkania1,
        adres_zamieszkania_2=adres_zamieszkania2,
        kod_urzedu=json_data.get("KodUrzedu"),
    ).parse_validate()

    out = {}

    for key in sdz2_schema:
        out[key] = sdz2_schema[key]

    for key in osoba_fizyczna1:
        out["os_1" + key] = osoba_fizyczna1[key]

    for key in osoba_fizyczna2:
        out["os_2" + key] = osoba_fizyczna2[key]

    for key in adres_zamieszkania1:
        out["ad_1" + key] = adres_zamieszkania1[key]

    for key in adres_zamieszkania2:
        out["ad_2" + key] = adres_zamieszkania2[key]

    return out


def generate_xml_sdz2(json_schema):
    try:
        parsed_json = validate_json_sdz2(json_schema)
    except ValueError as e:
        print(e)
        return

    # Tworzenie głównego elementu
    deklaracja = ET.Element("Deklaracja", xmlns="http://crd.gov.pl/wzor/2023/12/13/13064/")

    # Nagłówek
    naglowek = ET.SubElement(deklaracja, "Naglowek")
    kod_formularza = ET.SubElement(
        naglowek,
        "KodFormularza",
        kodSystemowy="PCC-3 (6)",
        kodPodatku="PCC",
        rodzajZobowiazania="Z",
        wersjaSchemy="1-0E",
    )
    kod_formularza.text = "PCC-3"
    # for f in ("27", "46", "53"):
        # P_26 -- podstawa opodatkowania
        # parsed_json[f"P_{f}"] = round(parsed_json.get("stawka_podatku") * parsed_json.get("P_26"), 0)

    ET.SubElement(naglowek, "WariantFormularza").text = "6"
    ET.SubElement(naglowek, "CelZlozenia", poz="P_7").text = str(parsed_json.get("declaration_purpose", 1))
    if parsed_json.get("declaration_date") is not None:
        ET.SubElement(naglowek, "Data", poz="P_5").text = parsed_json.get("declaration_date").strftime("%Y-%m-%d")
    if parsed_json.get("kod_urzedu") is not None:
        ET.SubElement(naglowek, "KodUrzedu").text = parsed_json.get("kod_urzedu")

    # Podmiot1
    podmiot1 = ET.SubElement(deklaracja, "Podmiot1", rola="Podatnik")
    osoba_fizyczna1 = ET.SubElement(podmiot1, "OsobaFizyczna")
    for key in ["pesel", "imie", "nazwisko", "data_urodzenia", "imie_ojca", "imie_matki"]:
        if parsed_json.get("os_1" + key) is not None:
            ET.SubElement(osoba_fizyczna1, key).text = parsed_json.get("os_1" + key)
    
    adres_zamieszkania1 = ET.SubElement(podmiot1, "AdresZamieszkania", rodzajAdresu="RAD")
    adres_pol1 = ET.SubElement(adres_zamieszkania1, "AdresPol")
    for key in ["kod_kraju", "wojewodztwo", "powiat", "gmina", "ulica", "nr_domu", "nr_lokalu", "miejscowosc", "kod_pocztowy"]:
        if parsed_json.get("ad_1" + key) is not None:
            ET.SubElement(adres_pol1, key).text = parsed_json.get("ad_1" + key)

    # Podmiot2
    podmiot2 = ET.SubElement(deklaracja, "Podmiot2", rola="Spadkodawca, Darczyńca lub inna osoba, od której lub po której zostały nabyte rzeczy lub prawa majątkowe")
    osoba_fizyczna2 = ET.SubElement(podmiot2, "OsobaFizyczna")

    for key in ["pesel", "imie", "nazwisko", "data_urodzenia", "imie_ojca", "imie_matki"]:
        if parsed_json.get("os_2" + key) is not None:
            ET.SubElement(osoba_fizyczna2, key).text = parsed_json.get("os_2" + key)

    adres_zamieszkania2 = ET.SubElement(podmiot2, "AdresZamieszkania", rodzajAdresu="RAD")
    adres_pol2 = ET.SubElement(adres_zamieszkania2, "AdresPol")
    for key in ["kod_kraju", "wojewodztwo", "powiat", "gmina", "ulica", "nr_domu", "nr_lokalu", "miejscowosc", "kod_pocztowy"]:
        if parsed_json.get("ad_2" + key) is not None:
            ET.SubElement(adres_pol2, key).text = parsed_json.get("ad_2" + key)

    # Pozycje szczegółowe
    pozycje_szczegolowe = ET.SubElement(deklaracja, "PozycjeSzczegolowe")
    for key in ["P_4", "P_40", "P_45", "P_46", "P_47", "P_48", "P_49", "P_50", "P_51", "P_52", "P_80", "P_81", "P_82", "P_87", "P_88", "P_89", "P_90", "P_91", "P_92"]:
        if parsed_json.get(key) is not None:
            ET.SubElement(pozycje_szczegolowe, key).text = parsed_json.get(key)

    ET.SubElement(deklaracja, "Pouczenia").text = str(1)

    # Tworzenie drzewa XML
    tree = ET.ElementTree(deklaracja)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
        tree.write(temp_file.name, encoding="utf-8", xml_declaration=True)
        return temp_file.name


    # ET.SubElement(pozycje_szczegolowe, "P_4").text = parsed_json.get("P_4")
    # ET.SubElement(pozycje_szczegolowe, "P_40").text = parsed_json.get("P_40")
    # ET.SubElement(pozycje_szczegolowe, "P_45").text = parsed_json.get("P_45")
    # ET.SubElement(pozycje_szczegolowe, "P_46").text = parsed_json.get("P_46")
    # ET.SubElement(pozycje_szczegolowe, "P_47").text = parsed_json.get("P_47")
    # ET.SubElement(pozycje_szczegolowe, "P_48").text = parsed_json.get("P_48")
    # ET.SubElement(pozycje_szczegolowe, "P_49").text = parsed_json.get("P_49")
    # ET.SubElement(pozycje_szczegolowe, "P_50").text = parsed_json.get("P_50")
    # ET.SubElement(pozycje_szczegolowe, "P_51").text = parsed_json.get("P_51")
    # ET.SubElement(pozycje_szczegolowe, "P_52").text = parsed_json.get("P_52")
    # ET.SubElement(pozycje_szczegolowe, "P_80").text = parsed_json.get("P_80")
    # ET.SubElement(pozycje_szczegolowe, "P_81").text = parsed_json.get("P_81")
    # ET.SubElement(pozycje_szczegolowe, "P_82").text = parsed_json.get("P_82")
    # ET.SubElement(pozycje_szczegolowe, "P_87").text = parsed_json.get("P_87")
    # ET.SubElement(pozycje_szczegolowe, "P_88").text = parsed_json.get("P_88")
    # ET.SubElement(pozycje_szczegolowe, "P_89").text = parsed_json.get("P_89")
    # ET.SubElement(pozycje_szczegolowe, "P_90").text = parsed_json.get("P_90")
    # ET.SubElement(pozycje_szczegolowe, "P_91").text = parsed_json.get("P_91")
    # ET.SubElement(pozycje_szczegolowe, "P_92").text = parsed_json.get("P_92")



    # person1 = parsed_json.get("person1")
    # person2 = parsed_json.get("person2")


    # if any(
    #     parsed_json.get(key) is not None
    #     for key in ["pesel", "imie", "nazwisko", "data_urodzenia", "imie_ojca", "imie_matki"]
    # ):

    # Podmiot

    
    

def generate_xml(json_schema):
    try:
        logger.info(json_schema)
        parsed_json = validate_json_pcc3(json_schema)
    except ValueError as e:
        logger.exception(e)
        return

    # print(parsed_json)
    # Tworzenie głównego elementu
    deklaracja = ET.Element("Deklaracja", xmlns="http://crd.gov.pl/wzor/2023/12/13/13064/")

    # Nagłówek
    naglowek = ET.SubElement(deklaracja, "Naglowek")
    kod_formularza = ET.SubElement(
        naglowek,
        "KodFormularza",
        kodSystemowy="PCC-3 (6)",
        kodPodatku="PCC",
        rodzajZobowiazania="Z",
        wersjaSchemy="1-0E",
    )
    kod_formularza.text = "PCC-3"
    if parsed_json.get("stawka_podatku") is not None and parsed_json.get("P_26") is not None:
        # P_26 -- podstawa opodatkowania
        for f in ("27", "46", "53"):
            parsed_json[f"P_{f}"] = round(parsed_json.get("stawka_podatku") * parsed_json.get("P_26"), 0)

    ET.SubElement(naglowek, "WariantFormularza").text = "6"
    ET.SubElement(naglowek, "CelZlozenia", poz="P_6").text = str(parsed_json.get("declaration_purpose", 1))
    if parsed_json.get("declaration_date") is not None:
        ET.SubElement(naglowek, "Data", poz="P_4").text = parsed_json.get("declaration_date").strftime("%Y-%m-%d")
    if parsed_json.get("kod_urzedu") is not None:
        ET.SubElement(naglowek, "KodUrzedu").text = parsed_json.get("kod_urzedu")

    # Podmiot
    if any(
        parsed_json.get(key) is not None
        for key in ["pesel", "imie", "nazwisko", "data_urodzenia", "imie_ojca", "imie_matki"]
    ):
        podmiot1 = ET.SubElement(deklaracja, "Podmiot1", rola="Podatnik")
        osoba_fizyczna = ET.SubElement(podmiot1, "OsobaFizyczna")
    if parsed_json.get("pesel") is not None:
        ET.SubElement(osoba_fizyczna, "PESEL").text = parsed_json.get("pesel")
    if parsed_json.get("imie") is not None:
        ET.SubElement(osoba_fizyczna, "ImiePierwsze").text = parsed_json.get("imie")
    if parsed_json.get("nazwisko") is not None:
        ET.SubElement(osoba_fizyczna, "Nazwisko").text = parsed_json.get("nazwisko")
    if parsed_json.get("data_urodzenia") is not None:
        ET.SubElement(osoba_fizyczna, "DataUrodzenia").text = parsed_json.get("data_urodzenia").strftime("%Y-%m-%d")
    if parsed_json.get("imie_ojca") is not None:
        ET.SubElement(osoba_fizyczna, "ImieOjca").text = parsed_json.get("imie_ojca")
    if parsed_json.get("imie_matki") is not None:
        ET.SubElement(osoba_fizyczna, "ImieMatki").text = parsed_json.get("imie_matki")

    if any(
        parsed_json.get(key) is not None
        for key in [
            "kod_kraju",
            "wojewodztwo",
            "powiat",
            "gmina",
            "ulica",
            "nr_domu",
            "nr_lokalu",
            "miejscowosc",
            "kod_pocztowy",
        ]
    ):
        adres = ET.SubElement(podmiot1, "AdresZamieszkaniaSiedziby", rodzajAdresu="RAD")
        adres_pol = ET.SubElement(adres, "AdresPol")
    if parsed_json.get("kod_kraju") is not None:
        ET.SubElement(adres_pol, "KodKraju").text = parsed_json.get("kod_kraju")
    if parsed_json.get("wojewodztwo") is not None:
        ET.SubElement(adres_pol, "Wojewodztwo").text = parsed_json.get("wojewodztwo")
    if parsed_json.get("powiat") is not None:
        ET.SubElement(adres_pol, "Powiat").text = parsed_json.get("powiat")
    if parsed_json.get("gmina") is not None:
        ET.SubElement(adres_pol, "Gmina").text = parsed_json.get("gmina")
    if parsed_json.get("ulica") is not None:
        ET.SubElement(adres_pol, "Ulica").text = parsed_json.get("ulica")
    if parsed_json.get("nr_domu") is not None:
        ET.SubElement(adres_pol, "NrDomu").text = parsed_json.get("nr_domu")
    if parsed_json.get("nr_lokalu") is not None:
        ET.SubElement(adres_pol, "NrLokalu").text = parsed_json.get("nr_lokalu")
    if parsed_json.get("miejscowosc") is not None:
        ET.SubElement(adres_pol, "Miejscowosc").text = parsed_json.get("miejscowosc")
    if parsed_json.get("kod_pocztowy") is not None:
        ET.SubElement(adres_pol, "KodPocztowy").text = parsed_json.get("kod_pocztowy")

    # P32 - stawka podatku

    # Pozycje szczegółowe

    pozycje_szczegolowe = ET.SubElement(deklaracja, "PozycjeSzczegolowe")

    # PODMIOT SKŁADAJACY DEKLARACJE
    # 1: "podmiot zobowiązany solidarnie do zapłaty podatku"
    # 5: "inny podmiot"
    # if parsed_json.get("P_7") is not None:
    ET.SubElement(pozycje_szczegolowe, "P_7").text = str(parsed_json.get("P_7", "1"))

    # PRZEDMIOT OPODATKOWANIA
    # 1: Umowa
    if parsed_json.get("P_20") is not None:
        ET.SubElement(pozycje_szczegolowe, "P_20").text = str(parsed_json.get("P_20"))

    # MIEJSCE POŁOŻENIA RZECZY LUB WYKONYWANIA PRAWA MAJĄTKOWEGO
    if parsed_json.get("P_21") is not None:
        ET.SubElement(pozycje_szczegolowe, "P_21").text = str(parsed_json.get("P_21"))

    if parsed_json.get("P_22") is not None:
        ET.SubElement(pozycje_szczegolowe, "P_22").text = str(parsed_json.get("P_22"))

    if parsed_json.get("P_23") is not None:
        ET.SubElement(pozycje_szczegolowe, "P_23").text = str(parsed_json.get("P_23"))

    # ET.SubElement(pozycje_szczegolowe, "P_24").text = str(parsed_json.get("taxation_base"))
    # ET.SubElement(pozycje_szczegolowe, "P_25").text = "10"
    if parsed_json.get("P_26") is not None:
        ET.SubElement(pozycje_szczegolowe, "P_26").text = str(parsed_json.get("P_26"))
    if parsed_json.get("P_27") is not None:
        ET.SubElement(pozycje_szczegolowe, "P_27").text = str(parsed_json.get("P_27"))
    if parsed_json.get("P_46") is not None:
        ET.SubElement(pozycje_szczegolowe, "P_46").text = str(parsed_json.get("P_46"))
    # if parsed_json.get("P_53") is not None:
    ET.SubElement(pozycje_szczegolowe, "P_53").text = str(parsed_json.get("P_53", "0"))
    if parsed_json.get("P_62") is not None:
        ET.SubElement(pozycje_szczegolowe, "P_62").text = str(parsed_json.get("P_62"))

    # Pouczenia
    ET.SubElement(deklaracja, "Pouczenia").text = str(1)

    # Tworzenie drzewa XML
    tree = ET.ElementTree(deklaracja)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
        tree.write(temp_file.name, encoding="utf-8", xml_declaration=True)
        return temp_file.name


if __name__ == "__main__":
    # name = generate_xml(
    #     {
    #         "Pesel": "86072926288",
    #         "P_4": "2024-09-18",
    #         "DataZlozeniaDeklaracji": "2024-09-19",
    #         "Imie": "Jan",
    #         "Nazwisko": "Kowalski",
    #         "DataUrodzenia": "1986-07-29",
    #         "ImieOjca": "Jan",
    #         "ImieMatki": "Maria",
    #         "KodKraju": "PL",
    #         "Wojewodztwo": "Małopolskie",
    #         "Powiat": "Kraków",
    #         "Gmina": "Kraków",
    #         "Miejscowosc": "Kraków",
    #         "Ulica": "Wizjonerów",
    #         "NrDomu": "7",
    #         "NrLokalu": "104",
    #         "KodPocztowy": "31-356",
    #         "P_6": "1",
    #         "P_7": "1",
    #         "P_20": "1",
    #         "P_21": "1",
    #         "P_22": "1",
    #         "P_23": "test123",
    #         "P_26": "1000",
    #         "P_62": "1",
    #         "KodUrzedu": "1234",
    #         "stawka_podatku": 2,
    #     }
    # )
    # print(name)
    # with open(name) as file:
    #     print(file.read())

    name = generate_xml_sdz2(
        {
            "P_4": "2024-09-04",
            "P_40": "1",
            "P_45": "1",
            "P_46": "1",
            "P_47": "1",
            "P_48": "1",
            "P_49": "1",
            "P_50": "1",
            "P_51": "1",
            "P_52": "1",
            "P_80": "1/3",
            "P_81": "Bank",
            "P_82": "123123",
            "P_87": "123123",
            "P_88": "3",
            "P_89": "1",
            "P_90": "1",
            "P_91": "1",
            "P_92": "1",
            "P_93": "asdf",
            
        }
    )

    print(name)
    with open(name) as file:
        print(file.read())