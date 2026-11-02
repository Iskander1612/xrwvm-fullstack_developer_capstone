import React,{useState} from 'react';
import Header from '../Header/Header';
import {api} from '../../api';
export default function Register(){
 const [values,setValues]=useState({userName:'',firstName:'',lastName:'',email:'',password:''}),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 const submit=async e=>{e.preventDefault();setBusy(true);setError('');try{const x=await api('/djangoapp/register',{method:'POST',body:JSON.stringify(values)});sessionStorage.setItem('username',x.userName);window.location.href='/';}catch(e){setError(e.message);setBusy(false)}};
 const fields=[['userName','Username','text','username'],['firstName','First Name','text','given-name'],['lastName','Last Name','text','family-name'],['email','Email','email','email'],['password','Password','password','new-password']];
 return <><Header/><main className="auth-layout"><div><div className="eyebrow">JOIN THE COMMUNITY</div><h1>Good advice.<br/>Better decisions.</h1><p className="muted">Create an account to review your dealership.</p></div><form className="card form" onSubmit={submit}><h2>Sign Up</h2>{fields.map(([key,label,type,auto])=><label key={key}>{label}<input name={key} type={type} autoComplete={auto} required minLength={key==='password'?8:1} value={values[key]} onChange={e=>setValues({...values,[key]:e.target.value})}/></label>)}{error&&<p role="alert" className="error">{error}</p>}<button className="button" disabled={busy}>{busy?'Creating account…':'Register'}</button><p>Have an account? <a href="/login">Login</a></p></form></main></>
}
