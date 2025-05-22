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
    let graphOutput = {}

    try {
      graphOutput = await Rivet.runGraphInFile('./philosophy-pipeline.rivet-project', {
        graph: 'Phase I.2/Literary Research Query',
        inputs: {
          final_selection: {
                type: 'object',
                value: final_selection
            },
        },
        remoteDebugger: debuggerServer,
        openAiKey: openAIKey,
      });
    }
    catch (err){
      res.send({message: "Failed to execute graph"}).status(500)
      console.log("\n\n" + err + "\n\n")
      return;
    }

    console.log("Executed Graph: Literary Research Query")

    res.send(graphOutput.output.value).status(200);
});

app.post('/litResearch/papers', async (req, res) => {

  const openAIKey = req.body.openAIKey;
  const search_results = req.body.search_results;
  const final_selection = req.body.final_selection;

  let graphOutput = {}
  try{
      graphOutput = await Rivet.runGraphInFile('./philosophy-pipeline.rivet-project', {
        graph: 'Phase I.2/Get Literature Papers',
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
  }
  catch (err){
    res.send({message: "Failed to execute graph"}).status(500)
    console.log("\n\n" + err + "\n\n")
    return;
  }

  console.log("Executed Graph: Get Literature Papers")

  res.send(graphOutput.output.value).status(200);
});


app.get('/mergedContext', async (req, res) => {

  const openAIKey = req.body.openAIKey;
  const framework = req.body.framework;
  const outline = req.body.outline;
  const key_moves = req.body.key_moves;
  const literature = req.body.literature;
  const final_selection = req.body.final_selection;
  const development_moves = req.body.development_moves;

  let graphOutput = {}

  try {
    graphOutput = await Rivet.runGraphInFile('./philosophy-pipeline.rivet-project', {
      graph: 'Phase II.5/Coalesce Previous Steps',
      inputs: {
        framework: {
              type: 'object',
              value: framework
        },
        outline: {
          type: 'object',
          value: outline
        },
        key_moves: {
          type: 'object',
          value: key_moves
        },
        literature: {
          type: 'object',
          value: literature
        },
        final_selection: {
          type: 'object',
          value: final_selection
        },
        development_moves: {
          type: 'object',
          value: development_moves
        },
      },
      remoteDebugger: debuggerServer,
      openAiKey: openAIKey,
    });
  }

  catch (err){
    res.send({message: "Failed to execute graph"}).status(500)
    console.log("\n\n" + err + "\n\n")
    return;
  }

  console.log("Executed Graph: Coalesce Previous Steps")

  res.send(graphOutput.output.value).status(200);
});

// Start the server
app.listen(listenPort, () => {
  console.log(`Server started on port ${listenPort}`);
  console.log(`Use this link to connect to the remote debugger in Rivet:\nws://localhost:8080`)
});
