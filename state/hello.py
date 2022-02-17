from typing import TYPE_CHECKING
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event
from helprs import write_msg
from models import User
from state.base import State

if TYPE_CHECKING:
    from bot import Bot
    from state import StateName


class Hello(State):
    key = "hello"

    text = (
        "Привет, {first_name}!"
        "Я помогу тебе найти идеальную пару!"
         "Начнем ?"

    )

    @classmethod
    def enter(cls, bot: "Bot", event: Event) -> None:
        user = bot.storage.get(User, event.user_id)

        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Новый поиск", color=VkKeyboardColor.PRIMARY)

        write_msg(
            bot.group_session,
            event.user_id,
            cls.text.format(first_name=user.first_name),
            keyboard=keyboard.get_keyboard(),
        )

    @classmethod
    def leave(cls, bot: "Bot", event: Event) -> "StateName":
        from state import StateName

        if event.text == "Новый поиск":
            return StateName.SELECT_COUNTRY
        else:
            return StateName.HELLO_ERROR


class HelloError(Hello):
    key = "hello_error"

    text = (
       "Ошибка ввода"
    )


class HelloAgain(Hello):
    key = "hello_again"

    text = (
        "{first_name}, Начнём  поиск?"

    )