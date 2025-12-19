import { setup } from 'xstate';

export const protocolMachine = setup({
  types: {} as {
    events: { type: 'LOG_MEASUREMENT'; value: number } | { type: 'NEXT_STEP' };
  }
}).createMachine({
  id: 'protocol',
  initial: 'idle',
  states: {
    idle: {
      on: {
        LOG_MEASUREMENT: 'checking'
      }
    },
    checking: {
      on: {
        NEXT_STEP: 'idle'
      }
    }
  }
});
