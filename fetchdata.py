# url = f"https://www.dustloop.com/wiki/api.php?action=cargoquery&tables=MoveData_GGST&fields=chara,input,name,damage,guard,startup,active,recovery,onBlock,onHit,riscGain,riscLoss,level,invuln,counter,prorate,cancel,images,hitboxes,type&format=json&formatversion=2&where=chara%20in%20('{character}')"

from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import sys

moves = ["5P", "5K", "c.S", "f.S", "5H", "5D", "5[D]",
        "2P", "2K", "2S", "2H", "2D",
        "6P", "6K", "6S", "6H", "6D", 
        "4D", "3K",
        "j.P", "j.K", "j.S", "j.H", "j.D",
        "236P", "236K", "236S", "236H", 
        "214P", "214K", "214S", "214H",
        "623P", "623K", "623S", "623H",
        "[4]6S", "[4]6H", "[2]8S", "[2]8H",
        "63214P", "63214K", "63214S", "63214H",
        "632146P", "632146K", "632146S", "632146H",
        "236236P", "236236K", "236236", "236236H",
        "214214P", "214214K", "214214S", "214214H"]

normals = ["5P", "5K", "c.S", "f.S", "5H", "5D", "5[D]",
        "2P", "2K", "2S", "2H", "2D",
        "6P", "6K", "6S", "6H", "6D", 
        "4D", "3K",
        "j.P", "j.K", "j.S", "j.H", "j.D",]


specials = ["236P", "236K", "236S", "236H", 
        "214P", "214K", "214S", "214H",
        "623P", "623K", "623S", "623H",
        "[4]6S", "[4]6H", "[2]8S", "[2]8H",]


overdrives = ["632146P", "632146K", "632146S", "632146H",
        "236236P", "236236K", "236236", "236236H",
        "214214P", "214214K", "214214S", "214214H"]



charas = [
    "A.B.A",
    "Anji Mito",
    "Asuka R",
    "Baiken",
    "Bridget",
    "Axl Low",
    "Chipp Zanuff",
    "Queen Dizzy",
    "Jam Kuradoberi",
    "Johnny",
    "Ky Kiske",
    "Millia Rage",
    "Sol Badguy",
    "Testament",
    "Potemkin",
    "Zato-1",
    "Faust",
    "May",
    "Leo Whitefang",
    "Ramlethal Valentine",
    "Nagoriyuki",
    "Giovanna",
    "I-No",
    "Slayer",
    "Venom",
    "Bedman",
    "Elphelt Valentine",
    "Jack-O",
    "Sin Kiske",
    "Happy Chaos",
    "Goldlewis Dickinson",
    "Lucy",
    "Unika"
]

def get_infos_from_query(qry):
    qry_splt = qry.split("#")
    for i in range(len(qry_splt)):
        if qry_splt[i] in moves:
            if i<2:
                return (qry_splt[i+2], qry_splt[i])
            else:
                return (qry_splt[i-2], qry_splt[i])
            

def get_chara_from_str(string):
    bestratio = 0
    bestname = None
    for c in charas:
        if string.lower() in c.lower():
            return c
        res = SequenceMatcher(None, c, string).ratio()
        if res > bestratio:
            bestratio = res
            bestname = c
    return bestname


def get_move_data(character, move):
    og = move
    index = None
    if "(" in move:
        index = move[-3::]  
        move = move[:-3]
    
    character = get_chara_from_str(character)
    if character=="Nagoriyuki" and move in ["f.S", "c.S", "2S", "2H", "5H", "6H", "f.SS", "f.SSS"]:
        lvl = input("Indiquer le niveau de Blood Rage (1/2/3/BR) : ")
        move = move + f" Level {lvl.strip()}"
    if " " in character:
        character.replace(" ", "_")
    url = f"https://www.dustloop.com/wiki/api.php?action=cargoquery&tables=MoveData_GGST&fields=chara,input,name,damage,guard,startup,active,recovery,onBlock,onHit,invuln,cancel,images,hitboxes,type&format=json&formatversion=2&where=chara%20in%20('{character}')"
    response = requests.get(url)
    data = response.json()
    move = [entry["title"] for entry in data["cargoquery"] if entry["title"]["input"]==move][0]
    return og, move, index

