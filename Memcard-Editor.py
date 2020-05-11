###
import binascii

#Filename to load for editing
global default_filename
default_filename = "EDIT.mcr"
#Application Loop
global run_again
run_again = True


#Offsets for formats
#GME 0x3140 - 0x2200 = 0xF40
#For first file, may be bytes inbetween files too
#Inbetween expected 0x4200, 0x5140 Result = 0xF40.
#I think ePSXe memcards are the same as [EMU] pSX 1_13 memcards, a diff showed no results

#Byte offset per sotn save = 1024*8
global global_save_byte_offset
global_save_byte_offset = 0

###===UTILITIES SECTION===###

#Keyboard input pause, prevent more stuff being printed and distracting from just recieved data
def continue_user_controlled_pause():
    raw_input("\n==============\nContinue...")


###I/O - Binary

#Write Bytes
def file_open_write_bytes(filename, offset, bytes_write):
    global global_save_byte_offset
    #offset += global_save_byte_offset
    
    fh = open(filename, "r+b")
    fh.seek(offset)
    fh.write(bytes_write)
    fh.close()

#Write Bytes (number of elements in array)
def file_open_write_bytes_number(filename, offset, bytes_write, number_bytes):
    fh = open(filename, "r+b")
    fh.seek(offset)
    for i in range(0, number_bytes-1):
        fh.write(bytes_write[i])
    fh.close()

#Read Bytes
def file_open_read_bytes(filename, offset, bytes_read_number):
    fh = open(filename, "r+b")
    fh.seek(offset)
    result = fh.read(bytes_read_number)
    fh.close()
    return result

###COPIED BYTES, HEX, INT CONVERTER
def bytes2int(str):
    return int(str.encode('hex'), 16)

def bytes2hex(str):
 return '0x'+str.encode('hex')

def int2bytes(i):
 h = int2hex(i)
 return hex2bytes(h)

def int2hex(i):
 return hex(i)

def hex2int(h):
 if len(h) > 1 and h[0:2] == '0x':
  h = h[2:]

 if len(h) % 2:
  h = "0" + h

 return int(h, 16)

def hex2bytes(h):
 if len(h) > 1 and h[0:2] == '0x':
  h = h[2:]

 if len(h) % 2:
  h = "0" + h

 return h.decode('hex')



###Endian Reverse
def reverse_endian(str):
    '''
    str_array = list(str)
    length = len(str_array)
    result = list(str)
    i2 = 0
    for i in range(0,length-1):
        result[i2] = str_array[i]
        i2+=1
    return ''.join(result)
    #return str[length-1:0]
    '''
    aBigEndianList = []
    for i in range(0, len(str), 2):
        aBigEndianList.insert(0, str[i:i+2])
    return "".join(aBigEndianList)

def Dump_endian_reverse(n): 
    s = '%x' % n
    if len(s) & 1:
        s = '0' + s
    return s.decode('hex')
    #print repr(Dump(1245427))



#To hex, and disabled raw because useless
def print_hexlify_and_normal(x):
    print(binascii.hexlify(x))
    #print("Raw:")
    #print(x)



###===READ MEMCARD SECTION===###

#Menu select read option
def read_memcard_data():
    print("Select Option to READ:\n")
    options_names = ["Save Location",
                     "Relics Data x2208 to x2281",
                     "Items Data 0x225f to 0x2360",
                     "Stats Data",
                     "ALL of the above",
                     "Directory of Files (Save)",
                     "Read Names from multiple save slots Memcard"]

    i_int = 1
    for i in options_names:
        print(repr(i_int) + ". "+i)
        i_int +=1

    option_id = input("\nOptionID: ")

    if option_id == 1:
        read_memcard_data_savelocation()
    elif option_id == 3:
        read_memcard_data_items()
    elif option_id == 4:
        read_memcard_data_stats()
    elif option_id == 5:
        print(">Save")
        read_memcard_data_savelocation()
        print(">Relics")
        read_memcard_data_relics()
        print(">Items")
        read_memcard_data_items()
        print(">Stats")
        read_memcard_data_stats()
    elif option_id == 6:
        read_directoryof_memcard_data()
    elif option_id == 7:
        read_memcard_multliple_names_infile()
    else:
        read_memcard_data_relics()



