import { exec } from 'child_process';

// Funzione per eseguire lo script Python
export default function runPythonScript(scriptPath: string): Promise<string> {
    return new Promise((resolve, reject) => {
        exec(`python ${scriptPath}`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error: ${error.message}`);
            } else if (stderr) {
                reject(`Stderr: ${stderr}`);
            } else {
                resolve(stdout);
            }
        });
    });
}


