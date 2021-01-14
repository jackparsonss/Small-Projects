import { Avatar, IconButton } from '@material-ui/core';
import React, { useState, useEffect } from 'react';
import './Chat.css';
import { AttachFile, InsertEmoticon, MoreVert, SearchOutlined } from '@material-ui/icons';
import MicIcon from '@material-ui/icons/Mic';
import axios from '../axios';


function Chat({ messages, seed }) {
   const [input, setInput] = useState('');

   
   const sendMessage = async (e) => {
      e.preventDefault();

      await axios.post('/messages/new',{
         message: input,
         msgName: 'Jack',
         timestamp: "Just now",
         received: true
      });

      setInput('');
   };

   return (
      <div className="chat">
         <div className="chat_header">
            <Avatar src={`https://avatars.dicebear.com/api/human/${seed}.svg`}/>
            <div className="chat_headerInfo">
               <h3>Room Name</h3>
               <p>Last seen at...</p>
            </div>

            <div className="chat_headerRight">
               <IconButton>                  
                  <SearchOutlined/>
               </IconButton>      
               <IconButton>
                  <AttachFile/>
               </IconButton>       
               <IconButton>
                  <MoreVert/>
               </IconButton>       
            </div>
         </div>
         <div className="chat_body">
            {messages.map((message) => (
               <p className={`chat_message ${message.received && 'chat_reciever'}`}>
                  <span className="chat_name">{message.msgName}</span>
                  {message.message}
                  <span className="chat_timestamp">
                     {message.timestamp}
                  </span>
               </p>
            ))}            
         </div>
         <div class="chat_footer">
            <IconButton>
               <InsertEmoticon/>
            </IconButton>
               <form>
                  <input value={input} onChange={e => setInput(e.target.value)} placeholder="Type a message" type="text"/>
                  <button onClick={sendMessage} type="submit">
                     Send a message
                  </button>
               </form>
               <IconButton>
                  <MicIcon/>
               </IconButton>
         </div>
      </div>
   );
}

export default Chat
