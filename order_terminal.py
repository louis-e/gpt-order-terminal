import openai, wave, struct, keyboard, os
from pvrecorder import PvRecorder

recorder = PvRecorder(device_index=-1, frame_length=512)
audio = []
AUDIO_PATH = 'order.mp3'

with open('../openai_api_key.txt') as f:
    openai.api_key = f.readline()

# Read the list of valid items from the file
valid_items = ''
for line in open('items.txt'):
    valid_items += ', ' + line.strip()
valid_items = valid_items[2:]

if len(valid_items) == 0:
    print('No valid items found! Please add them to items.txt')
    os._exit(1)


# Record customer dialog
print(f"SYSTEM: Recording customer dialog... Press ENTER to stop recording.")
recorder.start()
while True:
    frame = recorder.read()
    audio.extend(frame)
    if keyboard.is_pressed('enter'):
        break

recorder.stop()
with wave.open(AUDIO_PATH, 'w') as f:
    f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
    f.writeframes(struct.pack("h" * len(audio), *audio))
recorder.delete()


# Transcribe customer dialog
print(f"SYSTEM: Customer dialog recorded sucessfully. Transcribing...")
audio_file = open(AUDIO_PATH, "rb")
try:
    customer_dialog = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        #prompt=valid_items
    ).text
except Exception as e:
    print(f"SYSTEM: Error occured while transcribing customer dialog: {e}")
    os._exit(1)

if len(customer_dialog) == 0:
    print(f"SYSTEM: Error occured while transcribing customer dialog")
    os._exit(1)
print(f"SYSTEM: Customer dialog transcribed sucessfully: {customer_dialog}")


# Create prompt
BASE_PROMPT = """You are the order terminal in a drive thru of a restaurant and your job is to extract the products from the customer dialog.
Extract the products from the customer dialog and respond in the following format: <Product name> (<quantity> <optional additional information>)
The product name must be the exact name of one of the items listed below. If there are multiple products, separate them with a comma.
If there is no additional information, do not include it in the response. If there are no products at all, respond with "NO-PRODUCTS-ORDERED".
If one of the products is not in the list of allowed items, respond with "INVALID-PRODUCT-%PRODUCT%", where %PRODUCT% is the name of the product.

This is the list of allowed items that can be ordered:
%ITEMS%

This is the customer order dialog:
%CUSTOMERDIALOG%
"""

prompt = BASE_PROMPT.replace('%ITEMS%', valid_items)
prompt = prompt.replace('%CUSTOMERDIALOG%', customer_dialog)
prompt = prompt.strip()
print(f"SYSTEM: Prompt prepared successfully. Sending API call...")


# API call
api_call = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.0,
    max_tokens=512,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

response = api_call.choices[0].text.strip()


# Response processing
invalid_items = []
if 'INVALID-PRODUCT-' in response: # Check for invalid products
    for product in response.split(','):
        if 'INVALID-PRODUCT-' in product:
            invalid_items.append(product.replace('INVALID-PRODUCT-', '').strip())
            response = response.replace(',' + product, '')
            
if len(response) == 0: # Check for empty response
    customer_response = 'Error occured while processing order - cancelling order!'
elif response == 'NO-PRODUCTS-ORDERED': # Check for no products
    customer_response = 'No products ordered - cancelling order!'
else:
    customer_response = f"Processing order: {response}"
    if len(invalid_items) > 0:
        customer_response += f"\nThe following products are currently not available: {', '.join(invalid_items)}"

print(f"SYSTEM: Processed API response successfully.\n\n{customer_response}") # Print customer response