#READ save Bytes
def read_memcard_data_savelocation():
    print("SAVE LOCATION READ")
    save_location = file_open_read_bytes(default_filename, 0x2220, 16)
    print(binascii.hexlify(save_location))
    print(save_location)

#Read relic bytes
def read_memcard_data_relics():
    relics_data = file_open_read_bytes(default_filename, 0x2208, 122)
    #print(binascii.hexlify(relics_data))
    #print(relics_data)
    print_hexlify_and_normal(relics_data)

#Read items bytes
def read_memcard_data_items():
    offset = 0x225f
    #to 0x2360
    bytes_read = 258
    items_data = file_open_read_bytes(default_filename, offset, bytes_read)
    print_hexlify_and_normal(items_data)

#Read stats bytes
def read_memcard_data_stats():
    offset = 0x2500
    bytes_read = 0x2500 - 0x2460
    print_hexlify_and_normal(file_open_read_bytes(default_filename, offset, bytes_read))

#Directory READ (read all files in directory) Save Data
def read_directoryof_memcard_data():
    import os
    current_path = os.path.dirname(os.path.realpath(__file__))

    result = input("\nSet save path? 1=Yes 0=Use current path: ")

    custom_path = False
    if result == 1:
        current_path = raw_input("\nSet directory: ")
        custom_path = True

    
    
    from os import listdir
    from os.path import isfile, join
    if custom_path == False:
        onlyfiles = [ f for f in listdir(current_path) if isfile(join(current_path,f)) ]
    else:
        onlyfiles = [ f for f in listdir(current_path) if isfile(join(current_path,f)) ]
    
    print(".mcr")
    names = []
    hexs = []
    for i in onlyfiles:
        #print i
        #extension = os.path.splitext(i)[1]
        fileName, fileExtension = os.path.splitext(i)

        i_read = i
        
        if custom_path:
            i_read = current_path + "\\" + i
 
        
        if fileExtension == ".mcr":# or True:
            names.append(fileName)
            print(fileName)
            
            hexs.append(binascii.hexlify( file_open_read_bytes(i_read, 0x2220, 16) ) )
            print( binascii.hexlify( file_open_read_bytes(i_read, 0x2220, 16) ) )

    print("\nArrays:\nsave_hexstring_array = [")
    for i in range(0,len(hexs)-1):
        print("\""+hexs[i]+"\",")
    print("]\nsave_name_array = [")
    for i in range(0,len(names)-1):
        print("\""+names[i]+"\",")
    print("]")


def read_memcard_multliple_names_infile():
    for i in range(0,15):
        #Card = 128KB, 128/8 = 16, 1 Slot for metadata, 15 slots left,
        #as using first slot just add 1024*8 (8KB) to get each save value
        sotn_name = file_open_read_bytes(default_filename, 0x2200 + i*1024*8, 8)
        print("SOTN Name " + repr(i) + ":\t\""+sotn_name + "\"\t-> " + binascii.hexlify(sotn_name) )

###===WRITE/EDIT MEMCARD SECTION===###

