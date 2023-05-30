'''

This class is the main executable for the dynamic-taxes module

'''

import dynamictaxes
import os
import re
import sys
import subprocess
import time

def get_config_path():
    real_path = os.path.realpath(__file__)
    real_path = real_path[:real_path.rfind("/")]
    return real_path + "/default.config"

def get_qsub_template_path():
    real_path = os.path.realpath(__file__)
    real_path = real_path[:real_path.rfind("/")]
    return real_path + "/qsub_template.txt"

def load_configs():
    config_path = get_config_path()
    config_dict = {}
    float_regex = re.compile("[0-9]+\.[0-9]+")
    int_regex = re.compile("[0-9]+")
    bool_regex = re.compile("True|False")
    with open(config_path, 'r') as cf:
        lines = cf.readlines()
        for line in lines:
            line = line.replace("\n", "").strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            content = [l.strip() for l in line.split("=")]
            val = content[1]
            if float_regex.match(val):
                config_dict[content[0]] = float(val)
            elif int_regex.match(val):
                config_dict[content[0]] = int(val)
            elif bool_regex.match(val):
                config_dict[content[0]] = bool(val)
            else:
                config_dict[content[0]] = val

    dynamictaxes.set_config(config_dict)
    return dynamictaxes.get_config("username") == "USERNAME" or dynamictaxes.get_config("exec_mode") == "EXEC_MODE" or dynamictaxes.get_config("conda_env") == "CONDA_ENV"

def gen_pytext(lines):
    pytext = "# This is an automatically generated temp file that is used for program execution.\n\nimport dynamictaxes as dt\ndt.init_configs()\n\n"
    loader_exists = False
    esa_shortcut = False
    for line in lines:
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue
        if '#' in line:
            line = line.split('#')[0]

        if line.startswith("load") or line.startswith("read"):
            if not loader_exists:
                pytext += "loader = dt.Loader()\n"
                loader_exists = True
            line = line[4:].strip()
            if line.endswith(".json"):
                pytext += "loader.load_from_json(\"" + line + "\")\n"
            else:
                pytext += "loader.load_from_dir(\"" + line + "\")\n"

        elif line.startswith("save json to"):
            if not loader_exists:
                raise Exception("Must load data first before in can be saved to JSON")
            line = line[len("save json to"):].strip()
            jsonpath = line.split()[0]
            compact = str('compact' in line.lower())
            pytext += "loader.save_to_json(\"" + jsonpath + "\", compact=" + compact + ")\n"

        elif line.startswith("render"):
            if not loader_exists:
                raise Exception("Must load data first before it can be rendered.")
            line_list = line.split()
            if line_list[1].lower() == 'ta':
                assert line_list[2] == "to", f"Illegal syntax. Must be like \"render ta to ...\""
                path = line_list[3]
                pytext += "loader.ta_spectrum.render(\"" + path + "\")\n"
            elif line_list[1].lower() == "all" and line_list[2].lower() == "esa":
                assert line_list[3] == "to", f"Illegal syntax. Must be like \"render all esa to ...\""
                path = line_list[4]
                if not esa_shortcut:
                    pytext += "esa_spectra = loader.ta_spectrum.esa_spectra\n"
                    esa_shortcut = True    
                pytext += "for i, esa in enumerate(esa_spectra):\n"
                pytext += "    esa.render(\"" + path + "_\" + str(i))\n"
            elif line_list[1].lower() == "every" and line_list[3].lower() == "esa":
                dist = line_list[2]
                offset = "0"
                if '+' in line_list[2]:
                    dist = line_list[2].split("+")[0]
                    offset = line_list[2].split("+")[1]
                assert dist.isdigit() and offset.isdigit() and line_list[4] == "to", f"Illegal syntax. Must be like \"render every 2[+1] esa to ...\""
                path = line_list[5]
                assert int(line_list[2]) > 0, f"Stepsize in ESA rendering must be positive."
                if not esa_shortcut:
                    pytext += "esa_spectra = loader.ta_spectrum.esa_spectra\n"
                    esa_shortcut = True
                pytext += "for i in range(" + offset + ", len(esa_spectra), " + dist + "):\n"
                pytext += "    esa_spectra[i].render(\"" + path + "_\" + str(i))\n"

    return pytext

