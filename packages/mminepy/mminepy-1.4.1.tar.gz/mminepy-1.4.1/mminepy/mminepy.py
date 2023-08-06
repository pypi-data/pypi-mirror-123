import inspect
import os
# 
import sys
sys.tracebacklimit = 0
global Event_name
Event_name = ''
global long
long = 0
global comnum
comnum = 0
global list_name_list
list_name_list = []
global type_list
type_list = []
global check_list
check_list = []
global python_space
python_space = 0
global test_value
test_value = 0
global var_dict
var_dict = {}
global pl1
global st1
global al_pl_1
global addition_list
addition_list = []
global howmany
howmany = -1
python_var = 0
global n
n = 0
global k
k = 0
global var_dict_type
var_dict_type = {"ArrayList":False,"Material":False,"Player":False,"Inventory":False,"World":False,"Location":False,"Block":False,"ItemStack":False,"Action":False}
global var_list
var_list = []
global check_list_var
check_list_var = 0
global javacode
javacode = ''
global Playerinclude
Playerinclude =False
def range(first,second):
    global check_list
    check_list.append("for_range")
    return [1]
class random:
    def randint(first,second):
        pass
def define_auto(code):
    var_name = code.split("=")[0]
    global var_list
    global var_dict
    global javacode
    if not var_list.__contains__(var_name):
        data = code.split("=")[1]
        code = data.split(".")[-1]
        type_Var = ""
        m = ''
        if code.__contains__('getPlayer') or code.__contains__('sender'):
            type_Var = "Player"
            m = 'public Player '+var_name+";\n"
        elif code.__contains__('getWorld'):
            type_Var = "World"
            m = 'public World '+var_name+";\n"
        elif code.__contains__('getItemInHand'):
            type_Var = "ItemStack"
            m = 'public ItemStack '+var_name+";\n"
        elif code.__contains__('getName') or code.__contains__('toString'):
            type_Var = "String"
            m = 'public String '+var_name+";\n"
        elif code.__contains__('getInventory'):
            type_Var = "Inventory"
            m = 'public Inventory '+var_name+";\n"
        elif code.__contains__('getLocation'):
            type_Var = "Location"
            m = 'public Location '+var_name+";\n"
        elif code.__contains__('getX') or code.__contains__('getY') or code.__contains__('getZ') or code.__contains__("randint"):
            m = 'public Integer '+var_name+";\n"
            type_Var = "Integar"
        elif code.__contains__('getBlock'):
            type_Var = "Block"
            m = 'public Block '+var_name+";\n"
        elif code.__contains__('getMaterial'):
            m = 'public Material '+var_name+";\n"
            type_Var = "Material"
        elif code.__contains__(".get("):
            code = code.replace(".get("," ")
            code = code.replace(")","")
            code = code.replace("="," ")
            code1 = code.split(" ")[0]
            code2 = code.split(" ")[1]
            code3 = code.split(" ")[2]
            m = 'public '+var_dict.get(code2)+' '+code1+";\n"
            type_Var = var_dict.get(code2)
        if not var_dict.__contains__(var_name):
            var_dict[var_name] = (type_Var)
        var_dict_type[type_Var] = True
        javacode = javacode.replace("public class Main extends JavaPlugin implements Listener{\n",
        "public class Main extends JavaPlugin implements Listener{\n"+'   '+m)
        var_list.append(var_name)
    return javacode
class space:
    def forfinish(code):
        global python_space
        global javacode
        global java_space
        global howmany
        global check_list    
        while not code.__contains__("   "*python_space):
            
            java_space -= 1
            javacode = space.getspace(javacode)
            javacode += "}\n"
            python_space -= 1
        return code
    def getspace(string):
        global java_space
        string += "   "*java_space
        return string
def init():
    file = open("data/src/main/resources/plugin.yml","w")
    file.write("name: minepy\nmain: Main.Main\nversion: 1.0\napi-version: 1.16\ncommands:\n")
    file.close()
    global bc1
    bc1 = Block()
    global ac1
    ac1 = Action()
    global mt1
    mt1 = Material()
    global inven1
    inven1 = Inventory()
    global is1
    is1 = ItemStack()
    global wr1
    wr1 = World()
    global al_wr_1
    al_wr_1 = ArrayList(world())
    global al_pl_1
    al_pl_1 = ArrayList(player())
    global pl1
    pl1 = Player()
    global lc1
    lc1 = Location()
    global check_list
    check_list.append('init')
def print(message):
    check_list.append('sys_activity')
class Player:
    def __init__(self):
        global addition_list
        if not addition_list.__contains__('org.bukkit.entity.Player'):
            addition_list.append('org.bukkit.entity.Player')
        global check_list
        self.type = "player"
        check_list.append("define")
    def setHealth(self,value):
        global check_list
        check_list.append("activity")
    def getName(self):
        return "hello"
    def sendMessage(self,*args):
        global check_list
        check_list.append("activity_message")
    def getLocation(self):
        return lc1
    def teleport(self,Location):
        global check_list
        check_list.append("activity")
    def sendTitle(self,main_,sub,open_time,status,close):
        global check_list
        check_list.append("activity_message")
    def hasPlayedBefore(self):
        pass
    def removePotionEffect(self,effectype,*detail):
        global check_list
        check_list.append("activity_potion")
    def addPotionEffect(self,effectype,second,hard,*detail):
        global check_list    
        check_list.append("activity_potion")
    def getName(self):
        return ""
    def getItemInHand(self):
        global is1
        return is1
    def getInventory(self):
        global inven1
        return inven1
class ArrayList:
    def __init__(self,typeof):
        global addition_list
        if not addition_list.__contains__('java.util.ArrayList'):
            addition_list.append('java.util.ArrayList')
        global check_list
        check_list.append("define")
        self.type = typeof
    def add(self,something):
        global check_list    
        check_list.append("activity")
    def get(self,index):
        global pl1
        if self.type == "player":
            return pl1
class String:
    def __init__(self):
        global check_list
        check_list.append("define")
class Event:
    def __init__(self,eventname):
        global check_list
        check_list.append("define_python")
    def getPlayer(self):
        return pl1
    def setCancelled(self,status):
        global check_list
        check_list.append("activity")
class Location:
    def __init__(self):
        global addition_list
        if not addition_list.__contains__('org.bukkit.Location'):
            addition_list.append('org.bukkit.Location')
        global check_list
        check_list.append("define")
    def getBlock(self):
        global bc1
        return bc1
    def setX(self,set):
        global check_list    
        check_list.append("activity") 
    def setY(self,set):
        global check_list    
        check_list.append("activity") 
    def setZ(self,set):
        global check_list    
        check_list.append("activity") 
    def getX(self):
        global type_list
        type_list.append("int")
        return 1
    def getY(self):
        global type_list
        type_list.append("int")
        return 1
    def getZ(self):
        global type_list
        type_list.append("int")
        return 1
class Random:
    def __init__(self):
        global addition_list
        addition_list.append('java.util.Random')
        global check_list
        check_list.append("define")
    def nextInt(self,value):
        return 15
class Bukkit:
    def getPlayers():
        global pl1
        global Playerinclude
        Playerinclude = True
        return pl1
    def getWorlds():
        global wr1
        return wr1
class Inventory:
    def __init__(self):
        global check_list
        check_list.append("define")
        global addition_list
        if not addition_list.__contains__('org.bukkit.inventory.Inventory'):
            addition_list.append('org.bukkit.inventory.Inventory')
    def addItem(self,itemStack):
        global check_list
        check_list.append("activity")
class ItemStack:
    def __init__(self):
        global addition_list
        if not addition_list.__contains__('org.bukkit.inventory.ItemStack'):
            addition_list.append('org.bukkit.inventory.ItemStack')
        global check_list
        check_list.append("define")
    def setMaterial(self,something):
        global is1
        global check_list
        check_list.append("activity")
        return is1
    def setAmount(self,amount):
        global is1
        global check_list
        check_list.append("activity")
        return is1
    def getMaterial(self):
        global is1
        return is1
class Command:
    def sender():
        global pl1
        return pl1
    def label():
        return ""
class World:
    def __init__(self):
        self.type = "world"
        global addition_list
        if not addition_list.__contains__('org.bukkit.World'):
            addition_list.append('org.bukkit.World')
        global check_list    
        check_list.append("define")
    def setGameRule(self,gamerule,status):
        if not addition_list.__contains__('org.bukkit.GameRule'):
            addition_list.append('org.bukkit.GameRule')
        global check_list    
        check_list.append("activity")
class Block:
    def __init__(self):
        self.type = "Block"
        global addition_list
        if not addition_list.__contains__('org.bukkit.block.Block'):
            addition_list.append('org.bukkit.block.Block')
        global check_list    
        check_list.append("define")
    def getMaterial(self):
        global mt1    
        return mt1
def time(when):
    global n
    n += 1
    if n == 1:
        global check_list
        check_list.append("while_time")
        return True
    else:
        n = 0
        return False
def event(when):
    global n
    n += 1
    if n == 1:
        global check_list
        check_list.append("while_event")
        return True
    else:
        n = 0
        return False
def when(*test):
    global k
    k += 1
    if k == 1:
        global check_list
        check_list.append("if")
        return True
    else:
        k = 0
        return False
def repeat(*var_name):
    if len(var_name) == 1:
        list_name = var_name[0]
        global pl1
        global wr1
    
        check_list.append("for")
        g = []
        global list_name_list
        list_name_list.append(list_name.type)
        if list_name.type == "player":
            g.append(pl1)
            return g
        elif list_name.type == "world":
            g.append(wr1)
            return g
def command(some):
    global n
    n += 1
    if n == 1:
        global check_list
        check_list.append("command")
        return True
    else:
        n = 0
        return False       
def tell():
    global check_list
    sys.stdout.write(",".join(check_list))
    sys.stdout.write("\n")
    check_list.append("tell")
