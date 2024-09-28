import datetime
import tempfile
import xml.etree.ElementTree as ET


class OsobaFizyczna:
    def __init__(self, pesel=None, imie=None, nazwisko=None, data_urodzenia=None, imie_ojca=None, imie_matki=None):
        self.pesel = pesel
        self.imie = imie
        self.nazwisko = nazwisko
        self.data_urodzenia = data_urodzenia
        self.imie_ojca = imie_ojca
        self.imie_matki = imie_matki

    @staticmethod
    def get_schema():
        return [
            {
                "Pesel": {
                    "description": "Numer Pesel",
                    "label": "Pesel",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{11}$",
                }
            },
            {
                "Imie": {
                    "description": "Imię",
                    "label": "Imię",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "Nazwisko": {
                    "description": "Nazwisko",
                    "label": "Nazwisko",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "ImieOjca": {
                    "description": "Imię ojca",
                    "label": "Imię ojca",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "ImieMatki": {
                    "description": "Imię matki",
                    "label": "Imię matki",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "Obywatelstwo": {
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
        if len(pesel) != 11:
            raise ValueError("Invalid PESEL length")

        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3, 1]
        sum = 0
        for i in range(len(pesel) - 1):
            sum += int(pesel[i]) * weights[i]

        control_sum = 10 - (sum % 10)
        if control_sum == 10:
            control_sum = 0

        if control_sum != int(pesel[-1]):
            raise ValueError("Invalid PESEL control sum")

        return pesel

    def get_data_urodzenia(self, pesel):
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

    def get_schema():
        return [
            {
                "KodKraju": {
                    "description": "Kod kraju",
                    "label": "Kod kraju",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "Wojewodztwo": {
                    "description": "Województwo",
                    "label": "Województwo",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "Powiat": {
                    "description": "Powiat",
                    "label": "Powiat",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "Gmina": {
                    "description": "Gmina",
                    "label": "Gmina",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "Miejscowosc": {
                    "description": "Miejscowość",
                    "label": "Miejscowość",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {
                "Ulica": {
                    "description": "Ulica",
                    "label": "Ulica",
                    "required": True,
                    "type": "string",
                    "pattern": "^[A-Za-z]{1,30}$",
                }
            },
            {"NrDomu": {"description": "Numer domu", "required": True, "type": "string", "pattern": "^[0-9]{1,10}$"}},
            {
                "NrLokalu": {
                    "description": "Numer lokalu",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{1,10}$",
                }
            },
            {
                "KodPocztowy": {
                    "description": "Kod pocztowy",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{2}-[0-9]{3}$",
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
        declaration_date,
        transaction_date,
        kod_urzedu,
        osoba_fizyczna,
        adres_zamieszkania,
        P_6,
        P_7,
        P_20,
        P_21,
        P_22,
        P_23,
        P_26,
        P_62,
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

    def get_schema():
        return [
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
            *OsobaFizyczna.get_schema(),
            *AdresZamieszkania.get_schema(),
            {
                "UrzadSkarbowy": {
                    "description": "Kod Urzędu Skarbowego",
                    "label": "Kod Urzędu Skarbowego",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{4}$",
                }
            },
            {
                "P_6": {
                    "description": "Cel złożenia deklaracji",
                    "label": "Cel złożenia deklaracji",
                    "required": False,
                    "type": "string",
                    "pattern": "^[0-9]{1}$",
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
                    "description": "Przedmiot opatkowania 1 - umowa",
                    "label": "Przedmiot opatkowania",
                    "required": True,
                    "type": "string",
                    "pattern": "^[0-9]{1}$",
                }
            },
            {
                "P_21": {
                    "description": "Miejsce położenia rzeczy 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa",
                    "label": "Miejsce położenia rzeczy",
                    "required": False,
                    "type": "string",
                    "pattern": "^[0-9]{1}$",
                }
            },
            {
                "P_22": {
                    "description": "Miejsce położenia CWC 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa",
                    "label": "Miejsce położenia CWC",
                    "required": False,
                    "type": "string",
                    "pattern": "^[0-9]{1}$",
                }
            },
            {"P_23": {"description": "Opis", "required": True, "type": "string"}},
            {
                "P_26": {
                    "description": "Podstawa opatkowania określona zgodnie z art. 6 ustawy (po zaokrągleniu do pełnych złotych)",  # noqa: E501
                    "label": "Podstawa opatkowania",
                    "required": True,
                    "type": "number",
                    "minimum": 1000,
                }
            },
            {"P_62": {"description": "Liczba osób", "required": True, "type": "string", "pattern": "^[0-9]{1,3}$"}},
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
        }

    def parse_validate_transaction_date(
        self,
    ):
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
        try:
            self.declaration_date = datetime.datetime.strptime(self.declaration_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid declaration date")  # noqa: B904

        if self.declaration_date < datetime.datetime(2024, 1, 1):
            raise ValueError("Invalid declaration date (before 2024-01-01)")

        return self.declaration_date

    def parse_validate_P6(self):
        try:
            self.P_6 = int(self.P_6)
        except ValueError:
            raise ValueError("Invalid declaration purpose")  # noqa: B904
        if self.P_6 in [1]:
            return self.P_6
        raise ValueError("Invalid declaration purpose")

    def parse_validate_P7(self):
        try:
            self.P_7 = int(self.P_7)
        except ValueError:
            raise ValueError("Invalid declarant")  # noqa: B904
        if self.P_7 in [1, 5]:
            return self.P_7
        raise ValueError("Invalid declarant (must be 1 or 5)")

    def parse_validate_P20(self):
        try:
            self.P_20 = int(self.P_20)
        except ValueError:
            raise ValueError("Invalid taxable subject")  # noqa: B904
        if self.P_20 in [1]:
            return self.P_20
        raise ValueError("Invalid taxable subject (must be 1)")

    def parse_validate_P21(self):
        accepted_values = [0, 1, 2]

        try:
            self.P_21 = int(self.P_21)
        except ValueError:
            raise ValueError("Invalid location of the asset")  # noqa: B904
        if self.P_21 in accepted_values:
            return self.P_21
        raise ValueError("Invalid location of the asset (must be 0, 1 or 2)")

    def parse_validate_P22(self):
        accepted_values = [0, 1, 2]

        try:
            self.P_22 = int(self.P_22)
        except ValueError:
            raise ValueError("Invalid location of the asset")  # noqa: B904
        if self.P_22 in accepted_values:
            return self.P_22
        raise ValueError("Invalid location of the asset (must be 0, 1 or 2)")

    def parse_validate_P26(self):
        try:
            self.P_26 = float(self.P_26)
        except ValueError:
            raise ValueError("Invalid taxation base")  # noqa: B904

        if self.P_26 < 1000:
            raise ValueError("Invalid taxation base (must be greater than 1000)")

        return round(self.P_26, 0)

    def parse_validate_P62(self):
        try:
            self.P_62 = int(self.P_62)
        except ValueError:
            raise ValueError("Invalid number of attachment")  # noqa: B904

        if self.P_62 < 1 and self.P_7 == 1:
            raise ValueError("Invalid number of attachment (must be greater than 0)")

        return self.P_62


def validate_json(json_data):
    # person data:
    osoba_fizyczna = OsobaFizyczna(
        pesel=json_data.get("Pesel"),
        imie=json_data.get("Imie"),
        nazwisko=json_data.get("Nazwisko"),
        imie_ojca=json_data.get("ImieOjca"),
        imie_matki=json_data.get("ImieMatki"),
    ).parse_validate()
    # Address data:
    adres_zamieszkania = AdresZamieszkania(
        kod_kraju=json_data.get("KodKraju"),
        wojewodztwo=json_data.get("Wojewodztwo"),
        powiat=json_data.get("Powiat"),
        gmina=json_data.get("Gmina"),
        miejscowosc=json_data.get("Miejscowosc"),
        ulica=json_data.get("Ulica"),
        nr_domu=json_data.get("NrDomu"),
        nr_lokalu=json_data.get("NrLokalu"),
        kod_pocztowy=json_data.get("KodPocztowy"),
    ).parse_validate()

    pcc_schema = PCC3_6_Schema(
        transaction_date=json_data.get("P_4"),
        declaration_date=json_data.get("DataZlozeniaDeklaracji"),
        kod_urzedu=json_data.get("KodUrzedu"),
        osoba_fizyczna=osoba_fizyczna,
        adres_zamieszkania=adres_zamieszkania,
        P_6=json_data.get("P_6"),
        P_7=json_data.get("P_7"),
        P_20=json_data.get("P_20"),
        P_21=json_data.get("P_21"),
        P_22=json_data.get("P_22"),
        P_23=json_data.get("P_23"),
        P_26=json_data.get("P_26"),
        P_62=json_data.get("P_62"),
    ).parse_validate()

    out = {}

    for key in pcc_schema:
        out[key] = pcc_schema[key]

    for key in osoba_fizyczna:
        out[key] = osoba_fizyczna[key]

    for key in adres_zamieszkania:
        out[key] = adres_zamieszkania[key]

    return out


def parse_validate_acceptance(acceptance):
    try:
        acceptance = int(acceptance)
    except ValueError:
        raise ValueError("Data must be accepted")  # noqa: B904

    return acceptance


def generate_xml(json_schema):
    try:
        parsed_json = validate_json(json_schema)
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
    ET.SubElement(naglowek, "WariantFormularza").text = "6"
    ET.SubElement(naglowek, "CelZlozenia", poz="P_6").text = str(parsed_json.get("declaration_purpose"))
    ET.SubElement(naglowek, "Data", poz="P_4").text = parsed_json.get("transaction_date").strftime("%Y-%m-%d")
    ET.SubElement(naglowek, "KodUrzedu").text = parsed_json.get("kod_urzedu")

    # Podmiot
    podmiot1 = ET.SubElement(deklaracja, "Podmiot1", rola="Podatnik")
    osoba_fizyczna = ET.SubElement(podmiot1, "OsobaFizyczna")
    ET.SubElement(osoba_fizyczna, "PESEL").text = parsed_json.get("pesel")
    ET.SubElement(osoba_fizyczna, "ImiePierwsze").text = parsed_json.get("imie")
    ET.SubElement(osoba_fizyczna, "Nazwisko").text = parsed_json.get("nazwisko")
    ET.SubElement(osoba_fizyczna, "DataUrodzenia").text = parsed_json.get("data_urodzenia").strftime("%Y-%m-%d")
    ET.SubElement(osoba_fizyczna, "ImieOjca").text = parsed_json.get("imie_ojca")
    ET.SubElement(osoba_fizyczna, "ImieMatki").text = parsed_json.get("imie_matki")

    adres = ET.SubElement(podmiot1, "AdresZamieszkaniaSiedziby", rodzajAdresu="RAD")
    adres_pol = ET.SubElement(adres, "AdresPol")
    ET.SubElement(adres_pol, "KodKraju").text = parsed_json.get("kod_kraju")
    ET.SubElement(adres_pol, "Wojewodztwo").text = parsed_json.get("wojewodztwo")
    ET.SubElement(adres_pol, "Powiat").text = parsed_json.get("powiat")
    ET.SubElement(adres_pol, "Gmina").text = parsed_json.get("gmina")
    ET.SubElement(adres_pol, "Ulica").text = parsed_json.get("ulica")
    ET.SubElement(adres_pol, "NrDomu").text = parsed_json.get("nr_domu")
    ET.SubElement(adres_pol, "NrLokalu").text = parsed_json.get("nr_lokalu")
    ET.SubElement(adres_pol, "Miejscowosc").text = parsed_json.get("miejscowosc")
    ET.SubElement(adres_pol, "KodPocztowy").text = parsed_json.get("kod_pocztowy")

    # P32 - stawka podatku

    # Pozycje szczegółowe
    pozycje_szczegolowe = ET.SubElement(deklaracja, "PozycjeSzczegolowe")

    # PODMIOT SKŁADAJACY DEKLARACJE
    # 1: "podmiot zobowiązany solidarnie do zapłaty podatku"
    # 5: "inny podmiot"
    ET.SubElement(pozycje_szczegolowe, "P_7").text = str(parsed_json.get("P_7"))

    # PRZEDMIOT OPODATKOWANIA
    # 1: Umowa
    ET.SubElement(pozycje_szczegolowe, "P_20").text = str(parsed_json.get("P_20"))

    # MIEJSCE POŁOŻENIA RZECZY LUB WYKONYWANIA PRAWA MAJĄTKOWEGO
    ET.SubElement(pozycje_szczegolowe, "P_21").text = str(parsed_json.get("P_21"))

    ET.SubElement(pozycje_szczegolowe, "P_22").text = str(parsed_json.get("P_22"))
    ET.SubElement(pozycje_szczegolowe, "P_23").text = str(parsed_json.get("P_23"))
    # ET.SubElement(pozycje_szczegolowe, "P_24").text = str(parsed_json.get("taxation_base"))
    # ET.SubElement(pozycje_szczegolowe, "P_25").text = "10"
    ET.SubElement(pozycje_szczegolowe, "P_26").text = str(parsed_json.get("P_26"))
    ET.SubElement(pozycje_szczegolowe, "P_27").text = str(parsed_json.get("P_27"))
    ET.SubElement(pozycje_szczegolowe, "P_46").text = str(parsed_json.get("P_46"))
    ET.SubElement(pozycje_szczegolowe, "P_53").text = str(parsed_json.get("P_53"))
    ET.SubElement(pozycje_szczegolowe, "P_62").text = str(parsed_json.get("P_62"))

    # Pouczenia
    ET.SubElement(deklaracja, "Pouczenia").text = str(parsed_json.get("1"))

    # Tworzenie drzewa XML
    tree = ET.ElementTree(deklaracja)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
        tree.write(temp_file.name, encoding="utf-8", xml_declaration=True)
        return temp_file.name


if __name__ == "__main__":
    name = generate_xml(
        {
            "Pesel": "86072926288",
            "P_4": "2024-09-18",
            "DataZlozeniaDeklaracji": "2024-09-19",
            "Imie": "Jan",
            "Nazwisko": "Kowalski",
            "DataUrodzenia": "1986-07-29",
            "ImieOjca": "Jan",
            "ImieMatki": "Maria",
            "KodKraju": "PL",
            "Wojewodztwo": "Małopolskie",
            "Powiat": "Kraków",
            "Gmina": "Kraków",
            "Miejscowosc": "Kraków",
            "Ulica": "Wizjonerów",
            "NrDomu": "7",
            "NrLokalu": "104",
            "KodPocztowy": "31-356",
            "P_6": "1",
            "P_7": "1",
            "P_20": "1",
            "P_21": "1",
            "P_22": "1",
            "P_23": "test123",
            "P_26": "1000",
            "P_62": "1",
            "KodUrzedu": "1234",
        }
    )

    with open(name) as file:
        print(file.read())
