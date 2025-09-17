from django.db import models
import json

class KategoriaDanychWrazliwych(models.TextChoices):
    OSOBOWE = "Personal Data", "Dane osobowe"
    FINANSOWE = "Financial Data", "Dane finansowe"
    BADAWCZE = "Research Data", "Dane badawcze"
    BIOMETRYCZNE = "Biometric Data", "Dane biometryczne"
    DZIECI = "Children Data", "Dane dzieci"
    EDUKACYJNE = "Educational Data", "Dane edukacyjne"
    KRYMINALNE = "Criminal Data", "Dane kryminalne"
    LOGOWANIE = "Login Data", "Dane logowania"
    LOKALIZACJA = "Location Data", "Dane lokalizacyjne"
    OBYWATELSTWA = "Citizenship Data", "Dane obywatelstwa"
    POLITYCZNE_RELIGIJNE = "Political or Religious Data", "Dane polityczne lub religijne"
    PRACOWNICZE = "Employee Data", "Dane pracownicze"
    TECHNOLOGICZNE = "Technological Data", "Dane technologiczne"    
    ZDROWOTNE = "Health Data", "Dane zdrowotne"

class WyboryJurysdykcji(models.TextChoices):
    RODO = "RODO", "Rozporządzenie Ogólne o Ochronie Danych (RODO)"
    GDPR = "GDPR", "General Data Protection Regulation (GDPR)"
    ISO_IEC_27701 = "ISO/IEC 27701", "Międzynarodowy standard zarządzania ochroną danych (ISO/IEC 27701)"
    ANPD = "ANPD", "Autoridade Nacional de Proteção de Dados (Brazylia)"
    APPI = "APPI", "Act on the Protection of Personal Information (Japonia)"
    BDSG = "Bundesdatenschutzgesetz (Niemcy)"
    CALOPPA = "CALOPPA", "California Online Privacy Protection Act (USA)"
    CPA = "CPA", "Colorado Privacy Act"
    CCPA = "CCPA", "California Consumer Privacy Act (CCPA)"
    CCPR = "CCPR", "Consumer Credit Protection Regulation (Australia)"
    CORPA = "CORPA", "Chilldren's Online Privacy Protection Act (USA)"
    DPA = "Data Protection Act (Wielka Brytania)"
    FADP = "FADP", "Federal Act on Data Protection (Szwajcaria)"
    FERPA = "FERPA", "Family Educational Rights and Privacy Act (USA)"
    GDPL = "GDPL", "General Data Protection Law (Chiny)"
    HIPAA = "HIPAA", "Health Insurance Portability and Accountability Act (HIPAA)"
    INDIA_DPDP = "INDIA-DPDP", "Digital Personal Data Protection Act (Indie)"
    KVKK = "KVKK", "Kişisel Verilerin Korunması Kanunu (Turcja)"
    LGPD = "LGPD", "Lei Geral de Proteção de Dados (Brazylia)"
    NZPA = "NZPA", "New Zealand Privacy Act"
    PDPA = "PDPA", "Personal Data Protection Act (Singapur)"
    PDPO = "PDPO", "Personal Data (Privacy) Ordinance (Hongkong)"
    PIPEDA = "PIPEDA", "Personal Information Protection and Electronic Documents Act (Kanada)"
    POPIA = "POPIA", "Protection of Personal Information Act (RPA)"
    SOX = "SOX", "Sarbanes-Oxley Act (USA)"
    VCPA = "VCDPA", "Virginia Consumer Data Protection Act"
    INNE = "INNE", "Inne"

class Sektor(models.TextChoices):
    ADMINISTRACJA = "Administracja", "Sektor Administracji Publicznej"
    AGROBIZNES = "Agrobiznes", "Sektor Agrobiznesu"
    NAUKA = "Nauka", "Sektor Badawczy i Naukowy"
    BUDOWNICTWO = "Budownictwo", "Sektor Budowlany i Inżynieryjny"
    EDUKACJA = "Edukacja", "Sektor Edukacyjny"
    ENERGIA = "Energia", "Sektor Energii i Usług Komunalnych"
    FINANSE = "Finanse", "Sektor Finansowy"
    HANDEL = "Handel", "Sektor Handlowy i E-commerce"
    LOGISTYKA = "Logistyka", "Sektor Logistyczny i Transportowy"
    PRZEMYSŁ_LOTNICZY = "Lotnictwo", "Sektor Lotniczy i Kosmiczny"
    MARKETING = "Marketing", "Sektor Marketingu i Reklamy"
    MEDIA = "Media", "Sektor Mediów i Rozrywki"
    MEDYCYNA = "Medycyna", "Sektor Medyczny"
    MODA = "Moda", "Sektor Mody i Urody"
    MOTORYZACJA = "Motoryzacja", "Sektor Motoryzacyjny"
    NIERUCHOMOŚCI = "Nieruchomości", "Sektor Nieruchomości"
    SRODOWISKO = "Środowisko", "Sektor Ochrony Środowiska"
    NON_PROFIT = "Non-Profit", "Sektor Organizacji Non-Profit"
    OCHRONA = "Ochrona", "Sektor Prywatnych Usług Ochrony"
    PRAWO = "Prawo", "Sektor Prawny i Usług Profesjonalnych"   
    PRODUKCJA = "Produkcja", "Sektor Produkcji"
    SZTUKA = "Sztuka", "Sektor Sztuki i Projektowania"
    SPORT = "Sport", "Sektor Sportowy i Rekreacyjny"
    TELEKOMUNIKACJA = "Telekomunikacja", "Sektor Telekomunikacyjny"
    PODROZE = "Podróże", "Sektor Turystyczny i Hotelarski"
    ROLNICTWO = "Rolnictwo", "Sektor Rolniczy"
    TECHNOLOGIE = "Technologie", "Sektor Technologiczny"
    UBEZPIECZENIA = "Ubezpieczenia", "Sektor Ubezpieczeń"
    ZASOBY_LUDZKIE = "Zasoby Ludzkie", "Sektor Zarządzania Zasobami Ludzkimi"
    ZYWNOSC = "Żywność", "Sektor Żywności i Napojów"
    INNE = "Inne", "Inne"

class UserData(models.Model):
    typ_danych = models.TextField(
        help_text="Lista typów danych wrażliwych w formacie JSON."
    )
    sektor = models.CharField(
        max_length=100,
        choices=Sektor.choices,
        default=Sektor.INNE
    )
    jurysdykcja = models.CharField(
        max_length=100,
        choices = WyboryJurysdykcji.choices,
        default = WyboryJurysdykcji.RODO
        )
    opis = models.TextField(blank=True, null=True)

    def set_typ_danych(self, typy):
        self.typ_danych = json.dumps(typy)

    def get_typ_danych(self):
        return json.loads(self.typ_danych)

    def __str__(self):
        typy = ", ".join(self.get_typ_danych)
        return f"{typy} - {self.get_sektor_display()} - {self.get_jurysdykcja_display()}"
