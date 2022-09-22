import os 
import shutil

def main():
    for subject in os.listdir("KDEF"):
        for pic in os.listdir(f"KDEF/{subject}"):
            if pic[6] == "S":
                if pic[4:6] in ["HA", "NE", "SA"]:
                    shutil.copyfile(f"KDEF/{subject}/{pic}", f"data/{pic}")
                
                

if __name__ == "__main__":
    main()
            