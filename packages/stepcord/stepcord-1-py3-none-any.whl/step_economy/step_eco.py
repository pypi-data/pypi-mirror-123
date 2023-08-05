from logging import error
import discord
from discord.ext import commands 
import sqlite3
import random



def on_ready_ustaw():
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS finanse(guild_id STR, user_id INT, bank INT , portfel INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS sklep(guild_id STR, cena INT, item STR, ranga INT)")
    db.commit()
    cursor.close()
    db.close()

def top_bank(user: discord.User, ilosc_top:int):
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} ORDER BY bank DESC LIMIT {ilosc_top}")
    xxx = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return xxx

def top_gotowka(user: discord.User, ilosc_top:int):
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} ORDER BY portfel DESC LIMIT {ilosc_top}")
    xxx = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return xxx

def na_start(gotowka, bank, user: discord.User):
    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} AND user_id = {user.id}")
    finanse = cursor.fetchone()
    if finanse:
        return
    if finanse == None:
        sql = "INSERT INTO finanse(guild_id, user_id, bank, portfel) VALUES(?,?,?,?)"
        val = (user.guild.id, user.id, int(bank), int(gotowka))
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()



def add_money(ilość_max:int, ilość_min:int, user: discord.User):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} AND user_id = {user.id}")
    finanse = cursor.fetchone()
    if finanse:
        zarobione = random.randint(ilość_max, ilość_min)
        cursor.execute(f"UPDATE finanse SET portfel = {finanse[3]} + {int(zarobione)} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
        db.commit()
        cursor.close()
        db.close()
        return zarobione
    else:
        db.commit()
        cursor.close()
        db.close()
        error = 'Error: developer nie ustawił w tym poleceniu poleceniu `na_start()`'
        return error



def info_bank(member: discord.Member):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {member.guild.id} AND user_id = {member.id}")
    finanse = cursor.fetchone()
    
    db.commit()
    cursor.close()
    db.close()

    if finanse:
        return finanse[2]
    else:

        error = 'Error: developer nie ustawił w tym poleceniu poleceniu `na_start()`'
        return error



def info_gotowka(member: discord.Member):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {member.guild.id} AND user_id = {member.id}")
    finanse = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    if finanse:
        return finanse[3]
    else:
        error = 'Error: developer nie ustawił w tym poleceniu poleceniu `na_start()`'
        return error

def admin_daj_gotowke(ilosc_gotowki:int, user: discord.User ,member: discord.Member):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {member.guild.id} AND user_id = {member.id}")
    finanse_member = cursor.fetchone()

    cursor.execute(f"UPDATE finanse SET portfel = {finanse_member[3]} + {ilosc_gotowki} WHERE guild_id= {user.guild.id} AND user_id = {member.id}")

    db.commit()
    cursor.close()
    db.close()
    return ilosc_gotowki


def daj_gotowke(ilosc_gotowki:int, user: discord.User, member: discord.Member, blad):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {member.guild.id} AND user_id = {member.id}")
    finanse_member = cursor.fetchone()

    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} AND user_id = {user.id}")
    finanse_user = cursor.fetchone()

    if ilosc_gotowki <= int(finanse_user[3]):
        cursor.execute(f"UPDATE finanse SET portfel = {finanse_user[3]} - {ilosc_gotowki} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
        cursor.execute(f"UPDATE finanse SET portfel = {finanse_member[3]} + {ilosc_gotowki} WHERE guild_id= {user.guild.id} AND user_id = {member.id}")
        db.commit()
        cursor.close()
        db.close()
        return ilosc_gotowki
    else:
        return blad

def wplac(ilosc_gotowki:int, user: discord.User, blad):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} AND user_id = {user.id}")
    finanse_user = cursor.fetchone()

    if ilosc_gotowki <= int(finanse_user[3]):
        cursor.execute(f"UPDATE finanse SET portfel = {finanse_user[3]} - {ilosc_gotowki} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
        cursor.execute(f"UPDATE finanse SET bank = {ilosc_gotowki} + {finanse_user[2]} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
        db.commit()
        cursor.close()
        db.close()
        return ilosc_gotowki
    else:
        return blad

def wyplac(ilosc:int, user: discord.User, blad):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} AND user_id = {user.id}")
    finanse_user = cursor.fetchone()

    if ilosc <= int(finanse_user[2]):
        cursor.execute(f"UPDATE finanse SET bank = {finanse_user[2]} - {ilosc} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
        cursor.execute(f"UPDATE finanse SET portfel = {ilosc} + {finanse_user[3]} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
        db.commit()
        cursor.close()
        db.close()
        return ilosc
    else:
        return blad

def okradanie(user: discord.User, member: discord.Member):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {member.guild.id} AND user_id = {member.id}")
    finanse_member = cursor.fetchone()

    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} AND user_id = {user.id}")
    finanse_user = cursor.fetchone()

    cursor.execute(f"UPDATE finanse SET portfel = {finanse_user[3]} + {finanse_member[3]} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
    cursor.execute(f"UPDATE finanse SET portfel = 0 WHERE guild_id= {user.guild.id} AND user_id = {member.id}")
    db.commit()
    cursor.close()
    db.close()
    return finanse_member[3]


def sklep(user: discord.User):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM sklep WHERE guild_id= {user.guild.id}")
    wynik = cursor.fetchall()   
    db.commit()
    cursor.close()
    db.close()
    return wynik

def dodaj_item_do_sklepu(user: discord.User, cena:int, item:str, ranga):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO sklep(guild_id,item, cena, ranga) VALUES(?,?,?,?)", (user.guild.id,item, cena, ranga))
    db.commit()
    cursor.close()
    db.close()
    return

def usun_item_ze_sklepu(user: discord.User, nazwa_itemu_ze_sklepu:str, blad):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM sklep WHERE guild_id= {user.guild.id}")
    wynik = cursor.fetchall()
    xyz = 0
    if wynik:
        for x in wynik:
            if x[2] == nazwa_itemu_ze_sklepu:
                cursor.execute(f"DELETE FROM sklep WHERE guild_id = ? AND item = ? AND cena = ? AND ranga = ?", (x[0],x[2],x[1],x[3]))
                db.commit()
                cursor.close()
                db.close()
                xyz += 1
                return x[2]
    if xyz == 0:
        return blad

def kup_item_ze_sklepu(user: discord.User, nazwa_itemu_ze_sklepu, blad_brak_finansów):    
    db = sqlite3.connect("economy.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM finanse WHERE guild_id = {user.guild.id} AND user_id = {user.id}")
    finanse_user = cursor.fetchone()

    cursor.execute(f"SELECT * FROM sklep WHERE guild_id= {user.guild.id}")
    wynik = cursor.fetchall()

    xyz = 0 

    if wynik:
        for x in wynik:
            if x[2] == nazwa_itemu_ze_sklepu:
                if x[1] <= finanse_user[3]: #sprawdza czy masz finanse na to 
                    
                    if x[3] == 0:
                        xyz = 1
                        rola_za_zakup = "Brak rangi za ten item."
                        cursor.execute(f"UPDATE finanse SET portfel = {finanse_user[3]} - {x[1]} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
                        db.commit()
                        cursor.close()
                        db.close()
                        return rola_za_zakup, xyz

                    xyz = 2 #jeżeli tak xyz == 2

                    rola_za_zakup = discord.utils.get(user.guild.roles, id=x[3])

                    for rola in user.guild.roles:
                        if rola_za_zakup == rola:
                            cursor.execute(f"UPDATE finanse SET portfel = {finanse_user[3]} - {x[1]} WHERE guild_id= {user.guild.id} AND user_id = {user.id}")
                            db.commit()
                            cursor.close()
                            db.close()
                            xyz = 3 #jeżeli jest taka ranga xyz == 3

                            return rola_za_zakup, xyz
                else:
                    return blad_brak_finansów, xyz

                if xyz == 2:
                    blad_zle_id = "Admin wprowadził błędne id rangi"
                    return blad_zle_id, xyz
            else:
                blad_zla_nazwa = "Wprowadziłeś złą nazwę"
                xyz = 4
                return blad_zla_nazwa, xyz