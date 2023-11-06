from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from assessments_parsing.assesments_parsing import get_marks

router:Router = Router()

# start command
@router.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(text=LEXICON_RU[message.text])
    print(message.from_user.full_name, message.from_user.id)

# help command
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU[message.text])

# get login:password
@router.message(lambda x: len(x.text.split(':')) == 2)
async def process_get_student_marks(message: Message):
    login, password = message.text.split(':')
    print(message.from_user.full_name, '->', login, password)
    await message.answer(text=LEXICON_RU['wait'])
    marks_table = get_marks(login=login, password=password)
    if marks_table:
        format_marks = [f'<b>предмет:</b> {sub}\n<b>Оценки:</b> {" ".join(marks["marks"])}\n<b>Средний балл:</b> {marks["avg"]}\n' for sub, marks in marks_table.items()]
        await message.answer(text="\n".join(format_marks))
    else:
        await message.answer(text=LEXICON_RU['site_error'])
    

