from appJar import gui
from register import register
from login import login
app = gui("Banking Stack")
credentialPath = ""
loggedIn = False
def loginPress():
    app.startSubWindow("Login",modal=True)
    
    app.addLabel("userLab", "Username:", 1, 0)
    app.addEntry("userEnt", 1, 1)
    app.addLabel("passLab", "Password:", 2, 0)
    app.addEntry("passEnt", 2, 1)
    app.addButtons(["Submit","Cancel"], loginButton,colspan=2)
    app.stopSubWindow()
    app.showSubWindow("Login")
    print("login")
def exitApplication():
    app.destroySubWindow("Application")
    credentialPath = ""
    loggedIn = False
    app.setTransparency(100)
def registerPress():
    app.startSubWindow("Register",modal=True)
    app.addLabel("spacer", " ")
    app.addLabel("nameLab", "Name:", 2, 0)
    app.addEntry("userNam", 2, 1)
    app.addLabel("userLab", "Username:", 3, 0)
    app.addEntry("userEnt", 3, 1)
    app.addLabel("mailLab", "Email:", 4, 0)
    app.addEntry("userMail", 4, 1)
    app.addLabel("passLab", "Password:", 5, 0)
    app.addEntry("passEnt", 5, 1)
    app.addLabel("spacer2", " ")
    app.addButtons(["Submit","Cancel"], registerButton,colspan=2)
    app.stopSubWindow()
    app.showSubWindow("Register")
    print("register")
    
def exitPress():
    app.stop()
    
def loginButton(btn):
    if btn == "Submit":
        exit_tuple = login(app.getEntry("userEnt"),app.getEntry("passEnt"))
        if exit_tuple[0] == False:
            app.errorBox("Invalid Input",exit_tuple[1])
        else:
            loggedIn = exit_tuple[0]
            credentialPath = exit_tuple[1]
            app.destroySubWindow("Login")
            app.setTransparency(0)
            app.startSubWindow("Application",modal=True)
            app.addImage("banktemp","bankingstack.png")
            app.addIconButton("Logout",exitApplication,"Logout")
            app.stopSubWindow()
            app.showSubWindow("Application")

        print("submit")
    
    if btn == "Cancel":
        app.destroySubWindow("Login")

def registerButton(btn):
    if btn == "Submit":

        exit_tuple = register(app.getEntry("userEnt"),app.getEntry("passEnt"),app.getEntry("userMail"))
        if exit_tuple[0] == False:
            app.errorBox("Invalid Input",exit_tuple[1])
        else:
            app.destroySubWindow("Register")

        
    
    if btn == "Cancel":
        app.destroySubWindow("Register")



def progGUI():

    app.addImage("bank","bankingstack.png")
    app.addButton("Login",loginPress)
    app.addButton("Register",registerPress)
    app.addButton("Exit",exitPress)
    app.go()



progGUI()