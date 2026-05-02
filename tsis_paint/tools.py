import pygame

def draw_shape(surface, color, start, end, shape_type, width):
    """рисует разные фигуры в зависимости от того, как пользователь тянул мышку"""
    
    width = max(1, int(width))
    x1, y1 = start  # начальная точка мыши
    x2, y2 = end    # конечная точка мыши
    
    # создаём прямоугольник-основу (база для всех фигур)
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

    if shape_type == 'rect':
        # обычный прямоугольник
        pygame.draw.rect(surface, color, rect, width)
        
    elif shape_type == 'square':
        # делаем квадрат (берём большую сторону, чтобы он был ровный)
        side = max(rect.width, rect.height)
        
        square_rect = pygame.Rect(
            x1 if x1 < x2 else x1 - side,  # корректируем позицию по X
            y1 if y1 < y2 else y1 - side,  # корректируем позицию по Y
            side, side
        )
        pygame.draw.rect(surface, color, square_rect, width)
        
    elif shape_type == 'circle':
        # радиус = половина большей стороны прямоугольника
        radius = max(rect.width, rect.height) // 2
        
        # центр круга вычисляется из стартовой точки + радиус
        center = (min(x1, x2) + radius, min(y1, y2) + radius)
        
        if radius > 0:
            pygame.draw.circle(surface, color, center, radius, width)
            
    elif shape_type == 'right_tri':
        # прямоугольный треугольник (3 точки)
        points = [(x1, y1), (x1, y2), (x2, y2)]
        
        # защита от слишком маленьких/одинаковых точек
        if len(set(points)) > 2:
            pygame.draw.polygon(surface, color, points, width)
            
    elif shape_type == 'eq_tri':
        # равносторонний/равнобедренный треугольник
        mid_x = (x1 + x2) // 2  # середина по X
        
        points = [(mid_x, y1), (x1, y2), (x2, y2)]
        
        if len(set(points)) > 2:
            pygame.draw.polygon(surface, color, points, width)
            
    elif shape_type == 'rhombus':
        # ромб через 4 точки (верх, право, низ, лево)
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        
        points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
        
        if len(set(points)) > 2:
            pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, position, fill_color):
    """заливка (как ведро в paint). работает через стек вместо рекурсии"""
    
    # переводим цвет в формат pygame (ускоряет сравнение пикселей)
    fill_color_mapped = surface.map_rgb(fill_color)
    
    x, y = position  # точка клика
    width, height = surface.get_size()  # размер холста
    if not (0 <= x < width and 0 <= y < height):
        return
    
    # получаем доступ к пикселям (блокируем поверхность)
    pixel_array = pygame.PixelArray(surface)
    
    # цвет пикселя, на который кликнули
    target_color_mapped = pixel_array[x, y]

    # если уже такой цвет — ничего не делаем
    if target_color_mapped == fill_color_mapped:
        pixel_array.close()
        return

    # стек вместо рекурсии (чтобы не было crash при большой области)
    stack = [(x, y)]
    
    while stack:
        cx, cy = stack.pop()
        
        # проверка границ (чтобы не выйти за экран)
        if 0 <= cx < width and 0 <= cy < height:
            
            # если цвет совпадает с целевым
            if pixel_array[cx, cy] == target_color_mapped:
                
                # перекрашиваем пиксель
                pixel_array[cx, cy] = fill_color_mapped
                
                # добавляем соседей (4 направления)
                stack.append((cx - 1, cy))
                stack.append((cx + 1, cy))
                stack.append((cx, cy - 1))
                stack.append((cx, cy + 1))
                
    # разблокируем поверхность после заливки
    pixel_array.close()
