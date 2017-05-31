def removeExistingData(existing, new):
    # Remove data we alredy have from the list of new data to parse
    print(existing)
    print(new)
    for i in new[:]:
        if i in existing:
            new.remove(i)
            print(new)
    print("%s new items to add." % (len(new)))
    return new


def fixArray(array, value):
    for i in range(0, len(array)):
        if len(array[i]) < value:
            for b in range(0, len(array[i])):
                array.append(array[i][b])
            array.remove(array[i])
    return array

array = [[1, 2, 3], [3, 4, 5], [["a", "b", "c"], ["c", "d", "e"]], [5, 6, 7]]
value = 3
array1 = [1, 2, 3, 4]
array2 = [2, 3, 5]
# print(removeExistingData(array1, array2))
print(array)
print(fixArray(array, value))
