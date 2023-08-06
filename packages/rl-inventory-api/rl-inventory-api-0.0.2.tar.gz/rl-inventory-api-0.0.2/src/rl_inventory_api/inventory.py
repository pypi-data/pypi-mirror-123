from pathlib import Path
from rl_inventory_api.item import Item
from rl_inventory_api.constants import Types, Rarities, Tradeable, Certifies, Colors
import csv
from dataclasses import astuple


class Inventory:
    def __init__(self, items: list[Item]):
        self.items = items

    @staticmethod
    def read(path=Path(str(Path.home()) + "\\AppData\\Roaming\\bakkesmod\\bakkesmod\\data\\inventory.csv")):
        with open(path, "r") as file:
            inv = list(csv.reader(file, delimiter=","))
        return Inventory([Item(*item) for item in inv[1:]])

    def save(self, path=str(Path.home()) + "\\inventory.csv"):
        with open(path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["product id", "name", "slot", "paint", "certification", "certification value",
                             "certification label", "quality", "crate", "tradeable", "amount", "instanceid"])
            writer.writerows([astuple(item) for item in self.items])

    def intuitive_filter(self, name=None, type_=None, color=None, certify=None, rarity=None, crate=None, tradeable=None,
                         amount=None):
        args = [("name", name), ("slot", type_), ("paint", color), ("certification_label", certify), ("quality", rarity),
                ("crate", crate), ("tradeable", tradeable), ("amount", amount)]

        def compare_with_context(item, attr, value):
            item_value = getattr(item, attr)
            if isinstance(value, str):
                return item_value == value
            elif isinstance(value, list):
                return item_value in value
        return self.filter(lambda item: all([compare_with_context(item, attr, value) for attr, value in args if value]))

    def quantity_items(self):
        return sum([item.quantity() for item in self.items])

    def get_values(self, attribute):
        return {getattr(item, attribute) for item in self.items}

    def get_names(self):
        return self.get_values("name")

    def get_types(self):
        return self.get_values("slot")

    def get_rarities(self):
        return self.get_values("quality")

    def get_colors(self):
        return self.get_values("paint")

    def get_series(self):
        return self.get_values("crate")

    def get_certifies(self):
        return self.get_values("certification_label")

    def filter(self, lamb):
        return Inventory(list(filter(lamb, self.items)))

    def filter_by_tradeable(self, tradeable):
        return self.filter(lambda item: item.tradeable == tradeable)

    def filter_tradeable(self):
        return self.filter_by_tradeable(Tradeable.TRUE)

    def filter_not_tradeable(self):
        return self.filter_by_tradeable(Tradeable.FALSE)

    def filter_by_name(self, name):
        return self.filter(lambda item: item.name == name)

    def filter_by_color(self, color):
        return self.filter(lambda item: item.paint == color)

    def filter_by_type(self, type_):
        return self.filter(lambda item: item.slot == type_)

    def filter_by_amount(self, amount):
        return self.filter(lambda item: int(item.amount) == int(amount))

    def filter_by_certify(self, certify):
        return self.filter(lambda item: item.certification_label == certify)

    def filter_by_series(self, series):
        return self.filter(lambda item: item.crate == series)

    def filter_by_rarity(self, rarity):
        return self.filter(lambda item: item.quality == rarity)

    def filter_uncommon(self):
        return self.filter_by_rarity(Rarities.UNCOMMON)

    def filter_rare(self):
        return self.filter_by_rarity(Rarities.RARE)

    def filter_very_rare(self):
        return self.filter_by_rarity(Rarities.VERY_RARE)

    def filter_import(self):
        return self.filter_by_rarity(Rarities.IMPORT)

    def filter_exotic(self):
        return self.filter_by_rarity(Rarities.EXOTIC)

    def filter_black_market(self):
        return self.filter_by_rarity(Rarities.BLACK_MARKET)

    def filter_limited(self):
        return self.filter_by_rarity(Rarities.LIMITED)

    def filter_painted(self):
        return self.filter(lambda item: item.is_painted())

    def filter_not_painted(self):
        return self.filter(lambda item: not item.is_painted())

    def filter_certified(self):
        return self.filter(lambda item: item.is_certificate())

    def filter_not_certified(self):
        return self.filter(lambda item: not item.is_certificate())

    def filter_non_crate(self):
        return self.filter(lambda item: item.is_non_crate())

    def filter_from_crate(self):
        return self.filter(lambda item: not item.is_non_crate())

    def filter_non_crate_by_rarity(self, rarity):
        return self.filter(lambda item: item.is_non_crate() and item.quality == rarity)

    def filter_ncr(self):
        return self.filter_non_crate_by_rarity(Rarities.RARE)

    def filter_ncvr(self):
        return self.filter_non_crate_by_rarity(Rarities.VERY_RARE)

    def filter_nci(self):
        return self.filter_non_crate_by_rarity(Rarities.IMPORT)

    def filter_nce(self):
        return self.filter_non_crate_by_rarity(Rarities.EXOTIC)

    def filter_blueprint(self):
        return self.filter(lambda item: item.is_blueprint())

    def filter_not_blueprint(self):
        return self.filter(lambda item: not item.is_blueprint())

    def filter_animated_decal(self):
        return self.filter_by_type(Types.ANIMATED_DECAL)

    def filter_antennas(self):
        return self.filter_by_type(Types.ANTENNA)

    def filter_avatar_border(self):
        return self.filter_by_type(Types.AVATAR_BORDER)

    def filter_cars(self):
        return self.filter_by_type(Types.BODY)

    def filter_decals(self):
        return self.filter_by_type(Types.DECAL)

    def filter_engine_audio(self):
        return self.filter_by_type(Types.ENGINE_AUDIO)

    def filter_goal_explosion(self):
        return self.filter_by_type(Types.GOAL_EXPLOSION)

    def filter_paint_finish(self):
        return self.filter_by_type(Types.PAINT_FINISH)

    def filter_player_anthem(self):
        return self.filter_by_type(Types.PLAYER_ANTHEM)

    def filter_banners(self):
        return self.filter_by_type(Types.PLAYER_BANNER)

    def filter_titles(self):
        return self.filter_by_type(Types.PLAYER_TITLE)

    def filter_boost(self):
        return self.filter_by_type(Types.ROCKET_BOOST)

    def filter_toppers(self):
        return self.filter_by_type(Types.TOPPER)

    def filter_trails(self):
        return self.filter_by_type(Types.TRAIL)

    def filter_wheels(self):
        return self.filter_by_type(Types.WHEELS)

    def filter_crimson(self):
        return self.filter_by_color(Colors.CRIMSON)

    def filter_sky_blue(self):
        return self.filter_by_color(Colors.SKY_BLUE)

    def filter_pink(self):
        return self.filter_by_color(Colors.PINK)

    def filter_orange(self):
        return self.filter_by_color(Colors.ORANGE)

    def filter_cobalt(self):
        return self.filter_by_color(Colors.COBALT)

    def filter_burnt_sienna(self):
        return self.filter_by_color(Colors.BURNT_SIENNA)

    def filter_titanium_white(self):
        return self.filter_by_color(Colors.TITANIUM_WHITE)

    def filter_grey(self):
        return self.filter_by_color(Colors.GREY)

    def filter_saffron(self):
        return self.filter_by_color(Colors.SAFFRON)

    def filter_lime(self):
        return self.filter_by_color(Colors.LIME)

    def filter_forest_green(self):
        return self.filter_by_color(Colors.FOREST_GREEN)

    def filter_black(self):
        return self.filter_by_color(Colors.BLACK)

    def filter_purple(self):
        return self.filter_by_color(Colors.PURPLE)

    def filter_aviator(self):
        return self.filter_by_certify(Certifies.AVIATOR)

    def filter_acrobat(self):
        return self.filter_by_certify(Certifies.ACROBAT)

    def filter_victor(self):
        return self.filter_by_certify(Certifies.VICTOR)

    def filter_striker(self):
        return self.filter_by_certify(Certifies.STRIKER)

    def filter_sniper(self):
        return self.filter_by_certify(Certifies.SNIPER)

    def filter_scorer(self):
        return self.filter_by_certify(Certifies.SCORER)

    def filter_playmaker(self):
        return self.filter_by_certify(Certifies.PLAYMAKER)

    def filter_guardian(self):
        return self.filter_by_certify(Certifies.GUARDIAN)

    def filter_paragon(self):
        return self.filter_by_certify(Certifies.PARAGON)

    def filter_sweeper(self):
        return self.filter_by_certify(Certifies.SWEEPER)

    def filter_turtle(self):
        return self.filter_by_certify(Certifies.TURTLE)

    def filter_tactician(self):
        return self.filter_by_certify(Certifies.TACTICIAN)

    def filter_showoff(self):
        return self.filter_by_certify(Certifies.SHOW_OFF)

    def filter_juggler(self):
        return self.filter_by_certify(Certifies.JUGGLER)

    def filter_goalkeeper(self):
        return self.filter_by_certify(Certifies.GOALKEEPER)
