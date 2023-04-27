import gradio as gr
import requests
import json
from pathlib import Path



all_params=[]

def clean_path(base_path: str, path: str):
    """"Strips unusual symbols and forcibly builds a path as relative to the intended directory."""
    # TODO: Probably could do with a security audit to guarantee there's no ways this can be bypassed to target an unwanted path.
    # Or swap it to a strict whitelist of [a-zA-Z_0-9]
    path = path.replace('\\', '/').replace('..', '_')
    if base_path is None:
        return path

    return f'{Path(base_path).absolute()}/{path}'
def load_params():
    
    f_name= clean_path('extensions/discord_bot', f'config.json')
    if Path(f_name).is_file():
        with open(f_name, 'r', encoding='utf-8') as format_file:
            all_params: dict[str, str] = json.load(format_file)
        return all_params


def output_modifier(string):
    global all_params
    all_params=load_params()
    # Replace the webhook URL with your own
    webhook_url = all_params

    # Define the message payload
    payload = {
        "content": string.replace("#", "")
    }

    # Send the POST request to the webhook URL with the payload
    response = requests.post(webhook_url, json=payload)

    # Check the response status code
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Error: {response.status_code}")

    return string
def ui():
    global all_params
    all_params=load_params()
    # JS to initialize the params for JS modules, we need to place this here because the params are loaded from settings.json when ui() is called
    
    with gr.Accordion('Discord Bot - Settings', elem_id='discord-bot-settings_accordion', open=True,):
        # Settings warning message and accordion style
        webhook_url = gr.Textbox(label='Webhook URL', info='The webhook URL for your bot',value=all_params)
        gr.HTML(value=f'''
         
          <p class="settings-warning" style="margin-bottom: 0;">Please wait for text generation to end before changing settings</p>
        ''')
    all_params = [webhook_url]
    webhook_url.change(save_settings,all_params)

def save_settings(all_params):
    with open(clean_path('extensions/discord_bot', f'config.json'), 'w', encoding='utf-8') as formatFile:
        json.dump(all_params, formatFile, ensure_ascii=False, indent=4)
 