def get_move_img_from_data(chara, move, movedata, index):
    i = 1
    if ";" in movedata['images']:
        for ur in movedata['images'].split(";"):
            url = ur.replace(' ', '_')
            response = requests.get(f"https://www.dustloop.com/w/File:{url}#Overview").text
            soup = BeautifulSoup(response, "html.parser")
            images = soup.find_all("img")

            for img in images:
                if not "logo" in img["src"] and not "svg" in img["src"]:
                    url = "https://www.dustloop.com" + img["src"]
                    break

            response = requests.get(url)
            
            img = Image.open(BytesIO(response.content))
            if index is not None:
                img.save(f"assets/downloaded_data/{chara}_{move[:-3].replace("/","")}({i}).png")
                i+=1
            else:
                img.save(f"assets/downloaded_data/{chara}_{move.replace("/","")}.png")
                return

    else:
        url = movedata['images'].replace(' ', '_')
        response = requests.get(f"https://www.dustloop.com/w/File:{url}#Overview").text
        soup = BeautifulSoup(response, "html.parser")
        images = soup.find_all("img")

        for img in images:
            if not "logo" in img["src"] and not "svg" in img["src"]:
                url = "https://www.dustloop.com" + img["src"]
                break

        response = requests.get(url)
        
        img = Image.open(BytesIO(response.content))
        img.save(f"assets/downloaded_data/{chara}_{move.replace("/","")}.png")

def is_gatling(A, B):
    if A not in normals or B not in normals:
        return False
    if "P" in A and ("P" in B or "6" in B):
        return True
    if "K" in A and ("D" in B or "6" in B):
        return True
    if "c.S" in A and ("S" in B or "H" in B or "D" in B or "6" in B):
        return True
    if "S" in A and ("H" in B):
        return True
    
# def calc_gap(chara, notation):
#     moveA, moveB = notation.split(">")
#     moveA = moveA.strip()
#     moveB = moveB.strip()

#     moveAdata = get_move_data(chara, moveA)
#     moveBdata = get_move_data(chara, moveB)

#     moveAreco = 0
#     moveAob = 0
#     moveAac = 0
#     moveBstartup = 0

#     if "," in moveAdata["recovery"]:
#         moveAreco = moveAdata["recovery"].split(",")[0]
#     else:
#         moveAreco = moveAdata["recovery"]

#     if "," in moveAdata["active"]:
#         moveAac = moveAdata["active"].split(",")[0]
#     else:
#         moveAac = moveAdata["active"]

#     if "," in moveAdata["onBlock"]:
#         moveAob = moveAdata["onBlock"].split(",")[0]
#     else:
#         moveAob = moveAdata["onBlock"]

#     if "," in moveBdata["startup"]:
#         moveBstartup = moveBdata["startup"].split(",")[0]
#     else:
#         moveBstartup = moveBdata["startup"]
    
#     moveAreco = int(moveAreco)
#     moveAob = int(moveAob)
#     moveAac = int(moveAac)
#     moveBstartup = int(moveBstartup)    
#     print(f" Move A recovery: {moveAreco}\n \
# Move A cancels: {moveAdata["cancel"]}\n\
# Move A on block: {moveAob}\n \
# Move A active frames: {moveAac}\n \
# Move B startup: {moveBstartup}")
#     # ============================================================ LINK
#     if not is_gatling(moveA, moveB):
#         print(f"{moveA} > {moveB} est un link.")
#         gap = abs(moveAob) + moveBstartup
#         print(f"Le gap entre le {moveA} et le {moveB} de {chara} est {gap}f.")
#     # ============================================================ GATLING
#     if is_gatling(moveA, moveB):
#         print(f"{moveA} > {moveB} est une gatling.")
#         cancelWindow = moveAreco + moveAac - 1
#         if moveBstartup < cancelWindow : 
#             print(f"{moveA} > {moveB} de {chara} est gapless.")
#         else:
#             gap = 
#     # ============================================================ SPECIAL CANCEL






    #query = input()
    #md = get_move_data(*get_infos_from_query(query))
    #get_move_img_from_data(md)

if __name__=="__main__":
    md = get_move_data("Slayer", "214P/K~H")
    get_move_img_from_data("Slayer", *md)