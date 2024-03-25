import requests
from bs4 import BeautifulSoup
# import pandas as pd
from redis_con import RedisConnection
from mongo import MongoConnect

def ingredients_scraper(soup) -> str:
    ingredients = soup.find_all("li",class_ = "pb-xxs pt-xxs list-item list-item--separator")
    all_ingredients = ""
    for ingredient in ingredients:
        all_ingredients += ingredient.text + "\n"  
    return all_ingredients

def steps_scraper(soup) -> str:
    steps = soup.find_all("li",class_ = "pb-xs pt-xs list-item")
    all_steps = ""
    for step in steps:
        all_steps += step.text + "\n"
    return all_steps

def recipe_scraper(link, hash, redis_conn, mongo , page_number):
    recipe_url = f"https://www.bbcgoodfood.com{link}"

    page = requests.get(recipe_url)
    
    soup = BeautifulSoup(page.text, "html.parser")

    all_ingredients = ingredients_scraper(soup)

    # redis_conn.hset(hash, "ingredients", all_ingredients)
        
    all_steps = steps_scraper(soup)
                            
    # redis_conn.hset(hash, "steps", all_steps)
    document = {
                    "link":         link,
                    "ingredients":  all_ingredients,
                    "steps":        all_steps
                }
    
    mongo.insert_recipes(page_number,document)

def link_scraper(url,redis_conn,mongo):
    
    page = requests.get(url)
    
    soup = BeautifulSoup(page.text, "html.parser")
    
    p_tag = soup.find('p', attrs={'role': 'status', 'class': 'ma-reset', 'aria-live': 'polite', 'aria-atomic': 'true'})
    
    if p_tag.text.strip() != "Sorry we couldn\'t find any results. Please try updating your search term.":
        all_recipes = soup.find_all("div",class_ = "card__section card__content")

        for recipe in all_recipes:
     
            # print(recipe.find("div", class_ = "card__rating rating"))
            if recipe.find("div", class_ = "card__rating rating") is not None:
                
                title = recipe.find("h2",class_ = "heading-4").text
                link = recipe.find("a", class_ = "link d-block").attrs["href"]
                title_new = title.replace(":", "")
                page_number = f"page {str(current_page)}"
                hash =  f"recipe:{page_number}: {title_new}"
                # redis_conn.hset(hash, "link", str(link))
                    
                recipe_scraper(link, hash, redis_conn, mongo, page_number)
               

                
                # data.append(item)
    else:
        proceed = False
        print(proceed)


if __name__ == '__main__':
    
    try:
        current_page = 1
        
        proceed = True
        
        data = []
        
        redis = RedisConnection()
            
        redis_conn = redis.redis_connection()
        
        mongo = MongoConnect()
        
        
        while(proceed == True):
                       
            print("Currently scraping page ", current_page)
            
            url = f"https://www.bbcgoodfood.com/search?q=Gordon+Ramsay+recipes&page={str(current_page)}"

            link_scraper(url, redis_conn, mongo)
            
            current_page += 1
            
            if current_page == 101:
                proceed = False
        # df = pd.DataFrame(data)
        # df.to_csv("recipes.csv")
    except Exception as e:
        print(e)
        raise e
    
    
    
    # try:
    #     current_page = 1
        
    #     proceed = True
        
    #     data = []
        
    #     while(proceed == True):
            
    #         redis = RedisConnection()
            
    #         redis_conn = redis.redis_connection()
            
            
            
    #         print("Currently scraping page ", current_page)
            
    #         url = f"https://www.bbcgoodfood.com/search?q=Gordon+Ramsay+recipes&page={str(current_page)}"

    #         page = requests.get(url)
            
    #         soup = BeautifulSoup(page.text, "html.parser")
            
    #         p_tag = soup.find('p', attrs={'role': 'status', 'class': 'ma-reset', 'aria-live': 'polite', 'aria-atomic': 'true'})
        
            
    #         if p_tag.text.strip() != "Sorry we couldn\'t find any results. Please try updating your search term.":
    #             all_recipes = soup.find_all("div",class_ = "card__section card__content")

    #             for recipe in all_recipes:
    #                 item ={}
    #                 # print(recipe.find("div", class_ = "card__rating rating"))
    #                 if recipe.find("div", class_ = "card__rating rating") is not None:
    #                     item['Title'] = recipe.find("h2",class_ = "heading-4").text
    #                     item['Link'] = recipe.find("a", class_ = "link d-block").attrs["href"]
    #                     recipe_key = redis_conn.set(f"recipe:page {str(current_page)}:{item['Title']}", item['Link'])
                        
    #                     # data.append(item)
                    
    #         else:
    #             proceed = False
    #             print(proceed)
                
    #         current_page += 1
            
    #         if current_page == 3:
    #             proceed = False
    #     # df = pd.DataFrame(data)
    #     # df.to_csv("recipes.csv")
    # except Exception as e:
    #     print(e)
    #     raise e
    
    