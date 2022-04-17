import email
from flask import Flask, redirect, url_for, render_template, request
import numpy as np
import pandas as pd
import os
import sqlite3

currentlocation = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route("/")
def main():
    # get num of users
   
    return render_template("home.html")


@app.route("/rate", methods=["GET", "POST"])
def displayComboName():
    global comboName
    if request.method == "POST":
        comboName = request.form["combo"]
        return render_template("rate.html", comboName=comboName)


@app.route("/feedback")
def displayFeedback():
    return render_template("resultSet.html", top=top, bottom=bottom, foot=foot, topName=topName, bottomName=bottomName,
                           footName=footName)


@app.route("/home")
def displayUserHome():
    return render_template("UserMainPage.html", message=message, loginName=loginName, Dtopwear=Dtopwear,
                           Dbottomwear=Dbottomwear, Dfootwear=Dfootwear, DRating=DRating)


@app.route("/viewmoretop")
def displayMoreTopOutfits():
    print(Dtopwear)
    print(Dbottomwear)
    print(Dfootwear)
    return render_template("viewmoretop.html", Dtopwear=Dtopwear, Dbottomwear=Dbottomwear, Dfootwear=Dfootwear,
                           DRating=DRating)


@app.route("/getrating", methods=["GET", "POST"])
def getRating():
    if request.method == "POST":
        rating = request.form["rating"]
        try:
            sqliteconnection = sqlite3.Connection(currentlocation + "\customer_database.db")
            cursor = sqliteconnection.cursor()

            query = """SELECT * from customer_details"""
            cursor.execute(query)
            records = cursor.fetchall()

            for row in records:
                if (row[4] == loginEmail):
                    customerId = row[0]

            if comboName == 'combo1':
                TopId = top[0]
                BottomId = bottom[0]
                FootId = foot[0]
            elif comboName == 'combo2':
                TopId = top[1]
                BottomId = bottom[1]
                FootId = foot[1]
            elif comboName == 'combo3':
                TopId = top[2]
                BottomId = bottom[2]
                FootId = foot[2]
            elif comboName == 'combo4':
                TopId = top[3]
                BottomId = bottom[3]
                FootId = foot[3]
            elif comboName == 'combo5':
                TopId = top[4]
                BottomId = bottom[4]
                FootId = foot[4]
            print(TopId, BottomId, FootId)
            params = (customerId, str(TopId), str(BottomId), str(FootId), rating)
            cursor.execute("INSERT INTO customer_ratings VALUES(?, ?, ?, ?, ?)", params)
            sqliteconnection.commit()
            query2 = """SELECT * from final_combo_ratings"""
            cursor.execute(query2)
            ratingRecords = cursor.fetchall()
            print(len(ratingRecords))
            # to check if same combo exists
            updateStatus = 0
            for row in ratingRecords:
                if ((TopId == row[1]) and (BottomId == row[2]) and (FootId == row[3])):
                    comboId = row[0]
                    finalRating = (rating + row[3]) * 0.5
                    sql_update_query = f"Update final_combo_ratings set rating = '{finalRating}' where comboId = '{comboId}';"
                    cursor.execute(sql_update_query)
                    sqliteconnection.commit()
                    print(finalRating)
                    updateStatus == 1

            if updateStatus == 0:
                params1 = (str(TopId), str(BottomId), str(FootId), rating)
                cursor.execute("INSERT INTO final_combo_ratings VALUES(NULL, ?, ?, ?, ?)", params1)
                sqliteconnection.commit()
                print(rating)

            return render_template("feedback.html", top=top, bottom=bottom, foot=foot, topName=topName,
                                   bottomName=bottomName, footName=footName), {"Refresh": "3; url=/feedback"}



        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)


@app.route("/LoginAndRegistration")
def LoginAndRegistration():
    return render_template("LoginAndRegistration.html")


