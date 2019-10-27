types = {
    'err': '[ERROR] \033[91m {} \033[0m',
    'progress': '[PROGRESS] \033[92m {} \033[0m'
}


def msg(msg_type, text, log):
    log(types[msg_type].format(text))
