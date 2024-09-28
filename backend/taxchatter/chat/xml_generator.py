import datetime
import xml.etree.ElementTree as ET

required_fields = [
    {"Pesel": "Numer Pesel"},
    {"Imie": "Imię"},
    {"Nazwisko": "Nazwisko"},
    {"DataUrodzenia": "Data urodzenia"},
    {"ImieOjca": "Imię ojca"},
    {"ImieMatki": "Imię matki"},
    {"KodKraju": "Kod kraju"},
    {"Wojewodztwo": "Województwo"},
    {"Powiat": "Powiat"},
    {"Gmina": "Gmina"},
    {"Ulica": "Ulica"},
    {"NrDomu": "Numer domu"},
    {"NrLokalu": "Numer lokalu"},
    {"Miejscowosc": "Miejscowość"},
    {"KodPocztowy": "Kod pocztowy"},
    # {"UrzadSkarbowy": "Kod Urzędu Skarbowego"},
    {"CelZlozeniaDeklaracji": "Cel złożenia deklaracji"},
    {"Podmiot": "Podmiot"},
    {"PrzedmiotOpatkowania": "Przedmiot opatkowania"},
    {"MiesjcePolozeniaRzeczy": "Miejsce położenia rzeczy"},
    {"MiesjcePolozeniaCwc": "Miejsce położenia CWC"},
    {"Opis": "Opis"},
    {"P_7": "Podmiot składający deklarację 1 - podmiot zobowiązany solidarnie do zapłaty podatku, 5 - inny podmiot"},
    {"P_20": "Przedmiot opatkowania 1 - umowa"},
    {"P_21": "Miejsce położenia rzeczy 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa"},
    {"P_22": "Miejsce położenia CWC 0 - nie dotyczy, 1 - w Polsce, 2 - poza granicą państwa"},
    {"P_23": "Opis"},
    {"P_26": "Podstawa opatkowania określona zgodnie z art. 6 ustawy (po zaokrągleniu do pełnych złotych)"},
    # {"P_27": "Podatek należny "},
    # {"P_46": "Podatek wymagany"},
    # {"P_53": "Podatek do zapłaty"},
    {"P_62": "Liczba osób"},
]

# Pesel
# data dokonania czynności i zawarcia umowy


input_json_schema = {
    "pesel": "1100901142",
    "kod_urzedu": "0271",
    "transaction_date": "2024-09-18",  # P4
    "declaration_date": "2024-08-18",
    "declaration_purpose": "1",  # P6
    "declarant": "1",  # P7
    "taxable_subject": "1",  # P20
    "location_of_the_asset": "1",  # P21
    "location_of_cwc": "1",  # P22
    "description": "test123",  # P23
    "taxation_base": 1000,  # P26
    # "taxation_rate": 10,
    "taxation_amount": 100,  # P27 to calculate
    "tax_required": 123,  # P46
    "tax_to_pay": 123,  # P53
    "number_of_attachment": 1,  # P62
    "acceptance": 1,  # I accept the instruction
}


