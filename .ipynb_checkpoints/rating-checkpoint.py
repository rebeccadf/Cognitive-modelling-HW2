import os
import random
import psutil
import pandas as pd
from PIL import Image

def main():
    rates = []
    name = input('Enter your name:')
    list_im = os.listdir("data")
    random.shuffle(list_im)
    for pic in list_im:
        #os.system(f'start data/{pic}')
        with Image.open(f'data/{pic}') as img:
            img.show()
        flag = True
        while flag:
            rate = input('Enter your rating: 1 (very sad) - 7 (very happy)')
            try:
                if int(rate) >= 1 and int(rate) < 8:
                    flag = False
                else:
                    raise ValueError
            except:
                print("Wrong input. Please enter again.")
        rates.append(rate)
    df = pd.DataFrame(data = {"Image ID": list_im, "Rating": rates})
    df.to_csv(f"{name}.csv")
                    
if __name__ == "__main__":
    main()
    