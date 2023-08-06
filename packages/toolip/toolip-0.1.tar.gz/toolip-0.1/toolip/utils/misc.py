from shortuuid import ShortUUID


def get_unique_id(length: int) -> str:
    return ShortUUID().random(length=length)
