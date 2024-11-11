import os
import sys
import shutil
from datetime import datetime
import readline

from commands import *
from tagging import *

def main():
    while True:
        try:
            current_dir = os.getcwd()
            command_prompt = input(f"{current_dir}> ").strip()

            if not command_prompt:
                continue

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
                break
            elif command == "clear":
                clear_terminal()
            elif command == "tagdir":
                tag_dir(current_dir, args)
            elif command == "tagfile":
                tag_file(args)
            elif command == "tags":
                list_tags(args)
            else:
                print(f"Command not found: {command}")
        except KeyboardInterrupt:
            print("\nExiting CLI.")
            break
        except Exception as e:
            print("Error:", e)
            continue

def clear_terminal():
    try:
        os.system("clear")
    except Exception as e:
        print("Error clearing terminal: ", e)

def completer(text, state):
    files = os.listdir('.')
    options = []
    for file in files:
        if file.startswith(text):
            options.append(file)

    if state < len(options):
        return options[state]
    return None


if __name__ == "__main__":
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    main()