def make():
    global Playerinclude
    global enable_space
    global addition_list
    global python_space
    global java_space
    java_space = 0
    global check_list
    global check_list_var
    global javacode
    global howmany
    check_list.append("make")
    while check_list[0] != 'init':
        del check_list[0]
    sys.stdout.write("['")
    sys.stdout.write("','".join(check_list))
    sys.stdout.write("']")
    sys.stdout.write("\n")
    javacode = ''
    import inspect
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    file = open(filename,"r")
    lines = file.readlines()
    global long
    for code in lines:
        code = str(code)
        code = code.replace("when=", "")
        getvalue = distinguish_execution(code)
        if getvalue == True:
            m = check_list[check_list_var]
            if len(check_list) > 1:
                if not check_list[1] == 'make':
                    code = space.forfinish(code)
            if m != 'make' and howmany == 1:
                howmany = 0
                code = space.forfinish(code)
                howmany = 1
            code = code.replace("   ","")
            code = code.replace("\n","")
            if m == 'init':
                del check_list[0] 
                javacode = space.getspace(javacode)
                javacode += 'public class Main extends JavaPlugin implements Listener{\n'
                java_space += 1
                addition_list.append('org.bukkit.plugin.java.JavaPlugin')
                addition_list.append('org.bukkit.event.Listener')
            elif code.__contains__(".")  and code.__contains__("=") and not(code.__contains__("while")) and not(code.__contains__("for")):
                if not (code.__contains__("randint")):
                    if not code[len(code)-2:len(code)] == "()":
                        # raise ValueError("you have to set () in '"+code+"'\n")
                        global long
                        raise Exception('you should put () in "'+filename+'", line '+str(long)+',')
                else:
                    if not var_list.__contains__("random"):
                        sg = "Random random;\n"
                        javacode = javacode.replace("public class Main extends JavaPlugin implements Listener{\n",
                        "public class Main extends JavaPlugin implements Listener{\n"+"   "+sg)
                        var_list.append("random")
                        addition_list.append("java.util.Random")
                    var = code.split("=")[0]
                    code1 = code.split("=")[1]
                    code1 = code1.split("(")[1]
                    code2 = code1.split(",")[0]
                    code3 = code1.split(",")[1]
                    code3 = code3.split(")")[0]
                    code = var+"="+"random.randint("+code3+")"+"+"+code2
                javacode = space.getspace(javacode)
                code = code.replace(" ","")
                javacode = define_auto(code)
                code = code.replace("randint","nextInt")
                code = code.replace("="," = ")
                if code.__contains__("getItemInHand"):
                    if not javacode.__contains__('@SuppressWarnings("deprecation")\n'+'   '+'public boolean'):
                        javacode = javacode.replace('public boolean','@SuppressWarnings("deprecation")\n'+'   '+'public boolean')
                code = code.replace("Command.sender()", "(Player) sender")
                code = code.replace("Command.","")
                code = code.replace("label()", "Label")
                code = code.replace("Material","Type")
                if code.__contains__("getX") or code.__contains__("getY") or code.__contains__("getZ"):
                    i1 = code.split("=")[0]
                    i2 = code.split("=")[1]
                    m = type_list[0]
                    del type_list[0]
                    code = i1+'= ('+str(m) +')'+ i2
                javacode += code +';\n'
            elif not code.__contains__("("):
                code = code.replace(" ","")
                var_name = code.split("=")[0]
                if not var_list.__contains__(var_name):
                    data = code.split("=")[1]
                    if data.__contains__('"'):
                        javacode = space.getspace(javacode)
                        javacode += 'String '+var_name+";\n"
                    else:
                        javacode = space.getspace(javacode)
                        javacode += 'Integer '+var_name+";\n"
                    var_list.append(var_name)
                javacode = space.getspace(javacode)
                code = code.replace("="," = ")
                javacode += code+";\n"
            elif m == 'while_time':
                del check_list[0] 
                javacode = space.getspace(javacode)
                javacode += '@Override\n'
                javacode = space.getspace(javacode)
                code = code.replace(" ","")
                code1 = code.replace('whiletime', '')
                code1 = code1.replace('(', '')
                code1 = code1.replace(')','')
                code1 = code1.replace(':','')
                code1 = code1.replace('\n','')
                if code1 == "Enable":
                    javacode += 'public void onEnable(){\n'
                if code1 == "Disable":
                    javacode += 'public void onDisable(){\n'
                python_space += 1
                java_space += 1
            elif m == 'while_event':
                global Event_name
                Event_name = ''
                del check_list[0] 
                code = code.replace("   ","")
                if not javacode.__contains__("Bukkit.getPluginManager().registerEvents(this,this)"):
                    addition_list.append("org.bukkit.Bukkit")
                    r = 2*"   "
                    javacode = javacode.replace('public void onEnable(){\n', 'public void onEnable(){\n'+r+'Bukkit.getPluginManager().registerEvents(this,this);\n')
                global test_value
                test_value += 1
                name = 'test'+str(test_value)
                javacode += "   "*java_space
                javacode += "@EventHandler\n"
                code = code.replace(" ","")
                code1 = code.replace('(', '')
                code1 = code1.replace(')','')
                code1 = code1.replace(':','')
                code1 = code1.replace('\n','')
                code1 = code1.replace('whileevent', '')
                if not addition_list.__contains__('org.bukkit.event.EventHandler'):
                    addition_list.append('org.bukkit.event.EventHandler')
                if code1.__contains__("Player") and not addition_list.__contains__('org.bukkit.event.player.'+code1):
                    addition_list.append('org.bukkit.event.player.'+code1)
                elif code1.__contains__("Block") and not addition_list.__contains__('org.bukkit.event.block.'+code1):
                    addition_list.append('org.bukkit.event.block.'+code1)
                elif code1.__contains__("Entity") and not addition_list.__contains__('org.bukkit.event.entity.'+code1):
                    addition_list.append('org.bukkit.event.entity.'+code1)
                elif code1 == "ProjectileHitEvent":
                    addition_list.append('org.bukkit.event.entity.'+code1)
                javacode = space.getspace(javacode)
                javacode += 'public void '+name+'('+code1+' e'+') {\n'
                python_space += 1
                java_space += 1
                Event_name = code1
            elif m == 'define_python':
                del check_list[0] 
                pass
            elif m == 'define':
                
                del check_list[0] 
                code = code.replace(" ","")
                i_list = code.split("=")
                variable_name = i_list[0]
                middle_part = i_list[1].replace("(","")
                middle_part = middle_part.replace(")","")
                if middle_part.__contains__("ArrayList"):
                    species = middle_part.replace("ArrayList","")
                    k = str(species[0])
                    species = k.upper() + species[1:len(species)]
                    m = 'public ArrayList<'+species+'> '+variable_name+' = new ArrayList<>();\n'
                    var_dict[variable_name] = species
                elif middle_part == "Random":
                    m = 'Random '+variable_name+' = new Random();\n'
                else:
                    if middle_part == "Player":
                        Playerinclude = True
                    m = 'public '+middle_part+' '+variable_name+';\n'
                javacode = javacode.replace("public class Main extends JavaPlugin implements Listener{\n",
                "public class Main extends JavaPlugin implements Listener{\n"+'   '+m)
                var_list.append(variable_name)
                var_dict_type[middle_part] = True
            elif m == 'activity':
                del check_list[0] 
                code = code.replace(" ","")
                code = code.replace("="," = ")
                javacode = space.getspace(javacode)
                code = code.replace("Material","Type")
                code = code.replace("()","")
                code = code.replace("True","true")
                if code.__contains__("setCancel") and Event_name == "PlayerJoinEvent":
                    raise Exception('PlayerJoinEvent cannot put setCancel "'+filename+'", line '+str(long)+',')
                javacode += code +';\n'
            elif m == 'activity_message':
                del check_list[0] 
                i1 = code.split(".")[0]
                i2 = i1.replace(" ","")
                javacode = space.getspace(javacode)
                if not code.__contains__('"'):
                    if code.__contains__('()'):
                        raise Exception('you should put only variable in "'+filename+'", line '+str(long)+',')
                    first_part = code.split("(")[1]
                    first_part = first_part.split(")")[0]
                    first_part = first_part.replace('"','')
                    try:
                        g = int(first_part)
                    except Exception:
                        if not (var_dict.get(first_part) == "String") and not(var_dict.get(first_part) == "Integar"):
                            raise Exception('you should put only String or int in "'+filename+'", line '+str(long)+',')
                code = code.replace(i1,i2)
                code = code.replace(")",'+"")')
                javacode += code+';\n'
                
            #potion들 다루어논것
            elif m == 'activity_potion':
                del check_list[0] 
                code = code.replace(" ","")
                code += ';\n'
                code = code.replace(" ","")
                if code.__contains__("add"):
                    code = code.replace(");","));")
                    code = code.replace("(Potion","(new PotionEffect(Potion")
                code = code.replace("()","")
                r = int(code.split(",")[1])
                r = r * 20
                code = code.split(",")[0]+','+str(r)+','+code.split(",")[2]
                javacode = space.getspace(javacode)
                javacode += code
                if not addition_list.__contains__("org.bukkit.potion.PotionEffect"):
                    addition_list.append("org.bukkit.potion.PotionEffect")
                    addition_list.append("org.bukkit.potion.PotionEffectType")
            elif m == 'sys_activity':
                del check_list[0] 
                if code.__contains__("print"):
                    code = code.replace(" ","")
                    code += ');\n'
                    javacode = space.getspace(javacode)
                    code = code.replace("print(","")
                    code = code.replace(");",";")
                    code = code.replace(")",'+"")')
                    javacode += 'System.out.println('+code
            elif m == "setnum":
                del check_list[0] 
                javacode = space.getspace(javacode)
                code = code.replace(" ","")
                code = code.replace("="," = ")
                code = code.replace("(","")
                code = code.replace(")","")
                if code.__contains__("add"):
                    code = code.replace("add","")
                    code = code.replace("setvar","")
                    code = code.replace(",","+")
                elif code.__contains__("subtract") or code.__contains__("minus"):
                    code = code.replace("subtract","")
                    code = code.replace("minus","")
                    code = code.replace("setvar","")
                    code = code.replace(",","-")
                elif code.__contains__("multiply"):
                    code = code.replace("multiply","")
                    code = code.replace("setvar","")
                    code = code.replace(",","*")
                elif code.__contains__("divide"):
                    code = code.replace("divide","")
                    code = code.replace("setvar","(int) ")
                    code = code.replace(",","/")
                else:
                    code = code.replace("setvar","")
                javacode += code+';\n'
            elif m == "for":
                del check_list[0] 
                code = code.replace(" ","")
                javacode = space.getspace(javacode)
                code = code.replace("for","")
                code = code.replace("t(","t")
                code = code.replace("):","")
                code = code.replace("in"," in")
                code = code.replace("repeat","")
                code = code.replace("getPlayers()","getOnlinePlayers()")
                i1 = code.split(" in")[0]
                i2 = code.split(" in")[1]
                i2 = i2.replace("\n","")
                global list_name_list
                type_var = list_name_list[0]
                k = str(type_var[0])
                type_var = k.upper() + type_var[1:len(type_var)]
                javacode += "for ("+type_var+" "+i1+":"+i2+"){\n"
                del list_name_list[0]
                python_space += 1
                java_space += 1
                var_dict_type[type_var] = True
            elif m == 'for_range':
                del check_list[0] 
                code = code.replace(" ","")
                code = code.replace('):','')
                code = code.replace("for","")
                var_name = code.split("inrange(")[0]
                code = code.split("inrange(")[1]
                start_1 = code.split(",")[0]
                end = code.split(",")[1]
                javacode = space.getspace(javacode)
                if not var_list.__contains__(var_name):
                    javacode += 'Integer '+var_name +';\n'
                    javacode = space.getspace(javacode)
                javacode += 'for('+var_name+' = '+str(int(start_1)-1)+'; '+var_name+' < '+end+'; '+ var_name+"++ ) {\n"
                python_space += 1
                java_space += 1
            elif m == 'if':
                del check_list[0] 
                code = code.replace(" ","")
                code = code.replace("when","")
                code = code.replace("while","if")
                code = code.replace("not","!")
                code = code.replace("==",".equals(")
                code = code.replace(":",") {")
                code =  code.replace("()","")
                code1 = code.split(" ")[0]
                if code.__contains__("and"):
                    code2 = code.split("and")
                    if code2.__contains__("!"):
                        code = code.replace("and","))and")
                    else:
                        code = code.replace("and",")and")
                elif code.__contains__("or"):
                    code2 = code.split("or")
                    if code2.__contains__("!"):
                        code = code.replace("or","))or")
                    else:
                        code = code.replace("or",")or")
                code = code.replace("and"," && ")
                code = code.replace("or"," || ")
                javacode = space.getspace(javacode)
                javacode += code+'\n'
                java_space += 1
                python_space += 1
            elif m == 'command':
                del check_list[0]
                code = space.forfinish(code)
                global comnum
                code = code.replace(" ","")
                code = code.replace('whilecommand("',"")
                code = code.replace('"):',"")
                name = 'onCommand'
                comnum += 1
                java_space = 1
                python_space = 0
                if not javacode.__contains__('public boolean '+name+'(CommandSender sender, Command cmd, String Label, String[] args) {\n'):
                    javacode += '   '
                    javacode += 'public boolean '+name+'(CommandSender sender, Command cmd, String Label, String[] args) {\n'
                java_space += 1
                python_space += 1
                javacode += '   '*2+'if (Label.equalsIgnoreCase("'+code+'")) {\n'
                java_space += 1
                howmany = 1
                if not addition_list.__contains__("org.bukkit.command.Command"): 
                    addition_list.append("org.bukkit.command.Command")
                    addition_list.append("org.bukkit.command.CommandSender")
                r = 2*"   "
                # javacode = javacode.replace('public void onEnable(){\n', 'public void onEnable(){\n'+r+'this.getCommand("'+code+'").setExecutor(this);\n')
                file = open("data/src/main/resources/plugin.yml","a")
                file.write('  '+code+':\n')
                file.close()
            elif m == "make":
                del check_list[0]
                if howmany == 1:
                    while java_space > 0:
                        if java_space == 2:
                            javacode = space.getspace(javacode)
                            javacode += "return false;\n"
                        java_space -= 1
                        javacode = space.getspace(javacode)
                        javacode += "}\n"
                else:
                    while java_space > 0:
                        java_space -= 1
                        javacode = space.getspace(javacode)
                        javacode += "}\n"
    if var_dict_type.get("Location") == False:
        addition_list.remove("org.bukkit.Location")
    if Playerinclude == False:
        addition_list.remove("org.bukkit.entity.Player")
    if var_dict_type.get("ArrayList") == False:
        addition_list.remove("java.util.ArrayList")
    if var_dict_type.get("World") == False:
        addition_list.remove("org.bukkit.World")
    if var_dict_type.get("ItemStack") == False:
        addition_list.remove("org.bukkit.inventory.ItemStack")
    if var_dict_type.get("Action") == False:
        addition_list.remove("org.bukkit.event.block.Action")
    if var_dict_type.get("Material") == False:
        addition_list.remove("org.bukkit.Material")
    if var_dict_type.get("Inventory") == False:
        addition_list.remove("org.bukkit.inventory.Inventory")
    if var_dict_type.get("Block") == False:
        addition_list.remove("org.bukkit.block.Block")
    addition = ""
    for code1 in addition_list:
        addition += 'import '+code1 +';\n'
    file = open("data/src/main/java/Main/Main.java","w")
    last_String = 'package Main;\n\n'+addition+javacode
    file.write(last_String)
