export type MeasurementType = 'glucose' | 'ketone' | 'weight' | 'gki';

export interface Measurement {
  id?: string;
  type: MeasurementType;
  value: number;
  unit: string;
  timestamp: string;
}

export interface PatientPseudoId {
  id: string;
}

export interface Protocol {
  id: string;
  name: string;
  version: string;
}
