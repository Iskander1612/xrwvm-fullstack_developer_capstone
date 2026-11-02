import React,{useState,useEffect} from 'react';
import {api} from '../../api';
export default function Header(){
 const [user,setUser]=useState(null);
 useEffect(()=>{api('/djangoapp/session').then(x=>setUser(x.userName)).catch(()=>{});},[]);
 const logout=async()=>{try{await api('/djangoapp/logout',{method:'POST'});sessionStorage.clear();window.location.href='/';}catch(e){alert(e.message)}};
 return <header className="header"><a className="brand" href="/">BEST<span>CARS</span><small>DEALERSHIP NETWORK</small></a><nav aria-label="Main navigation"><a href="/">Dealerships</a><a href="/about">About Us</a><a href="/contact">Contact Us</a></nav><div className="account">{user?<><span className="username">{user}</span><button className="button secondary" onClick={logout}>Logout</button></>:<><a href="/login">Login</a><a className="button" href="/register">Sign Up</a></>}</div></header>
}