def parse_json(json_data):
    # transaction_date
    transaction_date = json_data.get("transaction_date")
    declaration_date = json_data.get("declaration_date", datetime.datetime.now())
    declaration_purpose = json_data.get("declaration_purpose")
    declarant = json_data.get("declarant")
    taxable_subject = json_data.get("taxable_subject")
    location_of_the_asset = json_data.get("location_of_the_asset", 0)
    location_of_cwc = json_data.get("location_of_cwc", 0)
    description = json_data.get("description")
    taxation_base = json_data.get("taxation_base")
    taxation_amount = json_data.get("taxation_amount")
    tax_required = json_data.get("tax_required")
    tax_to_pay = json_data.get("tax_to_pay")
    number_of_attachment = json_data.get("number_of_attachment")
    acceptance = json_data.get("acceptance")

    declaration_date = parse_validate_declaration_date(declaration_date)
    transaction_date = parse_validate_transaction_date(transaction_date, declaration_date)

    declaration_purpose = parse_validate_declaration_purpose(declaration_purpose)
    declarant = parse_validate_declarant(declarant)
    taxable_subject = parse_validate_taxable_subject(taxable_subject)
    location_of_the_asset = parse_validate_location_of_the_asset(location_of_the_asset)
    description = parse_validate_description(description)
    taxation_base = parse_validate_taxation_base(taxation_base)
    taxation_amount = round(taxation_base * 0.02, 0)
    tax_required = taxation_amount
    tax_to_pay = round(tax_required * 0.02, 0)
    number_of_attachment = parse_validate_number_of_attachment(number_of_attachment, declarant)
    acceptance = parse_validate_acceptance(acceptance)

    return {
        "transaction_date": transaction_date,
        "declaration_date": declaration_date,
        "declaration_purpose": declaration_purpose,
        "declarant": declarant,
        "taxable_subject": taxable_subject,
        "location_of_the_asset": location_of_the_asset,
        "location_of_cwc": location_of_cwc,
        "description": description,
        "taxation_base": taxation_base,
        "taxation_amount": taxation_amount,
        "tax_required": tax_required,
        "tax_to_pay": tax_to_pay,
        "number_of_attachment": number_of_attachment,
        "acceptance": acceptance,
    }


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


def parse_validate_declaration_purpose(declaration_purpose):
    try:
        declaration_purpose = int(declaration_purpose)
    except ValueError:
        raise ValueError("Invalid declaration purpose")  # noqa: B904
    if declaration_purpose in [1]:
        return declaration_purpose
    raise ValueError("Invalid declaration purpose")


def parse_validate_declarant(declarant):
    try:
        declarant = int(declarant)
    except ValueError:
        raise ValueError("Invalid declarant")  # noqa: B904
    if declarant in [1, 5]:
        return declarant
    raise ValueError("Invalid declarant (must be 1 or 5)")


def parse_validate_taxable_subject(taxable_subject):
    try:
        taxable_subject = int(taxable_subject)
    except ValueError:
        raise ValueError("Invalid taxable subject")  # noqa: B904
    if taxable_subject in [1]:
        return taxable_subject
    raise ValueError("Invalid taxable subject (must be 1)")


def parse_validate_location_of_the_asset(location_of_the_asset):
    accepted_values = [0, 1, 2]

    try:
        location_of_the_asset = int(location_of_the_asset)
    except ValueError:
        raise ValueError("Invalid location of the asset")  # noqa: B904
    if location_of_the_asset in accepted_values:
        return location_of_the_asset
    raise ValueError("Invalid location of the asset (must be 0, 1 or 2)")


def parse_validate_description(description):
    return description


def parse_validate_taxation_base(taxation_base):
    try:
        value = float(taxation_base)
    except ValueError:
        raise ValueError("Invalid taxation base")  # noqa: B904

    if value < 1000:
        raise ValueError("Invalid taxation base (must be greater than 1000)")

    return round(value, 0)


def parse_validate_taxation_amount(taxation_amount):
    return taxation_amount


def parse_validate_tax_required(tax_required):
    return tax_required


def parse_validate_tax_to_pay(tax_to_pay):
    return tax_to_pay


