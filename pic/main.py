# -*- coding: utf-8 -*-
# @Date    	: 2016-04-04 17:01:40
# @Author  	: mr0cheng
# @email	: c15271843451@gmail.com

import time
import numpy as np
import csv
import matplotlib.pyplot as plt
import pickle
from matplotlib.legend_handler import HandlerLine2D

#--------stable-------------------
import os,sys
path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)
import static_data as sd
CURRENT_PATH=sd.CURRENT_PATH
ARTIST_FOLDER=sd.ARTIST_FOLDER
USER_FOLDER=sd.USER_FOLDER
ARTIST=sd.ARTIST
SONGS=sd.SONGS
SONG_P_D_C=sd.SONG_P_D_C
ARTIST_P_D_C=sd.ARTIST_P_D_C
USER_P_D_C=sd.USER_P_D_C
SONG_FAN=sd.SONG_FAN
ARTIST_FAN=sd.ARTIST_FAN
DAYS=sd.DAYS
START_UNIX  =sd.START_UNIX
DAY_SECOND  =sd.DAY_SECOND
START_WEEK=sd.START_WEEK
ALL_USER=sd.ALL_USER
ALL_USER_INFO=sd.ALL_USER_INFO
USER_SONG_RELATION=sd.USER_SONG_RELATION
USER_SONG_FOLDER = sd.USER_SONG_FOLDER
ALL_SONG = sd.ALL_SONG
SONG_INFO = sd.SONG_INFO
USER_INFO_FILTER=sd.USER_INFO_FILTER
SONG_UNIQUE_USER = sd.SONG_UNIQUE_USER
#--------stable-------------------

'''
date:
    %Y%m%d 20150301
'''
def date2Num(date):
    return (int(time.mktime(time.strptime(date,'%Y%m%d')))-START_UNIX)//DAY_SECOND

