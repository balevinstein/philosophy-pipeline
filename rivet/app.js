import * as Rivet from '@ironclad/rivet-node';
import * as Express from 'express';
import express from 'express'

const app = express();
const listenPort = 4040;


app.use(Express.urlencoded({ extended: true }))
app.use(Express.json())

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.post('/litResearch', async (req, res) => {

    const openAIKey = req.body.openAIKey;
    const question = req.body.question;
    console.log({openAIKey})

    const answer = await Rivet.runGraphInFile('./phil_pipeline.rivet-project', {
        graph: 'Literary Research Query',
        inputs: {
            question: {
                type: 'string',
                value: question
            },
        },
        openAiKey: openAIKey,
    });

    console.log("Exectued Graph")
    console.log({answer})

    res.send(answer).status(200);
});

app.get('/test', (req, res) => {
    res.send('Hello World!');
  });

// Start the server
app.listen(listenPort, () => {
  console.log(`Server started on port ${listenPort}`);
});
