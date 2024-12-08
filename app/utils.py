async def clear_text(data, materials): 
    data = data.split(':')
    data = ' '.join(data)
    
    # Добавляем data только если его нет в materials
    if data not in materials:
        materials.append(data)
        a = True
    else:
        a = False
    text = 'Из списка ниже выберите, те материалы, которые у вас есть\nОни появятся в списке ниже:\n'
    for material in materials:
        text += f'\n• {material} ✅'
    
    return text, materials, a
