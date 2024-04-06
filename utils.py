import pandas as pd

df = pd.read_csv("data/sau_respostas_form.csv")

def column_items(index:int):
    items = []
    for i in df[df.columns[index]]:
        items.append(i)
    return items

def unique_items(items:list):
    unique = []
    for n in items:
        if n not in unique:
            unique.append(n)
    return unique

def count_ocurrences(items: list, x: any):
    count = 0
    for i in items:
        if (i == x):
            count = count + 1
    return count

def config_strlabel(label: str):
    count = 0
    line_break_char = 0
    for char in label:
        print(char)
        count = count + 1
    for i in range(0, 100):
        if i % count == 0:
            line_break_char = count / 2
            return label[:int(line_break_char)] + "\n" + label[int(line_break_char) + 1:]
        
def calculate_percentage_of_value(major: int, minor: int):
    diff = major - minor
    ratio = diff / major
    return ratio * 100
    
def split_all_items(x: list, alias: str, index: int, expections: list):
    for subitems in column_items(index):
        subitems = subitems.split(alias)
        for item in subitems:
            if item not in expections:
                x.append(item)
            else:
                pass
def rm_leading_whitespace(y: list):
    items_to_rm = []
    for item in y:
        if item.startswith(' '):
            items_to_rm.append(item)
        for item2 in items_to_rm:
                if item2 in y:
                    y[y.index(item)] = item2.lstrip(' ')

def rm_duplicated_item_by_key(y: list, key: str):
    for i in y:
        if i == key:
            y.remove(i)

def rm_multiples_duplicated_items(y: list, alias: str):
    count_to_rm = 0
    for rm in y:
        if alias in rm:
                count_to_rm = count_to_rm + 1
                index_to_rm = y.index(rm)
        if count_to_rm > 1:
            y.remove(y[index_to_rm])

def check_item_equality(y: list, x: list, item_index: int):
    count = 0
    for i in x:
        if i in y[item_index]:
            count = count + 1
    return count