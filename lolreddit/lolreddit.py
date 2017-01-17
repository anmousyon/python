'''/r/leagueoflegends helper'''

import re
import requests
import praw
from peewee import *
import collections
import csv
from pprint import pprint
from cassiopeia import riotapi

db = SqliteDatabase('league.db')

class Champions(Model):
    label = TextField()
    name = TextField()
    tooldtip = TextField()
    ptooltip = TextField()
    pcost = TextField()
    pcooldown = TextField()
    presource = TextField()
    qtext = TextField()
    qtooltip = TextField()
    qcost = TextField()
    qcooldown = TextField()
    qresource = TextField()
    wtext = TextField()
    wtooltip = TextField()
    wcost = TextField()
    wcooldown = TextField()
    wresource = TextField()
    etext = TextField()
    etooltip = TextField()
    ecost = TextField()
    ecooldown = TextField()
    eresource = TextField()
    rtext = TextField()
    rtooltip = TextField()
    rcost = TextField()
    rcooldown = TextField()
    rresource = TextField()
    armor = TextField()
    armorperlevel = TextField()
    attackdamage = TextField()
    attackdamageperlevel = TextField()
    attackrange = TextField()
    attackspeedoffset = TextField()
    attackspeedperlevel = TextField()
    crit = TextField()
    critperlevel = TextField()
    hp = TextField()
    hpperlevel = TextField()
    hpregen = TextField()
    hpregenperlevel = TextField()
    movespeed = TextField()
    mp = TextField()
    mpperlevel = TextField()
    mpregen = TextField()
    mpregenperlevel = TextField()
    spellblock = TextField()
    spellblockperlevel = TextField()

class Items(Model):
    label = TextField()
    name = TextField()
    tooltip = TextField()
    flatarmormod = TextField()
    flatattackspeedmod = TextField()
    flatblockmod = TextField()
    flatcritchancemod = TextField()
    flatcritdamagemod = TextField()
    flatexpbonus = TextField()
    flatenergypoolmod = TextField()
    flatenergyregenmod = TextField()
    flathppoolmod = TextField()
    flathpregenmod = TextField()
    flatmppoolmod = TextField()
    flatmpregenmod = TextField()
    flatmagicdamagemod = TextField()
    flatmovementspeedmod = TextField()
    flatphysicaldamagemod = TextField()
    flatspellblockmod = TextField()
    percentarmormod = TextField()
    percentattackspeedmod = TextField()
    percentblockmod = TextField()
    percentcritchancemod = TextField()
    percentcritdamagemod = TextField()
    percentdodgemod = TextField()
    percentexpbonus = TextField()
    percenthppoolmod = TextField()
    percenthpregenmod = TextField()
    percentlifestealmod = TextField()
    percentmppoolmod = TextField()
    percentmpregenmod = TextField()
    percentmagicdamagemod = TextField()
    percentmovementspeedmod = TextField()
    percentphysicaldamagemod = TextField()
    percentspellblockmod = TextField()
    percentspellvampmod = TextField()
    rflatarmormodperlevel = TextField()
    rflatarmorpenetrationmod = TextField()
    rflatarmorpenetrationmodperlevel = TextField()
    rflatcritchancemodperlevel = TextField()
    rflatcritdamagemodperlevel = TextField()
    rflatdodgemod = TextField()
    rflatdodgemodperlevel = TextField()
    rflatenergymodperlevel = TextField()
    rflatenergyregenmodperlevel = TextField()
    rflatgoldper10mod = TextField()
    rflathpmodperlevel = TextField()
    rflathpregenmodperlevel = TextField()
    rflatmpmodperlevel = TextField()
    rflatmpregenmodperlevel = TextField()
    rflatmagicdamagemodperlevel = TextField()
    rflatmagicpenetrationmod = TextField()
    rflatmagicpenetrationmodperlevel = TextField()
    rflatmovementspeedmodperlevel = TextField()
    rflatphysicaldamagemodperlevel = TextField()
    rflatspellblockmodperlevel = TextField()
    rflattimedeadmod = TextField()
    rflattimedeadmodperlevel = TextField()
    rpercentarmorpenetrationmod = TextField()
    rpercentarmorpenetrationmodperlevel = TextField()
    rpercentattackspeedmodperlevel = TextField()
    rpercentcooldownmod = TextField()
    rpercentcooldownmodperlevel = TextField()
    rpercentmagicpenetrationmod = TextField()
    rpercentmagicpenetrationmodperlevel = TextField()
    rpercentmovementspeedmodperlevel = TextField()
    rpercenttimedeadmod = TextField()
    rpercenttimedeadmodperlevel = TextField()



