import {
  GraphId,
  GraphInputs,
  GraphOutputs,
  coerceType,
  currentDebuggerState,
  loadProjectFromFile,
  runGraph
} from '@ironclad/rivet-node';

import { rivetDebuggerServerState } from '../RivetDebuggerRoutes.js';
// import { env } from 'process';
import fs from 'fs';

export async function runMessageGraph(input: { type: 'assistant' | 'user'; message: string }[]): Promise<string> {
  
  const outputs = await runRivetGraph('5BI0Pfuu2naOUKqGUO-yZ' as GraphId, {
    messages: {
      type: 'object[]',
      value: input,
    },
  });

  return coerceType(outputs.output, 'string');
}

export async function runRivetGraph(graphId: GraphId, inputs?: GraphInputs): Promise<GraphOutputs> {
  const project = currentDebuggerState.uploadedProject ?? await loadProjectFromFile('../chat.rivet-project');

  const outputs = await runGraph(project, {
    graph: "Main Graph", //graphId
    openAiKey: process.env.OPENAIKEY, //1d584b105cb848da99e146f2c30a915b
    openAiEndpoint: "https://aidevswe.openai.azure.com/openai/deployments/IFAB/chat/completions?api-version=2024-02-15-preview",
    chatNodeHeaders: {
      "api-key": process.env.OPENAIKEY || ''
    },
    inputs: {
      "input": inputs!.messages
    },
    remoteDebugger: rivetDebuggerServerState.server ?? undefined,
    externalFunctions: {
      writeToJsonFile: async (_context: any, data: any) => {
        fs.writeFile('input.json', data, 'utf8', (err) => {
          if (err) {
              console.error('Errore nella scrittura del file:', err);
              return {
                type: 'string',
                value: err,
              };
          } else {
              console.log('Oggetto JSON scritto correttamente nel file input.json');
              return {
                type: 'string',
                value: 'status 200',
              };
          }
        });    
      }  
    },
  });

  return outputs;
}
