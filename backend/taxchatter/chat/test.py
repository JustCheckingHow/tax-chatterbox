from chat.xml_generator import generate_xml
from django.test import TestCase


class TestXmlGenerator(TestCase):
    def test_generate_xml(self):
        results = generate_xml(
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
                "Wojewodztwo": "Mazowieckie",
                "Powiat": "Makowski",
                "Gmina": "Krasnosielc",
                "Ulica": "Mazowiecka",
                "NrDomu": "1",
                "NrLokalu": "1",
                "Miejscowosc": "Mazowiecka",
                "KodPocztowy": "05-001",
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

        self.assertIsNotNone(results)
        print(results)
        # self.assertTrue(xml_content.startswith("<?xml version='1.0' encoding='UTF-8'?>"))
