import random


class CryAboutIt(Exception):
    pass


class ImposterAmongUs(Exception):
    pass


class GetFuckedRetard(Exception):
    pass


class HaHaJonathan(Exception):
    pass


def RandomError() -> Exception:
    errorList: list[Exception] = [
        CryAboutIt(),
        ImposterAmongUs(),
        GetFuckedRetard(),
        HaHaJonathan()
    ]

    errorIndex = random.randint(0, len(errorList) - 1)

    return errorList[errorIndex]
