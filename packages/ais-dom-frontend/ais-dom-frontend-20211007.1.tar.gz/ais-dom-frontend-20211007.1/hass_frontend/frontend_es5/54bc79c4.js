"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2020],{23682:function(e,t,r){function n(e,t){if(t.length<e)throw new TypeError(e+" argument"+(e>1?"s":"")+" required, but only "+t.length+" present")}r.d(t,{Z:function(){return n}})},90394:function(e,t,r){function n(e){if(null===e||!0===e||!1===e)return NaN;var t=Number(e);return isNaN(t)?t:t<0?Math.ceil(t):Math.floor(t)}r.d(t,{Z:function(){return n}})},79021:function(e,t,r){r.d(t,{Z:function(){return a}});var n=r(90394),i=r(34327),o=r(23682);function a(e,t){(0,o.Z)(2,arguments);var r=(0,i.Z)(e),a=(0,n.Z)(t);return isNaN(a)?new Date(NaN):a?(r.setDate(r.getDate()+a),r):r}},32182:function(e,t,r){r.d(t,{Z:function(){return a}});var n=r(90394),i=r(34327),o=r(23682);function a(e,t){(0,o.Z)(2,arguments);var r=(0,i.Z)(e),a=(0,n.Z)(t);if(isNaN(a))return new Date(NaN);if(!a)return r;var s=r.getDate(),c=new Date(r.getTime());c.setMonth(r.getMonth()+a+1,0);var u=c.getDate();return s>=u?c:(r.setFullYear(c.getFullYear(),c.getMonth(),s),r)}},59429:function(e,t,r){r.d(t,{Z:function(){return o}});var n=r(34327),i=r(23682);function o(e){(0,i.Z)(1,arguments);var t=(0,n.Z)(e);return t.setHours(0,0,0,0),t}},13250:function(e,t,r){r.d(t,{Z:function(){return o}});var n=r(34327),i=r(23682);function o(e){(0,i.Z)(1,arguments);var t=(0,n.Z)(e);return t.setDate(1),t.setHours(0,0,0,0),t}},34327:function(e,t,r){r.d(t,{Z:function(){return o}});var n=r(23682);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function o(e){(0,n.Z)(1,arguments);var t=Object.prototype.toString.call(e);return e instanceof Date||"object"===i(e)&&"[object Date]"===t?new Date(e.getTime()):"number"==typeof e||"[object Number]"===t?new Date(e):("string"!=typeof e&&"[object String]"!==t||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}},8330:function(e,t,r){r.d(t,{P:function(){return n}});var n=function(e,t){var r,n=!(arguments.length>2&&void 0!==arguments[2])||arguments[2],i=!(arguments.length>3&&void 0!==arguments[3])||arguments[3],o=0;return function(){for(var a=arguments.length,s=new Array(a),c=0;c<a;c++)s[c]=arguments[c];var u=function(){o=!1===n?0:Date.now(),r=void 0,e.apply(void 0,s)},l=Date.now();o||!1!==n||(o=l);var f=t-(l-o);f<=0||f>t?(r&&(clearTimeout(r),r=void 0),o=l,e.apply(void 0,s)):r||!1===i||(r=window.setTimeout(u,f))}}},99990:function(e,t,r){r.d(t,{W:function(){return a}});var n=r(58763);function i(e,t,r,n,i,o,a){try{var s=e[o](a),c=s.value}catch(u){return void r(u)}s.done?t(c):Promise.resolve(c).then(n,i)}var o={};var a=function(e,t,r,a,u){var f=r.cacheKey,d=new Date,h=new Date(d);h.setHours(h.getHours()-r.hoursToShow);var p=h,y=!1,m=o[f+"_".concat(r.hoursToShow)];if(m&&p>=m.startTime&&p<=m.endTime&&m.language===u){if(p=m.endTime,y=!0,d<=m.endTime)return m.prom}else m=o[f]=function(e,t,r){return{prom:Promise.resolve({line:[],timeline:[]}),language:e,startTime:t,endTime:r,data:{line:[],timeline:[]}}}(u,h,d);var v=m.prom,g=function(){var r,u=(r=regeneratorRuntime.mark((function r(){var i,u,g;return regeneratorRuntime.wrap((function(r){for(;;)switch(r.prev=r.next){case 0:return r.prev=0,r.next=3,Promise.all([v,(0,n.vq)(e,t,p,d,y)]);case 3:u=r.sent,i=u[1],r.next=11;break;case 7:throw r.prev=7,r.t0=r.catch(0),delete o[f],r.t0;case 11:return g=(0,n.Nu)(e,i,a),y?(s(g.line,m.data.line),c(g.timeline,m.data.timeline),l(h,m.data)):m.data=g,r.abrupt("return",m.data);case 14:case"end":return r.stop()}}),r,null,[[0,7]])})),function(){var e=this,t=arguments;return new Promise((function(n,o){var a=r.apply(e,t);function s(e){i(a,n,o,s,c,"next",e)}function c(e){i(a,n,o,s,c,"throw",e)}s(void 0)}))});return function(){return u.apply(this,arguments)}}();return m.prom=g(),m.startTime=h,m.endTime=d,m.prom},s=function(e,t){e.forEach((function(e){var r=e.unit,n=t.find((function(e){return e.unit===r}));n?e.data.forEach((function(e){var t=n.data.find((function(t){return e.entity_id===t.entity_id}));t?t.states=t.states.concat(e.states):n.data.push(e)})):t.push(e)}))},c=function(e,t){e.forEach((function(e){var r=t.find((function(t){return t.entity_id===e.entity_id}));r?r.data=r.data.concat(e.data):t.push(e)}))},u=function(e,t){if(0===t.length)return t;var r=t.findIndex((function(t){return new Date(t.last_changed)>e}));if(0===r)return t;var n=-1===r?t.length-1:r-1;return t[n].last_changed=e,t.slice(n)},l=function(e,t){t.line.forEach((function(t){t.data.forEach((function(t){t.states=u(e,t.states)}))})),t.timeline.forEach((function(t){t.data=u(e,t.data)}))}},38026:function(e,t,r){r.r(t),r.d(t,{HuiHistoryGraphCard:function(){return N}});var n,i,o,a=r(7599),s=r(26767),c=r(5701),u=r(17717),l=r(228),f=r(8330),d=(r(22098),r(17633),r(99990)),h=r(53658),p=r(90271);function y(e){return y="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},y(e)}function m(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function v(e,t,r,n,i,o,a){try{var s=e[o](a),c=s.value}catch(u){return void r(u)}s.done?t(c):Promise.resolve(c).then(n,i)}function g(e){return function(){var t=this,r=arguments;return new Promise((function(n,i){var o=e.apply(t,r);function a(e){v(o,n,i,a,s,"next",e)}function s(e){v(o,n,i,a,s,"throw",e)}a(void 0)}))}}function w(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function b(e,t){return b=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},b(e,t)}function k(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=H(e);if(t){var i=H(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return E(this,r)}}function E(e,t){if(t&&("object"===y(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return _(e)}function _(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function S(){S=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!T(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var u=c.extras;if(u){for(var l=0;l<u.length;l++)this.addElementPlacement(u[l],t);r.push.apply(r,u)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return x(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?x(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=O(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:j(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=j(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function D(e){var t,r=O(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function P(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function T(e){return e.decorators&&e.decorators.length}function C(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function j(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function O(e){var t=function(e,t){if("object"!==y(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==y(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===y(t)?t:String(t)}function x(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function A(e,t,r){return A="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=H(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}},A(e,t,r||e)}function H(e){return H=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},H(e)}var N=function(e,t,r,n){var i=S();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(C(o.descriptor)||C(i.descriptor)){if(T(o)||T(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(T(o)){if(T(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}P(o,i)}else t.push(o)}return t}(a.d.map(D)),e);return i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,s.M)("hui-history-graph-card")],(function(e,t){var s,y,v=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&b(e,t)}(n,t);var r=k(n);function n(){var t;w(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(_(t)),t}return n}(t);return{F:v,d:[{kind:"method",static:!0,key:"getConfigElement",value:(y=g(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.all([r.e(88985),r.e(28055),r.e(69505),r.e(56087),r.e(36992),r.e(74535),r.e(36902),r.e(52524)]).then(r.bind(r,52524));case 2:return e.abrupt("return",document.createElement("hui-history-graph-card-editor"));case 3:case"end":return e.stop()}}),e)}))),function(){return y.apply(this,arguments)})},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"history-graph",entities:["sun.sun"]}}},{kind:"field",decorators:[(0,c.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,u.S)()],key:"_stateHistory",value:void 0},{kind:"field",decorators:[(0,u.S)()],key:"_config",value:void 0},{kind:"field",key:"_configEntities",value:void 0},{kind:"field",key:"_names",value:function(){return{}}},{kind:"field",key:"_cacheConfig",value:void 0},{kind:"field",key:"_fetching",value:function(){return!1}},{kind:"field",key:"_throttleGetStateHistory",value:void 0},{kind:"method",key:"getCardSize",value:function(){var e,t;return null!==(e=this._config)&&void 0!==e&&e.title?2:0+2*((null===(t=this._configEntities)||void 0===t?void 0:t.length)||1)}},{kind:"method",key:"setConfig",value:function(e){var t=this;if(!e.entities||!Array.isArray(e.entities))throw new Error("Entities need to be an array");if(!e.entities.length)throw new Error("You must include at least one entity");this._configEntities=e.entities?(0,p.A)(e.entities):[];var r=[];this._configEntities.forEach((function(e){r.push(e.entity),e.name&&(t._names[e.entity]=e.name)})),this._throttleGetStateHistory=(0,f.P)((function(){t._getStateHistory()}),e.refresh_interval||1e4),this._cacheConfig={cacheKey:r.join(),hoursToShow:e.hours_to_show||24},this._config=e}},{kind:"method",key:"shouldUpdate",value:function(e){return!!e.has("_stateHistory")||(0,h.W)(this,e)}},{kind:"method",key:"updated",value:function(e){if(A(H(v.prototype),"updated",this).call(this,e),this._config&&this.hass&&this._throttleGetStateHistory&&this._cacheConfig&&(e.has("_config")||e.has("hass"))){var t=e.get("_config");!e.has("_config")||(null==t?void 0:t.entities)===this._config.entities&&(null==t?void 0:t.hours_to_show)===this._config.hours_to_show?e.has("hass")&&setTimeout(this._throttleGetStateHistory,1e3):this._throttleGetStateHistory()}}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?(0,a.dy)(i||(i=m(["\n      <ha-card .header=",'>\n        <div\n          class="content ','"\n        >\n          <state-history-charts\n            .hass=',"\n            .isLoadingData=","\n            .historyData=","\n            .names=","\n            up-to-now\n            no-single\n          ></state-history-charts>\n        </div>\n      </ha-card>\n    "])),this._config.title,(0,l.$)({"has-header":!!this._config.title}),this.hass,!this._stateHistory,this._stateHistory,this._names):(0,a.dy)(n||(n=m([""])))}},{kind:"method",key:"_getStateHistory",value:(s=g(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!this._fetching){e.next=2;break}return e.abrupt("return");case 2:return this._fetching=!0,e.prev=3,e.t0=Object,e.t1={},e.next=8,(0,d.W)(this.hass,this._cacheConfig.cacheKey,this._cacheConfig,this.hass.localize,this.hass.language);case 8:e.t2=e.sent,this._stateHistory=e.t0.assign.call(e.t0,e.t1,e.t2);case 10:return e.prev=10,this._fetching=!1,e.finish(10);case 13:case"end":return e.stop()}}),e,this,[[3,,10,13]])}))),function(){return s.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,a.iv)(o||(o=m(["\n      ha-card {\n        height: 100%;\n      }\n      .content {\n        padding: 16px;\n      }\n      .has-header {\n        padding-top: 0;\n      }\n    "])))}}]}}),a.oi)}}]);