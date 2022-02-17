from typing import TYPE_CHECKING
from vk_api.longpoll import Event
from models import User
from state.base import State

if TYPE_CHECKING:
    from bot import Bot
    from state import StateName


class Initial(State):
    key = "initial"

    @classmethod
    def enter(cls, bot: "Bot", event: Event) -> None:
        pass

    @classmethod
    def leave(cls, bot: "Bot", event: Event) -> "StateName":
        from state import StateName

        user = bot.storage.get(User, event.user_id)

        user_info = bot.session.method(
            "users.get", {"user_ids": event.user_id, "fields": "city, merital"}
        )[0]
        first_name = user_info["first_name"]
        last_name = user_info["last_name"]

        try:
            merital_id = user_info["merial"]["id"]
        except KeyError:
            merital_id = None

        try:
            city_id = user_info["city"]["id"]
        except KeyError:
            city_id = None

        user.first_name = first_name
        user.last_name = last_name
        user.merital_id = merital_id
        user.city_id = city_id

        bot.storage.save(user)
        return StateName.HELLO