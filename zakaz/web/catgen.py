# -*- coding: utf-8 -*- 
from app.models import Shop, Tag
from app import db

data = {"tags": {"1": "Самые популярные", "2": "Мужская и женская одежда", "3": "Женские магазины", "4": "Детские товары",
                 "5": "Аксессуары косметика, парфюмерия", "6": "Топ бренды", "7": "Гипер маркеты", "8": "Обувь",
                 "9": "Электроника", "10": "Спорт, Отдых, Туризм", "11": "+ Size"},
        "shops": [{"domain": "6pm.com", "image": "1_6pm.png", "tags": [1, 2], "weight": 1},
                  {"domain": "abercrombie.com", "image": "2_Abercrombie&Fitch.png", "tags": [2], "weight": 1},
                  {"domain": "absolutelyaudrey.com", "image": "3_AbsolutelyAudrey.png", "tags": [5], "weight": 1},
                  {"domain": "adidas.com", "image": "4_adidas.png", "tags": [10], "weight": 1},
                  {"domain": "ae.com", "image": "5_ae.png", "tags": [2], "weight": 1},
                  {"domain": "aeropostale.com", "image": "6_aeropostal.png", "tags": [2], "weight": 1},
                  {"domain": "aerosoles.com", "image": "7_Aerosoles.png", "tags": [8], "weight": 1},
                  {"domain": "affairlingerie.com", "image": "8_affairlingerie.png", "tags": [3], "weight": 1},
                  {"domain": "agentprovocateur.com", "image": "9_agentprovocateur.png", "tags": [3], "weight": 1},
                  {"domain": "aldoshoes.com", "image": "10_aldo.png", "tags": [8], "weight": 1},
                  {"domain": "amazon.com", "image": "11_amazon.png", "tags": [1, 7, 11], "weight": 1},
                  {"domain": "americanapparel.net", "image": "12_amerapparel.png", "tags": [1, 2], "weight": 1},
                  {"domain": "amiclubwear.com", "image": "13_amiclubwear.png", "tags": [3], "weight": 1},
                  {"domain": "andrewmarc.com", "image": "14_andrewmark.png", "tags": [6], "weight": 1},
                  {"domain": "anntaylor.com", "image": "15_anna-taylor.png", "tags": [3], "weight": 1},
                  {"domain": "anonymousla.com", "image": "16_anonymouse.png", "tags": [5], "weight": 1},
                  {"domain": "anthropologie.com", "image": "17_anthropologie.png", "tags": [3], "weight": 1},
                  {"domain": "apple.com", "image": "18_apple.png", "tags": [1, 9], "weight": 1},
                  {"domain": "armani.com", "image": "19_armani.png", "tags": [6], "weight": 1},
                  {"domain": "armaniexchange.com", "image": "20_armaniexchange.png", "tags": [6], "weight": 1},
                  {"domain": "babiesrus.com", "image": "21_babierus.png", "tags": [4], "weight": 1},
                  {"domain": "backcountry.com", "image": "22_backcountry.png", "tags": [1, 10], "weight": 1},
                  {"domain": "bagshop.com", "image": "23_bagshop.png", "tags": [5], "weight": 1},
                  {"domain": "bananarepublic.com", "image": "24_bananarepublic.png", "tags": [2], "weight": 1},
                  {"domain": "barneys.com", "image": "25_barneys.png", "tags": [6], "weight": 1},
                  {"domain": "bellsshoes.com", "image": "26_bellsshoes.png", "tags": [8], "weight": 1},
                  {"domain": "bestbuy.com", "image": "27_bestbuy.png", "tags": [7], "weight": 1},
                  {"domain": "bhphotovideo.com", "image": "28_bhphotovideo.png", "tags": [9], "weight": 1},
                  {"domain": "bluefly.com", "image": "29_bluefly.png", "tags": [6], "weight": 1},
                  {"domain": "bodybuilding.com", "image": "30_bodybuilding.png", "tags": [10], "weight": 1},
                  {"domain": "bootyparlor.com", "image": "31_bootyparlor.png", "tags": [3], "weight": 1},
                  {"domain": "buckle.com", "image": "32_buckle.png", "tags": [2], "weight": 1},
                  {"domain": "calvinklein.com", "image": "33_calvina.png", "tags": [6], "weight": 1},
                  {"domain": "carters.com", "image": "34_carters.png", "tags": [1, 4], "weight": 1},
                  {"domain": "chanel.com", "image": "35_chanel.png", "tags": [6], "weight": 1},
                  {"domain": "charlotterusse.com", "image": "36_charlotterusse.png", "tags": [3, 11], "weight": 1},
                  {"domain": "childrensplace.com", "image": "37_childrensplace.png", "tags": [4], "weight": 1},
                  {"domain": "colehaan.com", "image": "38_colehaan.png", "tags": [8], "weight": 1},
                  {"domain": "converse.com", "image": "39_converse.png", "tags": [8], "weight": 1},
                  {"domain": "costco.com", "image": "40_costco.png", "tags": [7], "weight": 1},
                  {"domain": "crazy8.com", "image": "41_crazy8.png", "tags": [4], "weight": 1},
                  {"domain": "crocs.com", "image": "42_crocs.png", "tags": [8], "weight": 1},
                  {"domain": "curlydani.com", "image": "43_curlydani.png", "tags": [4], "weight": 1},
                  {"domain": "diapers.com", "image": "44_diapers.png", "tags": [4], "weight": 1},
                  {"domain": "digikey.com", "image": "45_digikey.png", "tags": [9], "weight": 1},
                  {"domain": "disneystore.com", "image": "46_disneystore.png", "tags": [4], "weight": 1},
                  {"domain": "djpremium.com", "image": "47_djpremium.png", "tags": [6], "weight": 1},
                  {"domain": "eastbay.com", "image": "48_eastbay.png", "tags": [10], "weight": 1},
                  {"domain": "ebags.com", "image": "49_ebags.png", "tags": [5], "weight": 1},
                  {"domain": "ebay.com", "image": "50_EBay.png", "tags": [7], "weight": 1},
                  {"domain": "esprit.com", "image": "51_esprit.png", "tags": [6], "weight": 1},
                  {"domain": "evo.com", "image": "52_evo.png", "tags": [10], "weight": 1},
                  {"domain": "fanatics.com", "image": "53_fanatics.png", "tags": [10], "weight": 1},
                  {"domain": "footlocker.com", "image": "54_footlocker.png", "tags": [10], "weight": 1},
                  {"domain": "forever21.com", "image": "55_forever21.png", "tags": [1, 2], "weight": 1},
                  {"domain": "fossil.com", "image": "56_fossil.png", "tags": [5], "weight": 1},
                  {"domain": "fredericks.com", "image": "57_fredericks.png", "tags": [3], "weight": 1},
                  {"domain": "freshpair.com", "image": "58_freshpair.png", "tags": [2], "weight": 1},
                  {"domain": "gap.com", "image": "59_gap.png", "tags": [1, 2], "weight": 1},
                  {"domain": "global.diesel.com", "image": "60_diesel.png", "tags": [6], "weight": 1},
                  {"domain": "global.tommy.com", "image": "61_tommy-hilfiger.png", "tags": [6], "weight": 1},
                  {"domain": "greatglam.com", "image": "62_greatglam.png", "tags": [3], "weight": 1},
                  {"domain": "guess.com", "image": "63_guess.png", "tags": [6], "weight": 1},
                  {"domain": "guitarcenter.com", "image": "64_guitarcenter.png", "tags": [10], "weight": 1},
                  {"domain": "gymboree.com", "image": "65_gymboree.png", "tags": [4], "weight": 1},
                  {"domain": "hanes.com", "image": "66_hanes.png", "tags": [2], "weight": 1},
                  {"domain": "heels.com", "image": "67_heels.png", "tags": [3], "weight": 1},
                  {"domain": "hm.com", "image": "68_hm.png", "tags": [2], "weight": 1},
                  {"domain": "howcool.com", "image": "69_howcool.png", "tags": [5], "weight": 1},
                  {"domain": "iherb.com", "image": "70_iherb.png", "tags": [10], "weight": 1},
                  {"domain": "irobot.com", "image": "71_irobot.png", "tags": [9], "weight": 1},
                  {"domain": "irregularchoice.com", "image": "72_irregularchoice.png", "tags": [5], "weight": 1},
                  {"domain": "isabellaoliver.com", "image": "73_isabellaoliver.png", "tags": [3], "weight": 1},
                  {"domain": "jackjones.com", "image": "74_jackjones.png", "tags": [2], "weight": 1},
                  {"domain": "jackspade.com", "image": "75_jackspade.png", "tags": [5], "weight": 1},
                  {"domain": "jcrew.com", "image": "76_jcrew.png", "tags": [2], "weight": 1},
                  {"domain": "juicycouture.com", "image": "77_juicycouture.png", "tags": [3], "weight": 1},
                  {"domain": "karmaloop.com", "image": "78_karmaloop.png", "tags": [5], "weight": 1},
                  {"domain": "katespade.com", "image": "79_katespade.png", "tags": [5], "weight": 1},
                  {"domain": "kitchenaid.com", "image": "80_kitchenaid.png", "tags": [9], "weight": 1},
                  {"domain": "lacoste.com", "image": "81_lacoste.png", "tags": [6], "weight": 1},
                  {"domain": "laperla.com", "image": "82_laperla.png", "tags": [3], "weight": 1},
                  {"domain": "lasenza.com", "image": "83_lasenza.png", "tags": [3], "weight": 1},
                  {"domain": "lee.com", "image": "84_lee.png", "tags": [6], "weight": 1},
                  {"domain": "leggs.com", "image": "85_Leggs.png", "tags": [3], "weight": 1},
                  {"domain": "levi.com", "image": "86_levi.png", "tags": [6], "weight": 1},
                  {"domain": "llbean.com", "image": "87_llbean.png", "tags": [10], "weight": 1},
                  {"domain": "lordandtaylor.com", "image": "88_lordandtaylor.png", "tags": [6], "weight": 1},
                  {"domain": "louisvuitton.com", "image": "89_louisvuitton.png", "tags": [6], "weight": 1},
                  {"domain": "macys.com", "image": "90_macys.png", "tags": [1, 7, 11], "weight": 1},
                  {"domain": "mango.com", "image": "91_mango.png", "tags": [2], "weight": 1},
                  {"domain": "miamiaccessories.com", "image": "92_miamiaccessories.png", "tags": [5], "weight": 1},
                  {"domain": "michaelkors.com", "image": "93_michaelkors.png", "tags": [6], "weight": 1},
                  {"domain": "mudhole.com", "image": "94_mudhole.png", "tags": [10], "weight": 1},
                  {"domain": "musiciansfriend.com", "image": "95_musiciansfriend.png", "tags": [10], "weight": 1},
                  {"domain": "myleather.com", "image": "96_myleather.png", "tags": [2], "weight": 1},
                  {"domain": "neimanmarcus.com", "image": "97_neimanmarcus.png", "tags": [6], "weight": 1},
                  {"domain": "newbalance.com", "image": "98_newbalance.png", "tags": [10], "weight": 1},
                  {"domain": "newegg.com", "image": "99_newegg.png", "tags": [9], "weight": 1},
                  {"domain": "nike.com", "image": "100_nike.png", "tags": [1, 10], "weight": 1},
                  {"domain": "nordstromrack.com", "image": "101_nordstromrack.png", "tags": [1, 2], "weight": 1},
                  {"domain": "oculus.com", "image": "102_oculus.png", "tags": [9], "weight": 1},
                  {"domain": "okaidi.com", "image": "103_okaidi.png", "tags": [4], "weight": 1},
                  {"domain": "oldnavy.com", "image": "104_oldnavy.png", "tags": [2], "weight": 1},
                  {"domain": "oshkosh.com", "image": "105_oshkosh.png", "tags": [4], "weight": 1},
                  {"domain": "overstock.com", "image": "106_overstock.png", "tags": [7], "weight": 1},
                  {"domain": "prodirectsoccer.com", "image": "107_prodirectsoccer.png", "tags": [10], "weight": 1},
                  {"domain": "pandora.net", "image": "108_pandora.png", "tags": [5], "weight": 1},
                  {"domain": "pullandbear.com", "image": "109_pullandbear.png", "tags": [2], "weight": 1},
                  {"domain": "ralphlauren.com", "image": "110_ralphlauren.png", "tags": [6], "weight": 1},
                  {"domain": "reebok.com", "image": "111_reebok.png", "tags": [10], "weight": 1},
                  {"domain": "runningwarehouse.com", "image": "112_runningwarehouse.png", "tags": [10], "weight": 1},
                  {"domain": "shoes.com", "image": "113_shoes.png", "tags": [8], "weight": 1},
                  {"domain": "shop.nordstrom.com", "image": "114_nordstrom.png", "tags": [2], "weight": 1},
                  {"domain": "sierratradingpost.com", "image": "115_sierratradingpost.png", "tags": [10], "weight": 1},
                  {"domain": "sperry.com", "image": "116_sperry.png", "tags": [8], "weight": 1},
                  {"domain": "ssense.com", "image": "117_ssense.png", "tags": [5], "weight": 1},
                  {"domain": "stevemadden.com", "image": "118_stevemadden.png", "tags": [8], "weight": 1},
                  {"domain": "store.pakerson.it", "image": "119_pakerson.png", "tags": [8], "weight": 1},
                  {"domain": "store.starbucks.com", "image": "120_starbucks.png", "tags": [9], "weight": 1},
                  {"domain": "tactics.com", "image": "121_tactics.png", "tags": [10], "weight": 1},
                  {"domain": "target.com", "image": "122_target.png", "tags": [7], "weight": 1},
                  {"domain": "the-house.com", "image": "123_house.png", "tags": [1, 10], "weight": 1},
                  {"domain": "timberland.com", "image": "125_timberland.png", "tags": [8], "weight": 1},
                  {"domain": "toryburch.com", "image": "126_toryburch.png", "tags": [3], "weight": 1},
                  {"domain": "tourneau.com", "image": "127_tourneau.png", "tags": [5], "weight": 1},
                  {"domain": "toysrus.com", "image": "128_toysrus.png", "tags": [4], "weight": 1},
                  {"domain": "toywiz.com", "image": "129_toywiz.png", "tags": [4], "weight": 1},
                  {"domain": "ugg.com", "image": "130_ugg.png", "tags": [8], "weight": 1},
                  {"domain": "underarmour.com", "image": "131_underarmour.png", "tags": [10], "weight": 1},
                  {"domain": "uniqlo.com", "image": "132_uniqlo.png", "tags": [2], "weight": 1},
                  {"domain": "us.asos.com", "image": "133_asos.png", "tags": [1, 2], "weight": 1},
                  {"domain": "us.puma.com", "image": "134_puma.png", "tags": [10], "weight": 1},
                  {"domain": "victoriassecret.com", "image": "135_victoriassecret.png", "tags": [1, 3], "weight": 1},
                  {"domain": "walmart.com", "image": "136_walmart.png", "tags": [7], "weight": 1},
                  {"domain": "wantedshoes.com", "image": "137_wantedshoes.png", "tags": [8], "weight": 1},
                  {"domain": "wetseal.com", "image": "138_wetseal.png", "tags": [3], "weight": 1},
                  {"domain": "yoox.com", "image": "139_yoox.png", "tags": [2], "weight": 1},
                  {"domain": "zappos.com", "image": "140_zappos.png", "tags": [1, 8], "weight": 1},
                  {"domain": "zara.com", "image": "141_zara.png", "tags": [2], "weight": 1},
                  {"domain": "zulily.com", "image": "142_zulily.png", "tags": [4], "weight": 1},
                  {"domain": "janieandjack.com", "image": "143_janieandjack.png", "tags": [1, 4], "weight": 1},
                  {"domain": "shopstyle.com", "image": "144_shopstyle.png", "tags": [1, 2], "weight": 1},
                  {"domain": "dillards.com", "image": "145_dillards.png", "tags": [3], "weight": 1},
                  {"domain": "maccosmetics.com", "image": "146_maccosmetics.png", "tags": [3], "weight": 1},
                  {"domain": "stuartweitzman.com", "image": "147_stuartweitzman.png", "tags": [3], "weight": 1},
                  {"domain": "tadashishoji.com", "image": "148_tadashishoji.png", "tags": [6, 11], "weight": 2},
                  {"domain": "jomashop.com", "image": "149_jomashop.png", "tags": [5], "weight": 1},
                  {"domain": "saksfifthavenue.com", "image": "150_saksfifthavenue.png", "tags": [6], "weight": 1},
                  {"domain": "modernechild.com", "image": "151_modernechild.png", "tags": [4], "weight": 1},
                  {"domain": "littlewoods.com", "image": "152_littlewoods.png", "tags": [4], "weight": 1},
                  {"domain": "childrensorchard.com", "image": "153_childrensorchard.png", "tags": [4], "weight": 1},
                  {"domain": "athleta.gap.com", "image": "154_athleta.png", "tags": [3], "weight": 1},
                  {"domain": "avenue.com", "image": "155_avenue.png", "tags": [11], "weight": 2},
                  {"domain": "boohoo.com", "image": "156_boohoo.png", "tags": [11], "weight": 2},
                  {"domain": "ashleystewart.com", "image": "157_ashleystewart.png", "tags": [11], "weight": 2},
                  {"domain": "citychiconline.com", "image": "158_citychiconline.png", "tags": [11], "weight": 2},
                  {"domain": "simplybe.com", "image": "159_simplybe.png", "tags": [11], "weight": 2},
                  {"domain": "torrid.com", "image": "160_torrid.png", "tags": [1, 11], "weight": 2},
                  {"domain": "lanebryant.com", "image": "161_lanebryant.png", "tags": [11], "weight": 2},
                  {"domain": "herbergers.com", "image": "162_herbergers.png", "tags": [2, 11], "weight": 1},
                  {"domain": "yandy.com", "image": "163_yandy.png", "tags": [3, 11], "weight": 1},
                  {"domain": "azazie.com", "image": "164_azazie.png", "tags": [3, 11], "weight": 1},
                  {"domain": "swakdesigns.com", "image": "165_swakdesigns.png", "tags": [11], "weight": 2}]}


#exit(0)
tags_map = {}
for tag_id, tag_value in data['tags'].items():
    tags_map[int(tag_id)] = Tag()
    tags_map[int(tag_id)].title = tag_value
    tags_map[int(tag_id)].weight = int(tag_id)


for shop in data['shops']:
    new_shop = Shop()
    new_shop.domain = shop['domain']
    new_shop.image = shop['image']
    new_shop.weight = shop['weight']
    new_shop.tags = [tag for tag_id, tag in tags_map.items() if tag_id in shop['tags']]
    db.session.add(new_shop)

db.session.commit()