export class ApiClient {
  constructor(private baseUrl: string) {}

  async getPatients() {
    return fetch(`${this.baseUrl}/api/clinician/patients`).then(r => r.json());
  }

  async postMeasurement(patientId: string, data: any) {
    return fetch(`${this.baseUrl}/api/patient/measurements`, {
      method: 'POST',
      body: JSON.stringify({ patientId, ...data }),
      headers: { 'Content-Type': 'application/json' }
    }).then(r => r.json());
  }
}
