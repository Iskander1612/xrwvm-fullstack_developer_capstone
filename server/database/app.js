const express = require('express');
const mongoose = require('mongoose');
const fs = require('node:fs');
const path = require('node:path');
const app = express();
const Reviews = require('./review');
const Dealerships = require('./dealership');
app.use(express.json({limit:'64kb'}));
const route = fn => async (req,res,next) => {try {await fn(req,res);} catch(e){next(e);}};
app.get('/', (req,res)=>res.json({service:'Cars Dealership MongoDB API',status:'ok'}));
app.get('/fetchReviews',route(async(req,res)=>res.json(await Reviews.find().lean())));
app.get('/fetchReviews/dealer/:id',route(async(req,res)=>res.json(await Reviews.find({dealership:Number(req.params.id)}).lean())));
app.get('/fetchDealers',route(async(req,res)=>res.json(await Dealerships.find().sort({id:1}).lean())));
app.get('/fetchDealers/:state',route(async(req,res)=>res.json(await Dealerships.find({state:req.params.state}).sort({id:1}).lean())));
app.get('/fetchDealer/:id',route(async(req,res)=>res.json(await Dealerships.find({id:Number(req.params.id)}).lean())));
app.post('/insert_review',route(async(req,res)=>{
 const fields=['dealership','review','purchase_date','car_make','car_model','car_year','name'];
 if(fields.some(key=>req.body[key]===undefined || String(req.body[key]).trim()==='')) return res.status(400).json({error:'Missing review fields'});
 const last = await Reviews.findOne().sort({id:-1});
 const review = await Reviews.create({...Object.fromEntries(fields.map(k=>[k,req.body[k]])),purchase:Boolean(req.body.purchase),id:(last?.id || 0)+1});
 res.status(201).json(review);
}));
app.use((err,req,res,next)=>{console.error(err.message);res.status(500).json({error:'Database operation failed'});});
async function start(){
 await mongoose.connect(process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/dealershipsDB');
 for(const [Model,file,key] of [[Dealerships,'dealerships.json','dealerships'],[Reviews,'reviews.json','reviews']]){
  const rows=JSON.parse(fs.readFileSync(path.join(__dirname,'data',file),'utf8'))[key];
  await Model.bulkWrite(rows.map(row=>({updateOne:{filter:{id:row.id},update:{$setOnInsert:row},upsert:true}})));
 }
 app.listen(process.env.PORT || 3030,'0.0.0.0',()=>console.log('Dealership API listening on port '+(process.env.PORT || 3030)));
}
start().catch(err=>{console.error(err.message);process.exit(1);});
