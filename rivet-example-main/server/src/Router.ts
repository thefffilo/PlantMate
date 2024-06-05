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
function deleteFile(filePath: string) {
  fs.unlink(filePath, (err) => {
      if (err) {
          console.error(`Errore nell'eliminazione del file ${filePath}:`, err);
          return;
      }
      console.log(`File ${filePath} eliminato con successo.`);
  });
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
                    let textOutput = '';
                    let imgSrcString = '';
                    fs.readFile('output.json', 'utf8', async (err, data)  => {
                      if (err) {
                          console.error('Errore nella lettura del file output.json:', err);
                      }
                      else {
                        const jsonData = JSON.parse(data);
                        // simple (and bad) method for removing json formatting from the output.
                        for (let key in jsonData) {
                            if (jsonData.hasOwnProperty(key)) {
                                textOutput += `${key}: ${jsonData[key]}\n`;
                            }
                        }
                      }

                      fs.readFile('output.png', (err, imageData) => {
                        if (err) {
                          console.error('Errore nella lettura del file output.png:', err);
                        } else {
                          const base64Image = imageData.toString('base64');
                          imgSrcString = `data:image/png;base64,${base64Image}`;
                        }
        
                        // Elimina i file dopo aver inviato la risposta
                        if(textOutput && imgSrcString)
                          res.json({ output: textOutput, image: imgSrcString });
                        else if(imgSrcString)
                          res.json({ image: imgSrcString });
                        else if (textOutput)
                          res.json({ output: textOutput });
                        else 
                          res.json({ output: "error" });
  
                        deleteFile('output.json');
                        deleteFile('output.png');
                      });
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
