import './App.css';
import Sidebar from './components/Sidebar';
import Chat from './components/Chat';
import { useEffect, useState } from 'react';
import Pusher from 'pusher-js';
import axios from './axios';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import Login from './components/Login';
import { useStateValue } from './StateProvider';

function App() {
  const [messages, setMessages] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [seed, setSeed] = useState('');
  const [{ user }, dispatch] = useStateValue();


  useEffect(()=>{
      setSeed(Math.floor(Math.random()* 1000))
   }, []);


  useEffect(()=>{
    axios.get('/messages/sync')
      .then(response=>{
        setMessages(response.data)
      })
  }, []);

  useEffect(()=>{
    axios.get('/rooms/sync')
      .then(response=>{
        setRooms(response.data)
      })
  }, []);

  useEffect(()=>{
    const pusher = new Pusher('70494b11377c35d67809', {
      cluster: 'us3'
    });

    const messageChannel = pusher.subscribe('messages');
    messageChannel.bind('inserted', (newMessage)=> {
      setMessages([...messages, newMessage]);
    });

    const roomChannel = pusher.subscribe('rooms');
    roomChannel.bind('inserted', (newRoom)=> {
      setRooms([...rooms, newRoom]);
    });

    return () =>{
      messageChannel.unbind_all();
      messageChannel.unsubscribe();
      roomChannel.unbind_all();
      roomChannel.unsubscribe();
    };
  }, [messages, rooms]);

  return (
    <div className="app">
      {!user ? (
        <Login/>
      ):(
        <div className="app_body">
          <Router>
            <Switch>          
              <Route path="/">            
                <Sidebar seed={seed} rooms={rooms}/>
                <Chat messages={messages} seed={seed}/>
              </Route>
            </Switch>
          </Router>
        </div>
      )}
    </div>
  );
}

export default App;
