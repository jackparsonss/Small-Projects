import mongoose from 'mongoose';

const whatsappSchema = mongoose.Schema({
   message: String,
   msgName: String,
   timestamp: String,
   received: Boolean 
});


export default mongoose.model('messagecontents', whatsappSchema);