from utils.formatted_text import show_menu_reports_formatted, show_product_list_formatted

# Creating table meal_report if it not exists
async def create_table_meal_report(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS meal_report(
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL,
        dish_name TEXT NOT NULL,
        calories_estimated BIGINT,
        protein_g NUMERIC(5,2),
        fat_g NUMERIC(5,2),
        carbs_g NUMERIC(5,2),
        balance_assessment TEXT DEFAULT NULL,
        meal_time TIME(0) WITHOUT TIME ZONE DEFAULT CURRENT_TIME,
        meal_day DATE DEFAULT CURRENT_DATE,
        products_list TEXT DEFAULT NULL
        );
        """)

# Adding new report to meal_report table
async def new_report(pool, telegram_id, dish_name, calories_estimated, protein_g, fat_g, carbs_g, balance_assessment=None, products_list=None):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO meal_report(
        telegram_id, dish_name, calories_estimated,
        protein_g, fat_g, carbs_g, balance_assessment, products_list)
        VALUES($1, $2, $3, $4, $5, $6, $7, $8)
        """, telegram_id, dish_name, calories_estimated, protein_g, fat_g, carbs_g, balance_assessment, products_list)

# Deleting old report from meal_report table
async def delete_report(pool, telegram_id, id):
    async with pool.acquire() as conn:
        await conn.execute("""
        DELETE FROM meal_report
        WHERE telegram_id = $1 AND id = $2;""", telegram_id, id)

# Get 3 last users reports from meal_report table
async def show_menu_reports(pool, telegram_id):
    async with pool.acquire() as conn:
        result = await conn.fetchrow("""
        SELECT dish_name, calories_estimated, protein_g, fat_g, carbs_g, balance_assessment, meal_time, meal_day FROM meal_report 
        WHERE telegram_id = $1 
        ORDER BY meal_day DESC, meal_time DESC
        LIMIT 1
        """, telegram_id)
        return await show_menu_reports_formatted(result)

# Get all users reports from meal_report table
async def show_all_reports(pool, telegram_id):
    async with pool.acquire() as conn:
        result = await conn.fetch("""
        SELECT dish_name, calories_estimated, protein_g, fat_g, carbs_g, balance_assessment, meal_time, meal_day, products_list FROM meal_report 
        WHERE telegram_id = $1 
        ORDER BY meal_day DESC, meal_time DESC
        """, telegram_id)
        return result

# Show users product list for last 7 days
async def show_product_list(pool, telegram_id):
    async with pool.acquire() as conn:
        result = await conn.fetch("""
        SELECT products_list FROM meal_report
        WHERE telegram_id = $1 AND meal_day >= NOW() - INTERVAL '7 days'
        """, telegram_id)
        return await show_product_list_formatted(result)