#STATS
def stat_edit():
    print("\n\n=STAT EDIT=\t\t[Read Stats]\t[Hex]\t\t[Hex]")

    #Names Of Stats
    stats_names =[
    "HP Health MAX", #HP MAX
    "HP Health Current", #HP 
    "MP Mana MAX\t", #MP MAX
    "MP Mana Current", #MP
    "HEARTS MAX\t",
    "HEARTS CURRENT",
    "STR STRENGTH\t", #Attack - sort of
    "CON CONSTITUTION", #Derfense - Sort of
    "INT INTELLIGENCE", #Magic and Subweapon
    "LCK LUCK\t", #Item Drop and Critical Hits
    "GOLD $$$\t",
    "LEVEL\t",
    "XP Experience" #Will automatically levelup if beyond next level goal
    ]
    #String Description of Reccomended Limits
    stats_limit_desc = [
    "1-9999", #HP
    "1-9999",
    "1-9999", #MP
    "1-9999",
    "1-9999", #HEARTS
    "1-9999",
    "0-99, extra:999", #STR
    "0-99, extra:999",
    "0-99, extra:999",
    "0-99, extra:999",
    "0-999999, extra 1048575", #GOLD
    "0-99", #LVL
    "0-9999999, no effect past?" #XP
    ]

    #Hex Location of the stat
    stat_hexlocation = [
    0x2478, #HP MAX [Swapped after testing
    0x2474, #HP
    0x2488, #MP MAX
    0x2484, #MP
    0x2480, #HEARTS MAX [Swapped after testing
    0x247C, #HEARTS
    0x248C, #STR
    0x2490, #CON
    0x2494, #INT
    0x2498, #LCK
    0x24C4, #GOLD to 24C6
    0x24BC, #LVL
    0x24C0 #XP to 0x24C2
    ]
    #Number of Bytes of the Stat
    stat_bytes_num = [
    2, #HP MAX
    2, #HP
    2, #MP MAX
    2, #MP
    2, #HEARTS MAX
    2, #HEARTS CURRENT
    2, #STR
    2, #CON
    2, #INT
    2, #LCK
    3, #Gold
    2, #LEVEL
    3 #XP
    ]
    stat_total_number = 13

    import struct

    #Header
    print("#. STAT\t\t\tDecimal Value\tBig Endian\tLittle Endian (memcard)")
    i_int = 0
    for i in stats_names:
        name = stats_names[i_int]
        offset = stat_hexlocation[i_int]
        bytes_num = stat_bytes_num[i_int]
        limit_desc = stats_limit_desc[i_int]
        
        
        #READ
        bytes_read = file_open_read_bytes(default_filename, offset, bytes_num)
        
        string_hexread = binascii.hexlify(bytes_read) #str.encode('hex')
        little_endian = bytes2int(bytes_read)
        string_numberread = int(reverse_endian(bytes_read.encode('hex')), 16)
        #bytes2int(Dump_endian_reverse(little_endian)) #little_endian.join(reversed(s))#[::-1]
        #struct.unpack('!7h', little_endian)#""#int.from_bytes(bytes_read, byteorder='little')
        #print(bytes_read)

        strhex_rev_endian = reverse_endian(bytes_read.encode('hex'))
        #PRINT
        print(repr(i_int) + ". "+i + "\t" + repr(string_numberread) + "\t\t" + string_hexread + "\t\t" + strhex_rev_endian)
        i_int +=1
    #print(repr(stat_total_number)+". [SET ALL STATS]")
    #i_int +=1
    print("\n"+repr(stat_total_number)+". [EXIT] End")
    #set all stats, use hex instead

    stat_id = input("\nStatID: ")

    if stat_id >= 0 and stat_id < stat_total_number:
        name = stats_names[stat_id]
        offset = stat_hexlocation[stat_id]
        bytes_num = stat_bytes_num[stat_id]
        limit_desc = stats_limit_desc[stat_id]
        #offset = bytearray.fromhex(hexlocation_string)

        print("\n"+name+"\t Limit Advice: "+limit_desc)
        #prev value
        new_value = input("\nNew ["+name+"] Value: ")
        #new_valueh = 
        
        #new_value_hex = int2hex(new_value) #binascii.hexlify(new_value)
        #new_value_bytearray = bytearray.fromhex(new_value_hex)
        
        

        new_value_bytearray = int2bytes(new_value)


        new_value_bytearray_length =len(new_value_bytearray)
        #print(new_value_bytearray_length)
        #while new_value_bytearray_length < bytes_num:
        #    new_value_bytearray.append(0)
        #new_value_bytearray_length =len(new_value_bytearray)


        new_value_hex = binascii.hexlify(new_value_bytearray)
        
        #Reverse endian
        oldval = new_value_hex
        new_value_hex = reverse_endian(new_value_hex)
        print(oldval + " | " + new_value_hex)

        #Add ends, so replace entire stat var instead of only how many bytes the input contains
        
        new_value_hex_length = len(new_value_hex)
        while new_value_hex_length < bytes_num*2:
            new_value_hex += "00"
            new_value_hex_length = len(new_value_hex)
        print(new_value_hex)
        new_value_bytearray =  bytearray.fromhex(new_value_hex) #reverse_endian(new_value_hex))

        #new_value_bytearray = bytearray.fromhex( reverse_endian(new_value_bytearray.encode('hex')) )

        print(binascii.hexlify(new_value_bytearray))
        
        
        file_open_write_bytes(default_filename, offset, new_value_bytearray)

        print_hexlify_and_normal(file_open_read_bytes(default_filename, offset, bytes_num))


        
        #Run again
        #again = input("\nRun [STATEDIT] again? 1=Yes: ")
        #return again == 1
        continue_user_controlled_pause()
        return True
    else:
        print("Exit [STATEDIT] End")#"No valid stat selected")
        return False



