import tkinter as tk
import pickle
from PIL import Image, ImageDraw, ImageOps, ImageTk
import os
import torch
from digit_recognizer import DigitRecognizer
from torchvision import transforms as tt
from shapely.geometry import LineString


class BoundingBox:
    def __init__(self, xmin=10000, ymin=10000, xmax=0, ymax=0):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
    
    def update_min_max(self, x, y):
        # this func serves for update min and max x y values
        if x > self.xmax:
            self.xmax = x
        if y > self.ymax:
            self.ymax = y
        if x < self.xmin:
            self.xmin = x
        if y < self.ymin:
            self.ymin = y

    def get_squared_cords(self):
        # this func expands image lower axis from both sides to make it square
        x_len = self.xmax - self.xmin
        y_len = self.ymax - self.ymin
        if x_len > y_len:
            diff = x_len - y_len
            squared_ymin = self.ymin - diff / 2
            squared_ymax = self.ymax + diff / 2
            return self.xmin, squared_ymin, self.xmax, squared_ymax
        elif y_len > x_len:
            diff = y_len - x_len
            squared_xmin = self.xmin - diff / 2
            squared_xmax = self.xmax + diff / 2
            return squared_xmin, self.ymin, squared_xmax, self.ymax
        else:
            return self.xmin, self.ymin, self.xmax, self.ymax
    
    def get_cords(self):
        return self.xmin, self.ymin, self.xmax, self.ymax
    
    def intersects(self, bounding_box):
        if self.xmin < bounding_box.xmax and self.xmax > bounding_box.xmin and self.ymin < bounding_box.ymax and self.ymax > bounding_box.ymin:
            return True
    
    def combine(self, bounding_box):
        self.xmin = min(self.xmin, bounding_box.xmin)
        self.ymin = min(self.ymin, bounding_box.ymin)
        self.xmax = max(self.xmax, bounding_box.xmax)
        self.ymax = max(self.ymax, bounding_box.ymax)
        return BoundingBox(self.xmin, self.ymin, self.xmax, self.ymax)
        

class Line:
    def __init__(self, line):
        self.line = line
    
    def append(self, x, y):
        self.line.append([x, y])
    
    def intersects(self, sec_line):
        linestring = LineString(self.line)
        sec_linestring = LineString(sec_line.line)
        return linestring.intersects(sec_linestring)
    
    def combine(self, sec_line):
        self.line = self.line.extend(sec_line.line)


class Exercise:
    def __init__(self):
        self.elements = []
        self.bounding_boxes = []
        self.lines = []
        self.folder_path = "/Users/osiprovin/Desktop/ml:dl/CV/Magic math notebook/DIGITS_examples"
        self.display_current_task()
        self.idx_to_replace = None
    
    def add(self, element, cords, line):
        self.elements.append(element)
        self.bounding_boxes.append(cords)
        self.lines.append(line)
        self.display_current_task()
    
    def pop(self, idx=-1):
        element = self.elements.pop(idx)
        bounding_box = self.bounding_boxes.pop(idx)
        line = self.lines.pop(idx)
        self.display_current_task()
        return element, bounding_box, line

    def get_element(self, idx):
        return self.elements[idx] if len(self.elements) > abs(idx) else None
    
    def get_image_size(self, idx):
        return self.bounding_boxes[idx] if len(self.bounding_boxes) > abs(idx) else None
    
    def solve(self):
        return eval("".join(self.elements))

    def answer_to_list(self, answer):
        return [i for i in str(answer)]
    
    def get_avarage_size(self):
        sum_x, sum_y = 0, 0
        for bounding_box in self.bounding_boxes:
            sum_x += bounding_box.xmax - bounding_box.xmin
            sum_y += bounding_box.ymax - bounding_box.ymin
        return int(sum_x / len(self.bounding_boxes)), int(sum_y / len(self.bounding_boxes))
    
    def draw_answer(self, answer, equal_sign_bounding_box):
        equal_sign_centr_x = (equal_sign_bounding_box.xmin + equal_sign_bounding_box.xmax) / 2
        equal_sign_centr_y = (equal_sign_bounding_box.ymin + equal_sign_bounding_box.ymax) / 2

        buffer = 80
        x = equal_sign_centr_x + buffer

        buffer_between_digits = 12

        symbols = self.answer_to_list(answer)
        avarage_size = self.get_avarage_size()
        resize =  tt.transforms.Resize(avarage_size)
        for symbol in symbols:
            image_name = f"{symbol}.png"
            image_path = os.path.join(self.folder_path, image_name)
            image = Image.open(image_path)
            image = resize(image)
            tk_image = ImageTk.PhotoImage(image)
            label1 = tk.Label(image=tk_image)
            label1.image = tk_image
            label1.place(x=x, y=equal_sign_centr_y, height=avarage_size[1], width=avarage_size[0], anchor='center')
            x += buffer_between_digits + avarage_size[0]
    
    def display_current_task(self):
        text = f'Current task: {"".join(self.elements)}'
        current_task = tk.Label(text=text)
        current_task.place(x=500, y=0, width=200)
    
    def replace(self, idx, sign_class, bounding_box, current_line):
        self.elements[idx] = sign_class
        self.bounding_boxes[idx] = bounding_box
        self.lines[idx] = current_line
        self.display_current_task()



        

