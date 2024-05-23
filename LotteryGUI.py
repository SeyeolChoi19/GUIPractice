import threading, playsound, random

import datetime as dt 
import pandas   as pd 

from BasicMethods import BasicMethods 

class LotteryGUI(BasicMethods):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def lottery_gui_settings_method(self, sound_effect_file: str, names_list: str):
        self.sound_effect_file  = sound_effect_file
        self.company_name_table = pd.read_excel(names_list)
        self.company_names_list = [(name.strip(), f"{title.strip()}님") for (name, title) in zip(list(self.company_name_table["이름"]), list(self.company_name_table["호칭"]))]
        self.winners_list       = f"./{str(dt.datetime.now().date())}_winners_list.txt"

    def __countdown(self, status_window):
        def update_countdown(count_in_seconds: int):
            if (count_in_seconds > 0):
                status_window.delete("1.0", "end")
                status_window.insert("1.0", f"\n\n{count_in_seconds}")
                status_window.tag_add("tag_name", "1.0", "end")
                count_in_seconds -= 1
                status_window.after(1000, update_countdown, count_in_seconds)
            else:
                random_name = random.choice(self.company_names_list)
                self.company_names_list.remove(random_name)
                status_window.delete("1.0", "end")
                status_window.insert("1.0", f"\n\n{random_name[0]} {random_name[1]}")
                status_window.tag_add("tag_name", "1.0", "end")

                with open(self.winners_list, "a", encoding = "utf-8") as f:
                    f.write(f"{str(dt.datetime.now())[0:16]} {random_name[0]} {random_name[1]}\n")

        update_countdown(5)
    
    def __backend_logic(self, status_window):
        threading.Thread(target = playsound.playsound, args=(self.sound_effect_file,)).start()
        self.__countdown(status_window)

    def random_name_generator(self):
        label_object  = self.create_label(" ", 0.05, 0.05)
        status_window = self.create_text_bar(5, 0, 0, 0.05, 0.1, 729, state = "normal", font_size = 55)
        status_window.tag_configure("tag_name", justify = "center")
        label_object.config(text = "랜덤 이름 뽑기")
        self.create_button("시작", lambda x: self.__backend_logic(status_window), 0.047, 0.90, 1, button_width = 103)

if (__name__ == "__main__"):
    lottery_object = LotteryGUI("랜덤 이름 뽑기", "Calibri")
    lottery_object.settings_method({"csv" : "csv"},  800, 600, 12)
    lottery_object.lottery_gui_settings_method("C:/Users/User/Downloads/065391_drumrollwav-88344.mp3", r"C:\Users\User\scrapDirectory\2024-05-23_에니어그램 결과.xlsx")
    lottery_object.random_name_generator()
    lottery_object.window.mainloop()