@app.route("/Login", methods=["GET", "POST"])
def checkLogin():
    if request.method == "POST":
        global loginEmail
        global loginPassword
        global logincount
        global loginName
        global message
        loginEmail = request.form["loginemail"]
        loginPassword = request.form["loginpassword"]
        sqlconnection = sqlite3.Connection(currentlocation + "\customer_database.db")
        cursor = sqlconnection.cursor()
        query = f"SELECT * from customer_details WHERE email = '{loginEmail}' AND password = '{loginPassword}';"
        cursor.execute(query)
        if not cursor.fetchone():
            return render_template("LoginFailed.html"), {"Refresh": "3; url=/LoginAndRegistration"}
        else:

            # update login count
            query1 = f"SELECT * from customer_details"
            cursor.execute(query1)
            rows = cursor.fetchall()
            for row in rows:
                if row[4] == loginEmail:
                    logincount = int(row[6])
                    loginName = row[1]

            logincount = logincount + 1
            logincount = str(logincount)
            sql_update_query = f"Update customer_details set logincount = '{logincount}' where email = '{loginEmail}';"
            cursor.execute(sql_update_query)
            sqlconnection.commit()
            if int(logincount) == 0:
                message = "Hello, "
            else:
                message = "Welcome Back, "

            # get display images for users main page

            global Dtopwear
            global Dbottomwear
            global Dfootwear
            global DRating

            Dtopwear = []
            Dbottomwear = []
            Dfootwear = []
            DRating = []

            query3 = f"SELECT * from final_combo_ratings ORDER BY rating DESC"
            cursor.execute(query3)
            rows2 = cursor.fetchall()
            for row2 in rows2:
                Dtopwear.append(row2[1])
                Dbottomwear.append(row2[2])
                Dfootwear.append(row2[3])
                DRating.append(row2[4])
                print(DRating)

            return render_template("UserMainPage.html", message=message, loginName=loginName, Dtopwear=Dtopwear,
                                   Dbottomwear=Dbottomwear, Dfootwear=Dfootwear, DRating=DRating)


@app.route("/Register", methods=["GET", "POST"])
def checkregister():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        dateofbirth = request.form["dateofbirth"]
        signupEmail = request.form["signupemail"]
        signupPassword = request.form["signuppassword"]
        logincount = 0
        params = (name, gender, dateofbirth, signupEmail, signupPassword, logincount)
        sqlconnection = sqlite3.Connection(currentlocation + "\customer_database.db")
        cursor = sqlconnection.cursor()
        # check if email already registered
        query = f"SELECT * from customer_details WHERE email = '{signupEmail}' AND password = '{signupPassword}';"
        cursor.execute(query)
        if cursor.fetchone():
            return render_template("SignupFailed.html"), {"Refresh": "3; url=/LoginAndRegistration"}
        else:
            cursor.execute("INSERT INTO customer_details VALUES(NULL, ?, ?, ?, ?, ?, ?)", params)
            sqlconnection.commit()
            return render_template("LoginAndRegistration.html")


