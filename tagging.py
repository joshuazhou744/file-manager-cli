def tag_dir(curr_dir, args):
    if len(args) != 1:
        print("Usage: tag <tagname>")
        return
    name = args[0]

def tag_file(args):
    pass

def list_tags(args=None):
    if not args:
        print("no tags to list yet")
    else:
        print(args)