class artist(object):
    #ARTIST_PLAY_FOLDER=''
    #ARTIST_FAN_FOLDER=''   only one picture, so just palce it in the root folder.
    SONG_PLAY_FOLDER = ""
    SONG_FAN_FOLDER = ""

    ARTIST_ID = ""
    FPATH = ""

    def __init__(self,artist_id):
        self.ARTIST_ID = artist_id

        self.FPATH = os.path.join(ARTIST_FOLDER, artist_id)
        if not os.path.exists(self.FPATH):
            os.mkdir(self.FPATH)

        self.SONG_PLAY_FOLDER = os.path.join(self.FPATH, "song_play")
        self.SONG_FAN_FOLDER = os.path.join(self.FPATH, "song_fan")
        if not os.path.exists(self.SONG_PLAY_FOLDER):
            os.mkdir(self.SONG_PLAY_FOLDER)
        if not os.path.exists(self.SONG_FAN_FOLDER):
            os.mkdir(self.SONG_FAN_FOLDER)

    def plot_artist_play(self):
        ylabel = "count"
        xlabel = "days"
        with open(ARTIST_P_D_C, "r") as fr:
            artist_id = fr.readline().strip("\n")
            while artist_id:
                play = list(map(int, fr.readline().strip("\n").split(",")))
                download = list(map(int, fr.readline().strip("\n").split(",")))
                collect = list(map(int, fr.readline().strip("\n").split(",")))

                if artist_id==self.ARTIST_ID:
                    play=np.array(play)
                    mu=np.mean(play)
                    sigma=np.sqrt((play*play).sum()/DAYS-mu*mu)
                    p = plt.plot(play, "bo", play, "b-", marker="o")
                    d = plt.plot(download, "ro", download, "r-", marker="o")
                    c = plt.plot(collect, "go", collect, "g-", marker="o")
                    plt.legend([p[1], d[1],c[1]], ["play", "download","collect"])
                    plt.title(''.join(('mu=',str(mu),',','sigma=',str(sigma))))

                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.savefig(os.path.join(self.FPATH, "play.png"))
                    plt.clf()
                    break
                artist_id = fr.readline().strip("\n")

    def plot_artist_fan(self):
        ylabel = "count"
        xlabel = "days"
        with open(ARTIST_FAN, "r") as fr:
            artist_id=fr.readline().strip("\n")
            while artist_id:
                fan = list(map(int, fr.readline().strip("\n").split(",")))
                if artist_id == self.ARTIST_ID:
                    fan=np.array(fan)
                    mu=np.mean(fan)
                    sigma=np.sqrt((fan*fan).sum()/DAYS-mu*mu)
                    f = plt.plot(fan, "bo", fan, "b-", marker="o")
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.legend([f[1]], ["artist fans"])
                    plt.title(''.join(('mu=',str(mu),',','sigma=',str(sigma))))
                    plt.savefig(os.path.join(self.FPATH, "fan.png"))
                    plt.clf()
                    break
                artist_id=fr.readline().strip("\n")

    def plot_song_play(self):
        ylabel = "count"
        xlabel = "days"
        songs = self.getSongsListByArtist_id()
        with open(SONG_P_D_C, "r") as fr:
            songs_id = fr.readline().strip("\n")
            while songs_id:
                play = list(map(int, fr.readline().strip("\n").split(",")))
                download = list(map(int, fr.readline().strip("\n").split(",")))
                collect = list(map(int, fr.readline().strip("\n").split(",")))
                if songs_id in songs:
                    play=np.array(play)
                    mu=np.mean(play)
                    sigma=np.sqrt((play*play).sum()/DAYS-mu*mu)
                    p = plt.plot(play, "bo", play, "b-", marker="o")
                    d = plt.plot(download, "ro", download, "r-", marker="o")
                    c = plt.plot(collect, "go", collect, "g-", marker="o")
                    plt.legend([p[1], d[1],c[1]], ["play", "download","collect"])
                    plt.title(''.join(('mu=',str(mu),',','sigma=',str(sigma))))
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.savefig(os.path.join(self.SONG_PLAY_FOLDER, songs_id+".png"))
                    plt.clf()
                    break
                songs_id=fr.readline().strip("\n")

    def plot_song_fan(self):
        ylabel = "count"
        xlabel = "days"
        songs = self.getSongsListByArtist_id()
        with open(SONG_FAN, "r") as fr:
            songs_id = fr.readline().strip("\n")
            while songs_id:
                fan = list(map(int, fr.readline().strip("\n").split(",")))
                if songs_id in songs:
                    fan=np.array(fan)
                    mu=np.mean(fan)
                    sigma=np.sqrt((fan*fan).sum()/DAYS-mu*mu)
                    f = plt.plot(fan, "bo", fan, "b-", marker="o")
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.title(''.join(('mu=',str(mu),',','sigma=',str(sigma))))
                    plt.legend([f[1]], ["song fans"])
                    plt.savefig(os.path.join(self.SONG_FAN_FOLDER, songs_id+".png"))
                    plt.clf()
                songs_id=fr.readline().strip("\n")

    """
    {songs_id:bool,songs_id:bool,...,songs_id:bool}
    """
    def getSongsListByArtist_id(self):
        songs = {}
        with open(ARTIST) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for row in spamreader:
                if self.ARTIST_ID==row[1]:
                    songs[row[0]] = True
        return songs

