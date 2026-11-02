export async function api(url, options={}) {
 const csrf = document.cookie.split('; ').find(x=>x.startsWith('csrftoken='))?.split('=')[1];
 const response = await fetch(url,{credentials:'same-origin',...options,headers:{'Content-Type':'application/json','X-CSRFToken':csrf || '',...options.headers}});
 const data = await response.json();
 if(!response.ok) throw new Error(data.error || data.status || 'Request failed');
 return data;
}
