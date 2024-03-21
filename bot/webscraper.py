import requests
from bs4 import BeautifulSoup
import pandas as pd
from redis_con import RedisConnection



if __name__ == '__main__':
    
    
    try:
        current_page = 1
        
        proceed = True
        
        data = []
        
        while(proceed == True):
            
            redis = RedisConnection()
            
            redis_conn = redis.redis_connection()
            
            
            
            print("Currently scraping page ", current_page)
            
            url = f"https://www.bbcgoodfood.com/search?q=Gordon+Ramsay+recipes&page={str(current_page)}"

            page = requests.get(url)
            
            soup = BeautifulSoup(page.text, "html.parser")
            
            p_tag = soup.find('p', attrs={'role': 'status', 'class': 'ma-reset', 'aria-live': 'polite', 'aria-atomic': 'true'})
        
            
            if p_tag.text.strip() != "Sorry we couldn\'t find any results. Please try updating your search term.":
                all_recipes = soup.find_all("div",class_ = "card__section card__content")

                for recipe in all_recipes:
                    item ={}
                    # print(recipe.find("div", class_ = "card__rating rating"))
                    if recipe.find("div", class_ = "card__rating rating") is not None:
                        item['Title'] = recipe.find("h2",class_ = "heading-4").text
                        item['Link'] = recipe.find("a", class_ = "link d-block").attrs["href"]
                        recipe_key = redis_conn.set(f"recipe:page {str(current_page)}:{item['Title']}", item['Link'])
                        
                        # data.append(item)
                    
            else:
                proceed = False
                print(proceed)
                
            current_page += 1
            
            if current_page == 3:
                proceed = False
        # df = pd.DataFrame(data)
        # df.to_csv("recipes.csv")
    except Exception as e:
        print(e)
        raise e
    
    