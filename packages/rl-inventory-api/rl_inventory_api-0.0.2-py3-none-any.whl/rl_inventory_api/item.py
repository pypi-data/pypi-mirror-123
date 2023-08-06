from rl_inventory_api.constants import Colors, Certifies, Series, Tradeable, Rarities, Types
from dataclasses import dataclass, field


@dataclass
class Item:
    product_id: int = field(repr=False)
    name: str
    slot: str
    paint: str
    certification: str = field(repr=False)
    certification_value: int = field(repr=False)
    certification_label: str
    quality: str
    crate: str
    tradeable: str
    amount: int
    instance_id: int = field(repr=False)

    def quantity(self):
        return int(self.amount)

    def is_painted(self):
        return self.paint != Colors.NONE

    def is_certificate(self):
        return self.certification_label != Certifies.NONE

    def is_tradeable(self):
        return self.tradeable == Tradeable.TRUE

    def is_non_crate(self):
        return self.crate == Series.NON_CRATE

    def is_uncommon(self):
        return self.quality == Rarities.UNCOMMON

    def is_rare(self):
        return self.quality == Rarities.RARE

    def is_very_rare(self):
        return self.quality == Rarities.VERY_RARE

    def is_import(self):
        return self.quality == Rarities.IMPORT

    def is_exotic(self):
        return self.quality == Rarities.EXOTIC

    def is_black_market(self):
        return self.quality == Rarities.BLACK_MARKET

    def is_limited(self):
        return self.quality == Rarities.LIMITED

    def is_ncr(self):
        return self.is_non_crate() and self.is_rare()

    def is_ncvr(self):
        return self.is_non_crate() and self.is_very_rare()

    def is_nci(self):
        return self.is_non_crate() and self.is_import()

    def is_nce(self):
        return self.is_non_crate() and self.is_exotic()

    def is_blueprint(self):
        return self.slot == Types.BLUEPRINT

    @staticmethod
    def get_decal_and_car_name_by_name(name):
        car, decal = name.split(":")
        decal = decal.strip()
        return car, decal

    def get_decal_and_car_name(self):
        return self.get_decal_and_car_name_by_name(self.name)
