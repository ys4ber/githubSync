from global_ import data_file, user, SYS, os, json, sys, app_name
from colors import RED, RESET, GREEN, YELLOW, BLUE

def check_for_git(dir_path):
    if not os.path.exists(f"{dir_path}/.git"):
        print(f"{RED}Not a git repository{RESET}")
        sys.exit(1)

def check_for_permissions(dir_path):
    if not os.access(dir_path, os.W_OK):
        print(f"{RED}Permission denied{RESET}")
        sys.exit(1)

def read():
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{RED}File is corrupted{RESET}")
        allow_reset = input(f"{YELLOW}Do you want to reset the file and continue? (y/n){RESET}")
        if allow_reset.lower() == "y":
            with open(data_file, 'w') as f:
                f.write("[]")
            print(f"{GREEN}File reset successfully{RESET}")
            return []
        else:
            print(f"{RED}Exiting...{RESET}")
            sys.exit(1)

def save(dirs):
    with open(data_file, 'w') as f:
        json.dump(dirs, f)

def add(dir_):
    dirs = read()
    check_for_permissions(dir_)
    check_for_git(dir_)
    if dir_ not in dirs:
        dirs.append(dir_)
        save(dirs)
        print(f"{GREEN}{dir_} SET{RESET}")
    else:
        print(f"{YELLOW}{dir_} already inserted{RESET}")

def remove(dir):
    try:
        dirs = read()
        dirs.remove(dir)
        save(dirs)
    except ValueError:
        print(f"{YELLOW}{dir} is not inserted{RESET}")

def prefix(dir_path):
    if dir_path == ".":
        return os.getcwd()
    elif dir_path == "..":
        return os.path.dirname(os.getcwd())
    elif dir_path == "~":
        return f"/home/{user}" if SYS == "LINUX" else f"C:\\Users\\{user}"
    return dir_path

def guard(argv):
    if len(argv) < 3:
        print(f"{RED}Missing argument{RESET}")
        sys.exit(1)
    dir_path = prefix(argv[2])
    if not os.path.exists(dir_path):
        print(f"{RED}Directory does not exist{RESET}")
        sys.exit(1)
    return dir_path

# -------------------------------------------------------------------------

def enable():
    try:
        if SYS == "LINUX":
            os.system(f"touch /home/{user}/.gitsync")
        else:
            os.system(f"echo. 2> C:\\Users\\{user}\\.gitsync")
    except:
        print(f"{RED}Error enabling the tool{RESET}")
        sys.exit(1)

def disable():
    try:
        if SYS == "LINUX":
            os.system(f"rm /home/{user}/.gitsync")
        else:
            os.system(f"del C:\\Users\\{user}\\.gitsync")
    except:
        print(f"{RED}Error disabling the tool{RESET}")
        sys.exit(1)

def is_active():
    try:
        if SYS == "LINUX":
            return os.path.exists(f"/home/{user}/.gitsync")
        else:
            return os.path.exists(f"C:\\Users\\{user}\\.gitsync")
    except:
        return False
    return False


#--------------------------------------------------------------------------

def push_to_origin(branch):
    try:
        os.system(f"cd {dir}")
        os.system("git add .")
        os.system("git commit -m 'Syncronized by {app_name}'")
        if branch:
            os.system(f"git push origin {branch}")
        else:
            os.system("git push")
    except Exception as e:
        print(f"{RED}{e}{RESET}")

def run():
    if not is_active():
        print(f"{YELLOW}Tool is disabled{RESET}")
        sys.exit(1)
    dirs = read()
    if not dirs or len(dirs) == 0:
        print(f"{YELLOW}No directories yet{RESET}")
        sys.exit(1)
    for dir in dirs:
        print(f"---{BLUE}{dir}{RESET}")
        try:
            os.system(f"cd {dir} && git pull")
        except Exception as e:
            print(f"{RED}{e}{RESET}")
            continue
        print(f"{GREEN}{dir} Up to date{RESET}")
        try:
            push_to_origin(None)
        except Exception as e:
            if "git branch --set-upstream-to=origin/<branch>" in str(e):
                print(f"{YELLOW}Branch not set, trying defualt branches[main, master]{RESET}")
                try:
                    push_to_origin("main")
                except:
                    try:
                        push_to_origin("master")
                    except Exception as e:
                        print(f"{RED}{e}{RESET}")
                        continue
            else:
                print(f"{RED}{e}{RESET}")
                continue
        print(f"{GREEN}{dir} Syncronized{RESET}")
    print(f"{GREEN}All directories are up to date{RESET}")