class user(object):
    def __init__(self,userid):
        self.USERID = userid
        self.USERFOLDER = USER_FOLDER
        if not os.path.exists(self.USERFOLDER):
            os.mkdir(self.USERFOLDER)

    def plotUserPlay(self):
        ylabel = "count"
        xlabel = "days"

        with open(USER_P_D_C, "r") as fr:
            userid = fr.readline().strip("\n")
            while userid:
                play = list(map(int, fr.readline().strip("\n").split(",")))
                download = list(map(int, fr.readline().strip("\n").split(",")))
                collect = list(map(int, fr.readline().strip("\n").split(",")))
                if userid == self.USERID :
                    play=np.array(play)
                    mu=np.mean(play)
                    sigma=np.sqrt((play*play).sum()/DAYS-mu*mu)
                    p = plt.plot(play, "bo", play, "b-", marker="o")
                    d = plt.plot(download, "ro", download, "r-", marker="o")
                    c = plt.plot(collect, "go", collect, "g-", marker="o")
                    plt.legend([p[1], d[1],c[1]], ["play", "download","collect"])
                    plt.title(''.join(('mu=',str(mu),',','sigma=',str(sigma))))
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.savefig(os.path.join(self.USERFOLDER, userid+".png"))
                    plt.clf()
                    break
                userid=fr.readline().strip("\n")

    """根据给出的数据文件得到所有的单独的用户信息"""
    @staticmethod
    def getAllUsers(doAnyway=False):
        if not doAnyway:
            if os.path.exists(ALL_USER):
                user = pickle.load(open(ALL_USER,'rb'),encoding="utf8")
                return user
        user = set([])
        with open(SONGS,'r') as csvfile:     #mars_tianchi_user_actions: user_id,song_id,gmt_create,action_type,Ds
            spamreader = csv.reader(csvfile,delimiter=",")
            for row in spamreader:
                user.add(row[0])
        fw = open(ALL_USER,'wb')
        pickle.dump(user,fw)
        return user

    """该静态方法通过获取所有的用户信息（点击播放，收藏、下载），之后将这些信息根据天数为x轴，次数为y轴进行可视化展示，存放在
    user文件夹下，同时会将当前获得的所有用户信息保存成一个userinfo.dat文件。首先检查这个文件是否存在来进行数据读取。
    """
    @staticmethod
    def getAllUserContent(users,doAnyway=False):
        userContent = {}
        if not doAnyway:
            if os.path.exists(ALL_USER_INFO):
                userContent = pickle.load(open(ALL_USER_INFO,'rb'))
        if len(userContent) == 0:
            with open(USER_P_D_C, "r") as fr:
                userid = fr.readline().strip("\n")
                while userid:
                    play = list(map(int, fr.readline().strip("\n").split(",")))
                    download = list(map(int, fr.readline().strip("\n").split(",")))
                    collect = list(map(int, fr.readline().strip("\n").split(",")))
                    userContent[userid] = [play,download,collect]
                    userid=fr.readline().strip("\n")
                pickle.dump(userContent,open(ALL_USER_INFO,"wb"))

        assert len(users) == len(userContent)
        return userContent


    @staticmethod
    def deplotAllUser(userContent):
        ylabel = "count"
        xlabel = "days"
        for id in userContent:
            play = userContent[id][0]
            download = userContent[id][1]
            collect = userContent[id][2]
            play=np.array(play)
            mu=np.mean(play)
            sigma=np.sqrt((play*play).sum()/DAYS-mu*mu)
            p = plt.plot(play, "bo", play, "b-", marker="o")
            d = plt.plot(download, "ro", download, "r-", marker="o")
            c = plt.plot(collect, "go", collect, "g-", marker="o")
            plt.legend([p[1], d[1],c[1]], ["play", "download","collect"])
            plt.title(''.join(('mu=',str(mu),',','sigma=',str(sigma))))
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.savefig(os.path.join(USER_FOLDER, id+".png"))
            plt.clf()

    @staticmethod
    def userContentFilter(userContent,minsum=10,maxvar = 3.5):    #3.5 is the 90% percentile number
        ret = {}
        for id in userContent:
            tempsum = 0;
            tempsum+=np.sum(userContent[id][0])
            tempsum+=np.sum(userContent[id][1])
            tempsum+=np.sum(userContent[id][2])
            if tempsum>=minsum and np.var(userContent[id][0])<=3.5:
                ret[id] = userContent[id]
        return ret

    @staticmethod
    def userSongRelation(userId,songId,userSongRelation):
        if not os.path.exists(USER_SONG_FOLDER):
            os.mkdir(USER_SONG_FOLDER)
        xlabel = "date"
        ylabel = "counts"
        songcount = userSongRelation[userId][songId]
        nparray = np.array(songcount)
        plt.plot(nparray, "bo", nparray, "b-", marker="o")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(os.path.join(USER_SONG_FOLDER, userId+"_"+songId+".png"))




