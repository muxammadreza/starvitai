export class ApiClient {
  constructor(private baseUrl: string, private token?: string) {}

  private get headers() {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  setToken(token: string) {
    this.token = token;
  }

  async getPatients() {
    return fetch(`${this.baseUrl}/api/clinician/patients`, {
      headers: this.headers
    }).then(r => r.json());
  }

  async postMeasurement(patientId: string, data: any) {
    return fetch(`${this.baseUrl}/api/patient/measurements`, {
      method: 'POST',
      body: JSON.stringify({ patientId, ...data }),
      headers: this.headers
    }).then(r => r.json());
  }

  async queryGraph(query: string, params: any) {
    return fetch(`${this.baseUrl}/api/research/graph/query`, {
      method: 'POST',
      body: JSON.stringify({ query, params }),
      headers: this.headers
    }).then(r => r.json());
  }
}

