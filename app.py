import os
import threading
from datetime import datetime

import gradio as gr
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from meeting_bot import iniciar_reuniao

# =========================================
# CONFIG
# =========================================

br_timezone = pytz.timezone("America/Sao_Paulo")

scheduler = BackgroundScheduler(timezone=br_timezone)
scheduler.start()


# =========================================
# BOT TRIGGER
# =========================================

def disparar_bot(url):
    thread = threading.Thread(
        target=iniciar_reuniao,
        args=(url,)
    )
    thread.start()


# =========================================
# AGENDAMENTO
# =========================================

def agendar_meeting(url, data_hora):

    if not url:
        return "❌ Informe o link"

    if data_hora.tzinfo is None:
        data_hora = br_timezone.localize(data_hora)

    agora = datetime.now(br_timezone)

    if data_hora < agora:
        return "❌ Data inválida"

    scheduler.add_job(
        disparar_bot,
        trigger="date",
        run_date=data_hora,
        args=[url]
    )

    return f"✅ Agendado para {data_hora}"


# =========================================
# UI
# =========================================

with gr.Blocks() as demo:

    gr.Markdown("# 🤖 Meeting Bot")

    url = gr.Textbox(label="Link da reunião")

    dt = gr.DateTime(label="Data e hora")

    btn = gr.Button("Agendar")

    out = gr.Markdown()

    btn.click(
        agendar_meeting,
        inputs=[url, dt],
        outputs=out
    )


# =========================================
# RENDER ENTRYPOINT
# =========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False
    )