#Relics
def relic_edit():
    print("\n\n=RELIC EDIT=")

    relics_hexarray = [
    "000000003000000000000000000000000000000000000000000000000008", #
    "030303030303030303030303030303030303030101010100000303030303"] # #at end0103 to 0303, equip vlad ring int+10
    offset = 0x2238
    #To 0x2255
    bytes_num = 30
    
    result = input("\nUnlock all relics? 1 = Yes 2 = Disable All Relics: ")
    if result == 1:
        hex_string_use = relics_hexarray[1]
    elif result == 2:
        hex_string_use = relics_hexarray[0]
    else:
        print("CANCELED RELIC EDIT...")
        return


    print(hex_string_use)


    hex_use = bytearray.fromhex(hex_string_use)

    
    print(hex_use)
    print(binascii.hexlify(hex_use))

    file_open_write_bytes(default_filename, offset, hex_use)


    
    print_hexlify_and_normal(file_open_read_bytes(default_filename, offset, bytes_num))



#Items
def item_edit():
    print("\n\n=ITEM EDIT=")

    all_items_hex = "636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363"
    offset = 0x225f
    
    if input("\nGet all items? 1 = Yes: ") == 1:
        hex_use = bytearray.fromhex(all_items_hex)

    
        print(hex_use)
        print(binascii.hexlify(hex_use))
        
        file_open_write_bytes(default_filename, offset, hex_use)
        read_memcard_data_items()



