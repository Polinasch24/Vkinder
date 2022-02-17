import datetime
import uuid
from typing import TYPE_CHECKING
from vk_api.longpoll import Event
from helprs import write_msg
from models import Match, Search, User
from base import TOTAL_STEPS, State

if TYPE_CHECKING:
    from bot import Bot
    from state import StateName


class AgeState(State):
    key = "select_age"

    text = (
        "Укажи возраст идеальной половинки"
    ) % (TOTAL_STEPS,)


    @classmethod
    def leave(cls, bot: "Bot", event: Event) -> "StateName":
        from state import StateName

        if event.text == "Отмена":
            return StateName.HELLO_AGAIN
        if event.text == "Назад":
            return StateName.SELECT_SEX

        user = bot.storage.get(User, event.user_id)

        msg: str = event.text.lower().strip()

        age: int


        if "-" in msg:
            try:
                from_, to = msg.split("-")
                age = int(from_.strip())

            except ValueError:
                return StateName.SELECT_AGE_ERROR
        else:
            try:
                age = int(msg)
            except ValueError:
                return StateName.SELECT_AGE_ERROR

        user.age = age

        write_msg(
            bot.group_session,
            event.user_id,
            (
                "Начинаем поиск!"
            ),
        )

        assert user.merital
        assert user.city_id
        assert user.sex is not None
        assert user.age

        search_params = {
            "merital_st": user.merital,
            "city": user.city_id,
            "sex": user.sex,
            "age_from": user.age
        }

        search_results = bot.session.method(
            "users.search",
            {
                "sort": 0,
                "count": 1000,
                "has_photo": 1,
                "status": "6",
                "fields": "id,verified,domain",
                "can_access_closed": 1,
                "is_closed": 0,
                **search_params,
            },
        )["items"]
        search_results = [
            person for person in search_results if not person["is_closed"]
        ]

        search_id = uuid.uuid4()
        search = Search(
            uuid=search_id,
            user_id=event.user_id,
            datetime=datetime.datetime.utcnow().isoformat(),
            **search_params,
        )
        bot.storage.save(search)

        for person in search_results:
            match = Match(
                uuid=uuid.uuid4(),
                search_id=search_id,
                vk_id=person["id"],
                first_name=person["first_name"],
                last_name=person["last_name"],
            )
            bot.storage.save(match)

        user.current_search = search_id
        user.current_search_item = 0
        bot.storage.save(user)
        return StateName.LIST_MATCHES


class AgeErrorState(AgeState):
    key = "select_age_error"

    text = (
        "Ошибка ввода!"
    )