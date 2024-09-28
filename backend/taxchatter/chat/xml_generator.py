import datetime
import tempfile
import xml.etree.ElementTree as ET

required_fields = [
    {"Pesel": {"description": "Numer Pesel", "required": True}},
    {"P_4": {"description": "Data Dokonania czynności", "required": True}},
    {"DataZlozeniaDeklaracji": {"description": "Data złożenia deklaracji", "required": False}},
    {"Imie": {"description": "Imię", "required": True}},
    {"Nazwisko": {"description": "Nazwisko", "required": True}},
    # {"DataUrodzenia": {"description": "Data urodzenia", "required": True}},
    {"ImieOjca": {"description": "Imię ojca", "required": True}},
    {"ImieMatki": {"description": "Imię matki", "required": True}},
    {"KodKraju": {"description": "Kod kraju", "required": True}},
    {"Wojewodztwo": {"description": "Województwo", "required": True}},
    {"Powiat": {"description": "Powiat", "required": True}},
    {"Gmina": {"description": "Gmina", "required": True}},
    {"Ulica": {"description": "Ulica", "required": True}},
    {"NrDomu": {"description": "Numer domu", "required": True}},
    {"NrLokalu": {"description": "Numer lokalu", "required": True}},
    {"Miejscowosc": {"description": "Miejscowość", "required": True}},
    {"KodPocztowy": {"description": "Kod pocztowy", "required": True}},
    # {"UrzadSkarbowy": "Kod Urzędu Skarbowego"},
    {"P_6": {"description": "Cel złożenia deklaracji", "required": False}},
    {
        "P_7": {
            "description": "Podmiot składający deklarację 1 - podmiot zobowiązany solidarnie do zapłaty podatku, 5 - \
inny podmiot",
            "required": True,
        }
    },
    {"P_20": {"description": "Przedmiot opatkowania 1 - umowa", "required": True}},
    {
        "P_21": {
            "description": "Miejsce położenia rzeczy 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa",
            "required": False,
        }
    },
    {
        "P_22": {
            "description": "Miejsce położenia CWC 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa",
            "required": False,
        }
    },
    {"P_23": {"description": "Opis", "required": True}},
    {
        "P_26": {
            "description": "Podstawa opatkowania określona zgodnie z art. 6 ustawy (po zaokrągleniu do pełnych złotych)",  # noqa: E501
            "required": True,
        }
    },
    {"P_62": {"description": "Liczba osób", "required": True}},
]


def validate_json(json_data):
    # transaction_date
    pesel = validate_pesel(json_data.get("Pesel"))
    P_4 = parse_validate_transaction_date(json_data.get("P_4"))
    declaration_date = parse_validate_declaration_date(json_data.get("DataZlozeniaDeklaracji", datetime.datetime.now()))
    imie = json_data.get("Imie")
    nazwisko = json_data.get("Nazwisko")
    data_urodzenia = get_data_urodzenia(pesel)
    # data_urodzenia = json_data.get("DataUrodzenia")
    imie_ojca = json_data.get("ImieOjca")
    imie_matki = json_data.get("ImieMatki")
    kod_kraju = json_data.get("KodKraju")
    wojewodztwo = json_data.get("Wojewodztwo")
    powiat = json_data.get("Powiat")
    gmina = json_data.get("Gmina")
    ulica = json_data.get("Ulica")
    nr_domu = json_data.get("NrDomu")
    nr_lokalu = json_data.get("NrLokalu")
    miejscowosc = json_data.get("Miejscowosc")
    kod_pocztowy = json_data.get("KodPocztowy")
    P_6 = parse_validate_P6(json_data.get("P_6"))
    P_7 = parse_validate_P7(json_data.get("P_7"))
    P_20 = parse_validate_P20(json_data.get("P_20"))
    P_21 = parse_validate_P21(json_data.get("P_21", "0"))
    P_22 = parse_validate_P22(json_data.get("P_22", "0"))
    P_23 = parse_validate_P23(json_data.get("P_23"))
    P_26 = parse_validate_P26(json_data.get("P_26"))
    P_62 = parse_validate_P62(json_data.get("P_62"))

    return {
        "pesel": pesel,
        "transaction_date": P_4,
        "declaration_date": declaration_date,
        "imie": imie,
        "nazwisko": nazwisko,
        "data_urodzenia": data_urodzenia,
        "imie_ojca": imie_ojca,
        "imie_matki": imie_matki,
        "kod_kraju": kod_kraju,
        "wojewodztwo": wojewodztwo,
        "powiat": powiat,
        "gmina": gmina,
        "ulica": ulica,
        "nr_domu": nr_domu,
        "nr_lokalu": nr_lokalu,
        "miejscowosc": miejscowosc,
        "kod_pocztowy": kod_pocztowy,
        "P_6": P_6,
        "P_7": P_7,
        "P_20": P_20,
        "P_21": P_21,
        "P_22": P_22,
        "P_23": P_23,
        "P_26": P_26,
        "P_62": P_62,
    }