##SAVE LOCATION###
def save_location_edit():
    
    print("\n\n=SAVE LOCATION EDIT=")

    #Save line location
    offset = 0x2220
    #Size of the save section
    byte_size = 16 #32 hex units = 16 8bit bytes

    #Hex Bytes String of Save location data
    savelocation_hexarray = [
    "050000000100000007009C0903002A00",
    "020000000200000041001D0011002500",
    "06000000020000000700AA0111002500",
    "00000000020000000C00330007001E00",
    "0C00000002000000000055001D001B00",
    "0C00000002000000000070011F001B00",
    "00000000020000000100140137001800",
    "01000000020000000200420133001300",
    "00000000020000000B00AB0027000900"]
    #030000000200000041001b0011002500#First Save?

    savelocation_hexarray_inverted = [
    "070000000100000032009C0937001800", #Glitch
    "0f000000010000003200c6093c000d00",

    "06000000020000002400080220002e00", #Mummy
    
    "0E000000000000002300150629000D00", #Galamoth
    "07000000010000002000630920002400"] #Final



    #NAMES
    savelocation_name = [
    "Entrance\t\tGlitched Underground Caverns Save",
    "Entrance\t\tFirst Save / Teleporter",
    "Entrance\t\tFirst Save / Teleporter - Mode 2 Bloody Zombies",
    "Alchemy Laboritory\tBoss",
    "Marble Gallery\t#1",
    "Marble Gallery\tClock/World Center/Maria",
    "Outerwall\t\tDoppleganger / Lower",
    "Long library",
    "Castle Keep\t\tRitcher Lion _Regular_Castle_Boss_"]

    savelocation_name_inverted = [
    "Glitched Third (Regular) OuterWall\t#1 - Lower",
    "Glitched Third (Regular) OuterWall\t#2 - Higher",

    "Inverted Olrox\t\t\tMummy Boss",
    
    "Inverted Floating Catacombs\t\tGalamoth Boss",
    "Inverted Marble Gallery\t\t_Final Save_"]


    #Unsorted
    savelocation_hexarray_unsorted = [
    "00000000010000002600c70922003200",




    "0c00000002000000000055001d001b00",



    "000000000200000005001d011c002900",
    "00000000020000000700160105002700",
    "01000000020000000200420133001300",
    "01000000020000000200420133001300",
    "00000000020000000100140137001800",
    "0e000000020000000900ea0028002500",
    "0e000000020000000900cd0028001b00",
    "00000000020000000900e1002b002100",
    "00000000020000000b00ab0027000900",
    "00000000020000000b00ab0027000900",
    "07000000020000000300590116003200",
    "040000000200000003003e011e003200",
    "0e000000020000000a0091010e001700",
    "09000000020000000a00820119001700",
    "06000000020000000700aa0111002500",
    "01000000020000002b00c30118003600",
    "0c00000002000000000070011f001b00",
    "02000000020000000400aa011f001100",
    "0900000002000000010059013c000d00",
    "0a000000020000002600d30122003200",

    "06000000020000002400080220002e00", #Mummy

    "06000000020000000700a20011002500",
    "0c000000020000000b00a90027000900",
    "020000000200000041001d0011002500",
    "0d0000000200000041001d0011002500",
    "0f0000000200000041001d0011002500",

    ##Saveedit Folder
    "03000000020000000b005d0127000900",
    "05000000020000000b005c0127000900",
    "07000000020000000b005e0127000900",
    "05000000020000002c00ed0138002100",
    "0a000000020000002600e4013d002300",
    "0d000000020000002a00c80126002800",
    "06000000020000002a00bf0131002800",
    "0200000002000000270043023a001800",
    "0500000002000000270012022e001a00",
    "0900000001000000220063090c002c00",
    "020000000200000020000d0222002400",
    "020000000200000020000d0222002400",
    "0e000000010000002100630908002700",
    "0e000000020000002c000a022f001c00",
    "0f000000010000003200c6093c000d00",
    "00000000020000000100140137001800",
    "09000000020000004100170005002700",
    "0a000000020000004100270011002500",
    "090000000200000007002c0011002500",
    "07000000020000004100040003002a00",
    "0b0000000200000000004e001d001b00",
    "070000000100000032009c0937001800"
    ]

    savelocation_name_unsorted = [
    ##test::: folder
    "Inverted/Anti Chapel",



    "Marble gallery first save",



    "Abandoned Mine\tboss cerebrus",
    "Entrance\t\thigh up save out of reach without upgrades",
    "Library\t\tbought some values of items",
    "Library\t\tgot lots of items from hack",
    "Outer Wall\t\tdoppleganger fight",
    "Underground Caverns\tboss save lower area",
    "Underground Caverns\tfirst save",
    "Underground Caverns\tnightmare save",
    "Delete\t\t\tbeatencrowboss at lion",
    "Delcastlekeep\t\trichter lion all items",
    "Catacombs\t\tboss legion granfalloon",
    "Catacombs\t\tentrance save",
    "Collisium\t\tboss save",
    "Collisium\t\tfirst save",
    "Entrance\t\tfirst save mode 2 bloody zombies",
    "Inverted lion ritcher",
    "Marble Gallery\tCenter World / Clock / Maria",
    "Olrox's Quarters\tBoss",
    "Outer Wall\t\tTop / next to clock tower",
    "Reverse Chapel\tsave 1 near reverse keep and medusa boss",

    "reverse olrox mummy boss",

    "unlock lion\t\trichter teleport - at entrance",
    "unlock lion\t\trichter teleport - at richter",
    "test0",
    "test01",
    "test02",

    #SAVEEDIT FOLDER
    "at lion been\t\tto load zone but not teleport",
    "at lion but not been to",
    "lion teleport unlocked",
    "Reverse Alchemy Lab\t\tat boss",
    "Reverse Chapel\t\t2 near alchemy lab",
    "Reverse Collisium\t\t2 near olrox",
    "Reverse Collisium\t\tboss near revserse chapel",
    "Reverse Entrance\t\tnear caslte door and caves",
    "Reverse Entrance\t\tteleport save",
    "Reverse Library Save",
    "Reverse Marble Gallery\t\tsave 1",
    "Reverse Marble Gallery\t\tsave 1_",
    "Reverse Outer Wall\t\tnext to creature boss 255 save",
    "Revesrse Alchehmy Lab\t\tSave 1",
    "third outer wall\t\thigher save",
    "richter",
    "richter_entrance\t\tabove save - wargs",
    "richter_entrance\t\tfirst accessible by alucard save",
    "richter_entrance\t\tteleporter bloody zombies",
    "richter_entrance\t\tunderground caverns save - entrance original with wargs",
    "richter_marble\t\tgallery",
    "richter_ultisave"
    ]

    #CASTLE ID
    print("Select one of the following\n"
          "\n0. Regular Castle (Non Inverted)"
          "\n1. Inverted Castle"
          "\n2. Unsorted (more of both)")

    number_castle = input("\nNumberID: ")



    #SAVE LOCATION ID
    if number_castle == 1:
        print("Select one of the following\n")
        i_int = 0
        for i in savelocation_name_inverted:
            print(repr(i_int) + ". "+i)
            i_int +=1
        #print("\n")
    elif number_castle == 2:
        print("Select one of the following\n")
        i_int = 0
        for i in savelocation_name_unsorted:
            print(repr(i_int) + ". "+i)
            i_int +=1
    else:
        print("Select one of the following\n")
        i_int = 0
        for i in savelocation_name:
            print(repr(i_int) + ". "+i)
            i_int +=1
        #print("\n")


    number_location = input("\nNumberID: ")

    hex_string_use = 0
    if number_castle == 1:
        hex_string_use = savelocation_hexarray_inverted[number_location]#.decode("hex")
    elif number_castle == 2:
        hex_string_use = savelocation_hexarray_unsorted[number_location]
    else:
        hex_string_use = savelocation_hexarray[number_location]#.decode("hex")

    
    hex_use = bytearray.fromhex(hex_string_use)

    print(hex_string_use)
    print(hex_use)
    print(binascii.hexlify(hex_use))

    #Write
    file_open_write_bytes(default_filename, offset, hex_use)

    #Results
    read_memcard_data_savelocation()