class Champion():
    def __init__(self, champion):
        self.name = champion.data.name
        self.label = champion.data.id
        self.spells = champion.data.spells
        self.stats = champion.data.stats

    def db_version(self):
        pass

    def clean_spells(self):
        all_spells = [None, None, None, None, None]
        for spell in self.spells:
            tooltip = spell.sanitizedTooltip
            effects = spell.effect
            cooldown = spell.cooldown
            cooldown_str = ""
            for c in cooldown:
                cooldown_str += str(c)
            cost = spell.cost
            cost_str = ""
            for c in cost:
                cost_str += str(c) + " "
            key = spell.key[-1]
            resource = spell.resource
            #print(tooltip)
            for i in range(len(effects)):
                if not effects[i]:
                    continue
                effects[i] = list(set(effects[i]))
                to_replace = "{{ e" + str(i) + " }}"
                effect_str = "("
                for e in effects[i]:
                    effect_str += str(int(e)) + ", "
                effect_str = effect_str[:-2] + ")"
                tooltip = tooltip.replace(to_replace, effect_str)
            #print(tooltip)
            if key == 'P':
                all_spells[0] = ['p', tooltip, cost, cooldown, resource]
            elif key == 'Q':
                all_spells[1] = ['q', tooltip, cost, cooldown, resource]
            elif key == 'W':
                all_spells[2] = ['w', tooltip, cost, cooldown, resource]
            elif key == 'E':
                all_spells[3] = ['e', tooltip, cost, cooldown, resource]
            elif key == 'R':
                all_spells[4] = ['r', tooltip, cost, cooldown, resource]
        self.spells = all_spells
        #print(self.spells)


class Item:
    def __init__(self, item):
        self.name = item.data.name
        self.label = item.data.id
        self.stats = item.data.stats

    def db_version(self):
        pass


class Riot:
    def __init__(self):
        riotapi.set_region("NA")
        riotapi.set_api_key("462d0d85-d692-4af5-b91f-4ed9cf0b2efe")
        self.champions = riotapi.get_champions()
        self.items = riotapi.get_items()

    def get_champion(self, label):
        for champion in self.champions:
            if champion.id == label:
                return champion

    def get_item(self, label):
        for item in self.items:
            if item.id == label:
                return item

    def get_champions(self):
        return self.champions

    def get_items(self):
        return self.items


class Filler:
    def __init__(self, champions, items):
        self.champions = champions
        self.items = items


    def fill_champions(self):
        for champion in self.champions:
            to_add = Champion(champion)
            to_add.clean_spells()
            #for_db = to_add.db_version()
            #for_db.add_to_db()
            #print(str(to_add.label) + " " + to_add.name)

    def fill_items(self):
        for item in self.items:
            to_add = Item(item)
            #for_db = to_add.db_version()
            #for_db.add_to_db()
            #print(str(to_add.label) + " " + to_add.name)


class Parser:
    def __init__(self, group):
        self.to_parse = group

    def separate(self):
        self.to_parse = self.to_parse[1:-1]
        self.to_parse = csv.reader(self.to_parse)

    def get_category(self, champions, items):
        for category in [champions, items]:
            if self.to_parse[0] in category:
                return self.to_parse[0]

    def get_needed(self):
        return self.to_parse[1:]

    def parse(self, champions, items):
        self.separate()
        category = self.get_category(champions, items)
        needed = self.get_needed()
        return category, needed


class Seeker():
    def __init__(self, anything, comment):
        self.anything = re.compile(r'\[(.*?)\]', re.IGNORECASE)
        self.to_check = comment

    def seek(self):
        return self.anything.match(self.to_check)

def main():
    riot = Riot()
    braum = riot.get_champion(201)
    print(braum.data.stats)
    cull = riot.get_item(1083)
    print(cull.data.stats)
    filler = Filler(riot.get_champions(), riot.get_items())
    filler.fill_champions()
    filler.fill_items()

main()