def parse_validate_number_of_attachment(number_of_attachment, declarant):
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
        parsed_json = parse_json(json_schema)
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
    ET.SubElement(naglowek, "KodUrzedu").text = "0271"

    # Podmiot
    podmiot1 = ET.SubElement(deklaracja, "Podmiot1", rola="Podatnik")
    osoba_fizyczna = ET.SubElement(podmiot1, "OsobaFizyczna")
    ET.SubElement(osoba_fizyczna, "PESEL").text = "1100901142"
    ET.SubElement(osoba_fizyczna, "ImiePierwsze").text = "JAN"
    ET.SubElement(osoba_fizyczna, "Nazwisko").text = "ŚPIEWAK"
    ET.SubElement(osoba_fizyczna, "DataUrodzenia").text = "1998-10-09"
    ET.SubElement(osoba_fizyczna, "ImieOjca").text = "ADRIAN"
    ET.SubElement(osoba_fizyczna, "ImieMatki").text = "JOANNA"

    adres = ET.SubElement(podmiot1, "AdresZamieszkaniaSiedziby", rodzajAdresu="RAD")
    adres_pol = ET.SubElement(adres, "AdresPol")
    ET.SubElement(adres_pol, "KodKraju").text = "PL"
    ET.SubElement(adres_pol, "Wojewodztwo").text = "MAŁOPOLSKIE"
    ET.SubElement(adres_pol, "Powiat").text = "M. KRAKÓW"
    ET.SubElement(adres_pol, "Gmina").text = "M. KRAKÓW"
    ET.SubElement(adres_pol, "Ulica").text = "KRAKOWSKA"
    ET.SubElement(adres_pol, "NrDomu").text = "10"
    ET.SubElement(adres_pol, "NrLokalu").text = "25"
    ET.SubElement(adres_pol, "Miejscowosc").text = "KRAKÓW"
    ET.SubElement(adres_pol, "KodPocztowy").text = "31-331"

    # P32 - stawka podatku

    # Pozycje szczegółowe
    pozycje_szczegolowe = ET.SubElement(deklaracja, "PozycjeSzczegolowe")

    # PODMIOT SKŁADAJACY DEKLARACJE
    # 1: "podmiot zobowiązany solidarnie do zapłaty podatku"
    # 5: "inny podmiot"
    ET.SubElement(pozycje_szczegolowe, "P_7").text = str(parsed_json.get("declarant"))

    # PRZEDMIOT OPODATKOWANIA
    # 1: Umowa
    ET.SubElement(pozycje_szczegolowe, "P_20").text = str(parsed_json.get("taxable_subject"))

    # MIEJSCE POŁOŻENIA RZECZY LUB WYKONYWANIA PRAWA MAJĄTKOWEGO
    ET.SubElement(pozycje_szczegolowe, "P_21").text = str(parsed_json.get("location_of_the_asset"))

    ET.SubElement(pozycje_szczegolowe, "P_22").text = str(parsed_json.get("location_of_cwc"))
    ET.SubElement(pozycje_szczegolowe, "P_23").text = str(parsed_json.get("description"))
    # ET.SubElement(pozycje_szczegolowe, "P_24").text = str(parsed_json.get("taxation_base"))
    # ET.SubElement(pozycje_szczegolowe, "P_25").text = "10"
    ET.SubElement(pozycje_szczegolowe, "P_26").text = str(parsed_json.get("taxation_base"))
    ET.SubElement(pozycje_szczegolowe, "P_27").text = str(parsed_json.get("taxation_amount"))
    ET.SubElement(pozycje_szczegolowe, "P_46").text = str(parsed_json.get("tax_required"))
    ET.SubElement(pozycje_szczegolowe, "P_53").text = str(parsed_json.get("tax_to_pay"))
    ET.SubElement(pozycje_szczegolowe, "P_62").text = str(parsed_json.get("number_of_attachment"))

    # Pouczenia
    ET.SubElement(deklaracja, "Pouczenia").text = str(parsed_json.get("acceptance"))

    # Tworzenie drzewa XML
    tree = ET.ElementTree(deklaracja)

    # Zapisywanie do pliku
    tree.write("deklaracja.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    generate_xml(
        {
            "transaction_date": "2024-09-18",
            "declaration_date": "2024-09-19",
            "declaration_purpose": "1",
            "declarant": "1",
            "taxable_subject": "1",
            "location_of_the_asset": "1",
            "location_of_cwc": "1",
            "description": "test123",
            "taxation_base": 1000,
            "taxation_amount": 20,
            "tax_required": 30,
            "tax_to_pay": 40,
            "number_of_attachment": 1,
            "acceptance": 1,
        }
    )
