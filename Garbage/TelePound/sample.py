import random

#returns random public chat
def getRandomChat(Chats):
    check=False
    temp = 0
    while not check:
        temp = random.randrange(0,len(Chats.objects),1)
        if not Chats.objects[temp].type == 'private':
            check=True
    return temp

#get statistics
def getNumberOfChats(Chats, type='any'):
    counter=0
    if type == 'private':
        for chat in Chats.objects:
            if chat.type == 'private':
                counter = counter + 1
    else:
        if type == 'public':
            for chat in Chats.objects:
                if chat.type == 'public':
                    counter = counter + 1
        else:
            for chat in Chats.objects:
                counter = counter + 1
    return counter

def getNumberOfMessages(Messages):
    counter = 0
    for each in Messages.objects:
        counter = counter + 1
    return counter

#sort chats
def sortChatsByName(Chats):
    i = 0
    k = 1
    while i < len(Chats.objects):
        while k < len(Chats.objects):
            if not compareString(Chats.objects[i].chat_name, Chats.objects[k].chat_name):
                Chats = swapChatElements(Chats, i, k)
            k = k + 1
        i = i + 1
        k = i + 1
    return Chats

def sortChatsByUsers(Chats, AvailableUsers):
    i = 0
    k = 0
    counter1 = 0
    counter2 = 0
    while i < len(Chats.objects):
        while k < len(Chats.objects):
            for each in AvailableUsers.objects:
                if Chats.objects.get(fk=each.chat) == Chats.objects[i]:
                    counter1 = counter1 + 1
                if Chats.objects.get(fk=each.chat) == Chats.objects[k]:
                    counter2 = counter2 + 1
            if counter1 < counter2:
                Chats = swapChatElements(Chats, i, k)
            counter1 = 0
            counter2 = 0
            k = k + 1
        i = i + 1
        k = i + 1
    return Chats

#additional method
def swapChatElements(Chats, first, second):
    temp = Chats.objects[first]
    Chats.objects[first] = Chats.objects[second]
    Chats.objects[second] = temp
    return Chats

def compareString(first, second):
    if first == min(first, second):
        if second == min(first, second):
            return False
        else:
            return first == min(first, second)
    else:
        return False
