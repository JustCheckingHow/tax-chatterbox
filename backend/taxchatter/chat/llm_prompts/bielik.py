RULES = """
Deklarację składa się w przypadku:
• zawarcia umowy: sprzedaży, zamiany rzeczy i praw majątkowych, pożyczki pieniędzy lub
rzeczy oznaczonych tylko co do gatunku (jeśli z góry nie zostanie ustalona suma pożyczki –
deklaracje składa się w przypadku każdorazowej wypłaty środków pieniężnych), o dział
spadku lub zniesienie współwłasności, gdy dochodzi w nich do spłat i dopłat, ustanowienia
odpłatnego użytkowania (w tym nieprawidłowego), depozytu nieprawidłowego lub spółki,
• przyjęcia darowizny z przejęciem długów i ciężarów albo zobowiązania darczyńcy,
• złożenia oświadczenia o ustanowieniu hipoteki lub zawarcia umowy ustanowienia hipoteki,
• uprawomocnia się orzeczenia sądu lub otrzymania wyroku sądu polubownego albo zawarcia
ugody w sprawach umów wyżej wymienionych,
• zawarcia umowy przeniesienia własności – jeśli wcześniej podpisana została umowa
zobowiązująca do przeniesienia własności, a teraz podpisana została umowa przeniesienia tej
własności,
• podwyższenia kapitału w spółce mającej osobowość prawną.
Deklaracji nie składa się, gdy:
• czynność cywilnoprawna jest dokonywana w formie aktu notarialnego i podatek jest
pobierany przez notariusza (płatnika podatku),
• podatnik składa zbiorczą deklarację w sprawie podatku od czynności cywilnoprawnych
(PCC-4),
• podatnikiem jest:
◦ kupujący na własne potrzeby sprzęt rehabilitacyjny, wózki inwalidzkie, motorowery,
motocykle lub samochody osobowe – jeśli ma: orzeczenie o znacznym albo
umiarkowanym stopniu niepełnosprawności (nieważne, jakie ma schorzenie), o
orzeczenie o lekkim stopniu niepełnosprawności w związku ze schorzeniami narządów
ruchu.
◦ organizacja pożytku publicznego – jeśli dokonuje czynności cywilnoprawnych tylko w
związku ze swoją nieodpłatną działalnością pożytku publicznego.
◦ jednostka samorządu terytorialnego,
◦ Skarb Państwa,
◦ Agencja Rezerw Materiałowych,
• korzysta się ze zwolnienia od podatku, gdy:
◦ kupowane są obce waluty,
◦ kupowane są i zamieniane waluty wirtualne,
◦ kupowane są rzeczy ruchome – i ich wartość rynkowa nie przekracza 1 000 zł,
◦ pożyczane jest nie więcej niż 36 120 zł (liczą się łącznie pożyczki z ostatnich 5 lat od
jednej osoby) – jeśli jest to pożyczka od bliskiej rodziny, czyli od: małżonka, dzieci,
wnuków, prawnuków, rodziców, dziadków, pradziadków, pasierbów, pasierbic,
rodzeństwa, ojczyma, macochy, zięcia, synowej, teściów,
◦ pożyczane są pieniądze od osób spoza bliskiej rodziny – jeśli wysokość pożyczki nie
przekracza 1 000 zł.
Deklarację składa się tylko w przypadkach umów, których przedmiotem są rzeczy i prawa majątkowe
(majątek), znajdujące się w Polsce. A jeśli są za granicą – to tylko jeśli ich nabywca mieszka albo ma
siedzibę w Polsce i zawarł umowę w Polsce. W przypadku umowy zamiany wystarczy, że w Polsce jest
jeden z zamienianych przedmiotów
"""

