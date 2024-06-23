import asyncio
import aiohttp
import pandas as pd
from mongodb_operations import get_newly_onboarded_sites
import config

async def fetch(session, coord):
    url = f"https://api.mapbox.com/search/geocode/v6/reverse?longitude={coord['longitude']}&latitude={coord['latitude']}&access_token={config.MAPBOX_ACCESS_TOKEN}"
    async with session.get(url) as response:
        return await response.json()

async def get_geocoding_results():
    # Get newly onboarded sites from MongoDB
    newly_onboarded_sites = get_newly_onboarded_sites()
    
    # Combine data from all collections into a single DataFrame
    coordinates = pd.concat(newly_onboarded_sites.values())
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, coord) for coord in coordinates.to_dict(orient='records')]
        results = await asyncio.gather(*tasks)
        
        geocoding_results = []
        
        for i, result in enumerate(results):
            full_address = 'N/A'
            if 'features' in result and len(result['features']) > 0:
                for feature in result['features']:
                    if 'full_address' in feature['properties']:
                        full_address = feature['properties']['full_address']
                        break
            geocoding_results.append({
                'reference_id': coordinates.iloc[i]['reference_id'],
                'latitude': coordinates.iloc[i]['latitude'],
                'longitude': coordinates.iloc[i]['longitude'],
                'full_address': full_address
            })
    
        base_df = pd.DataFrame(geocoding_results)

        geocoding_df = base_df[base_df.isin(['N/A']).any(axis=1)]
        print(geocoding_df)
        # Return None if the DataFrame is empty, otherwise return the cleaned DataFrame
        if geocoding_df.empty:
            return None
        
        else:
            return geocoding_df
        



   
