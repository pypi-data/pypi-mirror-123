"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[25825],{7323:(e,t,r)=>{r.d(t,{p:()=>i});const i=(e,t)=>e&&e.config.components.includes(t)},71186:(e,t,r)=>{var i=r(7599),n=r(5701),a=r(17717),o=r(55070),s=r(18457);r(32833);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var a="static"===n?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const y=e=>{const t=parseFloat(e);return isFinite(t)?t:null};let v=function(e,t,r,i){var n=l();if(i)for(var a=0;a<i.length;a++)n=i[a](n);var o=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var n,a=e[i];if("method"===a.kind&&(n=t.find(r)))if(h(a.descriptor)||h(n.descriptor)){if(u(a)||u(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(u(a)){if(u(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}d(a,n)}else t.push(a)}return t}(o.d.map(c)),e);return n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"data",value:()=>[]},{kind:"field",decorators:[(0,n.C)()],key:"names",value:()=>!1},{kind:"field",decorators:[(0,n.C)()],key:"unit",value:void 0},{kind:"field",decorators:[(0,n.C)()],key:"identifier",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"isSingleDevice",value:()=>!1},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"endTime",value:void 0},{kind:"field",decorators:[(0,a.S)()],key:"_chartData",value:void 0},{kind:"field",decorators:[(0,a.S)()],key:"_chartOptions",value:void 0},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-chart-base
        .data=${this._chartData}
        .options=${this._chartOptions}
        chart-type="line"
      ></ha-chart-base>
    `}},{kind:"method",key:"willUpdate",value:function(e){this.hasUpdated||(this._chartOptions={parsing:!1,animation:!1,scales:{x:{type:"time",adapters:{date:{locale:this.hass.locale}},ticks:{maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:e=>e.tick&&e.tick.major?{weight:"bold"}:{}},time:{tooltipFormat:"datetimeseconds"}},y:{ticks:{maxTicksLimit:7},title:{display:!0,text:this.unit}}},plugins:{tooltip:{mode:"nearest",callbacks:{label:e=>`${e.dataset.label}: ${(0,s.u)(e.parsed.y,this.hass.locale)} ${this.unit}`}},filler:{propagate:!0},legend:{display:!this.isSingleDevice,labels:{usePointStyle:!0}}},hover:{mode:"nearest"},elements:{line:{tension:.1,borderWidth:1.5},point:{hitRadius:5}},locale:(0,s.H)(this.hass.locale)}),e.has("data")&&this._generateData()}},{kind:"method",key:"_generateData",value:function(){let e=0;const t=getComputedStyle(this),r=this.data,i=[];let n;if(0===r.length)return;n=this.endTime||new Date(Math.max(...r.map((e=>new Date(e.states[e.states.length-1].last_changed).getTime())))),n>new Date&&(n=new Date);const a=this.names||{};r.forEach((r=>{const s=r.domain,l=a[r.entity_id]||r.name;let c=null;const d=[],u=(e,t)=>{t&&(e>n||(d.forEach(((r,i)=>{null===t[i]&&c&&null!==c[i]&&r.data.push({x:e.getTime(),y:c[i]}),r.data.push({x:e.getTime(),y:t[i]})})),c=t))},h=(t,r=!1,i=!1,n)=>{n||(n=(0,o.E)(e),e++),d.push({label:t,fill:!!i&&"origin",borderColor:n,backgroundColor:n+"7F",stepped:!!r&&"before",pointRadius:0,data:[]})};if("thermostat"===s||"climate"===s||"water_heater"===s){const e=r.states.some((e=>{var t;return null===(t=e.attributes)||void 0===t?void 0:t.hvac_action})),i="climate"===s&&e?e=>{var t;return"heating"===(null===(t=e.attributes)||void 0===t?void 0:t.hvac_action)}:e=>"heat"===e.state,n="climate"===s&&e?e=>{var t;return"cooling"===(null===(t=e.attributes)||void 0===t?void 0:t.hvac_action)}:e=>"cool"===e.state,a=r.states.some(i),o=r.states.some(n),c=r.states.some((e=>e.attributes&&e.attributes.target_temp_high!==e.attributes.target_temp_low));h(`${this.hass.localize("ui.card.climate.current_temperature",{name:l})}`,!0),a&&h(`${this.hass.localize("ui.card.climate.heating",{name:l})}`,!0,!0,t.getPropertyValue("--state-climate-heat-color")),o&&h(`${this.hass.localize("ui.card.climate.cooling",{name:l})}`,!0,!0,t.getPropertyValue("--state-climate-cool-color")),c?(h(`${this.hass.localize("ui.card.climate.target_temperature_mode",{name:l,mode:this.hass.localize("ui.card.climate.high")})}`,!0),h(`${this.hass.localize("ui.card.climate.target_temperature_mode",{name:l,mode:this.hass.localize("ui.card.climate.low")})}`,!0)):h(`${this.hass.localize("ui.card.climate.target_temperature_entity",{name:l})}`,!0),r.states.forEach((e=>{if(!e.attributes)return;const t=y(e.attributes.current_temperature),r=[t];if(a&&r.push(i(e)?t:null),o&&r.push(n(e)?t:null),c){const t=y(e.attributes.target_temp_high),i=y(e.attributes.target_temp_low);r.push(t,i),u(new Date(e.last_changed),r)}else{const t=y(e.attributes.temperature);r.push(t),u(new Date(e.last_changed),r)}}))}else if("humidifier"===s)h(`${this.hass.localize("ui.card.humidifier.target_humidity_entity",{name:l})}`,!0),h(`${this.hass.localize("ui.card.humidifier.on_entity",{name:l})}`,!0,!0),r.states.forEach((e=>{if(!e.attributes)return;const t=y(e.attributes.humidity),r=[t];r.push("on"===e.state?t:null),u(new Date(e.last_changed),r)}));else{let e,t;h(l,"sensor"===s);let i=null;r.states.forEach((r=>{const n=y(r.state),a=new Date(r.last_changed);if(null!==n&&i){var o;const r=a.getTime(),s=i.getTime(),l=null===(o=t)||void 0===o?void 0:o.getTime();u(i,[(s-l)/(r-l)*(n-e)+e]),u(new Date(s+1),[null]),u(a,[n]),t=a,e=n,i=null}else null!==n&&null===i?(u(a,[n]),t=a,e=n):null===n&&null===i&&void 0!==e&&(i=a)}))}u(n,c),Array.prototype.push.apply(i,d)})),this._chartData={datasets:i}}}]}}),i.oi);customElements.define("state-history-chart-line",v)},69884:(e,t,r)=>{r.a(e,(async e=>{var t=r(7599),i=r(26767),n=r(5701),a=r(17717),o=r(55070),s=r(44583),l=r(58831),c=r(18457),d=r(87744),u=(r(32833),e([s]));function h(){h=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var a="static"===n?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!m(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return k(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?k(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function k(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}s=(u.then?await u:u)[0];const b=new Set(["battery","door","garage_door","gas","lock","motion","opening","problem","safety","smoke","window"]),w=new Set(["on","off","home","not_home","unavailable","unknown","idle"]),E=new Map;let _=0;const D=(e,t,r)=>{if("on"!==e&&"off"!==e||!(e=>e&&"binary_sensor"===(0,l.M)(e.entity_id)&&"device_class"in e.attributes&&b.has(e.attributes.device_class))(t)||(e="on"===e?"off":"on"),E.has(e))return E.get(e);if(w.has(e)){const t=r.getPropertyValue(`--state-${e}-color`);return E.set(e,t),t}const i=(0,o.E)(_);return _++,E.set(e,i),i};!function(e,t,r,i){var n=h();if(i)for(var a=0;a<i.length;a++)n=i[a](n);var o=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var n,a=e[i];if("method"===a.kind&&(n=t.find(r)))if(y(a.descriptor)||y(n.descriptor)){if(m(a)||m(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(m(a)){if(m(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}f(a,n)}else t.push(a)}return t}(o.d.map(p)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([(0,i.M)("state-history-chart-timeline")],(function(e,r){return{F:class extends r{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"data",value:()=>[]},{kind:"field",decorators:[(0,n.C)()],key:"names",value:()=>!1},{kind:"field",decorators:[(0,n.C)()],key:"unit",value:void 0},{kind:"field",decorators:[(0,n.C)()],key:"identifier",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"isSingleDevice",value:()=>!1},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"endTime",value:void 0},{kind:"field",decorators:[(0,a.S)()],key:"_chartData",value:void 0},{kind:"field",decorators:[(0,a.S)()],key:"_chartOptions",value:void 0},{kind:"method",key:"render",value:function(){return t.dy`
      <ha-chart-base
        .data=${this._chartData}
        .options=${this._chartOptions}
        .height=${30*this.data.length+30}
        chart-type="timeline"
      ></ha-chart-base>
    `}},{kind:"method",key:"willUpdate",value:function(e){this.hasUpdated||(this._chartOptions={maintainAspectRatio:!1,parsing:!1,animation:!1,scales:{x:{type:"timeline",position:"bottom",adapters:{date:{locale:this.hass.locale}},ticks:{autoSkip:!0,maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:e=>e.tick&&e.tick.major?{weight:"bold"}:{}},grid:{offset:!1},time:{tooltipFormat:"datetimeseconds"}},y:{type:"category",barThickness:20,offset:!0,grid:{display:!1,drawBorder:!1,drawTicks:!1},ticks:{display:1!==this.data.length},afterSetDimensions:e=>{e.maxWidth=.18*e.chart.width},position:(0,d.HE)(this.hass)?"right":"left"}},plugins:{tooltip:{mode:"nearest",callbacks:{title:e=>e[0].chart.data.labels[e[0].datasetIndex],beforeBody:e=>e[0].dataset.label||"",label:e=>{const t=e.dataset.data[e.dataIndex];return[t.label||"",(0,s.E8)(t.start,this.hass.locale),(0,s.E8)(t.end,this.hass.locale)]},labelColor:e=>({borderColor:e.dataset.data[e.dataIndex].color,backgroundColor:e.dataset.data[e.dataIndex].color})}},filler:{propagate:!0}},locale:(0,c.H)(this.hass.locale)}),e.has("data")&&this._generateData()}},{kind:"method",key:"_generateData",value:function(){const e=getComputedStyle(this);let t=this.data;t||(t=[]);const r=new Date(t.reduce(((e,t)=>Math.min(e,new Date(t.data[0].last_changed).getTime())),(new Date).getTime()));let i=this.endTime||new Date(t.reduce(((e,t)=>Math.max(e,new Date(t.data[t.data.length-1].last_changed).getTime())),r.getTime()));i>new Date&&(i=new Date);const n=[],a=[],o=this.names||{};t.forEach((t=>{let s,l=null,c=null,d=r;const u=o[t.entity_id]||t.name,h=[];t.data.forEach((r=>{let n=r.state;n||(n=null),new Date(r.last_changed)>i||(null===l?(l=n,c=r.state_localize,d=new Date(r.last_changed)):n!==l&&(s=new Date(r.last_changed),h.push({start:d,end:s,label:c,color:D(l,this.hass.states[t.entity_id],e)}),l=n,c=r.state_localize,d=s))})),null!==l&&h.push({start:d,end:i,label:c,color:D(l,this.hass.states[t.entity_id],e)}),a.push({data:h,label:t.entity_id}),n.push(u)})),this._chartData={labels:n,datasets:a}}},{kind:"get",static:!0,key:"styles",value:function(){return t.iv`
      ha-chart-base {
        --chart-max-height: none;
      }
    `}}]}}),t.oi)}))},77243:(e,t,r)=>{r.a(e,(async e=>{var t=r(7599),i=r(26767),n=r(5701),a=r(7323),o=(r(71186),r(69884)),s=e([o]);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var a="static"===n?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}o=(s.then?await s:s)[0];!function(e,t,r,i){var n=l();if(i)for(var a=0;a<i.length;a++)n=i[a](n);var o=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var n,a=e[i];if("method"===a.kind&&(n=t.find(r)))if(h(a.descriptor)||h(n.descriptor)){if(u(a)||u(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(u(a)){if(u(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}d(a,n)}else t.push(a)}return t}(o.d.map(c)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([(0,i.M)("state-history-charts")],(function(e,r){return{F:class extends r{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"historyData",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"names",value:()=>!1},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"endTime",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Boolean,attribute:"up-to-now"})],key:"upToNow",value:()=>!1},{kind:"field",decorators:[(0,n.C)({type:Boolean,attribute:"no-single"})],key:"noSingle",value:()=>!1},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"isLoadingData",value:()=>!1},{kind:"method",key:"render",value:function(){if(!(0,a.p)(this.hass,"history"))return t.dy` <div class="info">
        ${this.hass.localize("ui.components.history_charts.history_disabled")}
      </div>`;if(this.isLoadingData&&!this.historyData)return t.dy` <div class="info">
        ${this.hass.localize("ui.components.history_charts.loading_history")}
      </div>`;if(this._isHistoryEmpty())return t.dy` <div class="info">
        ${this.hass.localize("ui.components.history_charts.no_history_found")}
      </div>`;const e=this.upToNow?new Date:this.endTime||new Date;return t.dy`
      ${this.historyData.timeline.length?t.dy`
            <state-history-chart-timeline
              .hass=${this.hass}
              .data=${this.historyData.timeline}
              .endTime=${e}
              .noSingle=${this.noSingle}
              .names=${this.names}
            ></state-history-chart-timeline>
          `:t.dy``}
      ${this.historyData.line.map((r=>t.dy`
          <state-history-chart-line
            .hass=${this.hass}
            .unit=${r.unit}
            .data=${r.data}
            .identifier=${r.identifier}
            .isSingleDevice=${!this.noSingle&&r.data&&1===r.data.length}
            .endTime=${e}
            .names=${this.names}
          ></state-history-chart-line>
        `))}
    `}},{kind:"method",key:"shouldUpdate",value:function(e){return!(1===e.size&&e.has("hass"))}},{kind:"method",key:"_isHistoryEmpty",value:function(){const e=!this.historyData||!this.historyData.timeline||!this.historyData.line||0===this.historyData.timeline.length&&0===this.historyData.line.length;return!this.isLoadingData&&e}},{kind:"get",static:!0,key:"styles",value:function(){return t.iv`
      :host {
        display: block;
        /* height of single timeline chart = 60px */
        min-height: 60px;
      }
      .info {
        text-align: center;
        line-height: 60px;
        color: var(--secondary-text-color);
      }
    `}}]}}),t.oi)}))},58763:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{vq:()=>p,_J:()=>f,Nu:()=>y,uR:()=>v,dL:()=>g,h_:()=>k,Cj:()=>b,hN:()=>w,Kj:()=>E,q6:()=>_,Nw:()=>D,m2:()=>S,VU:()=>C,Kk:()=>P});var i=r(59429),n=r(79021),a=r(13250),o=r(32182),s=r(29171),l=r(22311),c=r(91741),d=e([s]);s=(d.then?await d:d)[0];const u=["climate","humidifier","water_heater"],h=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],p=(e,t,r,i,n=!1,a,o=!0)=>{let s="history/period";return r&&(s+="/"+r.toISOString()),s+="?filter_entity_id="+t,i&&(s+="&end_time="+i.toISOString()),n&&(s+="&skip_initial_state"),void 0!==a&&(s+=`&significant_changes_only=${Number(a)}`),o&&(s+="&minimal_response"),e.callApi("GET",s)},f=(e,t,r,i)=>e.callApi("GET",`history/period/${t.toISOString()}?end_time=${r.toISOString()}&minimal_response${i?`&filter_entity_id=${i}`:""}`),m=(e,t)=>e.state===t.state&&(!e.attributes||!t.attributes||h.every((r=>e.attributes[r]===t.attributes[r]))),y=(e,t,r)=>{const i={},n=[];if(!t)return{line:[],timeline:[]};t.forEach((t=>{if(0===t.length)return;const a=t.find((e=>e.attributes&&("unit_of_measurement"in e.attributes||"state_class"in e.attributes)));let o;o=a?a.attributes.unit_of_measurement||" ":{climate:e.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:e.config.unit_system.temperature}[(0,l.N)(t[0])],o?o in i?i[o].push(t):i[o]=[t]:n.push(((e,t,r)=>{const i=[],n=r.length-1;for(const a of r)i.length>0&&a.state===i[i.length-1].state||(a.entity_id||(a.attributes=r[n].attributes,a.entity_id=r[n].entity_id),i.push({state_localize:(0,s.D)(e,a,t),state:a.state,last_changed:a.last_changed}));return{name:(0,c.C)(r[0]),entity_id:r[0].entity_id,data:i}})(r,e.locale,t))}));return{line:Object.keys(i).map((e=>((e,t)=>{const r=[];for(const e of t){const t=e[e.length-1],i=(0,l.N)(t),n=[];for(const t of e){let e;if(u.includes(i)){e={state:t.state,last_changed:t.last_updated,attributes:{}};for(const r of h)r in t.attributes&&(e.attributes[r]=t.attributes[r])}else e=t;n.length>1&&m(e,n[n.length-1])&&m(e,n[n.length-2])||n.push(e)}r.push({domain:i,name:(0,c.C)(t),entity_id:t.entity_id,states:n})}return{unit:e,identifier:t.map((e=>e[0].entity_id)).join(""),data:r}})(e,i[e]))),timeline:n}},v=(e,t)=>e.callWS({type:"history/list_statistic_ids",statistic_type:t}),g=(e,t,r,i,n="hour")=>e.callWS({type:"history/statistics_during_period",start_time:t.toISOString(),end_time:null==r?void 0:r.toISOString(),statistic_ids:i,period:n}),k=e=>e.callWS({type:"recorder/validate_statistics"}),b=(e,t,r)=>e.callWS({type:"recorder/update_statistics_metadata",statistic_id:t,unit_of_measurement:r}),w=(e,t)=>e.callWS({type:"recorder/clear_statistics",statistic_ids:t}),E=e=>{if(!e||e.length<2)return null;const t=e[e.length-1].sum;if(null===t)return null;const r=e[0].sum;return null===r?t:t-r},_=(e,t)=>{let r=null;for(const i of t){if(!(i in e))continue;const t=E(e[i]);null!==t&&(null===r?r=t:r+=t)}return r},D=(e,t)=>e.some((e=>null!==e[t])),S=(e,t)=>{let r=null;if(0===t.length||0===e.length)return null;const i=(e=>{const t={};return e.forEach((e=>{if(0===e.length)return;let r=null;e.forEach((e=>{if(null===e.sum)return;if(null===r)return void(r=e.sum);const i=e.sum-r;e.start in t?t[e.start]+=i:t[e.start]=i,r=e.sum}))})),t})(t);return e.forEach((e=>{const t=i[e.start];void 0!==t&&(null===r?r=t*(e.mean/100):r+=t*(e.mean/100))})),r},C=e=>{if(null==e||!e.length)return[];const t=[];let r,a;e.length>1&&new Date(e[0].start).getDate()===new Date(e[1].start).getDate()&&t.push({...e[0],start:(0,i.Z)((0,n.Z)(new Date(e[0].start),-1)).toISOString()});for(const n of e){const e=new Date(n.start).getDate();void 0===a&&(a=e),a!==e&&(t.push({...r,start:(0,i.Z)(new Date(r.start)).toISOString()}),a=e),r=n}return t.push({...r,start:(0,i.Z)(new Date(r.start)).toISOString()}),t},P=e=>{if(null==e||!e.length)return[];const t=[];let r,i;e.length>1&&new Date(e[0].start).getMonth()===new Date(e[1].start).getMonth()&&t.push({...e[0],start:(0,a.Z)((0,o.Z)(new Date(e[0].start),-1)).toISOString()});for(const n of e){const e=new Date(n.start).getMonth();void 0===i&&(i=e),i!==e&&(t.push({...r,start:(0,a.Z)(new Date(r.start)).toISOString()}),i=e),r=n}return t.push({...r,start:(0,a.Z)(new Date(r.start)).toISOString()}),t}}))}}]);
//# sourceMappingURL=c5776de1.js.map