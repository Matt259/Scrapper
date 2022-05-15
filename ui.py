import json
import tkinter as tk
from tkinter import filedialog, END, messagebox



from main import soupActivation
import pymongo
from pymongo import MongoClient
#import dnspython
#tinker imports

#luster = MongoClient("mongodb+srv://duckmeat:duckmeat123@cluster0.92tmn.mongodb.net/games?retryWrites=true&w=majority")



#firebase/mongo
def filter(gameNames, gamePrices):
    gameText.delete('1.0', END)

    gamePriceInput =  priceText.get("1.0", END)
    gameSearchInput = searchText.get("1.0", END)
    gameSearchInput=gameSearchInput.replace('\n','')


    if len(gamePriceInput)<=1 and len(gameSearchInput)<=1:
        index = 0
        while index <= len(gameNames) - 1:
            gameText.insert(tk.END,'Game name: {0} ; Game Price: {1}' .format({gameNames[index]},{gamePrices[index]})+'\n')
            index=index+1

    elif len(gamePriceInput)>1 and len(gameSearchInput) <=1:
        numberCheck = checkIfNumber()
        if numberCheck == True:
            index=0
            foundPrices=0
            while index <= len(gameNames)-1:
                if float(priceText.get("1.0", END)) >=float(gamePrices[index]):
                    gameText.insert(tk.END, 'Game name: {0} ; Game Price: {1}'.format({gameNames[index]},{gamePrices[index]}) + '\n')
                    index = index + 1
                    foundPrices=foundPrices+1
                else:
                    index=index+1
            if foundPrices == 0:
                messagebox.showinfo("Price point", "Unfortunately none of the games match that price")
        else:
            messagebox.showerror("Price", "Please insert a number")

    elif len(gamePriceInput)<=1 and len(gameSearchInput)>1:
        gameNamesFiltered,gamePricesFiltered=findMatchingGames(gameNames,gamePrices)
        if len(gameNamesFiltered)<=0:
            messagebox.showinfo("Description", "Unfortunately there were no games found that match that description")
        else:
            index=0
            while index<=len(gamePricesFiltered)-1:
                gameText.insert(tk.END, 'Game name: {0} ; Game Price: {1}'.format({gameNamesFiltered[index]},{gamePricesFiltered[index]}) + '\n')
                index=index+1

    elif len(gameSearchInput)>1 and len(gamePriceInput)>1:
        numberCheck = checkIfNumber()
        if numberCheck == True:
            index = 0
            foundMatches = 0
            while index <= len(gameNames) - 1:
                if float(priceText.get("1.0", END)) >= float(gamePrices[index]) and gameSearchInput.lower() in gameNames[index].lower():
                    gameText.insert(tk.END, 'Game name: {0} ; Game Price: {1}'.format({gameNames[index]},{gamePrices[index]}) + '\n')
                    index = index + 1
                    foundMatches = foundMatches + 1
                else:
                    index = index + 1
            if foundMatches == 0:
                messagebox.showinfo("Description", "Unfortunately none of the games match those descriptions")
        else:
            messagebox.showerror("Price", "Please insert a number")



def findMatchingGames(gameNames,gamePrices):

    gameNamesFiltered=[]
    gamePricesFiltered=[]
    gameSearchInput = searchText.get("1.0", END)
    gameSearchInput=gameSearchInput.replace('\n','')

    index = 0
    while index <=  len(gameNames)-1:
        if gameSearchInput.lower() in gameNames[index].lower():
            gameNamesFiltered.append(gameNames[index])
            gamePricesFiltered.append(gamePrices[index])
            index=index+1
        else:
            index=1+index
    return gameNamesFiltered,gamePricesFiltered

def checkIfNumber():
    gamePriceInput = priceText.get("1.0", END)
    try:
        parsed=float(gamePriceInput)
        if type(parsed)==float:
            return True
    except ValueError:
        return False

def printGames(gameNames, gamePrices):
    if gameText.compare("end-1c", "==", "1.0"):
        messagebox.showerror("Print to text file", "Error, no data in primary window")
    else:
        file = filedialog.asksaveasfile(defaultextension='*.txt', filetypes=[("Text file",".txt"),("HTML file", ".html"),("All files", ".*"),])
        file.write(str(gameText.get('1.0',END)))
        file.close()
        messagebox.showinfo("Print to text file", "File saved successfully")

