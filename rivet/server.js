import * as Rivet from '@ironclad/rivet-node';
import * as Express from 'express';
import express from 'express'

const app = express();
const listenPort = 4040;
const debuggerServer = Rivet.startDebuggerServer({port: 8080});

app.use(Express.urlencoded({ extended: true }))
app.use(Express.json())


app.get('/life', (req, res) => {
  res.send('I\'m Alive').status(200);
});

app.post('/litResearch', async (req, res) => {

    const openAIKey = req.body.openAIKey;
    const final_selection = req.body.final_selection;

    const graphOutput = await Rivet.runGraphInFile('./philosphy-pipeline.rivet-project', {
        graph: 'Literary Research Query',
        inputs: {
          final_selection: {
                type: 'object',
                value: final_selection
            },
        },
        remoteDebugger: debuggerServer,
        openAiKey: openAIKey,
    });

    console.log("Exectued Graph: Literary Research Query")

    res.send(graphOutput.output.value).status(200);
});

app.post('/litResearch/papers', async (req, res) => {

  const openAIKey = req.body.openAIKey;
  const search_results = req.body.search_results;
  const final_selection = req.body.final_selection;

  const graphOutput = await Rivet.runGraphInFile('./philosphy-pipeline.rivet-project', {
      graph: 'Get Literature Papers',
      inputs: {
        search_results: {
            type: 'object',
            value: search_results
          },
        final_selection: {
          type: 'object',
          value: final_selection
        }
      },
      remoteDebugger: debuggerServer,
      openAiKey: openAIKey,
  });

  console.log("Exectued Graph: Get Literature Papers")

  res.send(graphOutput.output.value).status(200);
});

// Start the server
app.listen(listenPort, () => {
  console.log(`Server started on port ${listenPort}`);
  console.log(`Use this link to connect to the remote debugger in Rivet:\nws://localhost:8080`)
});
