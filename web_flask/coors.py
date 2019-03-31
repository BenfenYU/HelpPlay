import collections

class AllName(object):
    def __init__(self):
        pass

    def translate(self,eng):
        return NAMES.get(eng).name
    
    def getCoor(self,key = None):
        if key:
            item = NAMES[key]

            return (item.lat,item.lng,key)
        else:
            coors = [(item.lat,item.lng,key)
             for key,item in NAMES.items()]
            
            return coors
    
    def items(self):
        return NAMES.items()


Viewer = collections.namedtuple('Viewer','name lng lat kind')

NAMES = {
    'MeetDroidFriends': Viewer( '？？？',121.656853,  31.140631,0),
    'TronLightcyclePowerRun': Viewer( '创极速光轮',121.656807,  31.141859,1),
	'RoaringRapids': Viewer( '雷鸣山漂流', 121.663177,  31.143061,6),
	'ChallengeTrails': Viewer( '古迹探索营的绳索挑战道',121.660767,  31.143658,1),
	'VistaTrail': Viewer( '古迹探索营的探索步行道',121.660767,  31.143658,1),
	'1879': Viewer( '？？？',121.663918,  31.143721,0),
	'OnceUponTimeAdventure': Viewer( '漫游童话时光',121.65963,  31.143789,5),
	'AliceWonderlandMaze': Viewer( '爱丽丝梦游仙境迷宫',121.659599,  31.144661,5),
	'1882': Viewer( '？？？',121.659691,  31.143629,0),
	'HunnyPotSpin': Viewer( '旋转疯蜜罐',121.65873,  31.14538,4),
	'DisneyPrincessesStorybookCourt': Viewer( '？？？',121.660767,  31.143658,0),
	'PeterPansFlight': Viewer( '小飞侠天空奇遇',121.657837,  31.14356,3),
	'SevenDwarfsMineTrain': Viewer( '七个小矮人矿山车',121.659721,  31.144939,1),
	'AdventuresWinniePooh': Viewer( '小熊维尼历险记', 121.658798,  31.14563,3),
	'VoyageToCrystalGrotto': Viewer( '晶彩奇航',121.65844,  31.14365,0),
	'DumboFlyingElephant': Viewer( '小飞象',121.659843,  31.14262,4),
	'FantasiaCarousel': Viewer( '旋转木马',121.661369,  31.142611,4),
	'1900': Viewer( '漫威英雄总部',121.658684,  31.1425,7),
	'1913': Viewer( '？？？',121.660767,  31.143658,0),
	'ExplorerCanoes': Viewer( '探险家独木舟', 121.662148,  31.143789,2),
	'PiratesOfCaribbean': Viewer( '加勒比海盗-沉落宝藏之战',121.66172,  31.145241,1),
	'ShipwreckShore': Viewer( '船奇戏水滩',121.66198,  31.14502,6),
	'SirensRevenge': Viewer( '探秘海妖复仇号',121.662781,  31.14517,6),
	'BuzzLightyearPlanetRescue': Viewer( '巴斯光年星际营救',121.6577,  31.14135,3),
	'JetPacks': Viewer( '喷气背包飞行器',121.660767,  31.143658,4),
	'StitchEncounter': Viewer( '太空幸会史迪奇',121.660767,  31.143658,6),
	'1905': Viewer( '？？？',121.660767,  31.143658,0),
	'SoaringOverHorizon': Viewer( '翱翔.飞跃地平线',121.660767,  31.143658,6),
	'MeetMickeyGardensImagination': Viewer( '米奇俱乐部', 121.659218,  31.142441,7),
	'CaptainAmerica': Viewer( '漫威英雄总部-美国队长',121.658684,  31.1425,7),
	'JungleFriendsHappyCircle': Viewer( '欢笑聚友会',121.664207,  31.14418,7),
	'CampDiscovery': Viewer( '？？？',121.660767,  31.143658,0),
	'MickeysFilmFestival': Viewer( '米奇电影节', 121.660767,  31.143658,3),
	'TronRealm': Viewer( '？？？',121.660767,  31.143658,0),
	'StarWarsLaunchBay': Viewer( '',121.656853,  31.140631,0),
	'MarvelUniverse': Viewer( '十二朋友园',121.660957,  31.143,6),
	'2596': Viewer( '？？？',121.660767,  31.143658,0),
	'SpiderMan': Viewer( '漫威英雄总部-蜘蛛侠',121.658684,  31.1425,7),
	'BecomeIronMan': Viewer( '漫威英雄总部-钢铁侠',121.658684,  31.1425,7),
	'ScreeningRoom': Viewer( '电影放映室',121.656853,  31.140631,5),
	'EncounterKyloRen': Viewer( '？？？',121.656853,  31.140631,0),
	'MeetDarthVader': Viewer( '？？？',121.656853,  31.140631,0),
	'MillenniumFalcon': Viewer( '？？？',121.656853,  31.140631,0),
    'RexsRCRacer': Viewer( '抱抱龙冲天赛车',121.656548,  31.143299,1),
    'SlinkyDogSpin': Viewer( '弹簧狗团团转',121.660767,  31.143658,4),
    'WoodysRoundUp': Viewer( '胡迪牛仔嘉年华',121.657333,  31.144051,4),
}

kinds = {
    '刺激':1,
    '水上':2,
    '黑暗':3,
    '旋转':4,
    '学龄前儿童':5,
    '青少年、成人':6,
    '互动项目':7
}
