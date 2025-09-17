from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
from .forms import UserDataForm
from .models import UserData
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import logging  # Logowanie błędów do konsoli
from .models import Sektor, KategoriaDanychWrazliwych, WyboryJurysdykcji
import textwrap

# Ustawienia loggera
logger = logging.getLogger(__name__)

def identify_sensitive_data(data_type):
    sensitive_data = {
        "osobowe": ["Imię i nazwisko", "Adres e-mail", "PESEL"],
        "finansowe": ["Numer karty kredytowej", "Numer konta bankowego"]
    }
    return sensitive_data.get(data_type.lower(), [])

def generate_strategy(sektor, jurysdykcja, typ_danych_list):
    strategy = {
        "policies": ["Użycie szyfrowania", "Dwuskładnikowa autoryzacja"],
        "technical_recommendations" : ["Firewall", "Regularne backupy"],
        "monitoring": ["Cykliczne audyty", "Zarządzanie naruszeniami danych"]
    }

    # Dodanie specyficznych polityk dla typu danych
    for typ_danych in typ_danych_list:
        # Sprawdz czy obecny typ pasuje do kategorii
        if typ_danych == KategoriaDanychWrazliwych.ZDROWOTNE:
            strategy["policies"].append("Zgodnoć z zasadami RODO dla danych medycznych")
            strategy["technical_recommendations"].append("Bezpieczne przechowywanie danych pacjentów (np. EHR)")

        if typ_danych == KategoriaDanychWrazliwych.FINANSOWE:
           strategy["policies"].append("Ochrona danych płatniczych zgodnie z PCI DSS")
           strategy["technical_recommendations"].append("Tokenizacja numerów kart")

        if typ_danych == KategoriaDanychWrazliwych.OSOBOWE:
            strategy["policies"].append("Zgodność z zasadami ochrony danych osobowych (RODO)")
            strategy["technical_recommendations"].append("Szyfrowanie danych osobowych podczas przechowywania i transmisji")

        if typ_danych == KategoriaDanychWrazliwych.BADAWCZE:
            strategy["policies"].append("Zgodność z zasadami ochrony danych w badaniach naukowych (np. GDPR dla badań)")
            strategy["technical_recommendations"].append("Zabezpieczenie danych badawczych w systemach z ograniczonym dostępem")

        if typ_danych ==  KategoriaDanychWrazliwych.BIOMETRYCZNE:
            strategy["policies"].append("Zgodność z zasadami RODO dla danych biometrycznych")
            strategy["technical_recommendations"].append("Wykorzystanie bezpiecznych metod uwierzytelniania biometrycznego (np. z certyfikowanymi urządzeniami)")

        if typ_danych == KategoriaDanychWrazliwych.DZIECI:
            strategy["policies"].append("Ochrona danych dzieci zgodnie z RODO i ustawą o ochronie dzieci")
            strategy["technical_recommendations"].append("Zgoda rodziców na przetwarzanie danych dzieci")

        if typ_danych == KategoriaDanychWrazliwych.EDUKACYJNE:
            strategy["policies"].append("Zgodność z zasadami ochrony danych w edukacji (np. FERPA w USA)")
            strategy["technical_recommendations"].append("Bezpieczne przechowywanie danych uczniów w systemach z kontrolą dostępu")

        if typ_danych == KategoriaDanychWrazliwych.KRYMINALNE:
            strategy["policies"].append("Ochrona danych kryminalnych zgodnie z odpowiednimi przepisami (np. GDPR i prawo karne)")
            strategy["technical_recommendations"].append("Wysokiej jakości szyfrowanie danych kryminalnych i monitoring dostępu")

        if typ_danych == KategoriaDanychWrazliwych.LOGOWANIE:
            strategy["policies"].append("Bezpieczeństwo danych logowania zgodnie z wymogami RODO i branżowymi standardami")
            strategy["technical_recommendations"].append("Wykorzystanie silnych haseł i uwierzytelniania wieloskładnikowego")

        if typ_danych == KategoriaDanychWrazliwych.LOKALIZACJA:
            strategy["policies"].append("Ochrona danych lokalizacyjnych zgodnie z RODO")
            strategy["technical_recommendations"].append("Ograniczenie zbierania danych lokalizacyjnych do minimum oraz szyfrowanie transmisji")

        if typ_danych == KategoriaDanychWrazliwych.OBYWATELSTWA:
            strategy["policies"].append("Ochrona danych dotyczących obywatelstwa zgodnie z odpowiednimi przepisami prawa")
            strategy["technical_recommendations"].append("Szyfrowanie danych obywatelskich oraz kontrola dostępu")

        if typ_danych == KategoriaDanychWrazliwych.POLITYCZNE_RELIGIJNE:
            strategy["policies"].append("Ochrona danych politycznych i religijnych zgodnie z zasadami RODO")
            strategy["technical_recommendations"].append("Zabezpieczenie danych przed nieautoryzowanym dostępem")

        if typ_danych == KategoriaDanychWrazliwych.PRACOWNICZE:
            strategy["policies"].append("Zgodność z RODO dla danych pracowniczych oraz przepisami prawa pracy")
            strategy["technical_recommendations"].append("Ochrona danych pracowników przy użyciu bezpiecznych systemów HR")

        if typ_danych == KategoriaDanychWrazliwych.TECHNOLOGICZNE:
            strategy["policies"].append("Ochrona danych technologicznych zgodnie z zasadami RODO i najlepszymi praktykami branżowymi")
            strategy["technical_recommendations"].append("Implementacja odpowiednich zabezpieczeń systemów IT (np. firewall, szyfrowanie danych)")


    # Dodanie zależnoci od sektora
    if sektor == Sektor.MEDYCYNA:
        strategy["technical_recommendations"].append("Zasady dostępu zgodne z HIPAA")

    if sektor == Sektor.TECHNOLOGIE:
        strategy["policies"].append("Przestrzeganie zasad dotyczących własności intelektualnej")
        strategy["technical_recommendations"].append("Regularne testy penetracyjne")

    if sektor.lower() == Sektor.EDUKACJA:
        strategy["policies"].append("Zabezpieczenie danych studentów zgodnie z FERPA")
        strategy["monitoring"].append("Raportowanie incydentów wrażliwych danych studentów")

    if sektor == Sektor.ADMINISTRACJA:
        strategy["policies"].append("Zgodność z przepisami dotyczącymi ochrony danych publicznych")
        strategy["technical_recommendations"].append("Wdrażanie certyfikowanych systemów zarządzania bezpieczeństwem (ISO 27001)")

    if sektor == Sektor.AGROBIZNES:
        strategy["policies"].append("Ochrona danych związanych z łańcuchem dostaw rolnych")
        strategy["technical_recommendations"].append("Monitorowanie systemów IoT stosowanych w uprawach i hodowli")

    if sektor == Sektor.NAUKA:
        strategy["policies"].append("Zasady otwartej nauki i ochrona danych badawczych")
        strategy["technical_recommendations"].append("Anonimizacja danych badawczych oraz szyfrowanie")

    if sektor == Sektor.BUDOWNICTWO:
        strategy["policies"].append("Ochrona projektów budowlanych i danych inżynieryjnych")
        strategy["technical_recommendations"].append("Bezpieczne przechowywanie cyfrowych planów i dokumentacji technicznej")

    if sektor == Sektor.ENERGIA:
        strategy["policies"].append("Ochrona infrastruktury krytycznej zgodnie z regulacjami")
        strategy["technical_recommendations"].append("Monitorowanie i ochrona przed cyberzagrożeniami (np. SIEM)")

    if sektor == Sektor.FINANSE:
        strategy["policies"].append("Zgodność z PSD2 i ochroną danych finansowych")
        strategy["technical_recommendations"].append("Monitorowanie transakcji w czasie rzeczywistym")

    if sektor == Sektor.HANDEL:
        strategy["policies"].append("Zgodność z przepisami ochrony danych klientów")
        strategy["technical_recommendations"].append("Bezpieczne systemy przechowywania danych transakcyjnych")

    if sektor == Sektor.LOGISTYKA:
        strategy["policies"].append("Ochrona danych dotyczących łańcucha dostaw i dostawców")
        strategy["technical_recommendations"].append("Monitorowanie logistyki w czasie rzeczywistym z zabezpieczeniem danych")

    if sektor == Sektor.PRZEMYSŁ_LOTNICZY:
        strategy["policies"].append("Ochrona danych w lotnictwie zgodnie z regulacjami ICAO")
        strategy["technical_recommendations"].append("Szyfrowanie i zabezpieczanie danych telemetrycznych")

    if sektor == Sektor.MARKETING:
        strategy["policies"].append("Zgodność z RODO oraz ePrivacy w marketingu")
        strategy["technical_recommendations"].append("Segmentacja i anonimizacja danych klientów")

    if sektor == Sektor.MEDIA:
        strategy["policies"].append("Ochrona danych użytkowników mediów cyfrowych")
        strategy["technical_recommendations"].append("Monitorowanie wycieków danych osobowych")
   
    if sektor == Sektor.MODA:
        strategy["policies"].append("Ochrona danych klientów w branży modowej")
        strategy["technical_recommendations"].append("Bezpieczne systemy do obsługi sklepów internetowych")

    if sektor == Sektor.MOTORYZACJA:
        strategy["policies"].append("Ochrona danych pojazdów i użytkowników IoT")
        strategy["technical_recommendations"].append("Zabezpieczenie komunikacji systemów autonomicznych")

    if sektor == Sektor.NIERUCHOMOŚCI:
        strategy["policies"].append("Ochrona danych klientów w sektorze nieruchomości")
        strategy["technical_recommendations"].append("Szyfrowanie dokumentacji transakcyjnej")

    if sektor == Sektor.SRODOWISKO:
        strategy["policies"].append("Zgodność z przepisami ochrony środowiska")
        strategy["technical_recommendations"].append("Bezpieczne monitorowanie danych o emisjach")

    if sektor == Sektor.NON_PROFIT:
        strategy["policies"].append("Zasady przejrzystości w ochronie danych darczyńców i beneficjentów")
        strategy["technical_recommendations"].append("Ochrona baz danych darczyńców")

    if sektor == Sektor.OCHRONA:
        strategy["policies"].append("Przestrzeganie przepisów ochrony danych w prywatnych usługach ochrony")
        strategy["technical_recommendations"].append("Bezpieczne przechowywanie danych monitoringu")

    if sektor == Sektor.PRAWO:
        strategy["policies"].append("Tajemnica adwokacka i ochrona danych klientów")
        strategy["technical_recommendations"].append("Zabezpieczone systemy zarządzania sprawami prawnymi")

    if sektor == Sektor.PRODUKCJA:
        strategy["policies"].append("Ochrona danych w procesach produkcji i automatyzacji")
        strategy["technical_recommendations"].append("Monitorowanie urządzeń produkcyjnych i zabezpieczenia")

    if sektor == Sektor.SZTUKA:
        strategy["policies"].append("Ochrona praw autorskich i danych twórców")
        strategy["technical_recommendations"].append("Szyfrowanie cyfrowych dzieł sztuki")

    if sektor == Sektor.SPORT:
        strategy["policies"].append("Ochrona danych sportowców i uczestników wydarzeń")
        strategy["technical_recommendations"].append("Zabezpieczenie danych wydarzeń sportowych")

    if sektor == Sektor.TELEKOMUNIKACJA:
        strategy["policies"].append("Przestrzeganie zasad ochrony danych telekomunikacyjnych")
        strategy["technical_recommendations"].append("Szyfrowanie komunikacji i danych użytkowników")

    if sektor == Sektor.PODROZE:
        strategy["policies"].append("Zabezpieczenie danych podróżnych i rezerwacji")
        strategy["technical_recommendations"].append("Anonimizacja danych o trasach podróży")

    if sektor == Sektor.ROLNICTWO:
        strategy["policies"].append("Ochrona danych związanych z działalnością rolniczą")
        strategy["technical_recommendations"].append("Monitorowanie systemów zarządzania uprawami i hodowlą")

    if sektor == Sektor.UBEZPIECZENIA:
        strategy["policies"].append("Przestrzeganie zasad ochrony danych polis i klientów")
        strategy["technical_recommendations"].append("Analiza ryzyka związanego z danymi klientów")

    if sektor == Sektor.ZASOBY_LUDZKIE:
        strategy["policies"].append("Ochrona danych pracowników zgodnie z RODO")
        strategy["technical_recommendations"].append("Bezpieczne systemy zarządzania HR")

    if sektor == Sektor.ZYWNOSC:
        strategy["policies"].append("Bezpieczeństwo danych związanych z produkcją i sprzedażą żywności")
        strategy["technical_recommendations"].append("Monitorowanie danych łańcucha dostaw")

    # Rozbudowanie strategii na podstawie konkretnej jurysdykcji
    if jurysdykcja == WyboryJurysdykcji.RODO or jurysdykcja == WyboryJurysdykcji.GDPR:
        strategy["policies"].append("Anonimizacja danych zgodnie z RODO/GDPR")
        strategy["monitoring"].append("Raportowanie naruszeń danych osobowych w ciągu 72 godzin")

    if jurysdykcja == WyboryJurysdykcji.HIPAA:
        strategy["policies"].append("Zgodność z HIPAA")
        strategy["monitoring"].append("Prowadzenie audytów HIPAA co najmniej raz w roku")

    if jurysdykcja == WyboryJurysdykcji.ISO_IEC_27701:
        strategy["policies"].append("Zgodność z wymaganiami ISO/IEC 27701")
        strategy["technical_recommendations"].append("Implementacja systemu zarządzania ochroną danych (PIMS)")

    if jurysdykcja == WyboryJurysdykcji.ANPD:
        strategy["policies"].append("Zgodność z zasadami ANPD")
        strategy["technical_recommendations"].append("Wdrożenie mechanizmów anonimizacji danych osobowych")

    if jurysdykcja == WyboryJurysdykcji.APPI:
        strategy["policies"].append("Zapewnienie zgodności z APPI (Japonia)")
        strategy["monitoring"].append("Regularne sprawdzanie polityki prywatności użytkowników")

    if jurysdykcja == WyboryJurysdykcji.BDSG:
        strategy["policies"].append("Przestrzeganie przepisów BDSG (Niemcy)")
        strategy["technical_recommendations"].append("Bezpieczne przechowywanie danych na terytorium Niemiec")

    if jurysdykcja == WyboryJurysdykcji.CALOPPA:
        strategy["policies"].append("Publikacja polityki prywatności zgodnie z CALOPPA")
        strategy["technical_recommendations"].append("Zapewnienie dostępu do polityki prywatności na każdej stronie")

    if jurysdykcja == WyboryJurysdykcji.CCPA:
        strategy["policies"].append("Zapewnienie prawa do usunięcia danych przez użytkownika (CCPA)")
        strategy["technical_recommendations"].append("Opt-out tracking systemów analitycznych")
        strategy["monitoring"].append("Regularne audyty zgodności z CCPA")

    if jurysdykcja == WyboryJurysdykcji.CORPA:
        strategy["policies"].append("Ochrona prywatności dzieci zgodnie z COPPA")
        strategy["technical_recommendations"].append("Weryfikacja wieku użytkowników przed rejestracją")

    if jurysdykcja == WyboryJurysdykcji.DPA:
        strategy["policies"].append("Zgodność z Data Protection Act (Wielka Brytania)")
        strategy["technical_recommendations"].append("Zapewnienie przenoszalności danych osobowych użytkowników")

    if jurysdykcja == WyboryJurysdykcji.FADP:
        strategy["policies"].append("Przestrzeganie FADP (Szwajcaria)")
        strategy["technical_recommendations"].append("Zapewnienie zgodności z wymogami dotyczącymi przechowywania danych w Szwajcarii")

    if jurysdykcja == WyboryJurysdykcji.FERPA:
        strategy["policies"].append("Ochrona danych edukacyjnych zgodnie z FERPA")
        strategy["monitoring"].append("Raportowanie incydentów naruszenia danych studentów")

    if jurysdykcja == WyboryJurysdykcji.INDIA_DPDP:
        strategy["policies"].append("Zgodność z DPDP Act (Indie)")
        strategy["technical_recommendations"].append("Zabezpieczenie danych zgodnie z wymogami DPDP")

    if jurysdykcja == WyboryJurysdykcji.LGPD:
        strategy["policies"].append("Zgodność z LGPD (Brazylia)")
        strategy["monitoring"].append("Zapewnienie przejrzystości w procesach przetwarzania danych")

    if jurysdykcja == WyboryJurysdykcji.PDPA:
        strategy["policies"].append("Zgodność z PDPA (Singapur)")
        strategy["technical_recommendations"].append("Zabezpieczenie danych zgodnie z PDPA")

    if jurysdykcja == WyboryJurysdykcji.POPIA:
        strategy["policies"].append("Zgodność z POPIA (RPA)")
        strategy["monitoring"].append("Monitorowanie zgodności z zasadami ochrony danych osobowych")

    if jurysdykcja == WyboryJurysdykcji.SOX:
        strategy["policies"].append("Zgodność z Sarbanes-Oxley Act (USA)")
        strategy["technical_recommendations"].append("Zapewnienie zgodności z wymogami audytowymi SOX")

    if jurysdykcja == WyboryJurysdykcji.VCPA:
        strategy["policies"].append("Zgodność z Virginia Consumer Data Protection Act")
        strategy["technical_recommendations"].append("Zapewnienie prawa do wglądu w dane przez użytkowników")

    return strategy

