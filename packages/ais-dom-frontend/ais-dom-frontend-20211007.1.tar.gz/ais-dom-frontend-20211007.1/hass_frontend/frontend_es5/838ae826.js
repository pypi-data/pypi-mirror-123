(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[47680],{47680:function(){var t;function e(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function r(t,e){for(var r=0;r<e.length;r++){var n=e[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}function n(t,e){return n=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},n(t,e)}function i(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var r,n=o(t);if(e){var i=o(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return a(this,r)}}function a(t,e){if(e&&("object"===h(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function o(t){return o=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},o(t)}function s(t,e){return function(t){if(Array.isArray(t))return t}(t)||function(t,e){var r=null==t?null:"undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(null==r)return;var n,i,a=[],o=!0,s=!1;try{for(r=r.call(t);!(o=(n=r.next()).done)&&(a.push(n.value),!e||a.length!==e);o=!0);}catch(u){s=!0,i=u}finally{try{o||null==r.return||r.return()}finally{if(s)throw i}}return a}(t,e)||c(t,e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function u(t,e){var r="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!r){if(Array.isArray(t)||(r=c(t))||e&&t&&"number"==typeof t.length){r&&(t=r);var n=0,i=function(){};return{s:i,n:function(){return n>=t.length?{done:!0}:{done:!1,value:t[n++]}},e:function(t){throw t},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var a,o=!0,s=!1;return{s:function(){r=r.call(t)},n:function(){var t=r.next();return o=t.done,t},e:function(t){s=!0,a=t},f:function(){try{o||null==r.return||r.return()}finally{if(s)throw a}}}}function c(t,e){if(t){if("string"==typeof t)return l(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);return"Object"===r&&t.constructor&&(r=t.constructor.name),"Map"===r||"Set"===r?Array.from(t):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?l(t,e):void 0}}function l(t,e){(null==e||e>t.length)&&(e=t.length);for(var r=0,n=new Array(e);r<e;r++)n[r]=t[r];return n}function f(t,e,r,n,i,a,o){try{var s=t[a](o),u=s.value}catch(c){return void r(c)}s.done?e(u):Promise.resolve(u).then(n,i)}function d(t){return function(){var e=this,r=arguments;return new Promise((function(n,i){var a=t.apply(e,r);function o(t){f(a,n,i,o,s,"next",t)}function s(t){f(a,n,i,o,s,"throw",t)}o(void 0)}))}}function h(t){return h="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},h(t)}!function(t){var e={};function r(n){if(e[n])return e[n].exports;var i=e[n]={i:n,l:!1,exports:{}};return t[n].call(i.exports,i,i.exports,r),i.l=!0,i.exports}r.m=t,r.c=e,r.d=function(t,e,n){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},r.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"==h(t)&&t&&t.__esModule)return t;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var i in t)r.d(n,i,function(e){return t[e]}.bind(null,i));return n},r.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="",r(r.s=0)}([function(a,o,c){"use strict";c.r(o);var l=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),f=l.prototype.html;function y(){return document.querySelector("hc-main")?document.querySelector("hc-main").hass:document.querySelector("home-assistant")?document.querySelector("home-assistant").hass:void 0}l.prototype.css;var p=y().callWS({type:"config/area_registry/list"}),v=y().callWS({type:"config/device_registry/list"}),g=y().callWS({type:"config/entity_registry/list"});function m(){return b.apply(this,arguments)}function b(){return(b=d(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(t.t0=window.cardToolsData,t.t0){t.next=12;break}return t.next=4,p;case 4:return t.t1=t.sent,t.next=7,v;case 7:return t.t2=t.sent,t.next=10,g;case 10:t.t3=t.sent,t.t0={areas:t.t1,devices:t.t2,entities:t.t3};case 12:return window.cardToolsData=t.t0,t.abrupt("return",window.cardToolsData);case 14:case"end":return t.stop()}}),t)})))).apply(this,arguments)}function _(t){var e=window.cardToolsData,r=[];if(!t)return r;var n,i=u(e.devices);try{for(i.s();!(n=i.n()).done;){var a=n.value;a.area_id===t.area_id&&r.push(a)}}catch(o){i.e(o)}finally{i.f()}return r}function w(t){var e=window.cardToolsData,r=[];if(!t)return r;var n,i=u(e.entities);try{for(i.s();!(n=i.n()).done;){var a=n.value;a.device_id===t.id&&r.push(a.entity_id)}}catch(o){i.e(o)}finally{i.f()}return r}function S(t,e){if("string"==typeof e&&"string"==typeof t&&(t.startsWith("/")&&t.endsWith("/")||-1!==t.indexOf("*")))return t.startsWith("/")||(t="/^".concat(t=t.replace(/\./g,".").replace(/\*/g,".*"),"$/")),new RegExp(t.slice(1,-1)).test(e);if("string"==typeof t){if(t.startsWith("<="))return parseFloat(e)<=parseFloat(t.substr(2));if(t.startsWith(">="))return parseFloat(e)>=parseFloat(t.substr(2));if(t.startsWith("<"))return parseFloat(e)<parseFloat(t.substr(1));if(t.startsWith(">"))return parseFloat(e)>parseFloat(t.substr(1));if(t.startsWith("!"))return parseFloat(e)!=parseFloat(t.substr(1));if(t.startsWith("="))return parseFloat(e)==parseFloat(t.substr(1))}return t===e}function O(t,e){return function(r){var n="string"==typeof r?t.states[r]:t.states[r.entity];if(!r)return!1;for(var i=0,a=Object.entries(e);i<a.length;i++){var o=s(a[i],2),c=(o[0],o[1]);switch(f.split(" ")[0]){case"options":case"sort":break;case"domain":if(!S(c,n.entity_id.split(".")[0]))return!1;break;case"entity_id":if(!S(c,n.entity_id))return!1;break;case"state":if(!S(c,n.state))return!1;break;case"name":if(!n.attributes.friendly_name||!S(c,n.attributes.friendly_name))return!1;break;case"group":if(!(c.startsWith("group.")&&t.states[c]&&t.states[c].attributes.entity_id&&t.states[c].attributes.entity_id.includes(n.entity_id)))return!1;break;case"attributes":for(var l=0,d=Object.entries(c);l<d.length;l++){for(var h=s(d[l],2),y=h[0],p=h[1],v=y.trim(),g=n.attributes;v&&g;){var m,b;b=(m=s(v.split(":"),2))[0],v=m[1],g=g[b]}if(void 0===g||void 0!==p&&!S(p,g))return!1}break;case"not":if(O(t,c)(r))return!1;break;case"device":if(!window.cardToolsData||!window.cardToolsData.devices)return!1;var j,k=!1,T=u(window.cardToolsData.devices);try{for(T.s();!(j=T.n()).done;){var C=j.value;S(c,C.name)&&w(C).includes(n.entity_id)&&(k=!0)}}catch(F){T.e(F)}finally{T.f()}if(!k)return!1;break;case"area":if(!window.cardToolsData||!window.cardToolsData.areas)return!1;var E,x=!1,D=u(window.cardToolsData.areas);try{for(D.s();!(E=D.n()).done;){var R=E.value;S(c,R.name)&&_(R).flatMap(w).includes(n.entity_id)&&(x=!0)}}catch(F){D.e(F)}finally{D.f()}if(!x)return!1;break;case"last_changed":if(!S(c,((new Date).getTime()-new Date(n.last_changed).getTime())/6e4))return!1;break;case"last_updated":if(!S(c,((new Date).getTime()-new Date(n.last_updated).getTime())/6e4))return!1;break;default:return!1}}return!0}}function j(t,e){return"string"==typeof e&&(e={method:e}),function(r,n){var i="string"==typeof r?t.states[r]:t.states[r.entity],a="string"==typeof n?t.states[n]:t.states[n.entity];if(void 0===i||void 0===a)return 0;var o=s(e.reverse?[-1,1]:[1,-1],2),u=o[0],c=o[1];function l(t,r){return e.ignore_case&&t.toLowerCase&&(t=t.toLowerCase()),e.ignore_case&&r.toLowerCase&&(r=r.toLowerCase()),e.numeric&&(isNaN(parseFloat(t))&&isNaN(parseFloat(r))||(t=isNaN(parseFloat(t))?void 0:parseFloat(t),r=isNaN(parseFloat(r))?void 0:parseFloat(r))),void 0===t&&void 0===r?0:void 0===t?u:void 0===r||t<r?c:t>r?u:0}switch(e.method){case"domain":return l(i.entity_id.split(".")[0],a.entity_id.split(".")[0]);case"entity_id":return l(i.entity_id,a.entity_id);case"friendly_name":case"name":return l(i.attributes.friendly_name||i.entity_id.split(".")[1],a.attributes.friendly_name||a.entity_id.split(".")[1]);case"state":return l(i.state,a.state);case"attribute":for(var f=i.attributes,d=a.attributes,h=e.attribute;h;){var y,p;if(p=(y=s(h.split(":"),2))[0],h=y[1],f=f[p],d=d[p],void 0===f&&void 0===d)return 0;if(void 0===f)return u;if(void 0===d)return c}return l(f,d);case"last_changed":case"last_updated":return e.numeric=!0,l(new Date(a.last_changed).getTime(),new Date(i.last_changed).getTime());case"last_triggered":return null==i.attributes.last_triggered||null==a.attributes.last_triggered?0:(e.numeric=!0,l(new Date(a.attributes.last_triggered).getTime(),new Date(i.attributes.last_triggered).getTime()));default:return 0}}}function k(t,e){var r=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null;if((t=new Event(t,{bubbles:!0,cancelable:!1,composed:!0})).detail=e||{},r)r.dispatchEvent(t);else{var n=function(){var t=document.querySelector("hc-main");return t?(t=(t=(t=t&&t.shadowRoot)&&t.querySelector("hc-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-view"):(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=document.querySelector("home-assistant"))&&t.shadowRoot)&&t.querySelector("home-assistant-main"))&&t.shadowRoot)&&t.querySelector("app-drawer-layout partial-panel-resolver"))&&t.shadowRoot||t)&&t.querySelector("ha-panel-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-root"))&&t.shadowRoot)&&t.querySelector("ha-app-layout #view"))&&t.firstElementChild}();n&&n.dispatchEvent(t)}}m();var T=window.cardHelpers,C=new Promise(function(){var t=d(regeneratorRuntime.mark((function t(e,r){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(T&&e(),t.t0=window.loadCardHelpers,!t.t0){t.next=8;break}return t.next=5,window.loadCardHelpers();case 5:T=t.sent,window.cardHelpers=T,e();case 8:case"end":return t.stop()}}),t)})));return function(e,r){return t.apply(this,arguments)}}());function E(t,e){var r=document.createElement("hui-error-card");return r.setConfig({type:"error",error:t,origConfig:e}),C.then((function(){k("ll-rebuild",{},r)})),r}var x=function(){if(window.fully&&"function"==typeof fully.getDeviceId)return fully.getDeviceId();if(!localStorage["lovelace-player-device-id"]){var t=function(){return Math.floor(1e5*(1+Math.random())).toString(16).substring(1)};localStorage["lovelace-player-device-id"]="".concat(t()).concat(t(),"-").concat(t()).concat(t())}return localStorage["lovelace-player-device-id"]}();customElements.define("hui-ais-monster-card",function(a){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&n(t,e)}(d,a);var o,s,c,l=i(d);function d(){return e(this,d),l.apply(this,arguments)}return o=d,s=[{key:"setConfig",value:function(t){var e=this;if(!t||!t.card)throw new Error("Invalid configuration");t=JSON.parse(JSON.stringify(t)),this._config?(this._config=t,this.hass=this.hass):(this._config=t,this.hass=y(),this._getEntities(),this.cardConfig=Object.assign({entities:this.entities},t.card),this.card=function(t){return T?T.createCardElement(t):function(t,e){if(!e||"object"!=h(e)||!e.type)return E("No ".concat(t," type configured"),e);var r=e.type;if(r=r.startsWith("custom:")?r.substr("custom:".length):"hui-".concat(r,"-").concat(t),customElements.get(r))return function(t,e){var r=document.createElement(t);try{r.setConfig(JSON.parse(JSON.stringify(e)))}catch(t){r=E(t,e)}return C.then((function(){k("ll-rebuild",{},r)})),r}(r,e);var n=E("Custom element doesn't exist: ".concat(r,"."),e);n.style.display="None";var i=setTimeout((function(){n.style.display=""}),2e3);return customElements.whenDefined(r).then((function(){clearTimeout(i),k("ll-rebuild",{},n)})),n}("card",t)}(this.cardConfig)),t.filter&&t.filter.template&&(this.template="",(String(t.filter.template).includes("{%")||String(t.filter.template).includes("{{"))&&function(t,r,n){t||(t=y().connection);var i=Object.assign({user:y().user.name,browser:x,hash:location.hash.substr(1)||" "},n.variables),a=n.template,o=n.entity_ids;t.subscribeMessage((function(t){var r=t.result;r=r.replace(/_\([^)]*\)/g,(function(t){return y().localize(t.substring(2,t.length-1))||t})),function(t){e.template=t,e._getEntities()}(r)}),{type:"render_template",template:a,variables:i,entity_ids:o})}(null,0,{template:t.filter.template,variables:{config:t},entity_ids:t.filter.entity_ids})),m().then((function(){return e._getEntities()}))}},{key:"_getEntities",value:function(){var t=this,e=function(t){return t?"string"==typeof t?{entity:t.trim()}:t:null},r=[];if(this._config.entities&&(r=r.concat(this._config.entities.map(e))),!this.hass||!this._config.filter)return r;if(this.template&&(r=r.concat(this.template.split(/[\s,]+/).map(e))),r=r.filter(Boolean),this._config.filter.include){var n,i=Object.keys(this.hass.states).map(e),a=u(this._config.filter.include);try{var o=function(){var e=n.value;if(void 0!==e.type)return r.push(e),"continue";var a=i.filter(O(t.hass,e)).map((function(t){return JSON.parse(JSON.stringify(new Object(Object.assign({},t,e.options))).replace(/this.entity_id/g,t.entity))}));void 0!==e.sort&&(a=a.sort(j(t.hass,e.sort))),r=r.concat(a)};for(a.s();!(n=a.n()).done;)o()}catch(d){a.e(d)}finally{a.f()}}if(this._config.filter.exclude){var s,c=u(this._config.filter.exclude);try{var l=function(){var e=s.value;r=r.filter((function(r){return"string"!=typeof r&&void 0===r.entity||!O(t.hass,e)(r)}))};for(c.s();!(s=c.n()).done;)l()}catch(d){c.e(d)}finally{c.f()}}if(this._config.sort&&(r=r.sort(j(this.hass,this._config.sort)),this._config.sort.count)){var f=this._config.sort.first||0;r=r.slice(f,f+this._config.sort.count)}this._config.unique&&function(){var t,e=function t(e,r){return h(e)==h(r)&&("object"!=h(e)?e===r:!Object.keys(e).some((function(t){return!Object.keys(r).includes(t)}))&&Object.keys(e).every((function(n){return t(e[n],r[n])})))},n=[],i=u(r);try{var a=function(){var r=t.value;n.some((function(t){return e(t,r)}))||n.push(r)};for(i.s();!(t=i.n()).done;)a()}catch(d){i.e(d)}finally{i.f()}r=n}(),this.entities=r}},{key:"entities",get:function(){return this._entities},set:function(t){(function(t,e){if(t===e)return!0;if(null==t||null==e)return!1;if(t.length!=e.length)return!1;for(var r=0;r<t.length;r++)if(JSON.stringify(t[r])!==JSON.stringify(e[r]))return!1;return!0})(t,this._entities)||(this._entities=t,this.cardConfig=Object.assign({},this.cardConfig,{entities:this._entities}),0===t.length&&!1===this._config.show_empty?(this.style.display="none",this.style.margin="0"):(this.style.display=null,this.style.margin=null))}},{key:"cardConfig",get:function(){return this._cardConfig},set:function(t){this._cardConfig=t,this.card&&this.card.setConfig(t)}},{key:"updated",value:function(t){var e=this;t.has("hass")&&this.hass&&(this.card.hass=this.hass,setTimeout((function(){return e._getEntities()}),0))}},{key:"createRenderRoot",value:function(){return this}},{key:"render",value:function(){return f(t||(e=["\n    ",""],r||(r=e.slice(0)),t=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(r)}}))),this.card);var e,r}},{key:"getCardSize",value:function(){var t=0;return this.card&&this.card.getCardSize&&(t=this.card.getCardSize()),1===t&&this.entities.length&&(t=this.entities.length),0===t&&this._config.filter&&this._config.filter.include&&(t=Object.keys(this._config.filter.include).length),t||1}}],c=[{key:"properties",get:function(){return{hass:{}}}}],s&&r(o.prototype,s),c&&r(o,c),d}(l)),k("ll-rebuild",{})}])}}]);