@app.route("/question")
def question():
    return render_template("question.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    global top
    global bottom
    global foot
    global topName
    global bottomName
    global footName
    UnderTone = ''
    Color1 = ""
    Color2 = ""
    Color3 = ""
    Color4 = ""
    Color5 = ""
    Color6 = ""
    Color7 = ""
    Color8 = ""
    Color9 = ""
    Color10 = ""
    Color11 = ""
    Color12 = ""
    Color13 = ""
    Color14 = ""
    Color15 = ""
    Color16 = ""
    Color17 = ""
    Color18 = ""
    Color19 = ""
    Color20 = ""
    Color21 = ""
    Color22 = ""
    Color23 = ""
    Color24 = ""
    Color25 = ""
    Color26 = ""

    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        dresscode = request.form['dresscode']
        season = request.form['season']
        skintone = request.form['skintone']

        if int(age) < 13 and gender == "Male":
            gender = "Boys"
        elif int(age) < 13 and gender == "Female":
            gender = "Girls"
        elif int(age) > 12 and gender == "Male":
            gender = "Men"
        elif int(age) > 12 and gender == "Female":
            gender = "Women"

            # SkinTone Classification
        if (skintone == "Porcelain" or skintone == "Honey" or skintone == "Almond" or skintone == "Espresso"):
            UnderTone = "Cool"
        if (
                skintone == "Beige" or skintone == "Warm Beige" or skintone == "Natural" or skintone == "Golden" or skintone == "Chestnut"):
            UnderTone = "Warm"
        if (skintone == "Ivory" or skintone == "Warm Ivory" or skintone == "Sand"):
            UnderTone = "Neutral"

        if UnderTone == "Cool":
            Color1 = "Black"
            Color2 = "Blue"
            Color3 = "Charcoal"
            Color4 = "Green"
            Color5 = "Grey"
            Color6 = "Grey Melange"
            Color7 = "Lavender"
            Color8 = "Lime Green"
            Color9 = "Magenta"
            Color10 = "Maroon"
            Color11 = "Multi"
            Color12 = "Pink"
            Color13 = "Purple"
            Color14 = "Sea Green"
            Color15 = "Silver"
            Color16 = "Teal"
            Color17 = "Turquoise Blue"
            Color18 = "White"

        if UnderTone == "Warm":
            Color1 = "Beige"
            Color2 = "Bronze"
            Color3 = "Brown"
            Color4 = "Coffee Brown"
            Color5 = "Green"
            Color6 = "Khaki"
            Color7 = "Lavender"
            Color8 = "Lime Green"
            Color9 = "Magenta"
            Color10 = "Multi"
            Color11 = "Navy Blue"
            Color12 = "Off White"
            Color13 = "Olive"
            Color14 = "Orange"
            Color15 = "Peach"
            Color16 = "Pink"
            Color17 = "Purple"
            Color18 = "Red"
            Color19 = "Rust"
            Color20 = "Sea Green"
            Color21 = "Tan"
            Color22 = "Taupe"
            Color23 = "Teal"
            Color24 = "Turquoise Blue"
            Color25 = "White"
            Color26 = "Yellow"

        if UnderTone == "Neutral":
            Color1 = "Blue"
            Color2 = "Charcoal"
            Color3 = "Cream"
            Color4 = "Green"
            Color5 = "Grey"
            Color6 = "Grey Melange"
            Color7 = "Lime Green"
            Color8 = "Maroon"
            Color9 = "Multi"
            Color10 = "Navy Blue"
            Color11 = "Off White"
            Color12 = "Peach"
            Color13 = "Pink"
            Color14 = "Sea Green"
            Color15 = "Silver"
            Color16 = "Taupe"
            Color17 = "Teal"
            Color18 = "Turquoise Blue"
            Color19 = "White"
            Color20 = "Yellow"

        df = pd.read_csv('ModifiedOutfits.csv')
        print("Find My Outfit ")

        # print(df)

        # Recommend for any skintone
        if skintone == 'Any':

            topwear = df.loc[
                (df['Category'] == 'Topwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & (
                        (df['season'] == season) | (df['season2'] == season) | (df['season'] == 'All'))]

            bw = pd.read_csv('ModifiedOutfits.csv')

            bottomwear = bw.loc[
                (df['Category'] == 'Bottomwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & (
                        (df['season'] == season) | (df['season2'] == season) | (df['season'] == 'All'))]

            fw = pd.read_csv('ModifiedOutfits.csv')

            footwear = fw.loc[
                (df['Category'] == 'Footwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & (
                        (df['season'] == season) | (df['season2'] == season) | (df['season'] == 'All'))]

        # Recommend for any season
        elif season == 'Any':

            topwear = df.loc[
                (df['Category'] == 'Topwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & ((df['baseColour'] == Color1) | (df['baseColour'] == Color2) | (
                            df['baseColour'] == Color3) | (
                                                                 df['baseColour'] == Color4) | (
                                                                     df['baseColour'] == Color5) | (
                                                                     df['baseColour'] == Color6) | (
                                                                     df['baseColour'] == Color7) | (
                                                                 df['baseColour'] == Color8) | (
                                                                     df['baseColour'] == Color9) | (
                                                                     df['baseColour'] == Color10) | (
                                                                     df['baseColour'] == Color11) | (
                                                                 df['baseColour'] == Color12) | (
                                                                     df['baseColour'] == Color13) | (
                                                                     df['baseColour'] == Color14) | (
                                                                     df['baseColour'] == Color15) | (
                                                                 df['baseColour'] == Color16) | (
                                                                     df['baseColour'] == Color17) | (
                                                                     df['baseColour'] == Color18) | (
                                                                     df['baseColour'] == Color19) | (
                                                                 df['baseColour'] == Color20) | (
                                                                     df['baseColour'] == Color21) | (
                                                                     df['baseColour'] == Color22) | (
                                                                     df['baseColour'] == Color23) | (
                                                                 df['baseColour'] == Color24) | (
                                                                     df['baseColour'] == Color25) | (
                                                                     df['baseColour'] == Color26))]

            bw = pd.read_csv('ModifiedOutfits.csv')

            bottomwear = bw.loc[
                (df['Category'] == 'Bottomwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & ((df['baseColour'] == Color1) | (df['baseColour'] == Color2) | (
                            df['baseColour'] == Color3) | (
                                                                 df['baseColour'] == Color4) | (
                                                                     df['baseColour'] == Color5) | (
                                                                     df['baseColour'] == Color6) | (
                                                                     df['baseColour'] == Color7) | (
                                                                 df['baseColour'] == Color8) | (
                                                                     df['baseColour'] == Color9) | (
                                                                     df['baseColour'] == Color10) | (
                                                                     df['baseColour'] == Color11) | (
                                                                 df['baseColour'] == Color12) | (
                                                                     df['baseColour'] == Color13) | (
                                                                     df['baseColour'] == Color14) | (
                                                                     df['baseColour'] == Color15) | (
                                                                 df['baseColour'] == Color16) | (
                                                                     df['baseColour'] == Color17) | (
                                                                     df['baseColour'] == Color18) | (
                                                                     df['baseColour'] == Color19) | (
                                                                 df['baseColour'] == Color20) | (
                                                                     df['baseColour'] == Color21) | (
                                                                     df['baseColour'] == Color22) | (
                                                                     df['baseColour'] == Color23) | (
                                                                 df['baseColour'] == Color24) | (
                                                                     df['baseColour'] == Color25) | (
                                                                     df['baseColour'] == Color26))]

            fw = pd.read_csv('ModifiedOutfits.csv')

            footwear = fw.loc[
                (df['Category'] == 'Footwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & ((df['baseColour'] == Color1) | (df['baseColour'] == Color2) | (
                            df['baseColour'] == Color3) | (
                                                                 df['baseColour'] == Color4) | (
                                                                     df['baseColour'] == Color5) | (
                                                                     df['baseColour'] == Color6) | (
                                                                     df['baseColour'] == Color7) | (
                                                                 df['baseColour'] == Color8) | (
                                                                     df['baseColour'] == Color9) | (
                                                                     df['baseColour'] == Color10) | (
                                                                     df['baseColour'] == Color11) | (
                                                                 df['baseColour'] == Color12) | (
                                                                     df['baseColour'] == Color13) | (
                                                                     df['baseColour'] == Color14) | (
                                                                     df['baseColour'] == Color15) | (
                                                                 df['baseColour'] == Color16) | (
                                                                     df['baseColour'] == Color17) | (
                                                                     df['baseColour'] == Color18) | (
                                                                     df['baseColour'] == Color19) | (
                                                                 df['baseColour'] == Color20) | (
                                                                     df['baseColour'] == Color21) | (
                                                                     df['baseColour'] == Color22) | (
                                                                     df['baseColour'] == Color23) | (
                                                                 df['baseColour'] == Color24) | (
                                                                     df['baseColour'] == Color25) | (
                                                                     df['baseColour'] == Color26))]

        # Recommend for any season and any skintone
        if (skintone == 'Any') and (season == 'Any'):

            topwear = df.loc[
                (df['Category'] == 'Topwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode)]

            bw = pd.read_csv('ModifiedOutfits.csv')

            bottomwear = bw.loc[
                (df['Category'] == 'Bottomwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode)]

            fw = pd.read_csv('ModifiedOutfits.csv')

            footwear = fw.loc[
                (df['Category'] == 'Footwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode)]

        # Recommend for all other compulsory options
        else:

            topwear = df.loc[
                (df['Category'] == 'Topwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & (
                        (df['season'] == season) | (df['season2'] == season) | (df['season'] == 'All')) & (
                            (df['baseColour'] == Color1) | (df['baseColour'] == Color2) | (
                                df['baseColour'] == Color3) | (
                                    df['baseColour'] == Color4) | (df['baseColour'] == Color5) | (
                                        df['baseColour'] == Color6) | (df['baseColour'] == Color7) | (
                                    df['baseColour'] == Color8) | (df['baseColour'] == Color9) | (
                                        df['baseColour'] == Color10) | (df['baseColour'] == Color11) | (
                                    df['baseColour'] == Color12) | (df['baseColour'] == Color13) | (
                                        df['baseColour'] == Color14) | (df['baseColour'] == Color15) | (
                                    df['baseColour'] == Color16) | (df['baseColour'] == Color17) | (
                                        df['baseColour'] == Color18) | (df['baseColour'] == Color19) | (
                                    df['baseColour'] == Color20) | (df['baseColour'] == Color21) | (
                                        df['baseColour'] == Color22) | (df['baseColour'] == Color23) | (
                                    df['baseColour'] == Color24) | (df['baseColour'] == Color25) | (
                                        df['baseColour'] == Color26))]

            bw = pd.read_csv('ModifiedOutfits.csv')

            bottomwear = bw.loc[
                (df['Category'] == 'Bottomwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & (
                        (df['season'] == season) | (df['season2'] == season) | (df['season'] == 'All')) & (
                            (df['baseColour'] == Color1) | (df['baseColour'] == Color2) | (
                                df['baseColour'] == Color3) | (
                                    df['baseColour'] == Color4) | (df['baseColour'] == Color5) | (
                                        df['baseColour'] == Color6) | (df['baseColour'] == Color7) | (
                                    df['baseColour'] == Color8) | (df['baseColour'] == Color9) | (
                                        df['baseColour'] == Color10) | (df['baseColour'] == Color11) | (
                                    df['baseColour'] == Color12) | (df['baseColour'] == Color13) | (
                                        df['baseColour'] == Color14) | (df['baseColour'] == Color15) | (
                                    df['baseColour'] == Color16) | (df['baseColour'] == Color17) | (
                                        df['baseColour'] == Color18) | (df['baseColour'] == Color19) | (
                                    df['baseColour'] == Color20) | (df['baseColour'] == Color21) | (
                                        df['baseColour'] == Color22) | (df['baseColour'] == Color23) | (
                                    df['baseColour'] == Color24) | (df['baseColour'] == Color25) | (
                                        df['baseColour'] == Color26))]

            fw = pd.read_csv('ModifiedOutfits.csv')

            footwear = fw.loc[
                (df['Category'] == 'Footwear') & ((df['gender'] == gender) | (df['gender'] == "Unisex")) & (
                            df['usage'] == dresscode) & (
                        (df['season'] == season) | (df['season2'] == season) | (df['season'] == 'All')) & (
                            (df['baseColour'] == Color1) | (df['baseColour'] == Color2) | (
                                df['baseColour'] == Color3) | (
                                    df['baseColour'] == Color4) | (df['baseColour'] == Color5) | (
                                        df['baseColour'] == Color6) | (df['baseColour'] == Color7) | (
                                    df['baseColour'] == Color8) | (df['baseColour'] == Color9) | (
                                        df['baseColour'] == Color10) | (df['baseColour'] == Color11) | (
                                    df['baseColour'] == Color12) | (df['baseColour'] == Color13) | (
                                        df['baseColour'] == Color14) | (df['baseColour'] == Color15) | (
                                    df['baseColour'] == Color16) | (df['baseColour'] == Color17) | (
                                        df['baseColour'] == Color18) | (df['baseColour'] == Color19) | (
                                    df['baseColour'] == Color20) | (df['baseColour'] == Color21) | (
                                        df['baseColour'] == Color22) | (df['baseColour'] == Color23) | (
                                    df['baseColour'] == Color24) | (df['baseColour'] == Color25) | (
                                        df['baseColour'] == Color26))]

        # convert dataframe id column to string
        Stringtopwear = topwear['id'].astype({"id": str})
        Stringbottomwear = bottomwear['id'].astype({"id": str})
        Stringfootwear = footwear['id'].astype({"id": str})

        # Empty list to get rated outfits
        Rtopwear = []
        Rbottomwear = []
        Rfootwear = []
        if int(logincount) < 100:
            # assign outfits
            sqlconnection = sqlite3.Connection(currentlocation + "\customer_database.db")
            cursor = sqlconnection.cursor()
            query1 = f"SELECT * from final_combo_ratings ORDER BY rating DESC"
            cursor.execute(query1)
            rows = cursor.fetchall()
            # count 5 sets of outfits
            outfitcount = 0
            for row in rows:

                if (row[1] in Stringtopwear) and (row[2] in Stringbottomwear) and (row[3] in Stringfootwear):
                    Rtopwear.append(row[1])
                    Rbottomwear.append(row[2])
                    Rfootwear.append(row[3])
                    outfitcount = outfitcount + 1
                    print(Rtopwear)
                    print(Rbottomwear)
                    print(Rfootwear)

                # break after getting 5 sets
                if outfitcount == 5:
                    break

            if outfitcount < 5:

                try:
                    # Get 5 sets of outfits
                    top = topwear['id'].sample(5).to_numpy()
                    topName = topwear['productDisplayName'].sample(5).to_numpy()

                    bottom = bottomwear['id'].sample(5).to_numpy()
                    bottomName = bottomwear['productDisplayName'].sample(5).to_numpy()

                    foot = footwear['id'].sample(5).to_numpy()
                    footName = footwear['productDisplayName'].sample(5).to_numpy()

                    # resultSet = {age, gender, event, season}

                except:

                    return render_template("noOutfitsFound.html"), {"Refresh": "3; url=/question"}

            else:
                # assign Rated outfits
                top = Rtopwear
                bottom = Rbottomwear
                foot = Rfootwear



        else:
            try:
                # Get 5 sets of outfits
                print("Reccomended Topwear")
                top = topwear['id'].sample(5).to_numpy()
                topName = topwear['productDisplayName'].sample(5).to_numpy()

                print("Reccomended Bottomwear")
                bottom = bottomwear['id'].sample(5).to_numpy()
                bottomName = bottomwear['productDisplayName'].sample(5).to_numpy()

                print("Reccomended Footwear")
                foot = footwear['id'].sample(5).to_numpy()
                footName = footwear['productDisplayName'].sample(5).to_numpy()

                # resultSet = {age, gender, event, season}

            except:

                return render_template("noOutfitsFound.html"), {"Refresh": "3; url=/question"}

        return render_template("resultSet.html", top=top, bottom=bottom, foot=foot, topName=topName,
                               bottomName=bottomName, footName=footName)
        # return redirect(url_for('answer', answer=resultSet))


if __name__ == "__main__":
    app.debug = True
    app.run()
