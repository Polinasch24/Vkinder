from typing import TYPE_CHECKING
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event
from helprs import write_msg
from models import User
from state.base import TOTAL_STEPS, State

if TYPE_CHECKING:
    from bot import Bot
    from state import StateName


class MeritalStatus(State):
    key = "select_merital"

    text = (
        "Семейное положение половинки"
    ) % (TOTAL_STEPS,)

    @classmethod
    def enter(cls, bot: "Bot", event: Event) -> None:
        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button("В браке", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Свободен/на", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Не важно", color=VkKeyboardColor.SECONDARY)
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

        selected_merital: str
        if event.text == "В браке":
            user.merital = 2
            selected_merital = "в браке"
        elif event.text == "Свободен/на":
            user.merital = 1
            selected_merital = "свободен/на"
        elif event.text == "Не важно":
            user.merital = 0
            selected_merital = "не важно"
        else:
            return StateName.SELECT_MERITAL_ERROR

        write_msg(
            bot.group_session, event.user_id, f" Ищем {selected_merital}!"
        )
        bot.storage.save(user)
        return StateName.SELECT_merital


class MeritalState(State):
    key = "select_merital_error"

    text = (
        "Ошибка ввода"
    )