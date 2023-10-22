import cv2
 
image = cv2.imread('minotaur_alpha_cr.jpg')
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow('Mask', image_hsv)
lower = (0, 0, 0)  # Нижний порог (черный цвет в цветовом пространстве HSV)
upper = (211,217,222)  # Верхний порог (белый цвет в цветовом пространстве HSV)
shapeMask = cv2.inRange(image_hsv, lower, upper)

# Выделение контуров объектов
contours, _ = cv2.findContours(shapeMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Проход по каждому контуру и нарисовать прямоугольник вокруг объекта

max_w = 0
max_h = 0

# Создайте пустой список для хранения вырезанных изображений
cropped_images = []

for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)  
        
    # Вырежьте контур из исходного изображения
    cropped_image = image[y:y+h, x:x+w]
    cropped_images.append(cropped_image)

# Отобразите и/или сохраните вырезанные изображения
for i, cropped_image in enumerate(cropped_images, start = 1):
    cv2.imwrite(f'minotaur_{i}.jpg', cropped_image)

for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    
    if w > 33 and h > 25:  
        if w > max_w:
            max_w = w  
        if h > max_h:
            max_h = h    
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
    # else: 
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1)

    # if w == 33 and h == 33:
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

print(max_w, max_h)

cv2.imshow('Image with Contours', image)
# cv2.imwrite('minotaur_all.png', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
