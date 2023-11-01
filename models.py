import dataclasses


@dataclasses.dataclass
class Device:
    title: str
    price: str
    old_price: str | None
    discount: str | None
    count_lost: str | None
    rating: str | None
    count_rating: str | None
    cover: str
    url: str