"""
GOT THE 'PLAY','DOWNLOAD' AND 'COLLECT' TIMES IN 'mars_tianchi_user_action.csv' FILE FOR EVERY DAY.
THEN GOT A 'SONGS' STRUCTURE.
LAST WRITE 'SONGS' INTO SONG.TXT FILE.
SONGS={'SONGS_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]],'SONGS_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]],'SONGS_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]]...}
user={songs_id:[{},{},{},...,{}],songs_id:[{},{},{},...,{}],songs_id:[{},{},{},...,{}]}
"""
def ifNoSongTXT(doAnyway=False):
    if not doAnyway:
        if os.path.exists(SONG_P_D_C) and os.path.exists(SONG_FAN) and os.path.exists(SONG_INFO):
            return

    user = {}
    songs = {}
    with open(SONGS) as csvfile:    #mars_tianchi_user_actions: user_id,song_id,gmt_create,action_type,Ds
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            if row[1] not in songs:
                songs[row[1]] = [[0 for i in range(DAYS)] for j in range(3)]
            songs[row[1]][int(row[3])-1][date2Num(row[4])] += 1

            if row[3] == "1":
                if row[1] not in user:
                    user[row[1]] = [{} for i in range(DAYS)]
                user[row[1]][date2Num(row[4])][row[0]] = True    #user:是一个dict,以song为key，存的是一首歌在记录的时间段内，用户的播放情况。

    with open(SONG_P_D_C, "w") as fw:
        for i in songs:
            fw.write(i+"\n")
            fw.write(",".join(str(x) for x in songs[i][0])+"\n")
            fw.write(",".join(str(x) for x in songs[i][1])+"\n")
            fw.write(",".join(str(x) for x in songs[i][2])+"\n")

    pickle.dump(songs,open(SONG_INFO,'wb'))
    pickle.dump(user,open(SONG_UNIQUE_USER,'wb'))
    with open(SONG_FAN, "w") as fw:
        for i in user:
            fw.write(i+"\n")
            fw.write(",".join(str(len(x)) for x in user[i])+"\n")


"""
BEFORE RUN THIS CODE,PLEASE RUN 'ifNoSongTxt' FIRSTLY!
ARTIST={'ARTIST_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]],'ARTIST_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]],'ARTIST_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]]...}
user={[{user_id:bool...},{user_id:bool...},...,{user_id:bool...}]}
"""
def ifNoArtistTXT(doAnyway=False):
    if not doAnyway:
        if os.path.exists(ARTIST_P_D_C) and os.path.exists(ARTIST_FAN):
            return
    user={}
    artist={}
    index={}
    with open(ARTIST) as csvfile:    #mars_tianchi_songs:song_id,artist_id,publish_time,song_init_plays,Language,gender
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            index[row[0]] = row[1]
            if row[1] not in artist:
                artist[row[1]] = [[0 for i in range(DAYS)] for j in range(3)]
                user[row[1]] = [{} for i in range(DAYS)]

    with open(SONG_P_D_C, "r") as fr:
        songs_id=fr.readline().strip("\n")
        while songs_id:
            temp=[]
            play = list(map(int, fr.readline().strip("\n").split(",")))
            download = list(map(int, fr.readline().strip("\n").split(",")))
            collect = list(map(int, fr.readline().strip("\n").split(",")))
            temp.append(play)
            temp.append(download)
            temp.append(collect)
            t=artist[index[songs_id]]
            for i in range(3):
                for j in range(DAYS):
                    t[i][j]+=temp[i][j]
            artist[index[songs_id]]=t
            songs_id=fr.readline().strip("\n")

    with open(ARTIST_P_D_C, "w") as fw:
        for i in artist:
            fw.write(i+"\n")
            fw.write(",".join(str(x) for x in artist[i][0])+"\n")
            fw.write(",".join(str(x) for x in artist[i][1])+"\n")
            fw.write(",".join(str(x) for x in artist[i][2])+"\n")

    with open(SONGS) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            if row[1] in index:
                user[index[row[1]]][date2Num(row[4])][row[0]]=True

    with open(ARTIST_FAN, "w") as fw:
        for i in user:
            fw.write(i+"\n")
            fw.write(",".join(str(len(x)) for x in user[i])+"\n")

