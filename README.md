# GPT Order Terminal

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-00d2ff.svg)](https://beta.openai.com/)

This project is a proof of concept for a fully automated restaurant drive-thru order terminal using OpenAI's GPT language model. This code allows you to extract products from a customer order dialog based on a predefined list of valid items which can be ordered. Multilingual input is supported.

## Installation and Usage

1. Clone the repository:

   ```shell
   git clone https://github.com/louis-e/gpt-order-terminal.git
   ```

2. Install the required dependencies:

   ```shell
   pip install openai pvrecorder keyboard
   ```

3. Save your OpenAI API key in a file named `openai_api_key.txt`.

4. Edit the `items.txt` file accordingly to your needs.

5. Run the code:

   ```shell
   python order_terminal.py
   ```

5. Follow the instructions to record the customer dialog. Press ENTER to stop recording.

## Example

```
SYSTEM: Recording customer dialog... Press ENTER to stop recording.
SYSTEM: Customer dialog recorded sucessfully. Transcribing...
SYSTEM: Customer dialog transcribed sucessfully: Hi there, I would like to order a cheeseburger and two cheesy fries as well as a coke. And for my daughter, let me see. One second. Ah, for my daughter I would like to order nachos, two chicken bites and a shake. That's it, thank you!
SYSTEM: Prompt prepared successfully. Sending API call...
SYSTEM: Processed API response successfully.

Processing order: Cheeseburger (1), Cheesy Fries (2), Coke (1), Nachos (1), Chicken Bites (2), Chocolate Shake (1)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.