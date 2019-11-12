# _BOARD_TT638    = "P150638V601G"
# _BOARD_TT338    = "P75338V621G"
# _BOARD_TP3381   = "TPMSD338PB801"
# _BOARD_TP3382   = "TPMSD338PB802"
# _BOARD_HL3382   = "HLMS338PC822"
# _BOARD_TP638    = "TPMS638PC822"

def is_P150638V601G(board):
    if board == "P150638V601G":
        return True
    return False
def is_P75338V621G(board):
    if board == "P75338V621G":
        return True
    return False
def is_TPMSD338PB801(board):
    if board == "TPMSD338PB801":
        return True
    return False
def is_TPMSD338PB802(board):
    if board == "TPMSD338PB802":
        return True
    return False
def is_HLMS338PC822(board):
    if board == "HLMS338PC822":
        return True
    return False
def is_TPMS638PC822(board):
    if board == "TPMS638PC822":
        return True
    return False

def is_cvt(board):
    if  is_HLMS338PC822(board) or \
        is_TPMSD338PB801(board) or \
        is_TPMSD338PB802(board) or \
        is_TPMS638PC822(board):
        return True
    return False

def is_tt(board):
    if  is_P75338V621G(board) or \
        is_P150638V601G(board):
        return True
    return False

def is_338(board):
    if  is_HLMS338PC822(board) or \
        is_TPMSD338PB801(board) or \
        is_TPMSD338PB802(board)  or \
        is_P75338V621G(board):
        return True
    return False

def is_638(board):
    if is_P150638V601G(board):
        return True
    return False
