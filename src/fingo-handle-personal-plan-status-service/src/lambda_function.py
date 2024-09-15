import json
from db.client import DynamoDBClient
from config.env import DYNAMODB_TABLE_NAME
import uuid

db_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    completed_id = event["completed_id"]
    path_info = event["path_info"]
    nodes = path_info["bedrock_response"]
    
    # Marcamos el path como completado
    completed_counter = 0

    for node in nodes:
        if node["id"] == completed_id:
            node["status"] = True
        
        if node["status"] == True:
            completed_counter += 1

    path_per = (completed_counter*100)/len(nodes)

    if path_per < 25:
        badges = []
    elif path_per >= 25 and path_per < 50:
        badges = [
            {
                "title": "Medalla de Bronce",
                "description": f"Completaste 25% de un path",
                "type": "bronce-medal"
            }
        ]
    elif path_per >= 50 and path_per < 75:
        badges = [
            {
                "title": "Medalla de Bronce",
                "description": f"Completaste 25% de un path",
                "type": "bronce-medal"
            },
            {
                "title": "Medalla de Plata",
                "description": f"Completaste 50% de un path",
                "type": "silver-medal"
            }
        ]
    elif path_per >= 75 and path_per < 100:
        badges = [
            {
                "title": "Medalla de Bronce",
                "description": f"Completaste 25% de un path",
                "type": "bronce-medal"
            },
            {
                "title": "Medalla de Plata",
                "description": f"Completaste 50% de un path",
                "type": "silver-medal"
            },
            {
                "title": "Medalla de Oro",
                "description": f"Completaste 75% de un path",
                "type": "gold-medal"
            }
        ]
    elif path_per == 100:
        badges = [
            {
                "title": "Medalla de Bronce",
                "description": f"Completaste 25% de un path",
                "type": "bronce-medal"
            },
            {
                "title": "Medalla de Plata",
                "description": f"Completaste 50% de un path",
                "type": "silver-medal"
            },
            {
                "title": "Medalla de Oro",
                "description": f"Completaste 75% de un path",
                "type": "gold-medal"
            },
            {
                "title": "Trofeo Platino",
                "description": f"Completaste 100% de un path",
                "type": "platinum-trophy"
            }
        ]


    # Actualizamos la información del path
    response = db_client.complete_node({
        'user_id': path_info['user_id'],
        'path_id': path_info['path_id'],
        'badge': badges,
        'bedrock_response': nodes,
        'percentage_completed': int(path_per)
    })

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps({
            'dynamodb_response': str(response['response'])
        })
    }