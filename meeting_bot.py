import time
from playwright.sync_api import sync_playwright


def iniciar_reuniao(url):

    print("Entrando na reunião:", url)

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--use-fake-ui-for-media-stream",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context()

        page = context.new_page()

        page.goto(url)

        time.sleep(10)

        try:
            page.click("text=Continuar sem microfone e câmera")
        except:
            pass

        try:
            page.click("text=Pedir para participar")
        except:
            pass

        print("Bot entrou ou aguardando aprovação...")

        # Simulação de reunião ativa
        time.sleep(300)

        browser.close()
