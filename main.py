import os
import sys
import shutil
from datetime import datetime
import curses

def main():
    curses.wrapper(run_cli)

def run_cli(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.clear()
    while True:
        try:
            current_dir = os.getcwd()
            input_prompt = f"{current_dir}> "
            stdscr.addstr(input_prompt)
            stdscr.refresh()
            command_prompt = ""

            while True:
                ch = stdscr.get_wch()
                if ch == '\t':
                    command_parts = command_prompt.split(" ")
                    if len(command_parts) > 1:
                        last_arg = command_parts[-1]
                        matches = autocomplete(current_dir, last_arg)
                        matches = autocomplete(current_dir, last_arg)
                        if matches:
                            stdscr.addstr("\nPossible matches:\n" + "  ".join(matches) + "\n")
                        else:
                            stdscr.addstr("\nNo matches found.\n")
                        stdscr.addstr(input_prompt + command_prompt)
                        stdscr.refresh()
                elif ch in ('\n', '\r'):
                    stdscr.addstr("\n")
                    break
                elif isinstance(ch, str) and ch.isprintable():
                    command_prompt += ch
                    stdscr.addstr(ch)
                    stdscr.refresh()
                elif ch in [curses.KEY_BACKSPACE, '\b', '\x7f']:
                    if len(command_prompt) > 0:
                        command_prompt = command_prompt[:-1]
                        y, x = stdscr.getyx()
                        if x > len(input_prompt):
                            stdscr.move(y, x - 1)
                            stdscr.delch()
                            stdscr.refresh()
                else:
                    pass
            process_command(command_prompt.strip())
        except KeyboardInterrupt:
            stdscr.addstr("\nExiting CLI.")
            stdscr.refresh()
            break
        except Exception as e:
            stdscr.addstr(f"\nError: {e}")
            stdscr.refresh()


def process_command(command_prompt):
    parts = command_prompt.split(" ")
    command = parts[0]
    args = parts[1:]

    if command == 'cd':
        change_directory(args)
    elif command == 'ls':
        list_directory(args)
    elif command == 'touch':
        create_file(args)
    elif command == 'mv':
        move_item(args)
    elif command == 'rm':
        remove_file(args)
    elif command == 'rmdir':
        remove_directory(args)
    elif command in ['exit', 'quit']:
        print("\nExiting CLI.")
        sys.exit(0)
    elif command == "clear":
        clear_terminal()
    else:
        print(f"Command not found: {command}")

def change_directory(args):
    if len(args) == 0 or args[0] == "~" or args[0] == "":
        os.chdir("/")
        return
    elif len(args) != 1:
        print("Usage: cd <directory>")
        return
    try:
        os.chdir(args[0])
    except FileNotFoundError:
        print(f"No such directory: {args[0]}")
    except NotADirectoryError:
        print(f"Not a directory: {args[0]}")
    except PermissionError:
        print(f"Permission denied: {args[0]}")

def list_directory(args):
    if args:
        path = args[0]
    else:
        path = '.'    
    try:
        items = os.listdir(path)
        
        file_details = []

        for item in items:
            item_path = os.path.join(path, item)
            try:
                stats = os.stat(item_path)
                size = stats.st_size # Size in bytes
                mtime = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                file_details.append((item, size, mtime))
            except Exception as e:
                print(f"\nError getting details for {item}: {e}")

        name_width = max((len(name) for name, _, _ in file_details), default=4)
        size_width = max((len(str(size)) for _, size, _ in file_details), default=4)
        mtime_width = 16

        print(f"{"Name".ljust(name_width)} {" Size".rjust(size_width)} {"Last Modified".rjust(mtime_width)}")
        print(f"{'-' * name_width}  {'-' * size_width}  {'-' * mtime_width}")

        for name, size, mtime in file_details:
            if os.path.isdir(os.path.join(path, name)):
                name = f"{name}/"
            print(f"{name.ljust(name_width)}  {str(size).rjust(size_width)}  {mtime.ljust(mtime_width)}")


    except FileNotFoundError:
        print(f"\nNo such directory: {path}")
    except NotADirectoryError:
        print(f"\nNot a directory: {path}")
    except PermissionError:
        print(f"\nPermission denied: {path}")

def create_file(args):
    if len(args) != 1:
        print("\nUsage: touch <filename>")
        return
    
    file_path = args[0]
    try:
        with open(file_path, 'a'):
            os.utime(file_path, None)
    except Exception as e:
        print("Error making file: ", e)

def move_item(args):
    if len(args) != 2:
        print("Usage: mv <source> <destination>")
        return
    src, dest = args
    try:
        shutil.move(src, dest)
    except FileNotFoundError:
        print(f"No such directory: {src}")
    except PermissionError:
        print(f"Permission denied.")
    except Exception as e:
        print(f"Error moving item: {e}")

def remove_file(args):
    if len(args) != 1:
        print("Usage: rm <filename>")
        return
    file_path = args[0]
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"No such file: {file_path}")
    except IsADirectoryError:
        print(f"Is a directory: {file_path}. Use rmdir to remove directories.")
    except PermissionError:
        print(f"Permission denied: {file_path}")

def remove_directory(args):
    if len(args) != 1:
        print("Usage: rmdir <directory>")
        return
    
    dir_path = args[0]
    try:
        os.removedirs(dir_path)
    except FileNotFoundError:
        print(f"No such directory: {dir_path}")
    except NotADirectoryError:
        print(f"Not a directory: {dir_path}")
    except OSError:
        print(f"Directory not empty: {dir_path}")
    except PermissionError:
        print(f"Permission denied: {dir_path}")

def autocomplete(curr_dir, arg):
    return ['hello', 'there']
    

def clear_terminal():
    try:
        os.system("clear")
    except Exception as e:
        print("Error clearing terminal: ", e)

if __name__ == "__main__":
    main()
