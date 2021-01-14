import mongoose from 'mongoose';

const rooms = mongoose.Schema({
   name: String
});

export default mongoose.model('rooms', rooms);