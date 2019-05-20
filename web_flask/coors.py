import collections

Viewer = collections.namedtuple('Viewer','name lng lat duration kind')

NAMES = {
    #'MeetDroidFriends': Viewer( '？？？',121.656853,  31.140631,0,0),
    'TronLightcyclePowerRun': Viewer( '创极速光轮',121.656807,  31.141859,900,1),
	'RoaringRapids': Viewer( '雷鸣山漂流', 121.663177,  31.143061,600,1),
	'ChallengeTrails': Viewer( '古迹探索营的绳索挑战道',121.660767,  31.143658,720,1),
	'VistaTrail': Viewer( '古迹探索营的探索步行道',121.660767,  31.143658,720,1),
	'1879': Viewer( '？？？',121.663918,  31.143721,0,0),
	'OnceUponTimeAdventure': Viewer( '漫游童话时光',121.65963,  31.143789,780,0),
	'AliceWonderlandMaze': Viewer( '爱丽丝梦游仙境迷宫',121.659599,  31.144661,780,0),
	'1882': Viewer( '？？？',121.659691,  31.143629,0,0),
	'HunnyPotSpin': Viewer( '旋转疯蜜罐',121.65873,  31.14538,240,0),
	'DisneyPrincessesStorybookCourt': Viewer( '迎宾阁',121.660767,  31.143658,540,0),
	'PeterPansFlight': Viewer( '小飞侠天空奇遇',121.657837,  31.14356,600,0),
	'SevenDwarfsMineTrain': Viewer( '七个小矮人矿山车',121.659721,  31.144939,600,1),
	'AdventuresWinniePooh': Viewer( '小熊维尼历险记', 121.658798,  31.14563,780,0),
	'VoyageToCrystalGrotto': Viewer( '晶彩奇航',121.65844,  31.14365,900,0),
	'DumboFlyingElephant': Viewer( '小飞象',121.659843,  31.14262,300,0),
	'FantasiaCarousel': Viewer( '旋转木马',121.661369,  31.142611,360,0),
	'1900': Viewer( '漫威英雄总部',121.658684,  31.1425,780,0),
	'1913': Viewer( '？？？',121.660767,  31.143658,0,0),
	'ExplorerCanoes': Viewer( '探险家独木舟', 121.662148,  31.143789,2700,0),
	'PiratesOfCaribbean': Viewer( '加勒比海盗-沉落宝藏之战',121.66172,  31.145241,1020,0),
	'ShipwreckShore': Viewer( '船奇戏水滩',121.66198,  31.14502,480,0),
	'SirensRevenge': Viewer( '探秘海妖复仇号',121.662781,  31.14517,660,0),
	'BuzzLightyearPlanetRescue': Viewer( '巴斯光年星际营救',121.6577,  31.14135,300,0),
	'JetPacks': Viewer( '喷气背包飞行器',121.660767,  31.143658,240,0),
	'StitchEncounter': Viewer( '太空幸会史迪奇',121.660767,  31.143658,900,0),
	'1905': Viewer( '？？？',121.660767,  31.143658,0,0),
	'SoaringOverHorizon': Viewer( '翱翔.飞跃地平线',121.660767,  31.143658,1500,0),
	'MeetMickeyGardensImagination': Viewer( '米奇俱乐部', 121.659218,  31.142441,540,0),
	'CaptainAmerica': Viewer( '漫威英雄总部-美国队长',121.658684,  31.1425,300,0),
	'JungleFriendsHappyCircle': Viewer( '欢笑聚友会',121.664207,  31.14418,240,0),
	'CampDiscovery': Viewer( '？？？',121.660767,  31.143658,0,0),
	'MickeysFilmFestival': Viewer( '米奇电影节', 121.660767,  31.143658,1080,0),
	'TronRealm': Viewer( '创界：雪佛兰数字挑战',121.660767,  31.143658,600,0),
	'StarWarsLaunchBay': Viewer( '？？？',121.656853,  31.140631,0,0),
	'MarvelUniverse': Viewer( '十二朋友园',121.660957,  31.143,240,0),
	'2596': Viewer( '？？？',121.660767,  31.143658,0,0),
	'SpiderMan': Viewer( '漫威英雄总部-蜘蛛侠',121.658684,  31.1425,300,0),
	'BecomeIronMan': Viewer( '漫威英雄总部-钢铁侠',121.658684,  31.1425,300,0),
	'ScreeningRoom': Viewer( '电影放映室',121.656853,  31.140631,1080,0),
	'EncounterKyloRen': Viewer( '？？？',121.656853,  31.140631,0,0),
	'MeetDarthVader': Viewer( '？？？',121.656853,  31.140631,0,0),
	'MillenniumFalcon': Viewer( '？？？',121.656853,  31.140631,0,0),
    'RexsRCRacer': Viewer( '抱抱龙冲天赛车',121.656548,  31.143299,300,0),
    'SlinkyDogSpin': Viewer( '弹簧狗团团转',121.660767,  31.143658,300,0),
    'WoodysRoundUp': Viewer( '胡迪牛仔嘉年华',121.657333,  31.144051,120,0),
}

kinds = {
	'緩速':1,
    '刺激':2,
    '水上':3,
    '黑暗':4,
    '旋转':5,
    '学龄前儿童':6,
    '互动项目':7
}

kinds_project = {
	1:['晶彩奇航','加勒比海盗——沉落宝藏之战'],
	2:['雷鸣山漂流','古迹探索营','加勒比海盗——沉落宝藏之战','七个小矮人矿山车','抱抱龙冲天赛车','创极速光轮'],
	3:['雷鸣山漂流','探险家独木舟'],
	4:['雷鸣山漂流','加勒比海盗——沉落宝藏之战','小熊维尼历险记','小飞侠天空奇遇','创极速光轮','巴斯光年星际营救','米奇电影节'],
	5:['旋转木马','小飞象','喷气背包飞行器','弹簧狗团团转','胡迪牛仔嘉年华','旋转疯蜜罐'],
	6:['探险家独木舟','雷鸣山漂流','欢笑聚友会','探秘海妖复仇号','加勒比海盗沉落宝藏之战','船奇戏水滩','爱丽丝梦游仙境迷宫',
	'七个小矮人矿山车','小熊维尼历险记','旋转疯蜜罐','弹簧狗团团转','巴斯光年星际营救','太空幸会史迪奇',
	'喷气背包飞行器','米奇俱乐部','小飞象','旋转木马','小飞侠天空奇遇','晶彩奇航','迎宾阁','漫游童话时光',
	'古迹探险营','米奇电影节','十二朋友园','漫威英雄总部','电影放映室','雪佛兰数字挑战'],
	7:['欢笑聚友会','探秘海妖复仇号','船奇戏水滩','漫游童话时光','迎宾阁','米奇俱乐部','漫威英雄总部',
	'太空幸会史迪奇','巴斯光年星际营救']
}

class AllName(object):
    def __init__(self):
        pass

    def get_kind(self,kind):
        yes_dict= {}
        kind_list = kinds_project[kind]
        for key,value in self.items():
            if value.name in kind_list:
                yes_dict[key] = value

        return yes_dict

    def translate(self,eng):
        return NAMES.get(eng).name
    
    def getCoor(self,key = None,names=NAMES):
        if key:
            item = names[key]

            return (item.lat,item.lng,key)
        else:
            coors = [(item.lat,item.lng,key)
             for key,item in names.items()]
            
            return coors
    
    def items(self):
        return NAMES.items()

