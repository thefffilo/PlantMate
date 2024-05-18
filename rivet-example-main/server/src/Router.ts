import { Router } from 'express';
import { WebSocketServer } from 'ws';

import { rivetDebuggerSocketRoutes, startRivetDebuggerServer } from './RivetDebuggerRoutes.js';
import { runMessageGraph, runRivetGraph } from './services/RivetRunner.js';
import runPythonScript from './services/pythonExecutor.js';

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Funzione per estrarre il codice Python da una stringa
function extractPythonCode(text: string): string {
    const regex = /```python\s*([\s\S]*?)\s*```/;
    const match = text.match(regex);
    return match ? match[1] : '';
}

const apiRouter = Router();

const scriptPath = 'script.py';

apiRouter.post('/rivet-example', async (req, res) => {
  const input = req.body.input as { type: 'user' | 'assistant'; message: string }[];
  const response = await runMessageGraph(input);

  const __filename = fileURLToPath(import.meta.url);
  const __dirname = dirname(__filename);

  try {
    const pythonCode = extractPythonCode(response);

    if(pythonCode){
      const filePath = path.join(__dirname, scriptPath);

      fs.writeFile(filePath, pythonCode, (err) => {
          if (err) {
              console.error('Error writing to script.py:', err);
          } else {
              console.log('Python code extracted and written to script.py');
              runPythonScript(filePath)
                .then(output => {
                    fs.readFile('output.json', 'utf8', (err, data) => {
                      if (err) {
                          console.error('Errore nella lettura del file output.json:', err);
                          return;
                      }
                      
                      console.log("output.json: ", data);
                      res.json({ output: data });
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    res.json({ output: response });
                });
          }
      });
    } else {
      res.json({ output: response });
    }
  } catch (error) {
    console.log(error);
  }
});

// **** Websocket for Rivet debugger **** //

const debuggerServer = new WebSocketServer({ noServer: true });
startRivetDebuggerServer(debuggerServer, {
  dynamicGraphRun: async ({ inputs, graphId }) => {
    await runRivetGraph(graphId, inputs);
  },
});
rivetDebuggerSocketRoutes(apiRouter, {
  path: '/rivet/debugger',
  wss: debuggerServer,
});

// **** Export default **** //

export default apiRouter;