def distinguish_execution(code):
    code = str(code)
    global long
    long += 1
    if not code.__contains__("import"):
        no_blank_i = code.replace(" ","")
        if not no_blank_i[0] == "#":
            if not code == "tell()":
                if not code == "Enable":
                    if not code == "Disable":
                        m = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
                        for h in code:
                            if m.__contains__(h):
                                return True
                        
    return False
class GameRule:
    def ANNOUNCE_ADVANCEMENTS(): return "gamerule"
    def COMMAND_BLOCK_OUTPUT(): return "gamerule"
    def DISABLE_ELYTRA_MOVEMENT_CHECK(): return "gamerule"
    def DO_DAYLIGHT_CYCLE(): return "gamerule"
    def DO_ENTITY_DROPS(): return "gamerule"
    def DO_FIRE_TICK(): return "gamerule"
    def DO_LIMITED_CRAFTING(): return "gamerule"
    def DO_MOB_LOOT(): return "gamerule"
    def DO_MOB_SPAWNING(): return "gamerule"
    def DO_TILE_DROPS(): return "gamerule"
    def DO_WEATHER_CYCLE(): return "gamerule"
    def KEEP_INVENTORY(): return "gamerule"
    def LOG_ADMIN_COMMANDS(): return "gamerule"
    def MOB_GRIEFING(): return "gamerule"
    def NATURAL_REGENERATION(): return "gamerule"
    def REDUCED_DEBUG_INFO(): return "gamerule"
    def SEND_COMMAND_FEEDBACK(): return "gamerule"
    def SHOW_DEATH_MESSAGES(): return "gamerule"
    def SPECTATORS_GENERATE_CHUNKS(): return "gamerule"
    def DISABLE_RAIDS(): return "gamerule"
    def DO_INSOMNIA(): return "gamerule"
    def DO_IMMEDIATE_RESPAWN(): return "gamerule"
    def DROWNING_DAMAGE(): return "gamerule"
    def FALL_DAMAGE(): return "gamerule"
    def FIRE_DAMAGE(): return "gamerule"
    def DO_PATROL_SPAWNING(): return "gamerule"
    def DO_TRADER_SPAWNING(): return "gamerule"
    def FORGIVE_DEAD_PLAYERS(): return "gamerule"
    def UNIVERSAL_ANGER(): return "gamerule"
    def RANDOM_TICK_SPEED(): return "gamerule"
    def SPAWN_RADIUS(): return "gamerule"
    def MAX_ENTITY_CRAMMING(): return "gamerule"
    def MAX_COMMAND_CHAIN_LENGTH(): return "gamerule"
class PotionEffectType:
    def SPEED(): return "effect"
    def SLOW(): return "effect"
    def FAST_DIGGING(): return "effect"
    def SLOW_DIGGING(): return "effect"
    def INCREASE_DAMAGE(): return "effect"
    def HEAL(): return "effect"
    def HARM(): return "effect"
    def JUMP(): return "effect"
    def CONFUSION(): return "effect"
    def REGENERATION(): return "effect"
    def DAMAGE_RESISTANCE(): return "effect"
    def FIRE_RESISTANCE(): return "effect"
    def WATER_BREATHING(): return "effect"
    def INVISIBILITY(): return "effect"
    def BLINDNESS(): return "effect"
    def NIGHT_VISION(): return "effect"
    def HUNGER(): return "effect"
    def WEAKNESS(): return "effect"
    def POISON(): return "effect"
    def WITHER(): return "effect"
    def HEALTH_BOOST(): return "effect"
    def ABSORPTION(): return "effect"
    def SATURATION(): return "effect"
    def GLOWING(): return "effect"
    def LEVITATION(): return "effect"
    def LUCK(): return "effect"
    def UNLUCK(): return "effect"
    def SLOW_FALLING(): return "effect"
    def CONDUIT_POWER(): return "effect"
    def DOLPHINS_GRACE(): return "effect"
    def BAD_OMEN(): return "effect"
    def HERO_OF_THE_VILLAGE(): return "effect"
class Action:
    def __init__(self):
        self.type = "Action"
        global addition_list
        if not addition_list.__contains__('org.bukkit.event.block.Action'):
            addition_list.append('org.bukkit.event.block.Action')
        global check_list    
        check_list.append("define")
def PlayerMoveEvent(*details):
    return "PlayerMoveEvent"
def BlockBreakEvent():
    return "BlockBreakEvent"
def PlayerInteractEvent():
    return "PlayerInteractEvent"
def PlayerJoinEvent():
    return "PlayerJoinEvent"
def PlayerItemHeldEvent():
    return "PlayerItemHeldEvent"
def BlockFertilizeEvent():
    return "BlockFertilizeEvent"
def BlockExplodeEvent():
    return "BlockExplodeEvent"
def BlockCookEvent():
    return "PlayerInteractEvent"
def BlockDropItemEvent():
    return "BlockDropItemEvent"
def BlockRedstoneEvent():
    return "BlockRedstoneEvent"
def EntityDeathEvent():
    return "EntityDeathEvent"
def EntityDropItemEvent():
    return "EntityDropItemEvent"
def EntityPickupItemEvent():
    return "EntityPickupItemEvent"
def EntityTeleportEvent():
    return "EntityTeleportEvent"
def PlayerDeathEvent():
    return "PlayerDeathEvent"
def ProjectileHitEvent():
    return "ProjectileHitEvent"
def player():
    return "player"
def world():
    return "world"
def Enable():
    return "Enable"
def Disable():
    return "Disable"