def testForSongTXT():
    count=0
    with open(SONG_P_D_C, "r") as fr:
        songs_id=fr.readline().strip("\n")
        while songs_id:
            temp=[]
            play=list(map(int, fr.readline().strip("\n").split(",")))
            download=list(map(int, fr.readline().strip("\n").split(",")))
            collect=list(map(int, fr.readline().strip("\n").split(",")))
            for i in play:
                count+=i
            for i in download:
                count+=i
            for i in collect:
                count+=i
            songs_id=fr.readline().strip("\n")
    print(count)    #5652232


def ifNoUserTXT(doAnyway=False):
    if not doAnyway:
        if os.path.exists(USER_P_D_C):
            return
    user = {}
    with open(SONGS) as csvfile:     # mars_tianchi_user_actions: user_id,song_id,gmt_create,action_type,Ds
        spamreader = csv.reader(csvfile,delimiter=",")
        for row in spamreader:
            if row[0] not in user:
                user[row[0]] = [[0 for i in range(DAYS)] for j in range(3)]
            user[row[0]][int(row[3])-1][date2Num(row[4])] += 1

    with open(USER_P_D_C,"w") as fw:
        for i in user:
            fw.write(i+"\n")
            fw.write(",".join(str(x) for x in user[i][0])+"\n")
            fw.write(",".join(str(x) for x in user[i][1])+"\n")
            fw.write(",".join(str(x) for x in user[i][2])+"\n")

def getUserSongRelation(doAnyway=False,userContent = None):
        if not doAnyway:
            if os.path.exists(USER_SONG_RELATION):
                usersong = pickle.load(open(USER_SONG_RELATION,'rb'))
                return usersong
        if userContent == None:
            usersong = {}  # usersong={userid,{songid,[0,0,0,0,....,0]}}
            with open(SONGS, 'r') as csvfile:  # mars_tianchi_user_actions: user_id,song_id,gmt_create,action_type,Ds
                spamreader = csv.reader(csvfile, delimiter=",")
                for row in spamreader:
                    if row[0] not in usersong:
                        usersong[row[0]] = {}
                    if row[1] not in usersong[row[0]]:
                        usersong[row[0]][row[1]] = [0 for i in range(DAYS)]
                    usersong[row[0]][row[1]][date2Num(row[4])] += 1



        pickle.dump(usersong,open(USER_SONG_RELATION,'wb'))
        return usersong

def getAllSongs(doAnyways=False):
    if not doAnyways:
        if os.path.exists(ALL_SONG):
            ret = pickle.load(open(ALL_SONG,'rb'))
            return ret
    ret = set([])
    with open(SONG_P_D_C,'r') as fr:
        songs_id=fr.readline().strip("\n")
        while songs_id:
            ret.add(songs_id)
            fr.readline()
            fr.readline()
            fr.readline()
            songs_id=fr.readline().strip("\n")
    print("song numbers: "+str(len(ret)))
    pickle.dump(ret,open(ALL_SONG,'wb'))
    return ret

def saveToLocal(content,fileName):
    pickle.dump(content,open(fileName,'wb'))

if __name__ == "__main__":
    ifNoSongTXT()
    ifNoArtistTXT()
    ifNoUserTXT()
    # a = artist("0c80008b0a28d356026f4b1097041689")
    # a.plot_artist_play()
    # a.plot_artist_fan()
    # a.plot_song_play()
    # a.plot_song_fan()
    u = user("")
    users = user.getAllUsers()
    print(len(users))    # 349946
    userContent = user.getAllUserContent(users)
    userContent = user.userContentFilter(userContent)
    saveToLocal(userContent,USER_INFO_FILTER)
    print(len(userContent))    # 102736
    # user.deplotAllUser(userContent)
    userSongRelation = getUserSongRelation(userContent)
    songs = getAllSongs()
    print(len(songs))

    user.userSongRelation("a0702dcf2cf489518b33e3cae29cda2c","6c2c6e5dd10de972e7db73ac0f8678e9",userSongRelation)
    #total time 371.4s
