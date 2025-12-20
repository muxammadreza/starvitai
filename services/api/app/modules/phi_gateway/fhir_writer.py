from app.adapters import fhir_store

from typing import Optional
async def write_observation_glucose_ketone_weight(patient_id: str, data: dict, token: Optional[str] = None):
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
    
    # Validate and append components
    try:
        if data.get('glucose'):
            observation['component'].append({
                "code": {"text": "Glucose"},
                "valueQuantity": {"value": float(data['glucose']), "unit": "mmol/L"}
            })
        
        if data.get('ketones'):
            observation['component'].append({
                "code": {"text": "Ketones"},
                "valueQuantity": {"value": float(data['ketones']), "unit": "mmol/L"}
            })

        if data.get('weight'):
             observation['component'].append({
                "code": {"text": "Weight"},
                "valueQuantity": {"value": float(data['weight']), "unit": "kg"}
            })
            
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid numeric value for measurement")

    if not observation['component']:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No valid measurements provided")
        
    return await fhir_store.create_resource("Observation", observation, token=token)
