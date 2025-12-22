import { z } from 'zod';

export const MeasurementSchema = z.object({
  type: z.enum(['glucose', 'ketone', 'weight']),
  value: z.number(),
  unit: z.string(),
  timestamp: z.string().datetime(),
  patientId: z.string().optional()
});

export type MeasurementEntry = z.infer<typeof MeasurementSchema>;
