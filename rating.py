import os
import random
import pandas as pd
from PIL import Image

def main():
    rates = []
    name = input('Enter your name: ')
    list_im = [f for f in os.listdir("data") if not f.startswith('.')]
    random.shuffle(list_im)
    for pic in list_im:
        #os.system(f'start data/{pic}')
        with Image.open(f'data/{pic}') as img:
            img.show()
        flag = True
        while flag:
            rate = input('Enter your rating from 1 (very sad) to 7 (very happy): ')
            try:
                if int(rate) >= 1 and int(rate) < 8:
                    flag = False
                else:
                    raise ValueError
            except:
                print("Wrong input. Please enter again.")
        rates.append(rate)
    df = pd.DataFrame(data = {"Image_ID": list_im, "Rating": rates})
    df.to_csv(f"{name}.csv")
                    
if __name__ == "__main__":
    main()
    