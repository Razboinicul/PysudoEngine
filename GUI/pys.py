import vars

def write_pys_file():
    f = open(vars.p_path+"/project.pyse", "w+")
    text = f"""name {vars.p_name}""" #May add more info to store in this file
    f.writelines(text)
    f.close()

def read_pys_file():
    f = open(vars.p_path+"/project.pyse", "r+")
    t = f.readlines()
    temp_name = t[0].split(" ")[1:]
    text=""
    for i in temp_name: text+=i+" "
    vars.p_name = text
    f.close()