def generate_pdf_report(strategy, filename="report.pdf"):
    try:
        # Próba rejestracji czcionki DejaVuSans
        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts', 'DejavuSans.ttf')

        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Nie znaleziono czcionki DejaVuSans w standardowych lokalizacjach")

        # Rejestracja czcionki DejaVuSans (obsługuje polskie znaki)
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
        font_name = 'DejaVuSans'
        # print(f"Czcionka załadowana pomylnie z {font_path}")
    except Exception as e:
        print(f"Błąd ładowania czcionki DejaVuSans: {e}")
        font_name = 'Helvetica' # Fallback do standardowej czcionki

    output_dir = "media/reports"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    c = canvas.Canvas(filepath, pagesize=letter)

    # Data wygenerowania raportu
    from datetime import datetime
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M")

    page_width, page_height = letter
    margin = 50 # Marginesy
    y = page_height - 80  # Początkowa pozycja tekstu

    def check_y_position(canvas, y, line_height):
        if y < margin: # Jesli tekst wyjdzie poza margines dolny
            canvas.showPage() # Nowa strona
            canvas.setFont(font_name, 10) # Reset czcionki
            return page_height - 80 # Zresetuj pozycję 'y'
        return y
    
    # Funkcja pomocnicza do zawijania tekstu z uwzględnienie stron
    def draw_wrapped_text(canvas, text, x, y, max_width, line_height):
        lines = textwrap.wrap(text, width = max_width)
        for line in lines:
            y -= line_height
            y = check_y_position(canvas, y, line_height) # Sprawdź pozycję
            canvas.drawString(x, y, line)
        return y

    # Nagłówek na każdej stronie
    def draw_header(canvas, title):
        c.setFont(font_name, 16)
        c.drawString(100, page_height - 50, title)

    # Rysowanie nagłówka
    draw_header(c, "Strategia Zarządzania Prywatnością")

    # Data
    c.setFont(font_name, 10)
    c.drawString(100, 730, f"Wygenerowano: {current_date}".encode('utf-8').decode('utf-8'))
    y -= 20
    c.line(100, y, 500, y)  # Linia oddzielająca
    y -= 30

    # Sekcja polityk
    c.setFont(font_name, 12)
    c.drawString(100, y, "Polityki bezpieczeństwa:".encode('utf-8').decode('utf-8'))
    y -= 20
    c.setFont(font_name, 10)
    for policy in strategy['policies']:
        y = draw_wrapped_text(c, f"• {policy}", 120, y, 60, 12)

    # Sekcja rekomendacji technicznych
    y -= 20 # Dodatkowy odstęp między sekcjami
    c.setFont(font_name, 12)
    c.drawString(100, y, "Rekomendacje techniczne:".encode('utf-8').decode('utf-8'))
    y -= 20
    c.setFont(font_name, 10)
    for rec in strategy['technical_recommendations']:
        y = draw_wrapped_text(c, f"• {rec}", 120, y, 60, 12)

    # Sekcja monitorowania
    y -= 20 # Dodatkowy odstęp między sekcjami
    c.setFont(font_name, 12)
    c.drawString(100, y, "Działania monitorujące:".encode('utf-8').decode('utf-8'))
    y -= 20
    c.setFont(font_name, 10)
    for monitor in strategy['monitoring']:
        y = draw_wrapped_text(c, f"• {monitor}", 120, y, 60, 12)

    # Stopka
    y = check_y_position(c, y, 12)
    c.setFont(font_name, 8)
    c.drawString(100, margin, "Dokument wygenerowany automatycznie. Wymagana weryfikacja przez specjalistę ds. bezpieczeństwa.".encode('utf-8').decode('utf-8'))

    c.save()
    return filepath

