from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from loader import db
from data.config import ADMINS
ADMINS = [int(i) for i in ADMINS]
async def home_keyboard(telegram_id):
    home = InlineKeyboardMarkup(row_width=2)
    home.add(InlineKeyboardButton(text='Xizmatlar',callback_data='services'),
        InlineKeyboardButton(text='Buyurtma Berish',callback_data='order'))
    if telegram_id in ADMINS:
        home.add(InlineKeyboardButton(text='Ishlar',callback_data='works'))
        home.add(InlineKeyboardButton(text="◀️Orqaga",callback_data='back_to_main_menu'))
        
    return home
async def services_keyboard():
    services_btn = InlineKeyboardMarkup(row_width=2)
    services = await db.select_services()
    for service in services:
        services_btn.insert(InlineKeyboardButton(text=service['fullname'],callback_data=f"service:{service['id']}"))
    services_btn.add(InlineKeyboardButton(text="◀️Orqaga",callback_data='home'))
    return services_btn
    

async def service_keyboard(services):
    service_btn = InlineKeyboardMarkup(row_width=3)
    for service in services:
        service_info = service[0]  
        service_btn.insert(InlineKeyboardButton(text=service_info['fullname'], callback_data=f"packages:{str(service_info['iid'])}:{str(service_info['service_id'])}"))
    service_btn.add(InlineKeyboardButton(text="◀️Orqaga",callback_data=f"services"))

    return service_btn

async def package_keyboard(service_id,package_id):
    package_btn = InlineKeyboardMarkup(row_width=1)
    package_btn.insert(InlineKeyboardButton(text="♻️Malumot Oish",callback_data=f"info:service_id:{service_id}:package:{package_id}"))
    package_btn.add(InlineKeyboardButton(text="◀️Orqaga",callback_data=f"service:{service_id}"))
    return package_btn


# # # # # # # # # # # # # # # # # # # # # # # # 
##             Home va Ofline tugmalari     # # 
# # # # # # # # # # # # # # # # # # # # # # # # 

async def create_online_offline_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="Online", callback_data="Online"))
    markup.insert(InlineKeyboardButton(text="Offline", callback_data="Offline"))
    markup.add(InlineKeyboardButton(text="◀️Orqaga", callback_data="home"))
    return markup
async def works_services(selected_services=None):
    if selected_services is None:
        selected_services = []
    
    services_btn = InlineKeyboardMarkup(row_width=2)
    services = await db.select_services()
    
    for service in services:
        is_selected = service['fullname'] in selected_services
        button_text = f"✅ {service['fullname']}" if is_selected else service['fullname']
        callback_data = f"offline:select_servic:{service['fullname']}"
        services_btn.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    
    services_btn.add(InlineKeyboardButton(text="📄INVOYS OLISH", callback_data="finalize_selection"))
    services_btn.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="home"))
    
    return services_btn
