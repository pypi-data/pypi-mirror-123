"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[99551],{12198:function(t,e,n){n.d(e,{D_:function(){return i},p6:function(){return a},mn:function(){return s},NC:function(){return l},Nh:function(){return d},yQ:function(){return h}});var r=n(14516);n(91177);var i=function(t,e){return o(e).format(t)},o=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{weekday:"long",month:"long",day:"numeric"})})),a=function(t,e){return u(e).format(t)},u=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric"})})),s=((0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{year:"numeric",month:"numeric",day:"numeric"})})),function(t,e){return c(e).format(t)}),c=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{day:"numeric",month:"short"})})),l=function(t,e){return f(e).format(t)},f=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{month:"long",year:"numeric"})})),d=function(t,e){return m(e).format(t)},m=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{month:"long"})})),h=function(t,e){return p(e).format(t)},p=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{year:"numeric"})}))},44583:function(t,e,n){n.d(e,{o0:function(){return o},E8:function(){return u}});var r=n(14516),i=n(65810);n(91177);var o=function(t,e){return a(e).format(t)},a=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric",hour:(0,i.y)(t)?"numeric":"2-digit",minute:"2-digit",hour12:(0,i.y)(t)})})),u=function(t,e){return s(e).format(t)},s=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric",hour:(0,i.y)(t)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,i.y)(t)})}));(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{year:"numeric",month:"numeric",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,i.y)(t)})}))},49684:function(t,e,n){n.d(e,{mr:function(){return o},Vu:function(){return u},xO:function(){return c}});var r=n(14516),i=n(65810);n(91177);var o=function(t,e){return a(e).format(t)},a=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{hour:"numeric",minute:"2-digit",hour12:(0,i.y)(t)})})),u=function(t,e){return s(e).format(t)},s=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{hour:(0,i.y)(t)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,i.y)(t)})})),c=function(t,e){return l(e).format(t)},l=(0,r.Z)((function(t){return new Intl.DateTimeFormat(t.language,{hour:(0,i.y)(t)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,i.y)(t)})}))},65810:function(t,e,n){n.d(e,{y:function(){return o}});var r=n(14516),i=n(66477),o=(0,r.Z)((function(t){if(t.time_format===i.zt.language||t.time_format===i.zt.system){var e=t.time_format===i.zt.language?t.language:void 0,n=(new Date).toLocaleString(e);return n.includes("AM")||n.includes("PM")}return t.time_format===i.zt.am_pm}))},25516:function(t,e,n){n.d(e,{i:function(){return r}});var r=function(t){return function(e){return{kind:"method",placement:"prototype",key:e.key,descriptor:{set:function(t){this["__".concat(String(e.key))]=t},get:function(){return this["__".concat(String(e.key))]},enumerable:!0,configurable:!0},finisher:function(n){var r=n.prototype.connectedCallback;n.prototype.connectedCallback=function(){if(r.call(this),this[e.key]){var n=this.renderRoot.querySelector(t);if(!n)return;n.scrollTop=this[e.key]}}}}}}},27269:function(t,e,n){n.d(e,{p:function(){return r}});var r=function(t){return t.substr(t.indexOf(".")+1)}},29171:function(t,e,n){n.d(e,{D:function(){return c}});var r=n(56007),i=n(12198),o=n(44583),a=n(49684),u=n(18457),s=n(22311),c=function(t,e,n,c){var l=void 0!==c?c:e.state;if(l===r.lz||l===r.nZ)return t("state.default.".concat(l));if(e.attributes.unit_of_measurement){if("monetary"===e.attributes.device_class)try{return(0,u.u)(l,n,{style:"currency",currency:e.attributes.unit_of_measurement})}catch(p){}return"".concat((0,u.u)(l,n)," ").concat(e.attributes.unit_of_measurement)}var f=(0,s.N)(e);if("input_datetime"===f){var d;if(!c)return e.attributes.has_time?e.attributes.has_date?(d=new Date(e.attributes.year,e.attributes.month-1,e.attributes.day,e.attributes.hour,e.attributes.minute),(0,o.o0)(d,n)):((d=new Date).setHours(e.attributes.hour,e.attributes.minute),(0,a.mr)(d,n)):(d=new Date(e.attributes.year,e.attributes.month-1,e.attributes.day),(0,i.p6)(d,n));try{var m=c.split(" ");if(2===m.length)return(0,o.o0)(new Date(m.join("T")),n);if(1===m.length){if(c.includes("-"))return(0,i.p6)(new Date("".concat(c,"T00:00")),n);if(c.includes(":")){var h=new Date;return(0,a.mr)(new Date("".concat(h.toISOString().split("T")[0],"T").concat(c)),n)}}return c}catch(y){return c}}return"humidifier"===f&&"on"===l&&e.attributes.humidity?"".concat(e.attributes.humidity," %"):"counter"===f||"number"===f||"input_number"===f?(0,u.u)(l,n):e.attributes.device_class&&t("component.".concat(f,".state.").concat(e.attributes.device_class,".").concat(l))||t("component.".concat(f,".state._.").concat(l))||l}},22311:function(t,e,n){n.d(e,{N:function(){return i}});var r=n(58831),i=function(t){return(0,r.M)(t.entity_id)}},91741:function(t,e,n){n.d(e,{C:function(){return i}});var r=n(27269),i=function(t){return void 0===t.attributes.friendly_name?(0,r.p)(t.entity_id).replace(/_/g," "):t.attributes.friendly_name||""}},18457:function(t,e,n){n.d(e,{H:function(){return o},u:function(){return a}});var r=n(66477),i=n(27593),o=function(t){switch(t.number_format){case r.y4.comma_decimal:return["en-US","en"];case r.y4.decimal_comma:return["de","es","it"];case r.y4.space_comma:return["fr","sv","cs"];case r.y4.system:return;default:return t.language}},a=function(t,e,n){var a=e?o(e):void 0;if(Number.isNaN=Number.isNaN||function t(e){return"number"==typeof e&&t(e)},(null==e?void 0:e.number_format)!==r.y4.none&&!Number.isNaN(Number(t))&&Intl)try{return new Intl.NumberFormat(a,u(t,n)).format(Number(t))}catch(s){return console.error(s),new Intl.NumberFormat(void 0,u(t,n)).format(Number(t))}return"string"==typeof t?t:"".concat((0,i.N)(t,null==n?void 0:n.maximumFractionDigits).toString()).concat("currency"===(null==n?void 0:n.style)?" ".concat(n.currency):"")},u=function(t,e){var n=Object.assign({maximumFractionDigits:2},e);if("string"!=typeof t)return n;if(!e||!e.minimumFractionDigits&&!e.maximumFractionDigits){var r=t.indexOf(".")>-1?t.split(".")[1].length:0;n.minimumFractionDigits=r,n.maximumFractionDigits=r}return n}},27593:function(t,e,n){n.d(e,{N:function(){return r}});var r=function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2;return Math.round(t*Math.pow(10,e))/Math.pow(10,e)}},96151:function(t,e,n){n.d(e,{T:function(){return r},y:function(){return i}});var r=function(t){requestAnimationFrame((function(){return setTimeout(t,0)}))},i=function(){return new Promise((function(t){r(t)}))}},56007:function(t,e,n){n.d(e,{nZ:function(){return r},lz:function(){return i},V_:function(){return o}});var r="unavailable",i="unknown",o=[r,i]},58763:function(t,e,n){n.d(e,{vq:function(){return h},_J:function(){return p},Nu:function(){return v},uR:function(){return g},dL:function(){return b},h_:function(){return _},Cj:function(){return w},hN:function(){return k},Kj:function(){return S},q6:function(){return D},Nw:function(){return E},m2:function(){return x},VU:function(){return O},Kk:function(){return T}});var r=n(59429),i=n(79021),o=n(13250),a=n(32182),u=n(29171),s=n(22311),c=n(91741);function l(t,e){var n="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!n){if(Array.isArray(t)||(n=function(t,e){if(!t)return;if("string"==typeof t)return f(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);"Object"===n&&t.constructor&&(n=t.constructor.name);if("Map"===n||"Set"===n)return Array.from(t);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return f(t,e)}(t))||e&&t&&"number"==typeof t.length){n&&(t=n);var r=0,i=function(){};return{s:i,n:function(){return r>=t.length?{done:!0}:{done:!1,value:t[r++]}},e:function(t){throw t},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,u=!1;return{s:function(){n=n.call(t)},n:function(){var t=n.next();return a=t.done,t},e:function(t){u=!0,o=t},f:function(){try{a||null==n.return||n.return()}finally{if(u)throw o}}}}function f(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=t[n];return r}var d=["climate","humidifier","water_heater"],m=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],h=function(t,e,n,r){var i=arguments.length>4&&void 0!==arguments[4]&&arguments[4],o=arguments.length>5?arguments[5]:void 0,a=!(arguments.length>6&&void 0!==arguments[6])||arguments[6],u="history/period";return n&&(u+="/"+n.toISOString()),u+="?filter_entity_id="+e,r&&(u+="&end_time="+r.toISOString()),i&&(u+="&skip_initial_state"),void 0!==o&&(u+="&significant_changes_only=".concat(Number(o))),a&&(u+="&minimal_response"),t.callApi("GET",u)},p=function(t,e,n,r){return t.callApi("GET","history/period/".concat(e.toISOString(),"?end_time=").concat(n.toISOString(),"&minimal_response").concat(r?"&filter_entity_id=".concat(r):""))},y=function(t,e){return t.state===e.state&&(!t.attributes||!e.attributes||m.every((function(n){return t.attributes[n]===e.attributes[n]})))},v=function(t,e,n){var r={},i=[];return e?(e.forEach((function(e){if(0!==e.length){var o,a=e.find((function(t){return t.attributes&&("unit_of_measurement"in t.attributes||"state_class"in t.attributes)}));(o=a?a.attributes.unit_of_measurement||" ":{climate:t.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:t.config.unit_system.temperature}[(0,s.N)(e[0])])?o in r?r[o].push(e):r[o]=[e]:i.push(function(t,e,n){var r,i=[],o=n.length-1,a=l(n);try{for(a.s();!(r=a.n()).done;){var s=r.value;i.length>0&&s.state===i[i.length-1].state||(s.entity_id||(s.attributes=n[o].attributes,s.entity_id=n[o].entity_id),i.push({state_localize:(0,u.D)(t,s,e),state:s.state,last_changed:s.last_changed}))}}catch(f){a.e(f)}finally{a.f()}return{name:(0,c.C)(n[0]),entity_id:n[0].entity_id,data:i}}(n,t.locale,e))}})),{line:Object.keys(r).map((function(t){return function(t,e){var n,r=[],i=l(e);try{for(i.s();!(n=i.n()).done;){var o,a=n.value,u=a[a.length-1],f=(0,s.N)(u),h=[],p=l(a);try{for(p.s();!(o=p.n()).done;){var v=o.value,g=void 0;if(d.includes(f)){g={state:v.state,last_changed:v.last_updated,attributes:{}};var b,_=l(m);try{for(_.s();!(b=_.n()).done;){var w=b.value;w in v.attributes&&(g.attributes[w]=v.attributes[w])}}catch(k){_.e(k)}finally{_.f()}}else g=v;h.length>1&&y(g,h[h.length-1])&&y(g,h[h.length-2])||h.push(g)}}catch(k){p.e(k)}finally{p.f()}r.push({domain:f,name:(0,c.C)(u),entity_id:u.entity_id,states:h})}}catch(k){i.e(k)}finally{i.f()}return{unit:t,identifier:e.map((function(t){return t[0].entity_id})).join(""),data:r}}(t,r[t])})),timeline:i}):{line:[],timeline:[]}},g=function(t,e){return t.callWS({type:"history/list_statistic_ids",statistic_type:e})},b=function(t,e,n,r){var i=arguments.length>4&&void 0!==arguments[4]?arguments[4]:"hour";return t.callWS({type:"history/statistics_during_period",start_time:e.toISOString(),end_time:null==n?void 0:n.toISOString(),statistic_ids:r,period:i})},_=function(t){return t.callWS({type:"recorder/validate_statistics"})},w=function(t,e,n){return t.callWS({type:"recorder/update_statistics_metadata",statistic_id:e,unit_of_measurement:n})},k=function(t,e){return t.callWS({type:"recorder/clear_statistics",statistic_ids:e})},S=function(t){if(!t||t.length<2)return null;var e=t[t.length-1].sum;if(null===e)return null;var n=t[0].sum;return null===n?e:e-n},D=function(t,e){var n,r=null,i=l(e);try{for(i.s();!(n=i.n()).done;){var o=n.value;if(o in t){var a=S(t[o]);null!==a&&(null===r?r=a:r+=a)}}}catch(u){i.e(u)}finally{i.f()}return r},E=function(t,e){return t.some((function(t){return null!==t[e]}))},x=function(t,e){var n=null;if(0===e.length||0===t.length)return null;var r,i=(r={},e.forEach((function(t){if(0!==t.length){var e=null;t.forEach((function(t){if(null!==t.sum)if(null!==e){var n=t.sum-e;t.start in r?r[t.start]+=n:r[t.start]=n,e=t.sum}else e=t.sum}))}})),r);return t.forEach((function(t){var e=i[t.start];void 0!==e&&(null===n?n=e*(t.mean/100):n+=e*(t.mean/100))})),n},O=function(t){if(null==t||!t.length)return[];var e,n,o=[];t.length>1&&new Date(t[0].start).getDate()===new Date(t[1].start).getDate()&&o.push(Object.assign({},t[0],{start:(0,r.Z)((0,i.Z)(new Date(t[0].start),-1)).toISOString()}));var a,u=l(t);try{for(u.s();!(a=u.n()).done;){var s=a.value,c=new Date(s.start).getDate();void 0===n&&(n=c),n!==c&&(o.push(Object.assign({},e,{start:(0,r.Z)(new Date(e.start)).toISOString()})),n=c),e=s}}catch(f){u.e(f)}finally{u.f()}return o.push(Object.assign({},e,{start:(0,r.Z)(new Date(e.start)).toISOString()})),o},T=function(t){if(null==t||!t.length)return[];var e,n,r=[];t.length>1&&new Date(t[0].start).getMonth()===new Date(t[1].start).getMonth()&&r.push(Object.assign({},t[0],{start:(0,o.Z)((0,a.Z)(new Date(t[0].start),-1)).toISOString()}));var i,u=l(t);try{for(u.s();!(i=u.n()).done;){var s=i.value,c=new Date(s.start).getMonth();void 0===n&&(n=c),n!==c&&(r.push(Object.assign({},e,{start:(0,o.Z)(new Date(e.start)).toISOString()})),n=c),e=s}}catch(f){u.e(f)}finally{u.f()}return r.push(Object.assign({},e,{start:(0,o.Z)(new Date(e.start)).toISOString()})),r}},26765:function(t,e,n){n.d(e,{Ys:function(){return a},g7:function(){return u},D9:function(){return s}});var r=n(47181),i=function(){return Promise.all([n.e(68200),n.e(30879),n.e(29907),n.e(32421),n.e(34821),n.e(29756)]).then(n.bind(n,1281))},o=function(t,e,n){return new Promise((function(o){var a=e.cancel,u=e.confirm;(0,r.B)(t,"show-dialog",{dialogTag:"dialog-box",dialogImport:i,dialogParams:Object.assign({},e,n,{cancel:function(){o(!(null==n||!n.prompt)&&null),a&&a()},confirm:function(t){o(null==n||!n.prompt||t),u&&u(t)}})})}))},a=function(t,e){return o(t,e)},u=function(t,e){return o(t,e,{confirmation:!0})},s=function(t,e){return o(t,e,{prompt:!0})}},61979:function(t,e,n){n.r(e);n(53918);var r,i,o,a,u,s,c,l,f,d=n(7599),m=n(26767),h=n(5701),p=n(17717),y=n(14516),v=n(47181),g=n(91741),b=(n(67065),n(58763)),_=n(26765),w=n(11654),k=function(){return Promise.all([n.e(29907),n.e(35487),n.e(89841),n.e(34821),n.e(80849)]).then(n.bind(n,24054))},S=function(){return Promise.all([n.e(29907),n.e(35487),n.e(89841),n.e(34821),n.e(29253)]).then(n.bind(n,74846))};function D(t){return D="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},D(t)}function E(t,e){return q(t)||function(t,e){var n=null==t?null:"undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(null==n)return;var r,i,o=[],a=!0,u=!1;try{for(n=n.call(t);!(a=(r=n.next()).done)&&(o.push(r.value),!e||o.length!==e);a=!0);}catch(s){u=!0,i=s}finally{try{a||null==n.return||n.return()}finally{if(u)throw i}}return o}(t,e)||Y(t,e)||B()}function x(t,e,n,r,i,o,a){try{var u=t[o](a),s=u.value}catch(c){return void n(c)}u.done?e(s):Promise.resolve(s).then(r,i)}function O(t,e){return e||(e=t.slice(0)),Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))}function T(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function I(t,e){return I=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},I(t,e)}function P(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var n,r=F(t);if(e){var i=F(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return j(this,n)}}function j(t,e){if(e&&("object"===D(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return C(t)}function C(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}function F(t){return F=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},F(t)}function A(){A=function(){return t};var t={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(t,e){["method","field"].forEach((function(n){e.forEach((function(e){e.kind===n&&"own"===e.placement&&this.defineClassElement(t,e)}),this)}),this)},initializeClassElements:function(t,e){var n=t.prototype;["method","field"].forEach((function(r){e.forEach((function(e){var i=e.placement;if(e.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?t:n;this.defineClassElement(o,e)}}),this)}),this)},defineClassElement:function(t,e){var n=e.descriptor;if("field"===e.kind){var r=e.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(t)}}Object.defineProperty(t,e.key,n)},decorateClass:function(t,e){var n=[],r=[],i={static:[],prototype:[],own:[]};if(t.forEach((function(t){this.addElementPlacement(t,i)}),this),t.forEach((function(t){if(!z(t))return n.push(t);var e=this.decorateElement(t,i);n.push(e.element),n.push.apply(n,e.extras),r.push.apply(r,e.finishers)}),this),!e)return{elements:n,finishers:r};var o=this.decorateConstructor(n,e);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(t,e,n){var r=e[t.placement];if(!n&&-1!==r.indexOf(t.key))throw new TypeError("Duplicated element ("+t.key+")");r.push(t.key)},decorateElement:function(t,e){for(var n=[],r=[],i=t.decorators,o=i.length-1;o>=0;o--){var a=e[t.placement];a.splice(a.indexOf(t.key),1);var u=this.fromElementDescriptor(t),s=this.toElementFinisherExtras((0,i[o])(u)||u);t=s.element,this.addElementPlacement(t,e),s.finisher&&r.push(s.finisher);var c=s.extras;if(c){for(var l=0;l<c.length;l++)this.addElementPlacement(c[l],e);n.push.apply(n,c)}}return{element:t,finishers:r,extras:n}},decorateConstructor:function(t,e){for(var n=[],r=e.length-1;r>=0;r--){var i=this.fromClassDescriptor(t),o=this.toClassDescriptor((0,e[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){t=o.elements;for(var a=0;a<t.length-1;a++)for(var u=a+1;u<t.length;u++)if(t[a].key===t[u].key&&t[a].placement===t[u].placement)throw new TypeError("Duplicated element ("+t[a].key+")")}}return{elements:t,finishers:n}},fromElementDescriptor:function(t){var e={kind:t.kind,key:t.key,placement:t.placement,descriptor:t.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===t.kind&&(e.initializer=t.initializer),e},toElementDescriptors:function(t){var e;if(void 0!==t)return(e=t,q(e)||function(t){if("undefined"!=typeof Symbol&&null!=t[Symbol.iterator]||null!=t["@@iterator"])return Array.from(t)}(e)||Y(e)||B()).map((function(t){var e=this.toElementDescriptor(t);return this.disallowProperty(t,"finisher","An element descriptor"),this.disallowProperty(t,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(t){var e=String(t.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var n=U(t.key),r=String(t.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=t.descriptor;this.disallowProperty(t,"elements","An element descriptor");var o={kind:e,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==e?this.disallowProperty(t,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=t.initializer),o},toElementFinisherExtras:function(t){return{element:this.toElementDescriptor(t),finisher:M(t,"finisher"),extras:this.toElementDescriptors(t.extras)}},fromClassDescriptor:function(t){var e={kind:"class",elements:t.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(t){var e=String(t.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(t,"key","A class descriptor"),this.disallowProperty(t,"placement","A class descriptor"),this.disallowProperty(t,"descriptor","A class descriptor"),this.disallowProperty(t,"initializer","A class descriptor"),this.disallowProperty(t,"extras","A class descriptor");var n=M(t,"finisher");return{elements:this.toElementDescriptors(t.elements),finisher:n}},runClassFinishers:function(t,e){for(var n=0;n<e.length;n++){var r=(0,e[n])(t);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");t=r}}return t},disallowProperty:function(t,e,n){if(void 0!==t[e])throw new TypeError(n+" can't have a ."+e+" property.")}};return t}function N(t){var e,n=U(t.key);"method"===t.kind?e={value:t.value,writable:!0,configurable:!0,enumerable:!1}:"get"===t.kind?e={get:t.value,configurable:!0,enumerable:!1}:"set"===t.kind?e={set:t.value,configurable:!0,enumerable:!1}:"field"===t.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===t.kind?"field":"method",key:n,placement:t.static?"static":"field"===t.kind?"own":"prototype",descriptor:e};return t.decorators&&(r.decorators=t.decorators),"field"===t.kind&&(r.initializer=t.value),r}function Z(t,e){void 0!==t.descriptor.get?e.descriptor.get=t.descriptor.get:e.descriptor.set=t.descriptor.set}function z(t){return t.decorators&&t.decorators.length}function R(t){return void 0!==t&&!(void 0===t.value&&void 0===t.writable)}function M(t,e){var n=t[e];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+e+"' to be a function");return n}function U(t){var e=function(t,e){if("object"!==D(t)||null===t)return t;var n=t[Symbol.toPrimitive];if(void 0!==n){var r=n.call(t,e||"default");if("object"!==D(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(t)}(t,"string");return"symbol"===D(e)?e:String(e)}function B(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function Y(t,e){if(t){if("string"==typeof t)return W(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);return"Object"===n&&t.constructor&&(n=t.constructor.name),"Map"===n||"Set"===n?Array.from(t):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?W(t,e):void 0}}function W(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=t[n];return r}function q(t){if(Array.isArray(t))return t}var V={entity_not_recorded:1,unsupported_unit_state:2,unsupported_state_class:3,units_changed:4,unsupported_unit_metadata:5};!function(t,e,n,r){var i=A();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var a=e((function(t){i.initializeInstanceElements(t,u.elements)}),n),u=i.decorateClass(function(t){for(var e=[],n=function(t){return"method"===t.kind&&t.key===o.key&&t.placement===o.placement},r=0;r<t.length;r++){var i,o=t[r];if("method"===o.kind&&(i=e.find(n)))if(R(o.descriptor)||R(i.descriptor)){if(z(o)||z(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(z(o)){if(z(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}Z(o,i)}else e.push(o)}return e}(a.d.map(N)),t);i.initializeClassElements(a.F,u.elements),i.runClassFinishers(a.F,u.finishers)}([(0,m.M)("developer-tools-statistics")],(function(t,e){var n,m,D=function(e){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&I(t,e)}(r,e);var n=P(r);function r(){var e;T(this,r);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return e=n.call.apply(n,[this].concat(o)),t(C(e)),e}return r}(e);return{F:D,d:[{kind:"field",decorators:[(0,h.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,h.C)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,p.S)()],key:"_data",value:function(){return[]}},{kind:"method",key:"firstUpdated",value:function(){this._validateStatistics()}},{kind:"field",key:"_columns",value:function(){var t=this;return(0,y.Z)((function(e){return{state:{title:"Entity",sortable:!0,filterable:!0,grows:!0,template:function(t,e){return(0,d.dy)(r||(r=O(["",""])),t?(0,g.C)(t):e.statistic_id)}},statistic_id:{title:"Statistic id",sortable:!0,filterable:!0,hidden:t.narrow,width:"30%"},unit_of_measurement:{title:"Unit",sortable:!0,filterable:!0,width:"10%"},issues:{title:"Issue",sortable:!0,filterable:!0,direction:"asc",width:"30%",template:function(t){return(0,d.dy)(i||(i=O(["",""])),t?t.map((function(t){return e("ui.panel.developer-tools.tabs.statistics.issues.".concat(t.type),t.data)||t.type})):e("ui.panel.developer-tools.tabs.statistics.no_issue"))}},fix:{title:"",template:function(n,r){return(0,d.dy)(o||(o=O(["",""])),r.issues?(0,d.dy)(a||(a=O(["<mwc-button @click="," .data=",">\n                ","\n              </mwc-button>"])),t._fixIssue,r.issues,e("ui.panel.developer-tools.tabs.statistics.fix_issue.fix")):"")},width:"113px"}}}))}},{kind:"method",key:"render",value:function(){return(0,d.dy)(u||(u=O(["\n      <ha-data-table\n        .columns=","\n        .data=",'\n        noDataText="No issues found!"\n        id="statistic_id"\n        clickable\n        @row-click=',"\n      ></ha-data-table>\n    "])),this._columns(this.hass.localize),this._data,this._rowClicked)}},{kind:"method",key:"_rowClicked",value:function(t){var e=t.detail.id;e in this.hass.states&&(0,v.B)(this,"hass-more-info",{entityId:e})}},{kind:"method",key:"_validateStatistics",value:(n=regeneratorRuntime.mark((function t(){var e,n,r,i,o,a=this;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,Promise.all([(0,b.uR)(this.hass),(0,b.h_)(this.hass)]);case 2:e=t.sent,n=E(e,2),r=n[0],i=n[1],o=new Set,this._data=r.map((function(t){return o.add(t.statistic_id),Object.assign({},t,{state:a.hass.states[t.statistic_id],issues:i[t.statistic_id]})})),Object.keys(i).forEach((function(t){o.has(t)||a._data.push({statistic_id:t,unit_of_measurement:"",state:a.hass.states[t],issues:i[t]})}));case 9:case"end":return t.stop()}}),t,this)})),m=function(){var t=this,e=arguments;return new Promise((function(r,i){var o=n.apply(t,e);function a(t){x(o,r,i,a,u,"next",t)}function u(t){x(o,r,i,a,u,"throw",t)}a(void 0)}))},function(){return m.apply(this,arguments)})},{kind:"field",key:"_fixIssue",value:function(){var t=this;return function(e){var n,r,i=e.currentTarget.data.sort((function(t,e){var n,r;return(null!==(n=V[t.type])&&void 0!==n?n:99)-(null!==(r=V[e.type])&&void 0!==r?r:99)}))[0];switch(i.type){case"entity_not_recorded":(0,_.Ys)(t,{title:"Entity not recorded",text:(0,d.dy)(s||(s=O(['State changes of this entity are not recorded, therefore,\n            we can not track long term statistics for it. <br /><br />You\n            probably excluded this entity, or have just included some\n            entities.<br /><br />See the\n            <a\n              href="https://www.home-assistant.io/integrations/recorder/#configure-filter"\n              target="_blank"\n              rel="noreferrer noopener"\n            >\n              recorder documentation</a\n            >\n            for more information.'])))});break;case"unsupported_state_class":(0,_.Ys)(t,{title:"Unsupported state class",text:(0,d.dy)(c||(c=O(["The state class of this entity, ",'\n            is not supported. <br />Statistics can not be generated until this\n            entity has a supported state class.<br /><br />If this state class\n            was provided by an integration, this is a bug. Please report an\n            issue.<br /><br />If you have set this state class yourself, please\n            correct it. The different state classes and when to use which can be\n            found in the\n            <a\n              href="https://developers.home-assistant.io/docs/core/entity/sensor/#long-term-statistics"\n              target="_blank"\n              rel="noreferrer noopener"\n            >\n              developer documentation</a\n            >.'])),i.data.state_class)});break;case"unsupported_unit_metadata":n=t,r={issue:i,fixedCallback:function(){t._validateStatistics()}},(0,v.B)(n,"show-dialog",{dialogTag:"dialog-statistics-fix-unsupported-unit-meta",dialogImport:S,dialogParams:r});break;case"unsupported_unit_state":(0,_.Ys)(t,{title:"Unsupported unit",text:(0,d.dy)(l||(l=O(["The unit of your entity is not a supported unit for the\n            device class of the entity, ",'.\n            <br />Statistics can not be generated until this entity has a\n            supported unit.<br /><br />If this unit was provided by an\n            integration, this is a bug. Please report an issue.<br /><br />If\n            you have set this unit yourself, and want to have statistics\n            generated, make sure the unit matches the device class. The\n            supported units are documented in the\n            <a\n              href="https://developers.home-assistant.io/docs/core/entity/sensor/#available-device-classes"\n              target="_blank"\n              rel="noreferrer noopener"\n            >\n              developer documentation</a\n            >.'])),i.data.device_class)});break;case"units_changed":!function(t,e){(0,v.B)(t,"show-dialog",{dialogTag:"dialog-statistics-fix-units-changed",dialogImport:k,dialogParams:e})}(t,{issue:i,fixedCallback:function(){t._validateStatistics()}});break;default:(0,_.Ys)(t,{title:"Fix issue",text:"Fixing this issue is not supported yet."})}}}},{kind:"get",static:!0,key:"styles",value:function(){return[w.Qx,(0,d.iv)(f||(f=O(["\n        .content {\n          padding: 16px;\n        }\n\n        th {\n          padding: 0 8px;\n          text-align: left;\n          font-size: var(\n            --paper-input-container-shared-input-style_-_font-size\n          );\n        }\n\n        :host([rtl]) th {\n          text-align: right;\n        }\n\n        tr {\n          vertical-align: top;\n          direction: ltr;\n        }\n\n        tr:nth-child(odd) {\n          background-color: var(--table-row-background-color, #fff);\n        }\n\n        tr:nth-child(even) {\n          background-color: var(--table-row-alternative-background-color, #eee);\n        }\n        td {\n          padding: 4px;\n          min-width: 200px;\n          word-break: break-word;\n        }\n      "])))]}}]}}),d.oi)}}]);