import json
from io import BytesIO
import requests
from PIL import Image
import mimetypes
import urllib.request
import os
import logging
from matplotlib import image

import pandas as pd
import numpy as np


from opensea_local.models.asset import Asset

def download_all_nft_assets(dir="data/raw/json",output_dir="data/raw/media"):    
    # Iterate over files in directory
    counter = 0
    print("number of files",len(os.listdir(dir)))
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        # Checking if it is a file
        if os.path.isfile(f):
            print("looking through {} file_num: {}".format(f,counter))
            counter += 1
            file = open(f, "r")
            asset = Asset(json.loads(file.read()))
            
            # Ensure ouput dir exists, else skip
            os.makedirs(output_dir,exist_ok=True)
            # Downlaod Image/Animation assets 
            try:
                url = asset.image_url
                response = requests.get(url)
                content_type = response.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                try:    
                    with open("{}/{}_{}_{}".format(output_dir,asset.collection_slug,asset.token_id,extension), 'wb') as f:
                        f.write(response.content)
                except:
                    pass
                try:
                    urllib.request.urlretrieve(url, "{}/{}_{}_{}".format(output_dir,asset.collection_slug,asset.token_id,extension)) 
                except:
                    pass
            except Exception as image_inst:
                    logging.debug('{} was unable to be downloaded, error: {}'.format(asset.image_url,image_inst))
                    print(url,image_inst) 
            try:
                url = asset.animation_url
                response = requests.get(url)
                content_type = response.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                try:    
                    with open("{}/{}_{}_{}".format(output_dir,asset.collection_slug,asset.token_id,extension), 'wb') as f:
                        f.write(response.content)
                except:
                    pass
                try:
                    urllib.request.urlretrieve(url, "{}/{}_{}_{}".format(output_dir,asset.collection_slug,asset.token_id,extension)) 
                except:
                    pass
            except Exception as animation_inst:
                    logging.debug('{} was unable to be downloaded, error: {}'.format(asset.animation_url,animation_inst))
                    print(url,animation_inst) 
            # Closing file
            file.close()
            # break


def create_dataframe(dir="data/raw/json",output_dir="data/preprocessed"):    
    # Iterate over files in directory
    counter = 0
    print("number of files",len(os.listdir(dir)))
    arr = np.array()
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        # Checking if it is a file
        if os.path.isfile(f):
            print("looking through {} file_num: {}".format(f,counter))
            counter += 1
            file = open(f, "r")
            asset = Asset(json.loads(file.read()))
            
            # Ensure ouput dir exists, else skip
            os.makedirs(output_dir,exist_ok=True)

            # Get Image/Animation data 
            try:
                image_url = asset.image_url
                response = requests.get(image_url)
                content_type = response.headers['content-type']
                image_extension = mimetypes.guess_extension(content_type)
                # if image_extension in ('.svg','.jpeg','.png'):
                #     image_extension_type = 'image'
                # if image_extension == '.gif':
                #     image_extension_type = 'gif'
                # if image_extension == '.mp4':
                #     extension_type = 'video'
                # if image_extension in ('.wav','.mp3'):
                #     extension_type = 'music'
                # else:
                #     extension_type = None
                try: 
                    image_data = image.imread("{}/{}_{}_{}".format(output_dir,asset.collection_slug,asset.token_id,image_extension))
                    image_data_shape = image_data.shape
                except:
                    image_data_shape = None

            except Exception as image_inst:
                    image_extension = None
                    image_data = None
                    image_data_shape = None
                    logging.debug('{} was unable to get image, error: {}'.format(asset.image_url,image_inst))
                    print(image_url,image_inst) 
            try:
                animation_url = asset.animation_url
                response = requests.get(animation_url)
                content_type = response.headers['content-type']
                animation_extension = mimetypes.guess_extension(content_type)
            except Exception as animation_inst:
                    animation_extension = None
                    logging.debug('{}  was unable to get animation, error: {}'.format(asset.animation_url,animation_inst))
                    print(animation_url,animation_inst)

            # Get asset data 
            try: 
                name = asset.name
                token_id = asset.token_id
                description = asset.description
            except Exception as asset_data_inst:
                logging.debug('Unable to get asset_data, error: {}'.format(asset_data_inst))
                print(asset_data_inst) 

            # Get price data
            try: 
                sale_timestamp = asset.sale_timestamp
                last_sale =  asset.last_sale
                average_price = asset.average_price
                count = asset.count
                floor_price = asset.floor_price
                market_cap = asset.market_cap
                num_owners = asset.num_owners 
                one_day_average_price = asset.one_day_average_price
                one_day_change = asset.one_day_change 
                one_day_sales = asset.one_day_sales 
                one_day_volume = asset.one_day_volume
                seven_day_average_price = asset.seven_day_average_
                seven_day_change = asset.seven_day_change
                seven_day_sales = asset.seven_day_sales 
                seven_day_volume = asset.seven_day_volume
                thirty_day_average_price = asset.thirty_day_average
                thirty_day_change = asset.thirty_day_change
                thirty_day_sales = asset.thirty_day_sales
                thirty_day_volume = asset.thirty_day_volume
                total_sales = asset.total_sales
                total_supply = asset.total_supply
                total_volume = asset.total_volume
            except Exception as price_data_inst:
                logging.debug('Unable to get price_data, error: {}'.format(price_data_inst))
                print(price_data_inst) 
            arr.append([name,token_id, description \
                        ,image_extension, image_data_shape, animation_extension \
                        ,sale_timestamp, last_sale, average_price \
                        ,count,floor_price, market_cap,num_owners \
                        ,one_day_average_price, one_day_change, one_day_sales, one_day_volume \
                        ,seven_day_average_price, seven_day_change, seven_day_sales, seven_day_volume \
                        ,thirty_day_average_price, thirty_day_change, thirty_day_sales, thirty_day_volume \
                        ,total_sales, total_supply, total_volume])
            # Closing file
            file.close()
            # break