###===Running Section===###

#Change the filename to load
def change_global_variables():
    global default_filename
    print(default_filename)
    default_filename = raw_input("New filename (same directory): ")

#Run the Application
def run():
    global default_filename
    global run_again
    
    print("=INFO="
          "\nThis script edits the _SOTN Memory card_."
          "\nIt edits a pSX_1_13 emulator .mcr file"
          "\n(Other formats may work, provided they are 128KB, maybe same for non metadata)"
          "\nIt is assumed the save game is at the save is at a certain position (0)."
          "\nCopy the save to a blank memory card in the bottom left corner"
          "\n(for the second memcard slot) within sotn to do this."
          )

    print("\n\nSET THE SAVE GAME IN THE SAME DIRECTORY AND CALL IT \"EDIT.mcr\"")

    
    print(default_filename)
    import os.path
    memcard_file_exists = os.path.isfile(default_filename)
    if memcard_file_exists:
        sotn_name = file_open_read_bytes(default_filename, 0x2200, 8)
        print("SOTN Name: \""+sotn_name + "\"  -> " + binascii.hexlify(sotn_name) )
    else:
        print("> _[!] File does NOT exist [!]_ !!!!!!")

    print("\nSelect Option:\n")#to edit
    options_names = ["[READ] data from memcards",
                     "[CHANGE] memory_card filename", #/directory
                     "[EDIT] Save location",
                     "[EDIT] Stats (GOLD, XP, LEVEL etc)",
                     "[EDIT] Relics Unlock",
                     "[EDIT] Items Get",
                     "[QUIT] EXIT"]

    i_int = 1
    for i in options_names:
        print(repr(i_int) + ". "+i)
        i_int +=1

    option_id = input("\nOptionID: ")

    if option_id == 1:
        read_memcard_data()
    elif option_id == 2:
        run_again = True
        change_global_variables()
        return
    elif option_id == 3:
        save_location_edit()
    elif option_id == 4:
        stat_run_again = True
        while stat_run_again:
            stat_run_again = stat_edit()
    elif option_id == 5:
        relic_edit()
    elif option_id == 6:
        item_edit()
    else:
        print("Exit...")
        run_again = False



#Application EXECUTE
#Loop the application, unless if exit is selected in run()
while run_again:
    run()
    '''if (run_again == False):
        try:
            if input("\n[*SCRIPT*] Again? 1 = Yes: ") == 1:
                run_again = True
        except ValueError:
            run_again = False'''
    continue_user_controlled_pause()
#Terminate
print(">END -----------------------")


# codigo fuente: https://pastebin.com/Sxch6dXC
# Autor Desconocido
