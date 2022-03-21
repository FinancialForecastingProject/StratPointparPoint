import itertools
import statistics
from typing import List
import requests as req
from datetime import datetime


class MBOUM:
    def __init__(self):
        pass
    
    
    def get_chart(self,symbol:str,timeframe=20) -> list:
        headers = {
            'X-Mboum-Secret': "DPEbphxr0mBRzEp956ORDzCn1DFQMX6Xhhf1g5GVw6t6LtJlNmkwmYDGKVed"
        }
        try:
            url = f"https://mboum.com/api/v1/hi/history/?symbol={symbol}&interval=1d&diffandsplits=true"
            response = req.request("GET", url, headers=headers).json()

            """
            result = [
                {
                    "date": datetime.fromtimestamp(int(value)),
                    "value": response[value]["close"],
                }
                for value in response
            ]
            """
            result = [ response['data']['items'][value]["close"] for value in response['data']['items']]

            return result[:timeframe]

        except Exception as error:
            print(response)
            raise error
        
    def resultats_rapports(self,list_actifs:List[str]) -> dict:
        results = {}
        
        # On construit un dictionnaire avec tous les charts des actifs de la liste
        charts = {actif: self.get_chart(actif) for actif in list_actifs}
        
        
        
        # Pour chaque actif 
        for actif_reference in charts:
            for actif_comparaison in charts:
                results[
                    f"distance rapport premiere valeur {actif_reference} "
                    + actif_comparaison
                ] = self.distance_rapport_premiere_valeur(
                    charts[actif_reference], charts[actif_comparaison]
                )

                results[
                    f"distance rapport moyenne {actif_reference} "
                    + actif_comparaison
                ] = self.distance_rapport_moyenne(
                    charts[actif_reference], charts[actif_comparaison]
                )
        
        return results                


    def distance_rapport_premiere_valeur(self,reference,comparison):  
        newreference = []
        newcomparison = []

        for i in range(len(reference)):
            newreference.append(reference[i] / reference[0])
            newcomparison.append(comparison[i] / comparison[0]) 

        distances = [
            abs(newreference[i] - newcomparison[i])
            for i in range(len(newreference))
        ]

        return {"somme":round(sum(distances),2),
                "moyenne":round(statistics.mean(distances),2)}
    
    def distance_rapport_moyenne(self,reference,comparison):          
        newreference = []
        newcomparison = []

        for i in range(len(reference)):
            newreference.append(reference[i] / statistics.mean(reference))
            newcomparison.append(comparison[i] / statistics.mean(comparison)) 

        distances = [
            abs(newreference[i] - newcomparison[i])
            for i in range(len(newreference))
        ]

        return {"somme":round(sum(distances),2),
                "moyenne":round(statistics.mean(distances),2)}
    
    
    
assets = ['TSLA','AMZN','MSFT','AAPL']


from pprint import pprint

pprint(MBOUM().resultats_rapports(assets))