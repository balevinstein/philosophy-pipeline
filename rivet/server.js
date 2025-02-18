import * as Rivet from '@ironclad/rivet-node';
import * as Express from 'express';
import express from 'express'

const app = express();
const listenPort = 4040;


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
        openAiKey: openAIKey,
    });

    console.log("Exectued Graph: Literary Research Query")

    res.send(graphOutput.output.value).status(200);
});

// Start the server
app.listen(listenPort, () => {
  console.log(`Server started on port ${listenPort}`);
});