def validate_pesel(pesel):
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


def parse_validate_transaction_date(transaction_date, declaration_date):
    try:
        transaction_date = datetime.datetime.strptime(transaction_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid transaction date")  # noqa: B904

    if transaction_date < datetime.datetime(2024, 1, 1):
        raise ValueError("Invalid transaction date (before 2024-01-01)")

    if transaction_date >= declaration_date:
        raise ValueError("Transaction date must be before declaration date")

    return transaction_date


def parse_validate_declaration_date(declaration_date):
    try:
        declaration_date = datetime.datetime.strptime(declaration_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid declaration date")  # noqa: B904

    if declaration_date < datetime.datetime(2024, 1, 1):
        raise ValueError("Invalid declaration date (before 2024-01-01)")

    return declaration_date


def get_data_urodzenia(pesel):
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


def parse_validate_P6(declaration_purpose):
    try:
        declaration_purpose = int(declaration_purpose)
    except ValueError:
        raise ValueError("Invalid declaration purpose")  # noqa: B904
    if declaration_purpose in [1]:
        return declaration_purpose
    raise ValueError("Invalid declaration purpose")


def parse_validate_P7(declarant):
    try:
        declarant = int(declarant)
    except ValueError:
        raise ValueError("Invalid declarant")  # noqa: B904
    if declarant in [1, 5]:
        return declarant
    raise ValueError("Invalid declarant (must be 1 or 5)")


def parse_validate_P20(taxable_subject):
    try:
        taxable_subject = int(taxable_subject)
    except ValueError:
        raise ValueError("Invalid taxable subject")  # noqa: B904
    if taxable_subject in [1]:
        return taxable_subject
    raise ValueError("Invalid taxable subject (must be 1)")


def parse_validate_P21(location):
    accepted_values = [0, 1, 2]

    try:
        location_of_the_asset = int(location)
    except ValueError:
        raise ValueError("Invalid location of the asset")  # noqa: B904
    if location_of_the_asset in accepted_values:
        return location_of_the_asset
    raise ValueError("Invalid location of the asset (must be 0, 1 or 2)")


def parse_validate_P22(location_of_the_asset):
    accepted_values = [0, 1, 2]

    try:
        location_of_the_asset = int(location_of_the_asset)
    except ValueError:
        raise ValueError("Invalid location of the asset")  # noqa: B904
    if location_of_the_asset in accepted_values:
        return location_of_the_asset
    raise ValueError("Invalid location of the asset (must be 0, 1 or 2)")


def parse_validate_P23(description):
    return description


def parse_validate_P26(taxation_base):
    try:
        value = float(taxation_base)
    except ValueError:
        raise ValueError("Invalid taxation base")  # noqa: B904

    if value < 1000:
        raise ValueError("Invalid taxation base (must be greater than 1000)")

    return round(value, 0)


def parse_validate_P62(number_of_attachment, declarant):
    try:
        number_of_attachment = int(number_of_attachment)
    except ValueError:
        raise ValueError("Invalid number of attachment")  # noqa: B904

    if number_of_attachment < 1 and declarant == 1:
        raise ValueError("Invalid number of attachment (must be greater than 0)")

    return number_of_attachment


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
    generate_xml(
        {
            "pesel": "86072926288",
            "transaction_date": "2024-09-18",
            "declaration_date": "2024-09-19",
            "imie": "Jan",
            "nazwisko": "Kowalski",
            "data_urodzenia": "1986-07-29",
            "imie_ojca": "Jan",
            "imie_matki": "Maria",
            "kod_kraju": "PL",
            "wojewodztwo": "Mazowieckie",
            "powiat": "Mazowiecki",
            "gmina": "Mazowiecka",
            "ulica": "Mazowiecka",
            "nr_domu": "1",
            "nr_lokalu": "1",
            "miejscowosc": "Mazowiecka",
            "kod_pocztowy": "05-001",
            "P_6": "1",
            "P_7": "1",
            "P_20": "1",
            "P_21": "1",
            "P_22": "1",
            "P_23": "test123",
            "P_26": "1000",
            "P_62": "1",
        }
    )
