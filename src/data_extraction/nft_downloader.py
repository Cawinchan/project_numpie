import json
import time
import os
import glob 

from opensea_local import assets,bundles,common,events

def nft_download(collection,number_of_nfts_per_collection,maximum_nfts_checked,order_direction,output_dir="data/raw/json"):
    """ Downloads json of nft's in collection to data/raw

    args:
        collection(dict): key: nft collection name value: nft collection address
        number_of_nfts_per_collection(int): maximum possible nft's in a collection
        maximum_nfts_checked(int): after this number of nft's are checked we end the loop
        order_direction(str): "asc" ascending, "desc" decending
    """

    # initalise total number of collections and collection names
    size_of_collection = len(collection)
    collection_name_keys = list(collection.keys())
    os.makedirs(output_dir,exist_ok=True)
    for i in range(size_of_collection):
        # nft_count tracks how many nfts we have from a collection and offset helps us skip nft's checked
        if len(glob.glob(output_dir+"/"+collection_name_keys[i]+'_*')) < number_of_nfts_per_collection:
            nft_count = 0
            offset = 0
            while nft_count < number_of_nfts_per_collection and offset < (number_of_nfts_per_collection*2):
                print("nft_count: ",nft_count)
                print("collection name: {} collection addr: {} nft count: {} offset: {}".format(collection_name_keys[i],collection.get(collection_name_keys[i]),nft_count,offset))
                offset += 30
                try:
                    asset_list = assets.get_assets(asset_contract_address=str(collection.get(collection_name_keys[i])),limit=30,offset=offset,order_direction=order_direction,order_by="sale_date")
                    # time.delay(10)
                    for j in range(len(asset_list)):
                        asset = asset_list[j]
                        # print(asset)
                        if int(asset.last_sale) != 0 and asset.last_sale != None and asset.num_sales > 0:
                            if not os.path.isfile(output_dir+"/{}_{}.txt".format(collection_name_keys[i],asset.token_id)): 
                                print(asset.name, asset.last_sale)
                                if asset.get_json():
                                    # print(asset.get_json())
                                    with open(output_dir+"/{}_{}.txt".format(collection_name_keys[i],asset.token_id), 'w') as outfile:
                                        json.dump(asset.get_json(), outfile)
                                    # os.makedirs("data/raw/events",exist_ok=True)
                                    # event_json = events.get_events(event_type='successful',asset_contract_address="0x06012c8cf97BEaD5deAe237070F9587f8E7A266d", token_id=896775)
                                    # with open("data/raw/events/{}_{}.txt".format(collection_name_keys[i],asset.token_id), 'w') as outfile:
                                    #     json.dump(event_json, outfile)
                            else:
                                print(asset.name,asset.token_id, " exists!")
                            nft_count += 1
                except Exception as inst:
                    print(inst)
                time.sleep(5)