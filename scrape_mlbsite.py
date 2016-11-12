import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
###
def run_program(a_sql_db, a_date_strMM_DD_YYYY, a_home_team, a_away_team):
    ### make url
    month = a_date_strMM_DD_YYYY[0:2]
    day = a_date_strMM_DD_YYYY[3:5]
    year = a_date_strMM_DD_YYYY[6:10]
    game_url = "http://gd2.mlb.com/components/game/mlb/year_" + year + "/month_" + month + "/day_" + day  + "/gid_" + year + "_" + month + "_" + day + "_" + a_away_team + "mlb_" + a_home_team + "mlb_1/inning/inning_all.xml"
    player_url = "http://gd2.mlb.com/components/game/mlb/year_" + year + "/month_" + month + "/day_" + day + "/gid_" + year + "_" + month + "_" + day + "_" + a_away_team + "mlb_" + a_home_team + "mlb_1/players.xml"
    # make table names
    game_table = "game_" + a_away_team + a_home_team + month + day + year
    player_table = "player_" + a_away_team + a_home_team + month + day + year
    # check the game_url if response if it works (all assumes then that the player_url works too)
    resp = requests.get(game_url)    
    if resp.status_code != 200:
        print game_url
        print "Entered an invalid date, home team, or away team"
        return False
    else:
        
        game_data = parse_mlbgame_site(game_url)
        player_data = parse_mlbplayer_site(player_url)

        create_mlb_sql(a_sql_db)
        insert_mlbgame_into_sql(a_sql_db, game_table,game_data)
        insert_mlbplayer_into_sql(a_sql_db, player_table, player_data)
    
    
### A function to past a list of casts and a corresponding list and cast them elementwise ###
# You need to know exactly how you want to cast each element
def cast_element(func,element):
    if element is None:
        return None
    elif str(element) == "-":
        return None
    else:
        return func(element)
# Convert zulu string into datetime
def cast_date_zulu(a_zulu_str):
    return datetime.strptime(a_zulu_str, '%Y-%m-%dT%H:%M:%SZ')
def cast_text_date(a_text_date):
    return datetime.strptime(a_text_date, '%B %d, %Y')


### This function creates a sql_db
def create_mlb_sql(sql_db_name):
    sqlite_file = sql_db_name

    # connecting to the database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    conn.close()