# noqa: E501
STAWKA_PODATKU_RULE = """
Stawki podatku określone są odrębnie dla każdej czynności[1], w tym m.in. wynoszą:
od umowy sprzedaży:
- nieruchomości, rzeczy ruchomych, prawa użytkowania wieczystego, własnościowego spółdzielczego prawa do lokalu mieszkalnego, spółdzielczego prawa do lokalu użytkowego oraz wynikających z przepisów prawa spółdzielczego: prawa do domu jednorodzinnego oraz prawa do lokalu w małym domu mieszkalnym - 2%,
innych praw majątkowych - 1%,
- od umowy pożyczki oraz depozytu nieprawidłowego - 0,5%, (z zastrzeżeniem przypadków, do których ma zastosowanie stawka 20 %),
- od umowy spółki - 0,5%.
WAŻNE: Obowiązuje 20% stawka podatku od umowy pożyczki, depozytu nieprawidłowego, użytkowania nieprawidłowego, jeżeli przed organem podatkowym w toku czynności sprawdzających, kontroli podatkowej, postępowania podatkowego lub kontroli celno-skarbowej:
- podatnik powołuje się na fakt zawarcia umowy pożyczki, depozytu nieprawidłowego lub ustanowienia użytkowania nieprawidłowego albo ich zmiany, a należny podatek od tych czynności nie został zapłacony,
- biorący pożyczkę, o którym mowa w art. 9 pkt 10 lit. b ustawy o podatku od czynności cywilnoprawnych (osoba najbliższa: małżonek, zstępny (dziecko, wnuk, prawnuk), wstępny (rodzice, dziadkowie, pradziadkowie), pasierb, rodzeństwo, ojczym, macocha i inne osoby uważane za zstępnych lub wstępnych w rozumieniu ustawy o podatku od spadków i darowizn), powołuje się na fakt zawarcia umowy pożyczki, a nie spełnił warunku udokumentowania otrzymania pieniędzy na rachunek bankowy, albo jego rachunek prowadzony przez spółdzielczą kasę oszczędnościowo-kredytową lub przekazem pocztowym.
Za zstępnych uważa się również przysposobionych i ich zstępnych oraz osoby, które przebywają lub przebywały w rodzinie zastępczej, w rodzinnym domu dziecka, w placówce opiekuńczo-wychowawczej lub w regionalnej placówce opiekuńczo-terapeutycznej. Za wstępnych uważa się także odpowiednio osoby tworzące rodzinę zastępczą, prowadzące rodzinny dom dziecka lub pracujące z dziećmi w placówce opiekuńczo-wychowawczej lub w regionalnej placówce opiekuńczo-terapeutycznej, a za rodziców uważa się również przysposabiających."""  # noqa: E501

USTAWA_PCC_ART_7 = """
Stawki podatku PCC
1. Stawki podatku wynoszą:
1)od umowy sprzedaży:
a) nieruchomości, rzeczy ruchomych, prawa użytkowania wieczystego, własnościowego spółdzielczego prawa do lokalu mieszkalnego, spółdzielczego prawa do lokalu użytkowego oraz wynikających z przepisów prawa spółdzielczego: prawa do domu jednorodzinnego oraz prawa do lokalu w małym domu mieszkalnym - 2 %,
b) innych praw majątkowych - 1 %;
2)od umów zamiany, dożywocia, o dział spadku, o zniesienie współwłasności oraz darowizny:
a) przy przeniesieniu własności nieruchomości, rzeczy ruchomych, prawa użytkowania wieczystego, własnościowego spółdzielczego prawa do lokalu mieszkalnego, spółdzielczego prawa do lokalu użytkowego oraz wynikających z przepisów prawa spółdzielczego: prawa do domu jednorodzinnego oraz prawa do lokalu w małym domu mieszkalnym - 2 %,
b) przy przeniesieniu własności innych praw majątkowych - 1 %;
3)od umowy ustanowienia odpłatnego użytkowania, w tym nieprawidłowego, oraz odpłatnej służebności - 1 %, z zastrzeżeniem ust. 5;
4)od umowy pożyczki oraz depozytu nieprawidłowego – 0,5%, z zastrzeżeniem ust. 5;
5)(uchylony)
6)(uchylony)
7) od ustanowienia hipoteki:
a) na zabezpieczenie wierzytelności istniejących - od kwoty zabezpieczonej wierzytelności - 0,1 %,
b) na zabezpieczenie wierzytelności o wysokości nieustalonej -19 zł;
8) (uchylony)
9)od umowy spółki - 0,5 %.
2.(uchylony)
3.Podatek pobiera się według stawki najwyższej:
1) jeżeli podatnik dokonując czynności cywilnoprawnej, w wyniku której nastąpiło przeniesienie własności, nie wyodrębnił wartości rzeczy lub praw majątkowych, do których mają zastosowanie różne stawki - od łącznej wartości tych rzeczy lub praw majątkowych;
2)jeżeli przedmiotem umowy zamiany są rzeczy lub prawa majątkowe, co do których obowiązują różne stawki.
4.(uchylony)
5.Stawka podatku wynosi 20%, jeżeli przed organem podatkowym w toku czynności sprawdzających, kontroli podatkowej, postępowania podatkowego lub kontroli celno-skarbowej:
1) podatnik powołuje się na fakt zawarcia umowy pożyczki, depozytu nieprawidłowego lub ustanowienia użytkowania nieprawidłowego albo ich zmiany, a należny podatek od tych czynności nie został zapłacony;
2) biorący pożyczkę, o którym mowa w art. 9 czynności cywilnoprawne zwolnione od podatku pkt 10 lit. b, powołuje się na fakt zawarcia umowy pożyczki, a nie spełnił warunku udokumentowania otrzymania pieniędzy na rachunek bankowy, albo jego rachunek prowadzony przez spółdzielczą kasę oszczędnościowo-kredytową lub przekazem pocztowym.
"""  # noqa: E501