def gamesToDB(cluster):
    games = gameText.get("1.0", END)
    db = cluster["games"]
    collection = db["data"]
    if len(games)<=1:
        messagebox.showerror("DB", "Error, no data in primary window")
    else:
        gamePriceInput = priceText.get("1.0", END)
        gameSearchInput = searchText.get("1.0", END)
        gameSearchInput = gameSearchInput.replace('\n', '')
        if len(gamePriceInput) <= 1 and len(gameSearchInput) <= 1:
            index = 0
            while index <= len(gameNames) - 1:
                post = {"games": gameNames[index], "price": gamePrices[index]}
                collection.insert_many([post])
                index = index + 1

        elif len(gamePriceInput) > 1 and len(gameSearchInput) <= 1:
            numberCheck = checkIfNumber()
            if numberCheck == True:
                index = 0
                foundPrices = 0
                while index <= len(gameNames) - 1:
                    if float(priceText.get("1.0", END)) >= float(gamePrices[index]):
                        post = {"games": gameNames[index], "price": gamePrices[index]}
                        collection.insert_many([post])
                        index = index + 1
                        foundPrices = foundPrices + 1
                    else:
                        index = index + 1
                if foundPrices == 0:
                    messagebox.showinfo("Price point", "Unfortunately none of the games match that price")
            else:
                messagebox.showerror("Price", "Please insert a number")

        elif len(gamePriceInput) <= 1 and len(gameSearchInput) > 1:
            gameNamesFiltered, gamePricesFiltered = findMatchingGames(gameNames, gamePrices)
            if len(gameNamesFiltered) <= 0:
                messagebox.showinfo("Description","Unfortunately there were no games found that match that description")
            else:
                index = 0
                while index <= len(gamePricesFiltered) - 1:
                    post = {"games": gameNames[index], "price": gamePrices[index]}
                    collection.insert_many([post])
                    index = index + 1

        elif len(gameSearchInput) > 1 and len(gamePriceInput) > 1:
            numberCheck = checkIfNumber()
            if numberCheck == True:
                index = 0
                foundMatches = 0
                while index <= len(gameNames) - 1:
                    if float(priceText.get("1.0", END)) >= float(gamePrices[index]) and gameSearchInput.lower() in gameNames[index].lower():
                        post = {"games": gameNames[index], "price": gamePrices[index]}
                        collection.insert_many([post])
                        index = index + 1
                        foundMatches = foundMatches + 1
                    else:
                        index = index + 1
                if foundMatches == 0:
                    messagebox.showinfo("Description", "Unfortunately none of the games match those descriptions")
            else:
                messagebox.showerror("Price", "Please insert a number")



#Creates the actual GUI/Pack is for attaching
root = tk.Tk()
root.title('game search')
root.geometry("500x500")
canvas = tk.Canvas(root,height=700,width =700,bg="#263D42")
canvas.pack()


#main field where games are printed
gameText=tk.Text(root,width=55,height=22,relief='groove',wrap='word')
gameText.place(x=5,y=5)


#Gets the value, depending on which option the user chooses, and stores it in v
#Anything left side filter related such as platforms,genres and operating systems
frame = tk.Canvas(root,height=120,width=120,bg='grey')
frame.place(x=0,y=375)


#filter fields from which the user can sort games by name or price
searchLabel=tk.Label(root,text="Find game by name",fg='black',bg='grey').place(x=5,y=380)
searchText=tk.Text(root,width=13,height=1,relief='groove',wrap='word',borderwidth=3)
searchText.place(x=5,y=400)

priceLabel=tk.Label(root,text="Price less or equal to",fg='black',bg='grey').place(x=5,y=440)
priceText=tk.Text(root,width=10,height=1,relief='groove',wrap='word',borderwidth=3)
priceText.place(x=5,y=460)


#buttons, 1 prints the textfields data to a txt file the other one shows the games based on filter input or just prints out all the games
gameNames, gamePrices = soupActivation()
searchButton = tk.Button(root,text="Search", padx=10,pady=5,fg="pink",bg="black",command =lambda:filter(gameNames, gamePrices))
searchButton.place(x=420,y=450)
textFileButton=tk.Button(root,text="Print", padx=10,pady=5,fg="pink",bg="black",command =lambda:printGames(gameNames, gamePrices))
textFileButton.place(x=340,y=450)
#bButton=tk.Button(root,text="DB", padx=10,pady=5,fg="pink",bg="black",command =lambda:gamesToDB(cluster))
#bButton.place(x=250,y=450)

#runs the GUI
root.mainloop()