def make_qsub_script(args_dict):
    template = ""
    with open(get_qsub_template_path(), "r") as tempf:
        template = "".join(tempf.readlines())
    template = template.replace("{username}", dynamictaxes.get_config("username"))
    template = template.replace("{conda_env}", dynamictaxes.get_config("conda_env"))
    template = template.replace("{pyscript}", args_dict["pyscript"])
    args_dict["qsubscript"] = "dttemp" + args_dict["selftime"]
    with open(args_dict["qsubscript"]+".sh", "w") as qsubf:
        qsubf.write(template)
    return args_dict

def prepare_script(args_dict):
    args = sys.argv[1:]
    args_dict["selftime"] = str(time.time()).replace(".", "") 

    if args_dict["configs_unset"] and not "--config" in args:
        args_dict["noexec"] = True
        print("Please run either of the following:\n\n    dt --config\n    dyntax --config\n    dynamic-taxes --config\n\nFor this program to work, you have to set the variables\n\n    username=<your username>\n    conda_env=<the prepared conda environment>\n    exec_mode=<local|cluster>\n\nPlease do this before you try to do anything else.")
        return args_dict

    if "--config" in args:
        config_path = get_config_path()
        subprocess.run(["nano", config_path])
        args_dict["noexec"] = True
        return args_dict
    if "--script" in args:
        script_path = args[args.index("--script")+1]
        lines = [] 
        with open(script_path, 'r') as sf:
            lines = sf.readlines()
        lines = [l.replace("\n", "").strip() for l in lines]
        pytext = gen_pytext(lines)
        args_dict["pyscript"] = "pytemp" + args_dict["selftime"]
        with open(args_dict["pyscript"]+".py", "w") as pf:
            pf.write(pytext)
    args_dict["noexec"] = "--noexec" in args
    if "--ta" in args:
        args_dict["ta"] = args[args.index("--ta")+1]
    if "--esa" in args:
        args_dict["esa"] = args[args.index("--esa")+1]
    if "--load-dir" in args:
        args_dict["load-dir"] = args[args.index("--load-dir")+1]
    if "--load-json" in args:
        args_dict["load-json"] = args[args.index("--load-json")+1]

    if not "--script" in args:
        pseudoscript = []
        if "load-dir" in args_dict:
            pseudoscript.append("load " + args_dict["load-dir"])
        if "load-json" in args_dict:
            pseudoscript.append("load " + args_dict["load-json"])
        if "ta" in args_dict:
            pseudoscript.append("render ta to " + args_dict["ta"])
        if "esa" in args_dict:
            pseudoscript.append("render all esa to " + args_dict["esa"])
        pytext = gen_pytext(pseudoscript)
        args_dict["pyscript"] = "pytemp" + args_dict["selftime"]
        with open(args_dict["pyscript"]+".py", "w") as pf:
            pf.write(pytext)

    args_dict["cluster"] = dynamictaxes.get_config("exec_mode") == "cluster"
    args_dict["local"] = dynamictaxes.get_config("exec_mode") == "local"
    if "--cluster" in args:
        args_dict["cluster"] = True
        args_dict["local"] = False
    elif "--local" in args:
        args_dict["local"] = True
        args_dict["cluster"] = False

    if args_dict["cluster"]:
        args_dict = make_qsub_script(args_dict)
    return args_dict  

def exec_script(args):
    if args["cluster"]:
        subprocess.run(["qsub", args["qsubscript"]+".sh"])
    elif args["local"]:
        subprocess.run(["python", args["pyscript"]+".py"])

def main():
    configs_unset = load_configs()
    args = prepare_script({"configs_unset" : configs_unset})
    if "noexec" in args:
        if args["noexec"]:
            return
    exec_script(args)


if __name__ == '__main__':
    main()
