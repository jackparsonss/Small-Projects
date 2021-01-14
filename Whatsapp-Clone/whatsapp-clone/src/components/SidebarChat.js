import { Avatar } from '@material-ui/core';
import React, { useEffect, useState } from 'react';
import './SidebarChat.css';
import axios from '../axios';


function SidebarChat({ addNewChat, roomName }) {
   const [seed, setSeed] = useState('');
   const [input, setInput] = useState('');

   const sendRoom = async (e) => {
      e.preventDefault();
      const roomName = prompt("Please enter a name for the chat");
      setInput(roomName);

      await axios.post('/rooms/new',{
         name: input,      
      });

      setInput('');
   };

   useEffect(()=>{
      setSeed(Math.floor(Math.random()* 1000))
   }, []);

   return !addNewChat ? (
      <div className="sidebarChat">
         <Avatar src={`https://avatars.dicebear.com/api/human/${seed}.svg`}/>
         <div className="sidebarChat_info">
            <h2>{roomName}</h2>
            <p>Last message</p>
         </div>
      </div>
   ): (
      <div onClick={sendRoom} className="sidebarChat">
         <h2>Add new Chat</h2>
      </div>
   )
}

export default SidebarChat