class SimpleDrawingApp:
    def __init__(self, root, digit_recognizer, transforms):

        self.root = root
        self.root.title("Magic Math Notebook")

        self.canvas = tk.Canvas(root, width=1000, height=800, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.release_draw)

        self.drawing = False
        self.last_x = 0
        self.last_y = 0


        self.exercise = Exercise()
        self.digit_recognizer = digit_recognizer
        self.transforms = transforms

        self.image = Image.new("RGB", (1000, 800), "white")
        self.draw_image = ImageDraw.Draw(self.image)

        self.exercise = Exercise()

    def start_draw(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

        self.current_bounding_box = BoundingBox()
        self.current_line = Line([])

    def draw(self, event):
        if self.drawing:
            x = event.x
            y = event.y

            # рисуем линию на холсте
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=3)

            # рисуем линию на изображении
            self.draw_image.line((self.last_x, self.last_y, x, y), fill="black", width=3)
            self.current_line.append(x, y)
            self.current_bounding_box.update_min_max(x, y)
            

            self.last_x = x
            self.last_y = y

    def release_draw(self, event):
        self.drawing = False

        # = check
        if self.exercise.get_element(-1) == "-":
            threshold = 4
            cords = self.current_bounding_box.get_cords()
            cropped_image = self.image.crop((cords[0]-threshold, cords[1]-threshold, cords[2]+threshold, cords[3]+threshold))
            len_x = cords[2] - cords[0]
            len_y = cords[3] - cords[1]
            diff = int(abs(len_x - len_y) / 2)

            if len_x > len_y:
                cropped_image = ImageOps.expand(cropped_image, (0, diff, 0, diff), fill='white')
            else:
                cropped_image = ImageOps.expand(cropped_image, (diff, 0, diff, 0), fill='white')
            
            if self.get_class(cropped_image) == "-":
                _, bounding_box, _ = self.exercise.pop()
                answer = self.exercise.solve()
                equal_sign_bounding_box = self.current_bounding_box.combine(bounding_box)
                self.exercise.draw_answer(answer, equal_sign_bounding_box)
                self.exercise = Exercise()
                return 1
                 
        # check if line is part of the previos object
        # line intersection check is heavier than boxes intersection, so lets check boxes firstly
        self.intersects = False
        for idx, previos_bounding_box in enumerate(self.exercise.bounding_boxes):

            if self.current_bounding_box.intersects(previos_bounding_box):
                previos_line = self.exercise.lines[idx]
                if self.current_line.intersects(previos_line):
                    self.intersects = True
                    self.current_bounding_box.combine(previos_bounding_box)
                    self.current_line.combine(previos_line)
                    break
                    # self.exercise.pop(idx)

        squared_cords = self.current_bounding_box.get_squared_cords()
        cropped_image = self.image.crop(squared_cords)
        sign_class = self.get_class(cropped_image)
        bounding_box = BoundingBox(xmin=squared_cords[0], ymin=squared_cords[1], xmax=squared_cords[2], ymax=squared_cords[3])


        if self.intersects:
            self.exercise.replace(idx, sign_class, bounding_box, self.current_line)
        else:
            self.exercise.add(sign_class, bounding_box, self.current_line)
    
    def get_class(self, image):
        transformed_image = self.transforms(image).unsqueeze(0)
        proba = self.digit_recognizer(transformed_image)
        predict = digit_recognizer.proba_to_predict(proba)
        sign_class = digit_recognizer.predict_to_class(predict)
        return sign_class
    
    def clear_area(self):
        # Задаем координаты области, которую хотим очистить
        x1, y1, x2, y2 = 100, 100, 400, 400
        # Находим все объекты в этой области
        items = self.canvas.find_overlapping(x1, y1, x2, y2)
        # Удаляем найденные объекты
        for item in items:
            self.canvas.delete(item)
            


if __name__ == "__main__":
    # путь к весам нейросети
    weights_path = "digit_recognizer.pth"
    # создаем экземпляр модели
    digit_recognizer = DigitRecognizer()
    # загружаем веса
    digit_recognizer.load_state_dict(torch.load(weights_path))

    # трансформации для изображения
    transforms = tt.Compose([
                 tt.Resize((28, 28)),
                 tt.Grayscale(),
                 tt.ToTensor()
                 ])

    # путь к папке в которой будут хранится фото символов для дальнейшей обработке нейросетью
    folder_path = "/Users/osiprovin/Desktop/ml:dl/CV/Magic math notebook/Saved_images"
    # создаем папку
    os.makedirs(folder_path, exist_ok=True)
    # создаем объект класса для обрабоки нарисованной фигуры

    # запускаем приложение
    root = tk.Tk()
    app = SimpleDrawingApp(root, digit_recognizer, transforms)
    root.mainloop()