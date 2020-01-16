ListenFlag = 1
X = 4
Y = 5

f = open("settings.csv", "w")
f.write(f"L,X,Y\n{ListenFlag},{X},{Y}")
f.close()
