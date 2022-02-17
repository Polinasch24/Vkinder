from typing import TYPE_CHECKING

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event

from helprs import write_msg
from models import User
from state.base import TOTAL_STEPS, State

if TYPE_CHECKING:
    from bot import Bot
    from state import StateName


class SexState(State):
    key = "select_sex"

    text = (
        "Кого мы ищем?"
    ) % (TOTAL_STEPS,)

    @classmethod
    def enter(cls, bot: "Bot", event: Event) -> None:
        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button("Мужчину", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Женщину", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Все равно", color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()

        keyboard.add_button("Назад", color=VkKeyboardColor.SECONDARY)
        keyboard.add_button("Отмена", color=VkKeyboardColor.NEGATIVE)

        write_msg(
            bot.group_session, event.user_id, cls.text, keyboard=keyboard.get_keyboard()
        )

    @classmethod
    def leave(cls, bot: "Bot", event: Event) -> "StateName":
        from state import StateName

        if event.text == "Отмена":
            return StateName.HELLO_AGAIN
        if event.text == "Назад":
            return StateName.SELECT_CITY

        user = bot.storage.get(User, event.user_id)

        selected_sex: str
        if event.text == "Мужчину":
            user.sex = 2
            selected_sex = "мужчин"
        elif event.text == "Женщину":
            user.sex = 1
            selected_sex = "женщин"
        elif event.text == "Все равно":
            user.sex = 0
            selected_sex = "всех"
        else:
            return StateName.SELECT_SEX_ERROR

        write_msg(
            bot.group_session, event.user_id, f" Ищем {selected_sex}!"
        )
        bot.storage.save(user)
        return StateName.SELECT_AGE


class SexErrorState(SexState):
    key = "select_sex_error"

    text = (
        "Ошибка ввода"
    )