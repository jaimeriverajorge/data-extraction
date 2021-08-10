import matplotlib.pyplot as plt

myDict = {(1, 2): True, (3, 4): False}
myList = [(10, 2), (35, 14)]
for i in myDict:
    print(i)

plt.plot(myList[0], myList[1], c="r")
plt.show()
