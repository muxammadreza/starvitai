from app.clients.medplum import medplum_client

async def write_observation_glucose_ketone_weight(patient_id: str, data: dict):
    # Construct FHIR Observation
    observation = {
        "resourceType": "Observation",
        "subject": {"reference": f"Patient/{patient_id}"},
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "custom-biomarker-panel",
                "display": "Starvit Panel"
            }]
        },
        "component": []
    }
    
    if 'glucose' in data:
         observation['component'].append({
             "code": {"text": "Glucose"},
             "valueQuantity": {"value": float(data['glucose']), "unit": "mmol/L"}
         })
         
    return await medplum_client.create_observation(observation)