### This function inserts game data into a game_table in the sql_db_name
def insert_mlbgame_into_sql(sql_db_name, game_table_name, mlbgame_data):
    sqlite_file = sql_db_name

    field= ['rownum','ind', 'atBat', 'deck', 'hole','inning_num','away_team','home_team','next','top_bot','atbat_action','atbat_num', 'balls', 'strikes', 'outs', 'start_tfs','tfs','batter','stand', 'b_height', 'pitcher', 'p_throws','des_atbat','event_num_atbat', 'event_atbat', 'play_guid_atbat', 'score_atbat', 'home_team_runs', 'away_team_runs','pitch_po_run','des_pit', 'id_pitch', 'type', 'tfs_pitch', 'x', 'y', 'event_num_pitch', 'sv_id', 'play_guid_pitch', 'start_speed', 'end_speed', 'sz_top', 'sz_bot', 'pfx_x', 'pfx_z', 'px', 'pz', 'x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'ax','ay', 'az', 'break_y', 'break_angle', 'break_length', 'pitch_type', 'type_confidence', 'zone', 'nasty', 'spin_dir', 'spin_rate', 'cc', 'mt', 'start', 'end', 'event_pitch', 'score_pitch', 'rbi', 'earned']
    field_type = ['INTEGER','TEXT','INTEGER','INTEGER','INTEGER','INTEGER','TEXT','TEXT','TEXT','TEXT','TEXT','INTEGER','TEXT','INTEGER','INTEGER','INTEGER','DATETIME','DATETIME','TEXT','TEXT','INTEGER','TEXT','TEXT','INTEGER','TEXT','TEXT','TEXT','INTEGER','INTEGER','TEXT','TEXT','INTEGER','TEXT','DATETIME','REAL','REAL','INTEGER','TEXT','TEXT','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','REAL','TEXT','REAL','INTEGER','INTEGER','REAL','REAL','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT']
    # connecting to the database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    # creating a new SQLITE table with columns
    createtable_text = "CREATE TABLE IF NOT EXISTS {game_table}(rownum 'INTEGER' PRIMARY KEY".format(game_table = game_table_name)
    for i in range(1,len(field)):
        createtable_text = createtable_text + ",{f} {ft}".format(f = field[i],ft = field_type[i])
    createtable_text = createtable_text + ')'    
    c.execute(createtable_text)
    conn.commit()
    # Committing changes and closing the connection to the database file
    stmt = "INSERT into {game_table}('rownum','ind', 'atBat', 'deck', 'hole','inning_num','away_team','home_team','next','top_bot','atbat_action','atbat_num', 'balls', 'strikes', 'outs', 'start_tfs','tfs','batter','stand', 'b_height', 'pitcher', 'p_throws','des_atbat','event_num_atbat', 'event_atbat', 'play_guid_atbat', 'score_atbat', 'home_team_runs', 'away_team_runs','pitch_po_run','des_pit', 'id_pitch', 'type', 'tfs_pitch', 'x', 'y', 'event_num_pitch', 'sv_id', 'play_guid_pitch', 'start_speed', 'end_speed', 'sz_top', 'sz_bot', 'pfx_x', 'pfx_z', 'px', 'pz', 'x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'ax','ay', 'az', 'break_y', 'break_angle', 'break_length', 'pitch_type', 'type_confidence', 'zone', 'nasty', 'spin_dir', 'spin_rate', 'cc', 'mt', 'start', 'end', 'event_pitch', 'score_pitch', 'rbi', 'earned') values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(game_table = game_table_name)
    for i in range(0,len(mlbgame_data)):
        c.execute(stmt, mlbgame_data[i])
    conn.commit()
    conn.close()

### This function inserts player_data into a player_table in the sql_db_name
def insert_mlbplayer_into_sql(sql_db_name, player_table_name, mlbplayer_data):
    sqlite_file = sql_db_name

    # id (INT), first (STR), last (STR), num(INT), boxname (STR), rl(STR), bats(STR), position (STR), current_position (STR), status(STR), avg (FLOAT), hr(INT), rbi(INT), bat_order(INT), game_position(STR), wins(INT), losses(INT), era(FLOAT), team_id(INT)
    field= ['rownum', 'venue','date', 'type', 'id', 'name','player_id','first','last','player_num','boxname','rl','bats','position','current_position','status','avg','hr','rbi','bat_order','game_position','wins','losses','era','team_id']
    field_type = ['INTEGER', 'INTEGER','DATETIME','TEXT','TEXT','TEXT', 'INTEGER', 'TEXT', 'TEXT', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'REAL', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT', 'INTEGER', 'INTEGER', 'REAL', 'INTEGER']
    # connecting to the database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    # creating a new SQLITE table with columns
    createtable_text = "CREATE TABLE IF NOT EXISTS {player_table}(rownum 'INTEGER' PRIMARY KEY".format(player_table = player_table_name)
    for i in range(1,len(field)):
        createtable_text = createtable_text + ",{f} {ft}".format(f = field[i],ft = field_type[i])
    createtable_text = createtable_text + ')'    
    c.execute(createtable_text)
    conn.commit()
    # Committing changes and closing the connection to the database file
    stmt = "INSERT into {player_table} values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(player_table = player_table_name)
    for i in range(0,len(mlbplayer_data)):
        c.execute(stmt, mlbplayer_data[i])
    conn.commit()
    conn.close()

    
def parse_mlbgame_site(url):

    resp = requests.get(url)
    # check to see response is 200
    if resp.status_code != 200:
        return False
    #create soup for url
    soup = BeautifulSoup(resp.content, "xml")

    # all data
    all_data = []
    count = 0
    # Collect gamedata (LEVEL 1 - General Info)
    gamedata = soup.game #use this instead of soup to get detail data
    gamedata_attrs = gamedata.attrs # dictionary containing gamedata info
    gamedata_list = [] # the list used to grab gamedata_attrs
    #grab gamedata
    game_key = ['ind', 'atBat', 'deck', 'hole']
    game_cast = [str,int,int,int]
    game_unicode = map(gamedata_attrs.get, game_key)
    for func, param in zip(game_cast, game_unicode):
        gamedata_list.append(cast_element(func, param))
    # Collect inning level (LEVEL 2)
    inning_data = gamedata.find_all('inning') # inning data transformed into list of each inning

    # For loop to go through each inning
    for inning in inning_data:
        inning_attrs = inning.attrs # dictionary containing inning data
        inning_list = [] # list used to grab inning_attrs

        # grab inning data
        inn_key = ['num','away_team','home_team','next']
        inn_cast = [int, str, str, str]
        inn_unicode = map(inning_attrs.get, inn_key)
        for func, param in zip(inn_cast, inn_unicode):
            inning_list.append(cast_element(func, param))
        
        # Collect top of the inning info and atbat/action
        topbot_inning = inning.find_all(['top','bottom'])
        for tb_inn in topbot_inning:
            atbat_action_list = [str(tb_inn.name)] # grab top or bottom of the inning data
            atbat_action_data = tb_inn.find_all(['atbat','action'])
            for ab_a in atbat_action_data:
                ab_a_key = ['num', 'b', 's', 'o', 'start_tfs_zulu','tfs_zulu','batter','stand', 'b_height', 'pitcher', 'p_throws','des','event_num', 'event', 'play_guid', 'score', 'home_team_runs', 'away_team_runs']
                ab_a_cast = [int, int, int, int, cast_date_zulu, cast_date_zulu, int, str, str, int, str, str, int, str, str, str, int, int]
                ab_a_unicode = map(ab_a.get, ab_a_key)
                ab_a_list = [str(ab_a.name)] #atbat or action
                for func,param in zip(ab_a_cast, ab_a_unicode):
                    ab_a_list.append(cast_element(func ,param))
                pitch_po_runner_data = ab_a.find_all(['pitch','runner','po'])
                for pit_po_r in pitch_po_runner_data:
                    pit_po_p_key = ['des', 'id', 'type', 'tfs_zulu', 'x', 'y', 'event_num', 'sv_id', 'play_guid', 'start_speed', 'end_speed', 'sz_top', 'sz_bot', 'pfx_x', 'pfx_z', 'px', 'pz', 'x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'ax','ay', 'az', 'break_y', 'break_angle', 'break_length', 'pitch_type', 'type_confidence', 'zone', 'nasty', 'spin_dir', 'spin_rate', 'cc', 'mt', 'start', 'end', 'event', 'score', 'rbi', 'earned']
                    pit_po_p_cast = [str, int, str, str, float, float, int, str, str, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, str, float, int, int, float, float, str, str, str, str, str, str, str, str]
                    pit_po_p_unicode = map(pit_po_r.get,pit_po_p_key)
                    pit_po_p = [str(pit_po_r.name)]
                    for func, param in zip(pit_po_p_cast, pit_po_p_unicode):
                        pit_po_p.append(cast_element(func, param))
                    count = count + 1
                    row = tuple([count] + gamedata_list + inning_list + atbat_action_list + ab_a_list + pit_po_p) # make a row and convert into a tuple
                    all_data.append(row)                         


    return all_data

def parse_mlbplayer_site(url):

    resp = requests.get(url)
    # check to see response is 200
    if resp.status_code != 200:
        return False
    #create soup for url
    soup = BeautifulSoup(resp.content, "xml")

    # all data
    all_data = []
    count = 0
    # Collect gamedata (LEVEL 1 - General Info)
    gamedata = soup.game #use this instead of soup to get detail data
    gamedata_attrs = gamedata.attrs # dictionary containing gamedata info
    
    #grab gamedata
    game_key = ['venue', 'date']
    game_cast = [str,cast_text_date]
    game_unicode = map(gamedata_attrs.get, game_key)
    gamedata_list = team_list = map(lambda x,y:cast_element(x,y), game_cast, game_unicode)

    # Collect team level (LEVEL 2)
    team_data = gamedata.find_all('team') # inning data transformed into list of each inning

    # For loop to go through each inning
    for team in team_data:
        team_attrs = team.attrs # dictionary containing team_data
        
        # grab team_data
        team_key = ['type','id','name']
        team_cast = [str, str, str]
        team_unicode = map(team_attrs.get, team_key)
        team_list = map(lambda x,y:cast_element(x,y), team_cast, team_unicode)

        # Collect player level (LEVEL 3)
        player_data = team.find_all('player')
        for player in player_data:
            player_attrs = player.attrs
            #grab player data
            player_key = ['id', 'first', 'last', 'num', 'boxname', 'rl', 'bats', 'position', 'current_position', 'status', 'avg', 'hr', 'rbi', 'bat_order', 'game_position', 'wins', 'losses', 'era', 'team_id']
            player_cast = [int, str, str, int, str, str, str, str, str, str, float, int, int, int, str, int, int, float, int]
            player_unicode = map(player_attrs.get, player_key)
            player_list = map(lambda x,y:cast_element(x,y), player_cast, player_unicode)
            count = count + 1
            row = tuple([count] + gamedata_list + team_list + player_list) # make a row and convert into a tuple
            all_data.append(row)                         


    return all_data
#### TESTING #####
url_game = "http://gd2.mlb.com/components/game/mlb/year_2015/month_07/day_10/gid_2015_07_10_arimlb_nynmlb_1/inning/inning_all.xml"
url_player = "http://gd2.mlb.com/components/game/mlb/year_2015/month_07/day_10/gid_2015_07_10_arimlb_nynmlb_1/players.xml"

m = parse_mlbgame_site(url_game)
p = parse_mlbplayer_site(url_player)






############################################## --------------------------------------####################################
#####                                                       DATA LEVELS                                             ##### 
############################################## --------------------------------------####################################

##### MLB PLAYER LEVELS #########
### LEVEL 1
# .game
# venue (STR), date (STR)

### LEVEL 2
# .team
# type (STR), id (STR), name (STR)

### LEVEL 3
# .player
# id (INT), first (STR), last (STR), num(INT), boxname (STR), rl(STR), bats(STR), position (STR), current_position (STR), status(STR), avg (FLOAT), hr(INT), rbi(INT), bat_order(INT), game_position(STR), wins(INT), losses(INT), era(FLOAT), team_id(INT)
#################################
#################################
##### MLB GAMEDATA LEVELS #########
### LEVEL 1
# .game
# atBat (INT), deck (INT), hole (INT), ind (STR)

### LEVEL 2
# .inning
# num (INT), away_team (STR), home_team (STR) , next (STR) *note next tells you if there is a bottom inning

### LEVEL 3
# .top
# .bottom *iff next = "Y"

### LEVEL 4
# .atbat
# num(INT), b(INT), s(INT), o(INT), start_tfs(INT), batter(INT), stand(STR),  b_height(STR), pitcher(INT), p_throws(STR), des(STR), event_num(INT), event(STR), play_guid(STR), score(STR), home_team_runs(INT), away_team_runs(INT)
##/ LEVEL 5
# .pitch
# des(STR), id(INT), type(STR), tfs(INT), x(FLOAT), y(FLOAT), event_num(INT), sv_id(STR), play_guid(STR), start_speed(FLOAT), end_speed(FLOAT), sz_top(FLOAT), sz_bot(FLOAT), pfx_x(FLOAT), pfx_z(FLOAT), px(FLOAT), pz(FLOAT), x0(FLOAT), y0(FLOAT), z0(FLOAT), vx0(FLOAT), vy0(FLOAT), vz0(FLOAT), ax(FLOAT),ay(FLOAT), az(FLOAT), break_y(FLOAT), break_angle(FLOAT), break_length(FLOAT), pitch_type(STR), type_confidence(FLOAT), zone(INT), nasty(INT), spin_dir(FLOAT), spin_rate(FLOAT), cc(STR), mt(STR)
# .runner
# id(INT), start(STR), end(STR), event(STR), event_num(INT), score(STR), rbi(STR), earned(STR)
# .po
# des(STR), event_num(INT), play_guid(STR)
##/
### LEVEL 4
# .action
# b(INT), s(INT), o(INT), des(STR), event(STR), tfs(STR),player(INT), pitch(INT), event_num(INT), home_team_runs(INT), away_team_runs(INT)

#### DATA TRANSFORM
###
# [atbat, deck,, hold, ind]
# [inning_num, away_team, home_team, next]
# [top/bottom]
# [atbat/action, num, b, s, o, start_tfs, batter, stand, b_height, pitcher, p_throws, des, event_num, event, play_guid, score, home_team_runs, away_team_runs, tfs]
# [pitch/po/runner , des, id, type, tfs, x, y, event_num, sv_id, play_guid, start_speed, end_speed, sz_top, sz_bot, pfx_x, pfx_z, px, pz,x0, y0, z0, vx0, vy0, vz0, ax, ay, az, break_y, break_angle, break_length, pitch_type, type_confidence, zone, nasty, spin_dir, spin_rate, cc, mt, score, rbi, earned]
