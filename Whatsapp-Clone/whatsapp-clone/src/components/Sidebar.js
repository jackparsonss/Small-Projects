import React from 'react';
import './Sidebar.css';
import DonutLargeIcon from '@material-ui/icons/DonutLarge';
import { Avatar, IconButton } from '@material-ui/core';
import ChatIcon from '@material-ui/icons/Chat';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import { SearchOutlined } from '@material-ui/icons';
import SidebarChat from './SidebarChat';


function Sidebar({seed, rooms}) {
   return (
      <div className="sidebar">         
         <div className="sidebar_header">
            <Avatar src={`https://avatars.dicebear.com/api/human/${seed}.svg`}/>
            <div className="sidebar_headerRight">  
               <IconButton>                  
                  <DonutLargeIcon/>
               </IconButton>      
               <IconButton>
                  <ChatIcon/>
               </IconButton>       
               <IconButton>
                  <MoreVertIcon/>
               </IconButton>       
            </div>
         </div>

         <div className="sidebar_search">
            <div className="sidebar_searchContainer">
               <SearchOutlined/>
               <input placeholder="Search or start a new chat" type="text"/>
            </div>
         </div>

         <div className="sidebar_chat">
            <SidebarChat addNewChat/>
            {rooms.map((room) => (
               <SidebarChat roomName={room.name}/>
            ))}      
         </div>
      </div>
   );
}

export default Sidebar
