"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[26127],{23682:(t,e,n)=>{function r(t,e){if(e.length<t)throw new TypeError(t+" argument"+(t>1?"s":"")+" required, but only "+e.length+" present")}n.d(e,{Z:()=>r})},90394:(t,e,n)=>{function r(t){if(null===t||!0===t||!1===t)return NaN;var e=Number(t);return isNaN(e)?e:e<0?Math.ceil(e):Math.floor(e)}n.d(e,{Z:()=>r})},79021:(t,e,n)=>{n.d(e,{Z:()=>i});var r=n(90394),a=n(34327),s=n(23682);function i(t,e){(0,s.Z)(2,arguments);var n=(0,a.Z)(t),i=(0,r.Z)(e);return isNaN(i)?new Date(NaN):i?(n.setDate(n.getDate()+i),n):n}},59699:(t,e,n)=>{n.d(e,{Z:()=>o});var r=n(90394),a=n(39244),s=n(23682),i=36e5;function o(t,e){(0,s.Z)(2,arguments);var n=(0,r.Z)(e);return(0,a.Z)(t,n*i)}},39244:(t,e,n)=>{n.d(e,{Z:()=>i});var r=n(90394),a=n(34327),s=n(23682);function i(t,e){(0,s.Z)(2,arguments);var n=(0,a.Z)(t).getTime(),i=(0,r.Z)(e);return new Date(n+i)}},32182:(t,e,n)=>{n.d(e,{Z:()=>i});var r=n(90394),a=n(34327),s=n(23682);function i(t,e){(0,s.Z)(2,arguments);var n=(0,a.Z)(t),i=(0,r.Z)(e);if(isNaN(i))return new Date(NaN);if(!i)return n;var o=n.getDate(),c=new Date(n.getTime());c.setMonth(n.getMonth()+i+1,0);var u=c.getDate();return o>=u?c:(n.setFullYear(c.getFullYear(),c.getMonth(),o),n)}},93752:(t,e,n)=>{n.d(e,{Z:()=>s});var r=n(34327),a=n(23682);function s(t){(0,a.Z)(1,arguments);var e=(0,r.Z)(t);return e.setHours(23,59,59,999),e}},70390:(t,e,n)=>{n.d(e,{Z:()=>a});var r=n(93752);function a(){return(0,r.Z)(Date.now())}},47538:(t,e,n)=>{function r(){var t=new Date,e=t.getFullYear(),n=t.getMonth(),r=t.getDate(),a=new Date(0);return a.setFullYear(e,n,r-1),a.setHours(23,59,59,999),a}n.d(e,{Z:()=>r})},59429:(t,e,n)=>{n.d(e,{Z:()=>s});var r=n(34327),a=n(23682);function s(t){(0,a.Z)(1,arguments);var e=(0,r.Z)(t);return e.setHours(0,0,0,0),e}},13250:(t,e,n)=>{n.d(e,{Z:()=>s});var r=n(34327),a=n(23682);function s(t){(0,a.Z)(1,arguments);var e=(0,r.Z)(t);return e.setDate(1),e.setHours(0,0,0,0),e}},27088:(t,e,n)=>{n.d(e,{Z:()=>a});var r=n(59429);function a(){return(0,r.Z)(Date.now())}},83008:(t,e,n)=>{function r(){var t=new Date,e=t.getFullYear(),n=t.getMonth(),r=t.getDate(),a=new Date(0);return a.setFullYear(e,n,r-1),a.setHours(0,0,0,0),a}n.d(e,{Z:()=>r})},34327:(t,e,n)=>{n.d(e,{Z:()=>a});var r=n(23682);function a(t){(0,r.Z)(1,arguments);var e=Object.prototype.toString.call(t);return t instanceof Date||"object"==typeof t&&"[object Date]"===e?new Date(t.getTime()):"number"==typeof t||"[object Number]"===e?new Date(t):("string"!=typeof t&&"[object String]"!==e||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}},7323:(t,e,n)=>{n.d(e,{p:()=>r});const r=(t,e)=>t&&t.config.components.includes(e)},33897:(t,e,n)=>{n.d(e,{q:()=>a});var r=n(58831);const a=t=>{const e=[],n={};return Object.keys(t).forEach((a=>{const s=t[a];"group"===(0,r.M)(a)?e.push(s):n[a]=s})),e.forEach((t=>t.attributes.entity_id.forEach((t=>{delete n[t]})))),{groups:e,ungrouped:n}}},57066:(t,e,n)=>{n.d(e,{Lo:()=>i,IO:()=>o,qv:()=>c,sG:()=>d});var r=n(97330),a=n(85415),s=n(38346);const i=(t,e)=>t.callWS({type:"config/area_registry/create",...e}),o=(t,e,n)=>t.callWS({type:"config/area_registry/update",area_id:e,...n}),c=(t,e)=>t.callWS({type:"config/area_registry/delete",area_id:e}),u=t=>t.sendMessagePromise({type:"config/area_registry/list"}).then((t=>t.sort(((t,e)=>(0,a.$)(t.name,e.name))))),l=(t,e)=>t.subscribeEvents((0,s.D)((()=>u(t).then((t=>e.setState(t,!0)))),500,!0),"area_registry_updated"),d=(t,e)=>(0,r.B)("_areaRegistry",u,l,t,e)},57292:(t,e,n)=>{n.d(e,{jL:()=>i,t1:()=>o,_Y:()=>c,q4:()=>l});var r=n(97330),a=n(91741),s=n(38346);const i=(t,e,n)=>t.name_by_user||t.name||n&&((t,e)=>{for(const n of e||[]){const e="string"==typeof n?n:n.entity_id,r=t.states[e];if(r)return(0,a.C)(r)}})(e,n)||e.localize("ui.panel.config.devices.unnamed_device"),o=(t,e,n)=>t.callWS({type:"config/device_registry/update",device_id:e,...n}),c=t=>t.sendMessagePromise({type:"config/device_registry/list"}),u=(t,e)=>t.subscribeEvents((0,s.D)((()=>c(t).then((t=>e.setState(t,!0)))),500,!0),"device_registry_updated"),l=(t,e)=>(0,r.B)("_dr",c,u,t,e)},23197:(t,e,n)=>{n.d(e,{VG:()=>f,AP:()=>g});var r=n(58831),a=n(22311),s=n(91741),i=n(33897),o=n(85415),c=n(5986),u=n(41499);const l=new Set(["automation","configurator","device_tracker","geo_location","persistent_notification","zone"]),d=new Set(["mobile_app"]),f=(t,e,n=!1)=>{const a=[],i=[],o=e.title?`${e.title} `:void 0;for(const[e,c]of t){const t=(0,r.M)(e);if("alarm_control_panel"===t){const t={type:"alarm-panel",entity:e};a.push(t)}else if("camera"===t){const t={type:"picture-entity",entity:e};a.push(t)}else if("climate"===t){const t={type:"thermostat",entity:e};a.push(t)}else if("humidifier"===t){const t={type:"humidifier",entity:e};a.push(t)}else if("light"===t&&n){const t={type:"light",entity:e};a.push(t)}else if("media_player"===t){const t={type:"media-control",entity:e};a.push(t)}else if("plant"===t){const t={type:"plant-status",entity:e};a.push(t)}else if("weather"===t){const t={type:"weather-forecast",entity:e,show_forecast:!1};a.push(t)}else if("sensor"===t&&(null==c?void 0:c.attributes.device_class)===u.A);else{let t;const n=o&&c&&(t=(0,s.C)(c))!==o&&t.startsWith(o)?{entity:e,name:p(t.substr(o.length))}:e;i.push(n)}}return i.length>0&&a.unshift({type:"entities",entities:i,...e}),a},p=t=>{return(e=t.substr(0,t.indexOf(" "))).toLowerCase()!==e?t:t[0].toUpperCase()+t.slice(1);var e},g=(t,e,n,r,u,p)=>{const g=((t,e)=>{const n={},r=new Set(e.filter((t=>d.has(t.platform))).map((t=>t.entity_id)));return Object.keys(t).forEach((e=>{const s=t[e];l.has((0,a.N)(s))||r.has(s.entity_id)||(n[e]=t[e])})),n})(r,n),h={};Object.keys(g).forEach((t=>{const e=g[t];e.attributes.order&&(h[t]=e.attributes.order)}));const y=((t,e,n,r)=>{const a={...r},s=[];for(const r of t){const t=[],i=new Set(e.filter((t=>t.area_id===r.area_id)).map((t=>t.id)));for(const e of n)(i.has(e.device_id)&&!e.area_id||e.area_id===r.area_id)&&e.entity_id in a&&(t.push(a[e.entity_id]),delete a[e.entity_id]);t.length>0&&s.push([r,t])}return{areasWithEntities:s,otherEntities:a}})(t,e,n,g),_=((t,e,n,r,u,l)=>{const d=(0,i.q)(u);d.groups.sort(((t,e)=>l[t.entity_id]-l[e.entity_id]));const p={};Object.keys(d.ungrouped).forEach((t=>{const e=d.ungrouped[t],n=(0,a.N)(e);n in p||(p[n]=[]),p[n].push(e.entity_id)}));let g=[];d.groups.forEach((t=>{g=g.concat(f(t.attributes.entity_id.map((t=>[t,u[t]])),{title:(0,s.C)(t),show_header_toggle:"hidden"!==t.attributes.control}))})),Object.keys(p).sort().forEach((e=>{g=g.concat(f(p[e].sort(((t,e)=>(0,o.$)((0,s.C)(u[t]),(0,s.C)(u[e])))).map((t=>[t,u[t]])),{title:(0,c.Lh)(t,e)}))}));const h={path:e,title:n,cards:g};return r&&(h.icon=r),h})(u,"default_view","Home",undefined,y.otherEntities,h),m=[];if(y.areasWithEntities.forEach((([t,e])=>{m.push(...f(e.map((t=>[t.entity_id,t])),{title:t.name}))})),p){const t=p.energy_sources.find((t=>"grid"===t.type));t&&t.flow_from.length>0&&m.push({title:"Energy distribution today",type:"energy-distribution",link_dashboard:!0})}return _.cards.unshift(...m),_}},76478:(t,e,n)=>{n.a(t,(async t=>{n.r(e),n.d(e,{OriginalStatesStrategy:()=>p});var r=n(28101),a=n(7323),s=n(11950),i=n(57066),o=n(57292),c=n(55424),u=n(74186),l=n(23197),d=t([c]);c=(d.then?await d:d)[0];let f=!1;class p{static async generateView(t){const e=t.hass;if(e.config.state===r.UE)return{cards:[{type:"starting"}]};if(e.config.safe_mode)return{cards:[{type:"safe-mode"}]};let n;f||(f=!0,(0,i.sG)(e.connection,(()=>{})),(0,o.q4)(e.connection,(()=>{})),(0,u.LM)(e.connection,(()=>{}))),(0,a.p)(e,"energy")&&(n=(0,c.ZC)(e));const[d,p,g,h]=await Promise.all([(0,s.l)(e.connection,i.sG),(0,s.l)(e.connection,o.q4),(0,s.l)(e.connection,u.LM),e.loadBackendTranslation("title")]);let y;if(n)try{y=await n}catch(t){}const _=(0,l.AP)(d,p,g,e.states,h,y);return e.config.components.includes("geo_location")&&_&&_.cards&&_.cards.push({type:"map",geo_location_sources:["all"]}),0===_.cards.length&&_.cards.push({type:"empty-state"}),_}static async generateDashboard(t){return{title:t.hass.config.location_name,views:[{strategy:{type:"original-states"}}]}}}}))}}]);