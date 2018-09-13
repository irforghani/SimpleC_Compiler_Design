f = open("dfa_0.txt")
b = open("input_string.txt")
token_file = open("Tokens.txt", 'w+')
ls = f.readlines()
new_ls = []
index = 0
index = 0
buffer = b.readlines()
stm = str()
litlist = []
litst = str()

for i in range(len(buffer)):
    buffer[i] = buffer[i][:-1]
for item in buffer:
    stm += item + " "
for i in range(0,len(stm)):
    if stm[i] != ' ':
        litst += stm[i]
    else:
        if(len(litst)> 0):
            litlist.append(litst)
            litst = ""

Tokens = []
for item in ls:
    if(len(item) != 1):
        index += 1
    else:
        break
index += 1
while(True):
    if len(ls[index]) != 1:
        new_ls.append(ls[index])
        index += 1
    else:
        break
for i in range (0,len(new_ls)):
    new_ls[i] = new_ls[i][:-1]




# def compile_proc(st: str):
#     index = 0
#     current = 0
#     accept = False
#     trap = False
#     for j in range (0,len(st)):
#         tmp = new_ls[0].split(' ')
#         for i in range(0,len(tmp)):
#             if tmp[i] == st[j]:
#                 index = i
#                 break
#         tmp = new_ls[int(current)+1].split(' ')
#         current = tmp[index]
#         if current == '100':
#             accept = True
#             break
#         if len((new_ls[int(current)+1].split(' '))[0]) > 1:
#             accept = True
#             tmp[index] = tmp[index][:-1]
#         else:
#             accept = False


    # return accept

token_str = ""
for i in litlist:
    token_str += str(i) + ' '

def insertChar(mystring, position, chartoinsert ):
    longi = len(mystring)
    mystring   =  mystring[:position] + chartoinsert + mystring[position:]
    return mystring

sigma = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def token_detect(ts: str()):
    for i in range(len(ts)):
        pre_index = 0
        post_index = 1
        for j in range(len(ts) - 1):
            if (ts[pre_index] in sigma) and (ts[post_index] not in sigma) and (ts[pre_index] != ' ') and (ts[post_index] != ' '):
                ts = insertChar(ts, post_index, ' ')
            pre_index += 1
            post_index += 1
        pre_index = 0
        post_index = 1
        for j in range(len(ts) - 1):
            if (ts[pre_index] not in sigma) and (ts[post_index] in sigma) and (ts[pre_index] != ' ') and (ts[post_index] != ' '):
                ts = insertChar(ts, post_index, ' ')
            pre_index += 1
            post_index += 1
        pre_index = 0
        post_index = 1
        for j in range(len(ts) - 1):
            if (ts[pre_index] not in sigma) and (ts[post_index] not in sigma) and (ts[pre_index] != ' ') and (ts[post_index] != ' ') and \
                    (ts[pre_index] != ':') and (ts[post_index] != '=') and (ts[pre_index] != '=') and (ts[post_index] != '=') and \
                    (ts[pre_index] != '<') and (ts[post_index] != '=') and (ts[pre_index] != '>') and (ts[post_index] != '=') and \
                    (ts[pre_index] != '<') and (ts[post_index] != '>'):
                ts = insertChar(ts, post_index, ' ')
            pre_index += 1
            post_index += 1
    return ts

def token_saving(ts: str()):
    mlist = []
    mstr = ""
    for i in range(0, len(ts)):
        if ts[i] != ' ':
            mstr += ts[i]
        else:
            if (len(mstr) > 0):
                Tokens.append(mstr)
                token_file.write(mstr + '\n')
                mstr = ""


# def scanner():
#     for m in range(0,len(litlist)):
#         first = 0
#         follow = 0
#         save = 0
#         while first <= len(litlist[m]) :
#             follow = first
#             while follow  <= len(litlist[m]):
#                 if compile_proc(litlist[m][first:follow - first + 1]):
#                     save = follow
#                 follow += 1
#             follow = save
#             Tokens.append(litlist[m][first:follow - first + 1])
#             token_file.write(litlist[m][first:follow - first + 1] + '\n')
#             first = follow + 1
#



token_str = token_detect(token_str)
token_saving(token_str)








# scanner()
print(Tokens)



