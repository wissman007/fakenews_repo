from service.reddit_api import Reddit
from service.scrapping_news import extract_newspaper_attempt

CLIENT_ID = "mV7cQmIvF_HI_f4rdB7qUQ"
SECRET_KEY = "mc8t6uX8xsdp_F67vzUdV1mzb8ElCA"

def main():
    my_redd_app = Reddit(CLIENT_ID,SECRET_KEY,'UselessUse','UselessJohnDoe')
    df_reddit = my_redd_app.build_reddit()
    df_reddit[['official_title', 'real_content']] = df_reddit['url'].apply(extract_newspaper_attempt)
    df_clean = df_reddit[df_reddit['official_title'] != 'None']
    return df_clean

#extract_newspaper_attempt(df_reddit)


# Rajout intermédiaire dans bq
# Fast Api pour le modèle
