// imports
import express from 'express';
import mongoose from 'mongoose';
import Messages from './dbMessages.js';
import Rooms from './dbRooms.js';
import Pusher from 'pusher';
import cors from 'cors';

// app config
const app = express();
const port = process.env.PORT || 9000;
const pusher = new Pusher({
   appId: "1107390",
   key: "70494b11377c35d67809",
   secret: "8de0227ad0070583c109",
   cluster: "us3",
   useTLS: true
});
 

// middleware
app.use(express.json())
app.use(cors())

// app.use((req,res,next)=>{
//    res.setHeader('Access-Control-Allow-Origin', '*');
//    res.setHeader('Access-Control-Allow-Headers', '*');
//    next();
// });

// DB config
const connection_url = 'mongodb+srv://admin:y3KKSFw1ef52hiLK@cluster0.jtqm7.mongodb.net/whatsappdb?retryWrites=true&w=majority';
mongoose.connect(connection_url,{
   useCreateIndex: true,
   useNewUrlParser: true,
   useUnifiedTopology: true
});

const db = mongoose.connection;

db.once('open', ()=>{
   console.log('DB is connected')
   const msgCollection = db.collection('messagecontents');
   const changeStream = msgCollection.watch();

   changeStream.on('change', (change)=>{
      console.log('a change occured');

      if (change.operationType === 'insert'){
         const messageDetails = change.fullDocument;
         pusher.trigger('messages', 'inserted', {
            msgName: messageDetails.name,
            message: messageDetails.message,
            timestamp: messageDetails.timestamp,
            received: messageDetails.received
         });
      }else{
         console.log('Error riggering Pusher');
      }
   });
});

db.once('open', ()=>{
   console.log('DB is connected')
   const roomCollecition = db.collection('rooms');
   const changeStream = roomCollecition.watch();

   changeStream.on('change', (change)=>{
      console.log('a change occured');

      if (change.operationType === 'insert'){
         const messageDetails = change.fullDocument;
         pusher.trigger('messages', 'inserted', {
            name: messageDetails.name,            
         });
      }else{
         console.log('Error triggering Pusher');
      }
   });
});


// api routes
app.get('/', (req, res)=>res.status(200).send('hello world'));

app.get('/messages/sync', (req, res) =>{   
   Messages.find((err, data) =>{
      if (err){
         res.status(500).send(err)
      } else{
         res.status(200).send(data)
      }
   })
})

app.post('/messages/new', (req, res) =>{
   const dbMessage = req.body

   Messages.create(dbMessage, (err, data) =>{
      if (err){
         res.status(500).send(err)
      } else{
         res.status(201).send(`new message created: \n ${data}`)
      }
   })
});

app.get('/rooms/sync', (req, res) =>{   
   Rooms.find((err, data) =>{
      if (err){
         res.status(500).send(err)
      } else{
         res.status(200).send(data)
      }
   })
})

app.post('/rooms/new', (req, res) =>{
   const dbRoom = req.body

   Rooms.create(dbRoom, (err, data) =>{
      if (err){
         res.status(500).send(err)
      } else{
         res.status(201).send(`new message created: \n ${data}`)
      }
   })
});

// listener
app.listen(port, ()=>console.log(`Listening on localhost: ${port}`));
