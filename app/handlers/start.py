from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from app.states import FormStates
from run import bot

import io
import re
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET

entry_router = Router()


@entry_router.message(CommandStart())
async def send_welcome(message: Message, state: FSMContext):
    await message.reply("Welcome! Please send me the .docx template file.")
    await state.set_state(FormStates.waiting_for_template)


@entry_router.message(FormStates.waiting_for_template)
async def process_template(message: Message, state: FSMContext):
    if not message.document or not message.document.file_name.endswith('.docx'):
        await message.reply("Please send a .docx file.")
        return

    file_name = message.document.file_name
    await state.update_data(file_id=message.document.file_id, file_name=file_name)
    await message.reply("Template received. Now, send me the data separated by commas.")
    await state.set_state(FormStates.waiting_for_data)


@entry_router.message(FormStates.waiting_for_data)
async def process_data(message: Message, state: FSMContext):
    data = message.text.split(',')
    state_data = await state.get_data()
    file_id = state_data['file_id']
    file_name = state_data['file_name']

    # Download the document
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_content = await bot.download_file(file_path)

    # Create a new in-memory file
    output = io.BytesIO()

    # Open the .docx file as a zip archive
    with ZipFile(file_content, 'r') as zip_ref:
        # Create a new zip archive
        with ZipFile(output, 'w', ZIP_DEFLATED) as zip_out:
            for item in zip_ref.infolist():
                content = zip_ref.read(item.filename)
                if item.filename == 'word/document.xml':
                    # Parse the XML content
                    root = ET.fromstring(content)
                    # Define the namespace
                    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

                    # Function to replace placeholders in text
                    def replace_placeholder(text):
                        def repl(match):
                            index = int(match.group(1)) - 1
                            return data[index] if index < len(data) else match.group(0)
                        return re.sub(r'\$(\d+)', repl, text)

                    # Find all text elements and replace placeholders
                    for elem in root.findall('.//w:t', ns):
                        elem.text = replace_placeholder(elem.text or '')

                    # Write the modified XML back to the zip archive
                    zip_out.writestr(item.filename, ET.tostring(root, encoding='UTF-8', xml_declaration=True))
                else:
                    # Copy other files as-is
                    zip_out.writestr(item.filename, content)

    # Reset file pointer to the beginning
    output.seek(0)

    # Send the modified file
    await message.reply_document(BufferedInputFile(output.getvalue(), filename=file_name))