class Material:
    def __init__(self):
        self.type = "Material"
        global addition_list
        if not addition_list.__contains__('org.bukkit.Material'):
            addition_list.append('org.bukkit.Material')
        global check_list    
        check_list.append("define")
    def toString(self):
        return "hello"
    def AIR(): return mt1
    def STONE(): return mt1
    def GRANITE(): return mt1
    def POLISHED_GRANITE(): return mt1
    def DIORITE(): return mt1
    def POLISHED_DIORITE(): return mt1
    def ANDESITE(): return mt1
    def POLISHED_ANDESITE(): return mt1
    def GRASS_BLOCK(): return mt1
    def DIRT(): return mt1
    def COARSE_DIRT(): return mt1
    def PODZOL(): return mt1
    def CRIMSON_NYLIUM(): return mt1
    def WARPED_NYLIUM(): return mt1
    def COBBLESTONE(): return mt1
    def OAK_PLANKS(): return mt1
    def SPRUCE_PLANKS(): return mt1
    def BIRCH_PLANKS(): return mt1
    def JUNGLE_PLANKS(): return mt1
    def ACACIA_PLANKS(): return mt1
    def DARK_OAK_PLANKS(): return mt1
    def CRIMSON_PLANKS(): return mt1
    def WARPED_PLANKS(): return mt1
    def OAK_SAPLING(): return mt1
    def SPRUCE_SAPLING(): return mt1
    def BIRCH_SAPLING(): return mt1
    def JUNGLE_SAPLING(): return mt1
    def ACACIA_SAPLING(): return mt1
    def DARK_OAK_SAPLING(): return mt1
    def BEDROCK(): return mt1
    def SAND(): return mt1
    def RED_SAND(): return mt1
    def GRAVEL(): return mt1
    def GOLD_ORE(): return mt1
    def IRON_ORE(): return mt1
    def COAL_ORE(): return mt1
    def NETHER_GOLD_ORE(): return mt1
    def OAK_LOG(): return mt1
    def SPRUCE_LOG(): return mt1
    def BIRCH_LOG(): return mt1
    def JUNGLE_LOG(): return mt1
    def ACACIA_LOG(): return mt1
    def DARK_OAK_LOG(): return mt1
    def CRIMSON_STEM(): return mt1
    def WARPED_STEM(): return mt1
    def STRIPPED_OAK_LOG(): return mt1
    def STRIPPED_SPRUCE_LOG(): return mt1
    def STRIPPED_BIRCH_LOG(): return mt1
    def STRIPPED_JUNGLE_LOG(): return mt1
    def STRIPPED_ACACIA_LOG(): return mt1
    def STRIPPED_DARK_OAK_LOG(): return mt1
    def STRIPPED_CRIMSON_STEM(): return mt1
    def STRIPPED_WARPED_STEM(): return mt1
    def STRIPPED_OAK_WOOD(): return mt1
    def STRIPPED_SPRUCE_WOOD(): return mt1
    def STRIPPED_BIRCH_WOOD(): return mt1
    def STRIPPED_JUNGLE_WOOD(): return mt1
    def STRIPPED_ACACIA_WOOD(): return mt1
    def STRIPPED_DARK_OAK_WOOD(): return mt1
    def STRIPPED_CRIMSON_HYPHAE(): return mt1
    def STRIPPED_WARPED_HYPHAE(): return mt1
    def OAK_WOOD(): return mt1
    def SPRUCE_WOOD(): return mt1
    def BIRCH_WOOD(): return mt1
    def JUNGLE_WOOD(): return mt1
    def ACACIA_WOOD(): return mt1
    def DARK_OAK_WOOD(): return mt1
    def CRIMSON_HYPHAE(): return mt1
    def WARPED_HYPHAE(): return mt1
    def OAK_LEAVES(): return mt1
    def SPRUCE_LEAVES(): return mt1
    def BIRCH_LEAVES(): return mt1
    def JUNGLE_LEAVES(): return mt1
    def ACACIA_LEAVES(): return mt1
    def DARK_OAK_LEAVES(): return mt1
    def SPONGE(): return mt1
    def WET_SPONGE(): return mt1
    def GLASS(): return mt1
    def LAPIS_ORE(): return mt1
    def LAPIS_BLOCK(): return mt1
    def DISPENSER(): return mt1
    def SANDSTONE(): return mt1
    def CHISELED_SANDSTONE(): return mt1
    def CUT_SANDSTONE(): return mt1
    def NOTE_BLOCK(): return mt1
    def POWERED_RAIL(): return mt1
    def DETECTOR_RAIL(): return mt1
    def STICKY_PISTON(): return mt1
    def COBWEB(): return mt1
    def GRASS(): return mt1
    def FERN(): return mt1
    def DEAD_BUSH(): return mt1
    def SEAGRASS(): return mt1
    def SEA_PICKLE(): return mt1
    def PISTON(): return mt1
    def WHITE_WOOL(): return mt1
    def ORANGE_WOOL(): return mt1
    def MAGENTA_WOOL(): return mt1
    def LIGHT_BLUE_WOOL(): return mt1
    def YELLOW_WOOL(): return mt1
    def LIME_WOOL(): return mt1
    def PINK_WOOL(): return mt1
    def GRAY_WOOL(): return mt1
    def LIGHT_GRAY_WOOL(): return mt1
    def CYAN_WOOL(): return mt1
    def PURPLE_WOOL(): return mt1
    def BLUE_WOOL(): return mt1
    def BROWN_WOOL(): return mt1
    def GREEN_WOOL(): return mt1
    def RED_WOOL(): return mt1
    def BLACK_WOOL(): return mt1
    def DANDELION(): return mt1
    def POPPY(): return mt1
    def BLUE_ORCHID(): return mt1
    def ALLIUM(): return mt1
    def AZURE_BLUET(): return mt1
    def RED_TULIP(): return mt1
    def ORANGE_TULIP(): return mt1
    def WHITE_TULIP(): return mt1
    def PINK_TULIP(): return mt1
    def OXEYE_DAISY(): return mt1
    def CORNFLOWER(): return mt1
    def LILY_OF_THE_VALLEY(): return mt1
    def WITHER_ROSE(): return mt1
    def BROWN_MUSHROOM(): return mt1
    def RED_MUSHROOM(): return mt1
    def CRIMSON_FUNGUS(): return mt1
    def WARPED_FUNGUS(): return mt1
    def CRIMSON_ROOTS(): return mt1
    def WARPED_ROOTS(): return mt1
    def NETHER_SPROUTS(): return mt1
    def WEEPING_VINES(): return mt1
    def TWISTING_VINES(): return mt1
    def SUGAR_CANE(): return mt1
    def KELP(): return mt1
    def BAMBOO(): return mt1
    def GOLD_BLOCK(): return mt1
    def IRON_BLOCK(): return mt1
    def OAK_SLAB(): return mt1
    def SPRUCE_SLAB(): return mt1
    def BIRCH_SLAB(): return mt1
    def JUNGLE_SLAB(): return mt1
    def ACACIA_SLAB(): return mt1
    def DARK_OAK_SLAB(): return mt1
    def CRIMSON_SLAB(): return mt1
    def WARPED_SLAB(): return mt1
    def STONE_SLAB(): return mt1
    def SMOOTH_STONE_SLAB(): return mt1
    def SANDSTONE_SLAB(): return mt1
    def CUT_SANDSTONE_SLAB(): return mt1
    def PETRIFIED_OAK_SLAB(): return mt1
    def COBBLESTONE_SLAB(): return mt1
    def BRICK_SLAB(): return mt1
    def STONE_BRICK_SLAB(): return mt1
    def NETHER_BRICK_SLAB(): return mt1
    def QUARTZ_SLAB(): return mt1
    def RED_SANDSTONE_SLAB(): return mt1
    def CUT_RED_SANDSTONE_SLAB(): return mt1
    def PURPUR_SLAB(): return mt1
    def PRISMARINE_SLAB(): return mt1
    def PRISMARINE_BRICK_SLAB(): return mt1
    def DARK_PRISMARINE_SLAB(): return mt1
    def SMOOTH_QUARTZ(): return mt1
    def SMOOTH_RED_SANDSTONE(): return mt1
    def SMOOTH_SANDSTONE(): return mt1
    def SMOOTH_STONE(): return mt1
    def BRICKS(): return mt1
    def TNT(): return mt1
    def BOOKSHELF(): return mt1
    def MOSSY_COBBLESTONE(): return mt1
    def OBSIDIAN(): return mt1
    def TORCH(): return mt1
    def END_ROD(): return mt1
    def CHORUS_PLANT(): return mt1
    def CHORUS_FLOWER(): return mt1
    def PURPUR_BLOCK(): return mt1
    def PURPUR_PILLAR(): return mt1
    def PURPUR_STAIRS(): return mt1
    def SPAWNER(): return mt1
    def OAK_STAIRS(): return mt1
    def CHEST(): return mt1
    def DIAMOND_ORE(): return mt1
    def DIAMOND_BLOCK(): return mt1
    def CRAFTING_TABLE(): return mt1
    def FARMLAND(): return mt1
    def FURNACE(): return mt1
    def LADDER(): return mt1
    def RAIL(): return mt1
    def COBBLESTONE_STAIRS(): return mt1
    def LEVER(): return mt1
    def STONE_PRESSURE_PLATE(): return mt1
    def OAK_PRESSURE_PLATE(): return mt1
    def SPRUCE_PRESSURE_PLATE(): return mt1
    def BIRCH_PRESSURE_PLATE(): return mt1
    def JUNGLE_PRESSURE_PLATE(): return mt1
    def ACACIA_PRESSURE_PLATE(): return mt1
    def DARK_OAK_PRESSURE_PLATE(): return mt1
    def CRIMSON_PRESSURE_PLATE(): return mt1
    def WARPED_PRESSURE_PLATE(): return mt1
    def POLISHED_BLACKSTONE_PRESSURE_PLATE(): return mt1
    def REDSTONE_ORE(): return mt1
    def REDSTONE_TORCH(): return mt1
    def SNOW(): return mt1
    def ICE(): return mt1
    def SNOW_BLOCK(): return mt1
    def CACTUS(): return mt1
    def CLAY(): return mt1
    def JUKEBOX(): return mt1
    def OAK_FENCE(): return mt1
    def SPRUCE_FENCE(): return mt1
    def BIRCH_FENCE(): return mt1
    def JUNGLE_FENCE(): return mt1
    def ACACIA_FENCE(): return mt1
    def DARK_OAK_FENCE(): return mt1
    def CRIMSON_FENCE(): return mt1
    def WARPED_FENCE(): return mt1
    def PUMPKIN(): return mt1
    def CARVED_PUMPKIN(): return mt1
    def NETHERRACK(): return mt1
    def SOUL_SAND(): return mt1
    def SOUL_SOIL(): return mt1
    def BASALT(): return mt1
    def POLISHED_BASALT(): return mt1
    def SOUL_TORCH(): return mt1
    def GLOWSTONE(): return mt1
    def JACK_O_LANTERN(): return mt1
    def OAK_TRAPDOOR(): return mt1
    def SPRUCE_TRAPDOOR(): return mt1
    def BIRCH_TRAPDOOR(): return mt1
    def JUNGLE_TRAPDOOR(): return mt1
    def ACACIA_TRAPDOOR(): return mt1
    def DARK_OAK_TRAPDOOR(): return mt1
    def CRIMSON_TRAPDOOR(): return mt1
    def WARPED_TRAPDOOR(): return mt1
    def INFESTED_STONE(): return mt1
    def INFESTED_COBBLESTONE(): return mt1
    def INFESTED_STONE_BRICKS(): return mt1
    def INFESTED_MOSSY_STONE_BRICKS(): return mt1
    def INFESTED_CRACKED_STONE_BRICKS(): return mt1
    def INFESTED_CHISELED_STONE_BRICKS(): return mt1
    def STONE_BRICKS(): return mt1
    def MOSSY_STONE_BRICKS(): return mt1
    def CRACKED_STONE_BRICKS(): return mt1
    def CHISELED_STONE_BRICKS(): return mt1
    def BROWN_MUSHROOM_BLOCK(): return mt1
    def RED_MUSHROOM_BLOCK(): return mt1
    def MUSHROOM_STEM(): return mt1
    def IRON_BARS(): return mt1
    def CHAIN(): return mt1
    def GLASS_PANE(): return mt1
    def MELON(): return mt1
    def VINE(): return mt1
    def OAK_FENCE_GATE(): return mt1
    def SPRUCE_FENCE_GATE(): return mt1
    def BIRCH_FENCE_GATE(): return mt1
    def JUNGLE_FENCE_GATE(): return mt1
    def ACACIA_FENCE_GATE(): return mt1
    def DARK_OAK_FENCE_GATE(): return mt1
    def CRIMSON_FENCE_GATE(): return mt1
    def WARPED_FENCE_GATE(): return mt1
    def BRICK_STAIRS(): return mt1
    def STONE_BRICK_STAIRS(): return mt1
    def MYCELIUM(): return mt1
    def LILY_PAD(): return mt1
    def NETHER_BRICKS(): return mt1
    def CRACKED_NETHER_BRICKS(): return mt1
    def CHISELED_NETHER_BRICKS(): return mt1
    def NETHER_BRICK_FENCE(): return mt1
    def NETHER_BRICK_STAIRS(): return mt1
    def ENCHANTING_TABLE(): return mt1
    def END_PORTAL_FRAME(): return mt1
    def END_STONE(): return mt1
    def END_STONE_BRICKS(): return mt1
    def DRAGON_EGG(): return mt1
    def REDSTONE_LAMP(): return mt1
    def SANDSTONE_STAIRS(): return mt1
    def EMERALD_ORE(): return mt1
    def ENDER_CHEST(): return mt1
    def TRIPWIRE_HOOK(): return mt1
    def EMERALD_BLOCK(): return mt1
    def SPRUCE_STAIRS(): return mt1
    def BIRCH_STAIRS(): return mt1
    def JUNGLE_STAIRS(): return mt1
    def CRIMSON_STAIRS(): return mt1
    def WARPED_STAIRS(): return mt1
    def COMMAND_BLOCK(): return mt1
    def BEACON(): return mt1
    def COBBLESTONE_WALL(): return mt1
    def MOSSY_COBBLESTONE_WALL(): return mt1
    def BRICK_WALL(): return mt1
    def PRISMARINE_WALL(): return mt1
    def RED_SANDSTONE_WALL(): return mt1
    def MOSSY_STONE_BRICK_WALL(): return mt1
    def GRANITE_WALL(): return mt1
    def STONE_BRICK_WALL(): return mt1
    def NETHER_BRICK_WALL(): return mt1
    def ANDESITE_WALL(): return mt1
    def RED_NETHER_BRICK_WALL(): return mt1
    def SANDSTONE_WALL(): return mt1
    def END_STONE_BRICK_WALL(): return mt1
    def DIORITE_WALL(): return mt1
    def BLACKSTONE_WALL(): return mt1
    def POLISHED_BLACKSTONE_WALL(): return mt1
    def POLISHED_BLACKSTONE_BRICK_WALL(): return mt1
    def STONE_BUTTON(): return mt1
    def OAK_BUTTON(): return mt1
    def SPRUCE_BUTTON(): return mt1
    def BIRCH_BUTTON(): return mt1
    def JUNGLE_BUTTON(): return mt1
    def ACACIA_BUTTON(): return mt1
    def DARK_OAK_BUTTON(): return mt1
    def CRIMSON_BUTTON(): return mt1
    def WARPED_BUTTON(): return mt1
    def POLISHED_BLACKSTONE_BUTTON(): return mt1
    def ANVIL(): return mt1
    def CHIPPED_ANVIL(): return mt1
    def DAMAGED_ANVIL(): return mt1
    def TRAPPED_CHEST(): return mt1
    def LIGHT_WEIGHTED_PRESSURE_PLATE(): return mt1
    def HEAVY_WEIGHTED_PRESSURE_PLATE(): return mt1
    def DAYLIGHT_DETECTOR(): return mt1
    def REDSTONE_BLOCK(): return mt1
    def NETHER_QUARTZ_ORE(): return mt1
    def HOPPER(): return mt1
    def CHISELED_QUARTZ_BLOCK(): return mt1
    def QUARTZ_BLOCK(): return mt1
    def QUARTZ_BRICKS(): return mt1
    def QUARTZ_PILLAR(): return mt1
    def QUARTZ_STAIRS(): return mt1
    def ACTIVATOR_RAIL(): return mt1
    def DROPPER(): return mt1
    def WHITE_TERRACOTTA(): return mt1
    def ORANGE_TERRACOTTA(): return mt1
    def MAGENTA_TERRACOTTA(): return mt1
    def LIGHT_BLUE_TERRACOTTA(): return mt1
    def YELLOW_TERRACOTTA(): return mt1
    def LIME_TERRACOTTA(): return mt1
    def PINK_TERRACOTTA(): return mt1
    def GRAY_TERRACOTTA(): return mt1
    def LIGHT_GRAY_TERRACOTTA(): return mt1
    def CYAN_TERRACOTTA(): return mt1
    def PURPLE_TERRACOTTA(): return mt1
    def BLUE_TERRACOTTA(): return mt1
    def BROWN_TERRACOTTA(): return mt1
    def GREEN_TERRACOTTA(): return mt1
    def RED_TERRACOTTA(): return mt1
    def BLACK_TERRACOTTA(): return mt1
    def BARRIER(): return mt1
    def IRON_TRAPDOOR(): return mt1
    def HAY_BLOCK(): return mt1
    def WHITE_CARPET(): return mt1
    def ORANGE_CARPET(): return mt1
    def MAGENTA_CARPET(): return mt1
    def LIGHT_BLUE_CARPET(): return mt1
    def YELLOW_CARPET(): return mt1
    def LIME_CARPET(): return mt1
    def PINK_CARPET(): return mt1
    def GRAY_CARPET(): return mt1
    def LIGHT_GRAY_CARPET(): return mt1
    def CYAN_CARPET(): return mt1
    def PURPLE_CARPET(): return mt1
    def BLUE_CARPET(): return mt1
    def BROWN_CARPET(): return mt1
    def GREEN_CARPET(): return mt1
    def RED_CARPET(): return mt1
    def BLACK_CARPET(): return mt1
    def TERRACOTTA(): return mt1
    def COAL_BLOCK(): return mt1
    def PACKED_ICE(): return mt1
    def ACACIA_STAIRS(): return mt1
    def DARK_OAK_STAIRS(): return mt1
    def SLIME_BLOCK(): return mt1
    def GRASS_PATH(): return mt1
    def SUNFLOWER(): return mt1
    def LILAC(): return mt1
    def ROSE_BUSH(): return mt1
    def PEONY(): return mt1
    def TALL_GRASS(): return mt1
    def LARGE_FERN(): return mt1
    def WHITE_STAINED_GLASS(): return mt1
    def ORANGE_STAINED_GLASS(): return mt1
    def MAGENTA_STAINED_GLASS(): return mt1
    def LIGHT_BLUE_STAINED_GLASS(): return mt1
    def YELLOW_STAINED_GLASS(): return mt1
    def LIME_STAINED_GLASS(): return mt1
    def PINK_STAINED_GLASS(): return mt1
    def GRAY_STAINED_GLASS(): return mt1
    def LIGHT_GRAY_STAINED_GLASS(): return mt1
    def CYAN_STAINED_GLASS(): return mt1
    def PURPLE_STAINED_GLASS(): return mt1
    def BLUE_STAINED_GLASS(): return mt1
    def BROWN_STAINED_GLASS(): return mt1
    def GREEN_STAINED_GLASS(): return mt1
    def RED_STAINED_GLASS(): return mt1
    def BLACK_STAINED_GLASS(): return mt1
    def WHITE_STAINED_GLASS_PANE(): return mt1
    def ORANGE_STAINED_GLASS_PANE(): return mt1
    def MAGENTA_STAINED_GLASS_PANE(): return mt1
    def LIGHT_BLUE_STAINED_GLASS_PANE(): return mt1
    def YELLOW_STAINED_GLASS_PANE(): return mt1
    def LIME_STAINED_GLASS_PANE(): return mt1
    def PINK_STAINED_GLASS_PANE(): return mt1
    def GRAY_STAINED_GLASS_PANE(): return mt1
    def LIGHT_GRAY_STAINED_GLASS_PANE(): return mt1
    def CYAN_STAINED_GLASS_PANE(): return mt1
    def PURPLE_STAINED_GLASS_PANE(): return mt1
    def BLUE_STAINED_GLASS_PANE(): return mt1
    def BROWN_STAINED_GLASS_PANE(): return mt1
    def GREEN_STAINED_GLASS_PANE(): return mt1
    def RED_STAINED_GLASS_PANE(): return mt1
    def BLACK_STAINED_GLASS_PANE(): return mt1
    def PRISMARINE(): return mt1
    def PRISMARINE_BRICKS(): return mt1
    def DARK_PRISMARINE(): return mt1
    def PRISMARINE_STAIRS(): return mt1
    def PRISMARINE_BRICK_STAIRS(): return mt1
    def DARK_PRISMARINE_STAIRS(): return mt1
    def SEA_LANTERN(): return mt1
    def RED_SANDSTONE(): return mt1
    def CHISELED_RED_SANDSTONE(): return mt1
    def CUT_RED_SANDSTONE(): return mt1
    def RED_SANDSTONE_STAIRS(): return mt1
    def REPEATING_COMMAND_BLOCK(): return mt1
    def CHAIN_COMMAND_BLOCK(): return mt1
    def MAGMA_BLOCK(): return mt1
    def NETHER_WART_BLOCK(): return mt1
    def WARPED_WART_BLOCK(): return mt1
    def RED_NETHER_BRICKS(): return mt1
    def BONE_BLOCK(): return mt1
    def STRUCTURE_VOID(): return mt1
    def OBSERVER(): return mt1
    def SHULKER_BOX(): return mt1
    def WHITE_SHULKER_BOX(): return mt1
    def ORANGE_SHULKER_BOX(): return mt1
    def MAGENTA_SHULKER_BOX(): return mt1
    def LIGHT_BLUE_SHULKER_BOX(): return mt1
    def YELLOW_SHULKER_BOX(): return mt1
    def LIME_SHULKER_BOX(): return mt1
    def PINK_SHULKER_BOX(): return mt1
    def GRAY_SHULKER_BOX(): return mt1
    def LIGHT_GRAY_SHULKER_BOX(): return mt1
    def CYAN_SHULKER_BOX(): return mt1
    def PURPLE_SHULKER_BOX(): return mt1
    def BLUE_SHULKER_BOX(): return mt1
    def BROWN_SHULKER_BOX(): return mt1
    def GREEN_SHULKER_BOX(): return mt1
    def RED_SHULKER_BOX(): return mt1
    def BLACK_SHULKER_BOX(): return mt1
    def WHITE_GLAZED_TERRACOTTA(): return mt1
    def ORANGE_GLAZED_TERRACOTTA(): return mt1
    def MAGENTA_GLAZED_TERRACOTTA(): return mt1
    def LIGHT_BLUE_GLAZED_TERRACOTTA(): return mt1
    def YELLOW_GLAZED_TERRACOTTA(): return mt1
    def LIME_GLAZED_TERRACOTTA(): return mt1
    def PINK_GLAZED_TERRACOTTA(): return mt1
    def GRAY_GLAZED_TERRACOTTA(): return mt1
    def LIGHT_GRAY_GLAZED_TERRACOTTA(): return mt1
    def CYAN_GLAZED_TERRACOTTA(): return mt1
    def PURPLE_GLAZED_TERRACOTTA(): return mt1
    def BLUE_GLAZED_TERRACOTTA(): return mt1
    def BROWN_GLAZED_TERRACOTTA(): return mt1
    def GREEN_GLAZED_TERRACOTTA(): return mt1
    def RED_GLAZED_TERRACOTTA(): return mt1
    def BLACK_GLAZED_TERRACOTTA(): return mt1
    def WHITE_CONCRETE(): return mt1
    def ORANGE_CONCRETE(): return mt1
    def MAGENTA_CONCRETE(): return mt1
    def LIGHT_BLUE_CONCRETE(): return mt1
    def YELLOW_CONCRETE(): return mt1
    def LIME_CONCRETE(): return mt1
    def PINK_CONCRETE(): return mt1
    def GRAY_CONCRETE(): return mt1
    def LIGHT_GRAY_CONCRETE(): return mt1
    def CYAN_CONCRETE(): return mt1
    def PURPLE_CONCRETE(): return mt1
    def BLUE_CONCRETE(): return mt1
    def BROWN_CONCRETE(): return mt1
    def GREEN_CONCRETE(): return mt1
    def RED_CONCRETE(): return mt1
    def BLACK_CONCRETE(): return mt1
    def WHITE_CONCRETE_POWDER(): return mt1
    def ORANGE_CONCRETE_POWDER(): return mt1
    def MAGENTA_CONCRETE_POWDER(): return mt1
    def LIGHT_BLUE_CONCRETE_POWDER(): return mt1
    def YELLOW_CONCRETE_POWDER(): return mt1
    def LIME_CONCRETE_POWDER(): return mt1
    def PINK_CONCRETE_POWDER(): return mt1
    def GRAY_CONCRETE_POWDER(): return mt1
    def LIGHT_GRAY_CONCRETE_POWDER(): return mt1
    def CYAN_CONCRETE_POWDER(): return mt1
    def PURPLE_CONCRETE_POWDER(): return mt1
    def BLUE_CONCRETE_POWDER(): return mt1
    def BROWN_CONCRETE_POWDER(): return mt1
    def GREEN_CONCRETE_POWDER(): return mt1
    def RED_CONCRETE_POWDER(): return mt1
    def BLACK_CONCRETE_POWDER(): return mt1
    def TURTLE_EGG(): return mt1
    def DEAD_TUBE_CORAL_BLOCK(): return mt1
    def DEAD_BRAIN_CORAL_BLOCK(): return mt1
    def DEAD_BUBBLE_CORAL_BLOCK(): return mt1
    def DEAD_FIRE_CORAL_BLOCK(): return mt1
    def DEAD_HORN_CORAL_BLOCK(): return mt1
    def TUBE_CORAL_BLOCK(): return mt1
    def BRAIN_CORAL_BLOCK(): return mt1
    def BUBBLE_CORAL_BLOCK(): return mt1
    def FIRE_CORAL_BLOCK(): return mt1
    def HORN_CORAL_BLOCK(): return mt1
    def TUBE_CORAL(): return mt1
    def BRAIN_CORAL(): return mt1
    def BUBBLE_CORAL(): return mt1
    def FIRE_CORAL(): return mt1
    def HORN_CORAL(): return mt1
    def DEAD_BRAIN_CORAL(): return mt1
    def DEAD_BUBBLE_CORAL(): return mt1
    def DEAD_FIRE_CORAL(): return mt1
    def DEAD_HORN_CORAL(): return mt1
    def DEAD_TUBE_CORAL(): return mt1
    def TUBE_CORAL_FAN(): return mt1
    def BRAIN_CORAL_FAN(): return mt1
    def BUBBLE_CORAL_FAN(): return mt1
    def FIRE_CORAL_FAN(): return mt1
    def HORN_CORAL_FAN(): return mt1
    def DEAD_TUBE_CORAL_FAN(): return mt1
    def DEAD_BRAIN_CORAL_FAN(): return mt1
    def DEAD_BUBBLE_CORAL_FAN(): return mt1
    def DEAD_FIRE_CORAL_FAN(): return mt1
    def DEAD_HORN_CORAL_FAN(): return mt1
    def BLUE_ICE(): return mt1
    def CONDUIT(): return mt1
    def POLISHED_GRANITE_STAIRS(): return mt1
    def SMOOTH_RED_SANDSTONE_STAIRS(): return mt1
    def MOSSY_STONE_BRICK_STAIRS(): return mt1
    def POLISHED_DIORITE_STAIRS(): return mt1
    def MOSSY_COBBLESTONE_STAIRS(): return mt1
    def END_STONE_BRICK_STAIRS(): return mt1
    def STONE_STAIRS(): return mt1
    def SMOOTH_SANDSTONE_STAIRS(): return mt1
    def SMOOTH_QUARTZ_STAIRS(): return mt1
    def GRANITE_STAIRS(): return mt1
    def ANDESITE_STAIRS(): return mt1
    def RED_NETHER_BRICK_STAIRS(): return mt1
    def POLISHED_ANDESITE_STAIRS(): return mt1
    def DIORITE_STAIRS(): return mt1
    def POLISHED_GRANITE_SLAB(): return mt1
    def SMOOTH_RED_SANDSTONE_SLAB(): return mt1
    def MOSSY_STONE_BRICK_SLAB(): return mt1
    def POLISHED_DIORITE_SLAB(): return mt1
    def MOSSY_COBBLESTONE_SLAB(): return mt1
    def END_STONE_BRICK_SLAB(): return mt1
    def SMOOTH_SANDSTONE_SLAB(): return mt1
    def SMOOTH_QUARTZ_SLAB(): return mt1
    def GRANITE_SLAB(): return mt1
    def ANDESITE_SLAB(): return mt1
    def RED_NETHER_BRICK_SLAB(): return mt1
    def POLISHED_ANDESITE_SLAB(): return mt1
    def DIORITE_SLAB(): return mt1
    def SCAFFOLDING(): return mt1
    def IRON_DOOR(): return mt1
    def OAK_DOOR(): return mt1
    def SPRUCE_DOOR(): return mt1
    def BIRCH_DOOR(): return mt1
    def JUNGLE_DOOR(): return mt1
    def ACACIA_DOOR(): return mt1
    def DARK_OAK_DOOR(): return mt1
    def CRIMSON_DOOR(): return mt1
    def WARPED_DOOR(): return mt1
    def REPEATER(): return mt1
    def COMPARATOR(): return mt1
    def STRUCTURE_BLOCK(): return mt1
    def JIGSAW(): return mt1
    def TURTLE_HELMET(): return mt1
    def SCUTE(): return mt1
    def FLINT_AND_STEEL(): return mt1
    def APPLE(): return mt1
    def BOW(): return mt1
    def ARROW(): return mt1
    def COAL(): return mt1
    def CHARCOAL(): return mt1
    def DIAMOND(): return mt1
    def IRON_INGOT(): return mt1
    def GOLD_INGOT(): return mt1
    def NETHERITE_INGOT(): return mt1
    def NETHERITE_SCRAP(): return mt1
    def WOODEN_SWORD(): return mt1
    def WOODEN_SHOVEL(): return mt1
    def WOODEN_PICKAXE(): return mt1
    def WOODEN_AXE(): return mt1
    def WOODEN_HOE(): return mt1
    def STONE_SWORD(): return mt1
    def STONE_SHOVEL(): return mt1
    def STONE_PICKAXE(): return mt1
    def STONE_AXE(): return mt1
    def STONE_HOE(): return mt1
    def GOLDEN_SWORD(): return mt1
    def GOLDEN_SHOVEL(): return mt1
    def GOLDEN_PICKAXE(): return mt1
    def GOLDEN_AXE(): return mt1
    def GOLDEN_HOE(): return mt1
    def IRON_SWORD(): return mt1
    def IRON_SHOVEL(): return mt1
    def IRON_PICKAXE(): return mt1
    def IRON_AXE(): return mt1
    def IRON_HOE(): return mt1
    def DIAMOND_SWORD(): return mt1
    def DIAMOND_SHOVEL(): return mt1
    def DIAMOND_PICKAXE(): return mt1
    def DIAMOND_AXE(): return mt1
    def DIAMOND_HOE(): return mt1
    def NETHERITE_SWORD(): return mt1
    def NETHERITE_SHOVEL(): return mt1
    def NETHERITE_PICKAXE(): return mt1
    def NETHERITE_AXE(): return mt1
    def NETHERITE_HOE(): return mt1
    def STICK(): return mt1
    def BOWL(): return mt1
    def MUSHROOM_STEW(): return mt1
    def STRING(): return mt1
    def FEATHER(): return mt1
    def GUNPOWDER(): return mt1
    def WHEAT_SEEDS(): return mt1
    def WHEAT(): return mt1
    def BREAD(): return mt1
    def LEATHER_HELMET(): return mt1
    def LEATHER_CHESTPLATE(): return mt1
    def LEATHER_LEGGINGS(): return mt1
    def LEATHER_BOOTS(): return mt1
    def CHAINMAIL_HELMET(): return mt1
    def CHAINMAIL_CHESTPLATE(): return mt1
    def CHAINMAIL_LEGGINGS(): return mt1
    def CHAINMAIL_BOOTS(): return mt1
    def IRON_HELMET(): return mt1
    def IRON_CHESTPLATE(): return mt1
    def IRON_LEGGINGS(): return mt1
    def IRON_BOOTS(): return mt1
    def DIAMOND_HELMET(): return mt1
    def DIAMOND_CHESTPLATE(): return mt1
    def DIAMOND_LEGGINGS(): return mt1
    def DIAMOND_BOOTS(): return mt1
    def GOLDEN_HELMET(): return mt1
    def GOLDEN_CHESTPLATE(): return mt1
    def GOLDEN_LEGGINGS(): return mt1
    def GOLDEN_BOOTS(): return mt1
    def NETHERITE_HELMET(): return mt1
    def NETHERITE_CHESTPLATE(): return mt1
    def NETHERITE_LEGGINGS(): return mt1
    def NETHERITE_BOOTS(): return mt1
    def FLINT(): return mt1
    def PORKCHOP(): return mt1
    def COOKED_PORKCHOP(): return mt1
    def PAINTING(): return mt1
    def GOLDEN_APPLE(): return mt1
    def ENCHANTED_GOLDEN_APPLE(): return mt1
    def OAK_SIGN(): return mt1
    def SPRUCE_SIGN(): return mt1
    def BIRCH_SIGN(): return mt1
    def JUNGLE_SIGN(): return mt1
    def ACACIA_SIGN(): return mt1
    def DARK_OAK_SIGN(): return mt1
    def CRIMSON_SIGN(): return mt1
    def WARPED_SIGN(): return mt1
    def BUCKET(): return mt1
    def WATER_BUCKET(): return mt1
    def LAVA_BUCKET(): return mt1
    def MINECART(): return mt1
    def SADDLE(): return mt1
    def REDSTONE(): return mt1
    def SNOWBALL(): return mt1
    def OAK_BOAT(): return mt1
    def LEATHER(): return mt1
    def MILK_BUCKET(): return mt1
    def PUFFERFISH_BUCKET(): return mt1
    def SALMON_BUCKET(): return mt1
    def COD_BUCKET(): return mt1
    def TROPICAL_FISH_BUCKET(): return mt1
    def BRICK(): return mt1
    def CLAY_BALL(): return mt1
    def DRIED_KELP_BLOCK(): return mt1
    def PAPER(): return mt1
    def BOOK(): return mt1
    def SLIME_BALL(): return mt1
    def CHEST_MINECART(): return mt1
    def FURNACE_MINECART(): return mt1
    def EGG(): return mt1
    def COMPASS(): return mt1
    def FISHING_ROD(): return mt1
    def CLOCK(): return mt1
    def GLOWSTONE_DUST(): return mt1
    def COD(): return mt1
    def SALMON(): return mt1
    def TROPICAL_FISH(): return mt1
    def PUFFERFISH(): return mt1
    def COOKED_COD(): return mt1
    def COOKED_SALMON(): return mt1
    def INK_SAC(): return mt1
    def COCOA_BEANS(): return mt1
    def LAPIS_LAZULI(): return mt1
    def WHITE_DYE(): return mt1
    def ORANGE_DYE(): return mt1
    def MAGENTA_DYE(): return mt1
    def LIGHT_BLUE_DYE(): return mt1
    def YELLOW_DYE(): return mt1
    def LIME_DYE(): return mt1
    def PINK_DYE(): return mt1
    def GRAY_DYE(): return mt1
    def LIGHT_GRAY_DYE(): return mt1
    def CYAN_DYE(): return mt1
    def PURPLE_DYE(): return mt1
    def BLUE_DYE(): return mt1
    def BROWN_DYE(): return mt1
    def GREEN_DYE(): return mt1
    def RED_DYE(): return mt1
    def BLACK_DYE(): return mt1
    def BONE_MEAL(): return mt1
    def BONE(): return mt1
    def SUGAR(): return mt1
    def CAKE(): return mt1
    def WHITE_BED(): return mt1
    def ORANGE_BED(): return mt1
    def MAGENTA_BED(): return mt1
    def LIGHT_BLUE_BED(): return mt1
    def YELLOW_BED(): return mt1
    def LIME_BED(): return mt1
    def PINK_BED(): return mt1
    def GRAY_BED(): return mt1
    def LIGHT_GRAY_BED(): return mt1
    def CYAN_BED(): return mt1
    def PURPLE_BED(): return mt1
    def BLUE_BED(): return mt1
    def BROWN_BED(): return mt1
    def GREEN_BED(): return mt1
    def RED_BED(): return mt1
    def BLACK_BED(): return mt1
    def COOKIE(): return mt1
    def FILLED_MAP(): return mt1
    def SHEARS(): return mt1
    def MELON_SLICE(): return mt1
    def DRIED_KELP(): return mt1
    def PUMPKIN_SEEDS(): return mt1
    def MELON_SEEDS(): return mt1
    def BEEF(): return mt1
    def COOKED_BEEF(): return mt1
    def CHICKEN(): return mt1
    def COOKED_CHICKEN(): return mt1
    def ROTTEN_FLESH(): return mt1
    def ENDER_PEARL(): return mt1
    def BLAZE_ROD(): return mt1
    def GHAST_TEAR(): return mt1
    def GOLD_NUGGET(): return mt1
    def NETHER_WART(): return mt1
    def POTION(): return mt1
    def GLASS_BOTTLE(): return mt1
    def SPIDER_EYE(): return mt1
    def FERMENTED_SPIDER_EYE(): return mt1
    def BLAZE_POWDER(): return mt1
    def MAGMA_CREAM(): return mt1
    def BREWING_STAND(): return mt1
    def CAULDRON(): return mt1
    def ENDER_EYE(): return mt1
    def GLISTERING_MELON_SLICE(): return mt1
    def BAT_SPAWN_EGG(): return mt1
    def BEE_SPAWN_EGG(): return mt1
    def BLAZE_SPAWN_EGG(): return mt1
    def CAT_SPAWN_EGG(): return mt1
    def CAVE_SPIDER_SPAWN_EGG(): return mt1
    def CHICKEN_SPAWN_EGG(): return mt1
    def COD_SPAWN_EGG(): return mt1
    def COW_SPAWN_EGG(): return mt1
    def CREEPER_SPAWN_EGG(): return mt1
    def DOLPHIN_SPAWN_EGG(): return mt1
    def DONKEY_SPAWN_EGG(): return mt1
    def DROWNED_SPAWN_EGG(): return mt1
    def ELDER_GUARDIAN_SPAWN_EGG(): return mt1
    def ENDERMAN_SPAWN_EGG(): return mt1
    def ENDERMITE_SPAWN_EGG(): return mt1
    def EVOKER_SPAWN_EGG(): return mt1
    def FOX_SPAWN_EGG(): return mt1
    def GHAST_SPAWN_EGG(): return mt1
    def GUARDIAN_SPAWN_EGG(): return mt1
    def HOGLIN_SPAWN_EGG(): return mt1
    def HORSE_SPAWN_EGG(): return mt1
    def HUSK_SPAWN_EGG(): return mt1
    def LLAMA_SPAWN_EGG(): return mt1
    def MAGMA_CUBE_SPAWN_EGG(): return mt1
    def MOOSHROOM_SPAWN_EGG(): return mt1
    def MULE_SPAWN_EGG(): return mt1
    def OCELOT_SPAWN_EGG(): return mt1
    def PANDA_SPAWN_EGG(): return mt1
    def PARROT_SPAWN_EGG(): return mt1
    def PHANTOM_SPAWN_EGG(): return mt1
    def PIG_SPAWN_EGG(): return mt1
    def PIGLIN_SPAWN_EGG(): return mt1
    def PIGLIN_BRUTE_SPAWN_EGG(): return mt1
    def PILLAGER_SPAWN_EGG(): return mt1
    def POLAR_BEAR_SPAWN_EGG(): return mt1
    def PUFFERFISH_SPAWN_EGG(): return mt1
    def RABBIT_SPAWN_EGG(): return mt1
    def RAVAGER_SPAWN_EGG(): return mt1
    def SALMON_SPAWN_EGG(): return mt1
    def SHEEP_SPAWN_EGG(): return mt1
    def SHULKER_SPAWN_EGG(): return mt1
    def SILVERFISH_SPAWN_EGG(): return mt1
    def SKELETON_SPAWN_EGG(): return mt1
    def SKELETON_HORSE_SPAWN_EGG(): return mt1
    def SLIME_SPAWN_EGG(): return mt1
    def SPIDER_SPAWN_EGG(): return mt1
    def SQUID_SPAWN_EGG(): return mt1
    def STRAY_SPAWN_EGG(): return mt1
    def STRIDER_SPAWN_EGG(): return mt1
    def TRADER_LLAMA_SPAWN_EGG(): return mt1
    def TROPICAL_FISH_SPAWN_EGG(): return mt1
    def TURTLE_SPAWN_EGG(): return mt1
    def VEX_SPAWN_EGG(): return mt1
    def VILLAGER_SPAWN_EGG(): return mt1
    def VINDICATOR_SPAWN_EGG(): return mt1
    def WANDERING_TRADER_SPAWN_EGG(): return mt1
    def WITCH_SPAWN_EGG(): return mt1
    def WITHER_SKELETON_SPAWN_EGG(): return mt1
    def WOLF_SPAWN_EGG(): return mt1
    def ZOGLIN_SPAWN_EGG(): return mt1
    def ZOMBIE_SPAWN_EGG(): return mt1
    def ZOMBIE_HORSE_SPAWN_EGG(): return mt1
    def ZOMBIE_VILLAGER_SPAWN_EGG(): return mt1
    def ZOMBIFIED_PIGLIN_SPAWN_EGG(): return mt1
    def EXPERIENCE_BOTTLE(): return mt1
    def FIRE_CHARGE(): return mt1
    def WRITABLE_BOOK(): return mt1
    def WRITTEN_BOOK(): return mt1
    def EMERALD(): return mt1
    def ITEM_FRAME(): return mt1
    def FLOWER_POT(): return mt1
    def CARROT(): return mt1
    def POTATO(): return mt1
    def BAKED_POTATO(): return mt1
    def POISONOUS_POTATO(): return mt1
    def MAP(): return mt1
    def GOLDEN_CARROT(): return mt1
    def SKELETON_SKULL(): return mt1
    def WITHER_SKELETON_SKULL(): return mt1
    def PLAYER_HEAD(): return mt1
    def ZOMBIE_HEAD(): return mt1
    def CREEPER_HEAD(): return mt1
    def DRAGON_HEAD(): return mt1
    def CARROT_ON_A_STICK(): return mt1
    def WARPED_FUNGUS_ON_A_STICK(): return mt1
    def NETHER_STAR(): return mt1
    def PUMPKIN_PIE(): return mt1
    def FIREWORK_ROCKET(): return mt1
    def FIREWORK_STAR(): return mt1
    def ENCHANTED_BOOK(): return mt1
    def NETHER_BRICK(): return mt1
    def QUARTZ(): return mt1
    def TNT_MINECART(): return mt1
    def HOPPER_MINECART(): return mt1
    def PRISMARINE_SHARD(): return mt1
    def PRISMARINE_CRYSTALS(): return mt1
    def RABBIT(): return mt1
    def COOKED_RABBIT(): return mt1
    def RABBIT_STEW(): return mt1
    def RABBIT_FOOT(): return mt1
    def RABBIT_HIDE(): return mt1
    def ARMOR_STAND(): return mt1
    def IRON_HORSE_ARMOR(): return mt1
    def GOLDEN_HORSE_ARMOR(): return mt1
    def DIAMOND_HORSE_ARMOR(): return mt1
    def LEATHER_HORSE_ARMOR(): return mt1
    def LEAD(): return mt1
    def NAME_TAG(): return mt1
    def COMMAND_BLOCK_MINECART(): return mt1
    def MUTTON(): return mt1
    def COOKED_MUTTON(): return mt1
    def WHITE_BANNER(): return mt1
    def ORANGE_BANNER(): return mt1
    def MAGENTA_BANNER(): return mt1
    def LIGHT_BLUE_BANNER(): return mt1
    def YELLOW_BANNER(): return mt1
    def LIME_BANNER(): return mt1
    def PINK_BANNER(): return mt1
    def GRAY_BANNER(): return mt1
    def LIGHT_GRAY_BANNER(): return mt1
    def CYAN_BANNER(): return mt1
    def PURPLE_BANNER(): return mt1
    def BLUE_BANNER(): return mt1
    def BROWN_BANNER(): return mt1
    def GREEN_BANNER(): return mt1
    def RED_BANNER(): return mt1
    def BLACK_BANNER(): return mt1
    def END_CRYSTAL(): return mt1
    def CHORUS_FRUIT(): return mt1
    def POPPED_CHORUS_FRUIT(): return mt1
    def BEETROOT(): return mt1
    def BEETROOT_SEEDS(): return mt1
    def BEETROOT_SOUP(): return mt1
    def DRAGON_BREATH(): return mt1
    def SPLASH_POTION(): return mt1
    def SPECTRAL_ARROW(): return mt1
    def TIPPED_ARROW(): return mt1
    def LINGERING_POTION(): return mt1
    def SHIELD(): return mt1
    def ELYTRA(): return mt1
    def SPRUCE_BOAT(): return mt1
    def BIRCH_BOAT(): return mt1
    def JUNGLE_BOAT(): return mt1
    def ACACIA_BOAT(): return mt1
    def DARK_OAK_BOAT(): return mt1
    def TOTEM_OF_UNDYING(): return mt1
    def SHULKER_SHELL(): return mt1
    def IRON_NUGGET(): return mt1
    def KNOWLEDGE_BOOK(): return mt1
    def DEBUG_STICK(): return mt1
    def MUSIC_DISC_13(): return mt1
    def MUSIC_DISC_CAT(): return mt1
    def MUSIC_DISC_BLOCKS(): return mt1
    def MUSIC_DISC_CHIRP(): return mt1
    def MUSIC_DISC_FAR(): return mt1
    def MUSIC_DISC_MALL(): return mt1
    def MUSIC_DISC_MELLOHI(): return mt1
    def MUSIC_DISC_STAL(): return mt1
    def MUSIC_DISC_STRAD(): return mt1
    def MUSIC_DISC_WARD(): return mt1
    def MUSIC_DISC_11(): return mt1
    def MUSIC_DISC_WAIT(): return mt1
    def MUSIC_DISC_PIGSTEP(): return mt1
    def TRIDENT(): return mt1
    def PHANTOM_MEMBRANE(): return mt1
    def NAUTILUS_SHELL(): return mt1
    def HEART_OF_THE_SEA(): return mt1
    def CROSSBOW(): return mt1
    def SUSPICIOUS_STEW(): return mt1
    def LOOM(): return mt1
    def FLOWER_BANNER_PATTERN(): return mt1
    def CREEPER_BANNER_PATTERN(): return mt1
    def SKULL_BANNER_PATTERN(): return mt1
    def MOJANG_BANNER_PATTERN(): return mt1
    def GLOBE_BANNER_PATTERN(): return mt1
    def PIGLIN_BANNER_PATTERN(): return mt1
    def COMPOSTER(): return mt1
    def BARREL(): return mt1
    def SMOKER(): return mt1
    def BLAST_FURNACE(): return mt1
    def CARTOGRAPHY_TABLE(): return mt1
    def FLETCHING_TABLE(): return mt1
    def GRINDSTONE(): return mt1
    def LECTERN(): return mt1
    def SMITHING_TABLE(): return mt1
    def STONECUTTER(): return mt1
    def BELL(): return mt1
    def LANTERN(): return mt1
    def SOUL_LANTERN(): return mt1
    def SWEET_BERRIES(): return mt1
    def CAMPFIRE(): return mt1
    def SOUL_CAMPFIRE(): return mt1
    def SHROOMLIGHT(): return mt1
    def HONEYCOMB(): return mt1
    def BEE_NEST(): return mt1
    def BEEHIVE(): return mt1
    def HONEY_BOTTLE(): return mt1
    def HONEY_BLOCK(): return mt1
    def HONEYCOMB_BLOCK(): return mt1
    def LODESTONE(): return mt1
    def NETHERITE_BLOCK(): return mt1
    def ANCIENT_DEBRIS(): return mt1
    def TARGET(): return mt1
    def CRYING_OBSIDIAN(): return mt1
    def BLACKSTONE(): return mt1
    def BLACKSTONE_SLAB(): return mt1
    def BLACKSTONE_STAIRS(): return mt1
    def GILDED_BLACKSTONE(): return mt1
    def POLISHED_BLACKSTONE(): return mt1
    def POLISHED_BLACKSTONE_SLAB(): return mt1
    def POLISHED_BLACKSTONE_STAIRS(): return mt1
    def CHISELED_POLISHED_BLACKSTONE(): return mt1
    def POLISHED_BLACKSTONE_BRICKS(): return mt1
    def POLISHED_BLACKSTONE_BRICK_SLAB(): return mt1
    def POLISHED_BLACKSTONE_BRICK_STAIRS(): return mt1
    def CRACKED_POLISHED_BLACKSTONE_BRICKS(): return mt1
    def RESPAWN_ANCHOR(): return mt1
    def WATER(): return mt1
    def LAVA(): return mt1
    def TALL_SEAGRASS(): return mt1
    def PISTON_HEAD(): return mt1
    def MOVING_PISTON(): return mt1
    def WALL_TORCH(): return mt1
    def FIRE(): return mt1
    def SOUL_FIRE(): return mt1
    def REDSTONE_WIRE(): return mt1
    def OAK_WALL_SIGN(): return mt1
    def SPRUCE_WALL_SIGN(): return mt1
    def BIRCH_WALL_SIGN(): return mt1
    def ACACIA_WALL_SIGN(): return mt1
    def JUNGLE_WALL_SIGN(): return mt1
    def DARK_OAK_WALL_SIGN(): return mt1
    def REDSTONE_WALL_TORCH(): return mt1
    def SOUL_WALL_TORCH(): return mt1
    def NETHER_PORTAL(): return mt1
    def ATTACHED_PUMPKIN_STEM(): return mt1
    def ATTACHED_MELON_STEM(): return mt1
    def PUMPKIN_STEM(): return mt1
    def MELON_STEM(): return mt1
    def END_PORTAL(): return mt1
    def COCOA(): return mt1
    def TRIPWIRE(): return mt1
    def POTTED_OAK_SAPLING(): return mt1
    def POTTED_SPRUCE_SAPLING(): return mt1
    def POTTED_BIRCH_SAPLING(): return mt1
    def POTTED_JUNGLE_SAPLING(): return mt1
    def POTTED_ACACIA_SAPLING(): return mt1
    def POTTED_DARK_OAK_SAPLING(): return mt1
    def POTTED_FERN(): return mt1
    def POTTED_DANDELION(): return mt1
    def POTTED_POPPY(): return mt1
    def POTTED_BLUE_ORCHID(): return mt1
    def POTTED_ALLIUM(): return mt1
    def POTTED_AZURE_BLUET(): return mt1
    def POTTED_RED_TULIP(): return mt1
    def POTTED_ORANGE_TULIP(): return mt1
    def POTTED_WHITE_TULIP(): return mt1
    def POTTED_PINK_TULIP(): return mt1
    def POTTED_OXEYE_DAISY(): return mt1
    def POTTED_CORNFLOWER(): return mt1
    def POTTED_LILY_OF_THE_VALLEY(): return mt1
    def POTTED_WITHER_ROSE(): return mt1
    def POTTED_RED_MUSHROOM(): return mt1
    def POTTED_BROWN_MUSHROOM(): return mt1
    def POTTED_DEAD_BUSH(): return mt1
    def POTTED_CACTUS(): return mt1
    def CARROTS(): return mt1
    def POTATOES(): return mt1
    def SKELETON_WALL_SKULL(): return mt1
    def WITHER_SKELETON_WALL_SKULL(): return mt1
    def ZOMBIE_WALL_HEAD(): return mt1
    def PLAYER_WALL_HEAD(): return mt1
    def CREEPER_WALL_HEAD(): return mt1
    def DRAGON_WALL_HEAD(): return mt1
    def WHITE_WALL_BANNER(): return mt1
    def ORANGE_WALL_BANNER(): return mt1
    def MAGENTA_WALL_BANNER(): return mt1
    def LIGHT_BLUE_WALL_BANNER(): return mt1
    def YELLOW_WALL_BANNER(): return mt1
    def LIME_WALL_BANNER(): return mt1
    def PINK_WALL_BANNER(): return mt1
    def GRAY_WALL_BANNER(): return mt1
    def LIGHT_GRAY_WALL_BANNER(): return mt1
    def CYAN_WALL_BANNER(): return mt1
    def PURPLE_WALL_BANNER(): return mt1
    def BLUE_WALL_BANNER(): return mt1
    def BROWN_WALL_BANNER(): return mt1
    def GREEN_WALL_BANNER(): return mt1
    def RED_WALL_BANNER(): return mt1
    def BLACK_WALL_BANNER(): return mt1
    def BEETROOTS(): return mt1
    def END_GATEWAY(): return mt1
    def FROSTED_ICE(): return mt1
    def KELP_PLANT(): return mt1
    def DEAD_TUBE_CORAL_WALL_FAN(): return mt1
    def DEAD_BRAIN_CORAL_WALL_FAN(): return mt1
    def DEAD_BUBBLE_CORAL_WALL_FAN(): return mt1
    def DEAD_FIRE_CORAL_WALL_FAN(): return mt1
    def DEAD_HORN_CORAL_WALL_FAN(): return mt1
    def TUBE_CORAL_WALL_FAN(): return mt1
    def BRAIN_CORAL_WALL_FAN(): return mt1
    def BUBBLE_CORAL_WALL_FAN(): return mt1
    def FIRE_CORAL_WALL_FAN(): return mt1
    def HORN_CORAL_WALL_FAN(): return mt1
    def BAMBOO_SAPLING(): return mt1
    def POTTED_BAMBOO(): return mt1
    def VOID_AIR(): return mt1
    def CAVE_AIR(): return mt1
    def BUBBLE_COLUMN(): return mt1
    def SWEET_BERRY_BUSH(): return mt1
    def WEEPING_VINES_PLANT(): return mt1
    def TWISTING_VINES_PLANT(): return mt1
    def CRIMSON_WALL_SIGN(): return mt1
    def WARPED_WALL_SIGN(): return mt1
    def POTTED_CRIMSON_FUNGUS(): return mt1
    def POTTED_WARPED_FUNGUS(): return mt1
    def POTTED_CRIMSON_ROOTS(): return mt1
    def POTTED_WARPED_ROOTS(): return mt1