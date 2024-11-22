import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ''  #@BerellExpressLearningBot
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)

kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Мужчина')
button4 = KeyboardButton(text='Женщина')
kb2.add(button3)
kb2.add(button4)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Нажми "Расчитать"', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()


@dp.message_handler(text=['Рассчитать'])
async def set_age(massage):
    await massage.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(massage, state):
    data = await state.update_data(age=float(massage.text))
    await massage.answer('Введите свой рост (в см целым числом или через точку)')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(massage, state):
    data = await state.update_data(growth=float(massage.text))
    await massage.answer('Введите свой вес (в кг целым числом или через точку)')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_sex(massage, state):
    data = await state.update_data(weight=float(massage.text))
    await massage.answer('Введите свой пол (Мужчина/Женщина)', reply_markup=kb2)
    await UserState.sex.set()


@dp.message_handler(state=UserState.sex)
async def send_calories(massage, state):
    await state.update_data(sex=massage.text.lower())
    data = await state.get_data()
    if data['sex'] == 'мужчина':
        await massage.answer(
            f"Ваша норма калорий {10.0 * data['weight'] + 6.25 * data['growth'] - 5.0 * data['age'] + 5}")
    elif data['sex'] == 'женщина':
        await massage.answer(
            f"Ваша норма калорий {10.0 * data['weight'] + 6.25 * data['growth'] - 5.0 * data['age'] - 161}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
