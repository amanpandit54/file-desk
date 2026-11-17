from pathlib import Path
import os


def createFile():
    try:
        name=input("Enter the filename: ")
        path=Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data=input("Enter file contents: ")
                fs.write(data)
            print("File created successfully..")
        else:
            print("Error: Filename already exists.. ")
    except Exception as err:
        print(f"Error : {err}")

def readFile():
    try:
        filename=input("Enter filename to read:")
        path=Path(filename)
        if path.exists:
            with open(path,"r") as fs:
                print(fs.read())
        else:
            print(f"File with filename: {filename} does not exists..")
    except Exception as err:
        print(f"Error: {err}")
   
def updateFile():
    try:
        name=input("Enter filename to update:")
        path=Path(name)

        if path.exists():
            print("Operations to perform:\n")
            print("1. Rename filename")
            print("2. Append filename")
            print("3. Overwrite filename")
            choice= int(input("Enter your option:"))

            if choice==1:
                newName=input("Enter new name:")
                newPath=Path(newName)
                if not newPath.exists():
                    path.rename(newPath)
                    print("Renamed successfully..")
                else:
                    print("File already exists..")

            elif choice==2:
                newContent=input("Enter content to append:")
                with open(path,"a") as fs:
                    fs.write(" \n"+newContent)
                print("File appended successfully..")

            elif choice==3:
                content=input("Enter content to overwrite:")
                with open(path,"w") as fs:
                    fs.write(content)
                print("File overwritten successfully..")

    except Exception as err:
        print(f"Error: {err}")

def deleteFile():
    try:
        name=input("Enter filename to delete:")
        path=Path(name)
        if path.exists():
            path.unlink()
            print("File deleted successfully..")
        else:
            print("No such file exists..")

    except Exception as err:
        print(f"Error: {err}")


print("Enter 1 to create a file")
print("Enter 2 to read a file")
print("Enter 3 to update a file")
print("Enter 4 to delete a file")

res=int(input("Enter your response:"))

if res==1:
    createFile()
if res==2:
    readFile()
if res==3:
    updateFile()
if res==4:
    deleteFile()