def privacy_report(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            user_data = form.save(commit=False) #Przechwytujemy dane, ale nie zapisujemy jeszcze
            typ_danych = form.cleaned_data['typ_danych'] # Lista wybranych typów danych
            user_data.set_typ_danych(typ_danych)
            user_data.save()
            logger.debug(f"Wybrane typy danych: {typ_danych}")  #debugger

            # Generowanie strategii. Przekazujemy listę typów danych do funkcji generującej strategię
            strategy = generate_strategy(user_data.sektor, user_data.jurysdykcja, typ_danych)

            # Generowanie raportu PDF
            try:
                report_filename = generate_pdf_report(strategy)
                if os.path.exists(report_filename):
                    # Zakładając, że MEDIA_URL jest skonfigurowane !!!
                    media_url = settings.MEDIA_URL
                    relative_path = os.path.relpath(report_filename, 'media')
                    return HttpResponse(f"Raport został wygenerowany jako <a href='{media_url}{relative_path}'>{os.path.basename(report_filename)}</a>")
                else:
                    return HttpResponse("Błąd: raport nie został wygenerowany.", status=500)
            except Exception as e:
                logger.error("Błąd generowania raportu", exc_info=True)
                return HttpResponse(f"Błąd podczas generowania raportu: {e}", status= 500)
        else:
            # Formularz jest nieprawidłowy
            return render(request, 'privacy/enter_data.html', {'form': form})
    else:
        # Obsługa zapytania GET
        form = UserDataForm()
    return render(request, 'privacy/enter_data.html', {'form': form})
