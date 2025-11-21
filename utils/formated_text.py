async def show_menu_reports_formated(result):
    if not result:
        return (
            "━━━━━━━━━━━━━━━\n"
            "📋 Last Meal\n"
            "❌ No meal reports found yet.\n"
            "━━━━━━━━━━━━━━━\n"
            "Add your first meal report to see it here!"
        )

    dish_name = result["dish_name"]
    calories_estimated = result["calories_estimated"]
    protein_g = result["protein_g"]
    fat_g = result["fat_g"]
    carbs_g = result["carbs_g"]
    balance_assessment = result["balance_assessment"]
    meal_time = result["meal_time"]
    meal_day = result["meal_day"]

    return (
        f"━━━━━━━━━━━━━━━\n"
        f"📋 Last Meal\n"
        f"🍽 Dish: {dish_name}\n"
        f"📅 Date: {meal_day} | 🕒 Time: {meal_time}\n"
        f"🔥 Calories: {calories_estimated} kcal\n"
        f"💪 Protein: {protein_g} g\n"
        f"🧈 Fat: {fat_g} g\n"
        f"🍞 Carbs: {carbs_g} g\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚖️ Balance assessment: {balance_assessment}"
    )

async def show_product_list_formated(result):
    if not result:
        return (
            "━━━━━━━━━━━━━━━\n"
            "🛒 Product List (7 Days)\n"
            "❌ No meal reports found for the last 7 days.\n"
            "━━━━━━━━━━━━━━━\n"
            "Add meals to see your product list here!"
        )

    formatted_result = [item["products_list"] for item in result if
                        item["products_list"] not in (None, "null", "NULL", "")]

    if not formatted_result:
        return (
            "━━━━━━━━━━━━━━━\n"
            "🛒 Product List (7 Days)\n"
            "❌ No meal reports found for the last 7 days.\n"
            "━━━━━━━━━━━━━━━\n"
            "Add meals to see your product list here!"
        )

    joined_result = "\n\n".join(formatted_result)
    return joined_result

async def user_personal_info_formated(result):
    if not result:
        return (
            "━━━━━━━━━━━━━━━\n"
            "👤 Personal Info\n"
            "❌ No personal information found.\n"
            "━━━━━━━━━━━━━━━\n"
            "Please fill out your profile first!"
        )

    age = result["age"]
    height = result["height"]
    weight = result["weight"]
    gender = result["gender"]
    goal = result["goal"]

    return (
        f"━━━━━━━━━━━━━━━\n"
        f"👤 Personal Info\n"
        f"📅 Age: {age}\n"
        f"📏 Height: {height} cm\n"
        f"⚖️ Weight: {weight} kg\n"
        f"🎯 Goal: {goal}\n"
        f"🚻 Gender: {gender}\n"
        f"━━━━━━━━━━━━━━━"
    )

async def make_reply_formated(data):
    # Getting and formating from make.com as string
    chat_id = int(data.get("chat_id"))
    dish_name = str(data.get("dish_name"))
    calories_estimated = int(data.get("calories_estimated"))
    protein_g = float(data.get("protein_g"))
    fat_g = float(data.get("fat_g"))
    carbs_g = float(data.get("carbs_g"))
    balance_assessment = str(data.get("balance_assessment"))
    products_list = str(data.get("products_list"))

    text = (
        f"<b>🍽 {dish_name}</b>\n"
        f"──────────────────────\n"
        f"  • <b>Calories:</b> {calories_estimated} kcal\n"
        f"  • <b>Protein:</b> {protein_g} g\n"
        f"  • <b>Fat:</b> {fat_g} g\n"
        f"  • <b>Carbohydrates:</b> {carbs_g} g\n\n"
        f"<i>💬 {balance_assessment}</i>"
    )

    return {
        "chat_id": chat_id,
        "text": text,
        "dish_name": dish_name,
        "calories_estimated": calories_estimated,
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carbs_g": carbs_g,
        "balance_assessment": balance_assessment,
        "products_list": products_list,
    }

async def make_reply_formatted(data):
    # Getting and formating from make.com as string
    chat_id = int(data.get("chat_id"))
    dish_name = str(data.get("dish_name"))
    calories_estimated = int(data.get("calories_estimated"))
    protein_g = float(data.get("protein_g"))
    fat_g = float(data.get("fat_g"))
    carbs_g = float(data.get("carbs_g"))
    balance_assessment = str(data.get("balance_assessment"))

    text = (
        f"<b>🍽 {dish_name}</b>\n"
        f"<code>────────────────────────────</code>\n"
        f"📊 <b>Nutritional Value:</b>\n"
        f"  • Calories: <b>{calories_estimated}</b> kcal\n"
        f"  • Protein: <b>{protein_g}</b> g\n"
        f"  • Fat: <b>{fat_g}</b> g\n"
        f"  • Carbohydrates: <b>{carbs_g}</b> g\n\n"
        f"💬 <i>{balance_assessment}</i>"
    )

    return {
        "chat_id": chat_id,
        "text": text
    }

async def make_build_formatted(data):
    # Getting and formating from make.com as string
    chat_id = int(data.get("chat_id"))
    dish_name = str(data.get("dish_name"))
    calories_estimated = int(data.get("calories_estimated"))
    protein_g = float(data.get("protein_g"))
    fat_g = float(data.get("fat_g"))
    carbs_g = float(data.get("carbs_g"))
    cook_process = str(data.get("cook_process"))

    text = (
        f"<b>🍽 {dish_name}</b>\n"
        f"<code>────────────────────────────</code>\n"
        f"📊 <b>Nutritional Value:</b>\n"
        f"  • Calories: <b>{calories_estimated}</b> kcal\n"
        f"  • Protein: <b>{protein_g}</b> g\n"
        f"  • Fat: <b>{fat_g}</b> g\n"
        f"  • Carbohydrates: <b>{carbs_g}</b> g\n\n"
        f"👩‍🍳 <b>Cooking Process:</b>\n"
        f"<i>{cook_process}</i>"
    )

    return {
        "chat_id": chat_id,
        "text": text
    }

async def make_shop_help_formatted(data):
    # Getting and formating from make.com as string
    chat_id = int(data.get("chat_id"))
    product_list = str(data.get("product_list"))

    text = (
        f"<b>🛒 Grocery list:</b>\n"
        f"<code>────────────────────────────</code>\n"
        f"{product_list}"
    )

    return {
        "chat_id": chat_id,
        "text": text
    }
