from app.adapters import fhir_store

from typing import Optional, Any
async def write_observation_glucose_ketone_weight(patient_id: str, data: dict, token: Optional[str] = None):
    # Construct FHIR Observation
    observation: dict[str, Any] = {
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
        glucose_val = None
        ketone_val = None

        if data.get('glucose'):
            glucose_val = float(data['glucose'])
            observation['component'].append({
                "code": {"text": "Glucose"},
                "valueQuantity": {"value": glucose_val, "unit": "mmol/L"}
            })
        
        if data.get('ketones'):
            ketone_val = float(data['ketones'])
            observation['component'].append({
                "code": {"text": "Ketones"},
                "valueQuantity": {"value": ketone_val, "unit": "mmol/L"}
            })

            # Calculate GKI if we have both
            if glucose_val is not None:
                gki = round(glucose_val / ketone_val, 2)
                observation['component'].append({
                    "code": {"text": "GKI", "coding": [{"system": "custom", "code": "GKI", "display": "Glucose Ketone Index"}]},
                    "valueQuantity": {"value": gki, "unit": "{index}"} # GKI is unitless/index
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
