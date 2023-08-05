/*! For license information please see 255aed7b.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[18263],{49706:(e,t,r)=>{r.d(t,{Rb:()=>s,Zy:()=>i,h2:()=>a,PS:()=>o,l:()=>n,ht:()=>l,f0:()=>c,tj:()=>d,uo:()=>h,lC:()=>u,Kk:()=>p,iY:()=>m,ot:()=>f,gD:()=>y});const s="hass:bookmark",i={alert:"hass:alert",alexa:"hass:amazon-alexa",air_quality:"hass:air-filter",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:cog",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:toggle-switch-outline",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:form-textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",number:"hass:ray-vertex",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",select:"hass:format-list-bulleted",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer-outline",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",zone:"hass:map-marker-radius"},a={aqi:"hass:air-filter",battery:"hass:battery",carbon_dioxide:"mdi:molecule-co2",carbon_monoxide:"mdi:molecule-co",current:"hass:current-ac",date:"hass:calendar",energy:"hass:lightning-bolt",gas:"hass:gas-cylinder",humidity:"hass:water-percent",illuminance:"hass:brightness-5",monetary:"mdi:cash",nitrogen_dioxide:"mdi:molecule",nitrogen_monoxide:"mdi:molecule",nitrous_oxide:"mdi:molecule",ozone:"mdi:molecule",pm1:"mdi:molecule",pm10:"mdi:molecule",pm25:"mdi:molecule",power:"hass:flash",power_factor:"hass:angle-acute",pressure:"hass:gauge",signal_strength:"hass:wifi",sulphur_dioxide:"mdi:molecule",temperature:"hass:thermometer",timestamp:"hass:clock",volatile_organic_compounds:"mdi:molecule",voltage:"hass:sine-wave"},o=["climate","cover","configurator","input_select","input_number","input_text","lock","media_player","number","scene","script","select","timer","vacuum","water_heater"],n=["alarm_control_panel","automation","camera","climate","configurator","counter","cover","fan","group","humidifier","input_datetime","light","lock","media_player","person","remote","script","sun","timer","vacuum","water_heater","weather"],l=["input_number","input_select","input_text","number","scene","select"],c=["camera","configurator","scene"],d=["closed","locked","off"],h="on",u="off",p=new Set(["fan","input_boolean","light","switch","group","automation","humidifier"]),m=new Set(["camera","media_player"]),f="°C",y="°F"},349:(e,t,r)=>{function s(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}r.d(t,{m:()=>a});const i=new class{constructor(){s(this,"_storage",{}),s(this,"_listeners",{}),window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const t=window.localStorage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const r=this._listeners[e].indexOf(t);-1!==r&&this._listeners[e].splice(r,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){this._storage[e]=t;try{window.localStorage.setItem(e,JSON.stringify(t))}catch(e){}}},a=(e,t,r)=>s=>{const a=String(s.key);e=e||String(s.key);const o=s.initializer?s.initializer():void 0;i.addFromStorage(e);const n=()=>i.hasKey(e)?i.getValue(e):o;return{kind:"method",placement:"prototype",key:s.key,descriptor:{set(r){((r,a)=>{let o;t&&(o=n()),i.setValue(e,a),t&&r.requestUpdate(s.key,o)})(this,r)},get:()=>n(),enumerable:!0,configurable:!0},finisher(o){if(t){const t=o.prototype.connectedCallback,n=o.prototype.disconnectedCallback;o.prototype.connectedCallback=function(){var r;t.call(this),this[`__unbsubLocalStorage${a}`]=(r=this,i.subscribeChanges(e,(e=>{r.requestUpdate(s.key,e)})))},o.prototype.disconnectedCallback=function(){n.call(this),this[`__unbsubLocalStorage${a}`]()},o.createProperty(s.key,{noAccessor:!0,...r})}}}}},97798:(e,t,r)=>{r.d(t,{g:()=>s});const s=e=>{switch(e){case"armed_away":return"hass:shield-lock";case"armed_vacation":return"hass:shield-airplane";case"armed_home":return"hass:shield-home";case"armed_night":return"hass:shield-moon";case"armed_custom_bypass":return"hass:security";case"pending":return"hass:shield-outline";case"triggered":return"hass:bell-ring";case"disarmed":return"hass:shield-off";default:return"hass:shield"}}},44634:(e,t,r)=>{r.d(t,{M:()=>s});const s=(e,t)=>{const r=Number(e.state),s=t&&"on"===t.state;let i="hass:battery";if(isNaN(r))return"off"===e.state?i+="-full":"on"===e.state?i+="-alert":i+="-unknown",i;const a=10*Math.round(r/10);return s&&r>10?i+=`-charging-${a}`:s?i+="-outline":r<=5?i+="-alert":r>5&&r<95&&(i+=`-${a}`),i}},82943:(e,t,r)=>{r.d(t,{m2:()=>s,q_:()=>i,ow:()=>a});const s=(e,t)=>{const r="closed"!==e;switch(null==t?void 0:t.attributes.device_class){case"garage":switch(e){case"opening":return"hass:arrow-up-box";case"closing":return"hass:arrow-down-box";case"closed":return"hass:garage";default:return"hass:garage-open"}case"gate":switch(e){case"opening":case"closing":return"hass:gate-arrow-right";case"closed":return"hass:gate";default:return"hass:gate-open"}case"door":return r?"hass:door-open":"hass:door-closed";case"damper":return r?"hass:circle":"hass:circle-slice-8";case"shutter":switch(e){case"opening":return"hass:arrow-up-box";case"closing":return"hass:arrow-down-box";case"closed":return"hass:window-shutter";default:return"hass:window-shutter-open"}case"blind":case"curtain":case"shade":switch(e){case"opening":return"hass:arrow-up-box";case"closing":return"hass:arrow-down-box";case"closed":return"hass:blinds";default:return"hass:blinds-open"}case"window":switch(e){case"opening":return"hass:arrow-up-box";case"closing":return"hass:arrow-down-box";case"closed":return"hass:window-closed";default:return"hass:window-open"}}switch(e){case"opening":return"hass:arrow-up-box";case"closing":return"hass:arrow-down-box";case"closed":return"hass:window-closed";default:return"hass:window-open"}},i=e=>{switch(e.attributes.device_class){case"awning":case"door":case"gate":return"hass:arrow-expand-horizontal";default:return"hass:arrow-up"}},a=e=>{switch(e.attributes.device_class){case"awning":case"door":case"gate":return"hass:arrow-collapse-horizontal";default:return"hass:arrow-down"}}},16023:(e,t,r)=>{r.d(t,{K:()=>l});var s=r(49706),i=r(97798);var a=r(82943),o=r(44634),n=r(41499);const l=(e,t,r)=>{const l=void 0!==r?r:null==t?void 0:t.state;switch(e){case"alarm_control_panel":return(0,i.g)(l);case"binary_sensor":return((e,t)=>{const r="off"===e;switch(null==t?void 0:t.attributes.device_class){case"battery":return r?"hass:battery":"hass:battery-outline";case"battery_charging":return r?"hass:battery":"hass:battery-charging";case"cold":return r?"hass:thermometer":"hass:snowflake";case"connectivity":return r?"hass:server-network-off":"hass:server-network";case"door":return r?"hass:door-closed":"hass:door-open";case"garage_door":return r?"hass:garage":"hass:garage-open";case"power":case"plug":return r?"hass:power-plug-off":"hass:power-plug";case"gas":case"problem":case"safety":return r?"hass:check-circle":"hass:alert-circle";case"smoke":return r?"hass:check-circle":"hass:smoke";case"heat":return r?"hass:thermometer":"hass:fire";case"light":return r?"hass:brightness-5":"hass:brightness-7";case"lock":return r?"hass:lock":"hass:lock-open";case"moisture":return r?"hass:water-off":"hass:water";case"motion":return r?"hass:walk":"hass:run";case"occupancy":case"presence":return r?"hass:home-outline":"hass:home";case"opening":return r?"hass:square":"hass:square-outline";case"sound":return r?"hass:music-note-off":"hass:music-note";case"update":return r?"mdi:package":"mdi:package-up";case"vibration":return r?"hass:crop-portrait":"hass:vibrate";case"window":return r?"hass:window-closed":"hass:window-open";default:return r?"hass:radiobox-blank":"hass:checkbox-marked-circle"}})(l,t);case"cover":return(0,a.m2)(l,t);case"humidifier":return r&&"off"===r?"hass:air-humidifier-off":"hass:air-humidifier";case"lock":switch(l){case"unlocked":return"hass:lock-open";case"jammed":return"hass:lock-alert";case"locking":case"unlocking":return"hass:lock-clock";default:return"hass:lock"}case"media_player":return"playing"===l?"hass:cast-connected":"hass:cast";case"zwave":switch(l){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}case"sensor":{const e=(e=>{const t=null==e?void 0:e.attributes.device_class;if(t&&t in s.h2)return s.h2[t];if(t===n.A)return e?(0,o.M)(e):"hass:battery";const r=null==e?void 0:e.attributes.unit_of_measurement;return r===s.ot||r===s.gD?"hass:thermometer":void 0})(t);if(e)return e;break}case"input_datetime":if(null==t||!t.attributes.has_date)return"hass:clock";if(!t.attributes.has_time)return"hass:calendar";break;case"sun":return"above_horizon"===(null==t?void 0:t.state)?s.Zy[e]:"hass:weather-night"}return e in s.Zy?s.Zy[e]:(console.warn(`Unable to find icon for domain ${e}`),s.Rb)}},36145:(e,t,r)=>{r.d(t,{M:()=>o});var s=r(49706),i=r(58831),a=r(16023);const o=e=>e?e.attributes.icon?e.attributes.icon:(0,a.K)((0,i.M)(e.entity_id),e):s.Rb},22098:(e,t,r)=>{var s=r(7599),i=r(26767),a=r(5701);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(s){t.forEach((function(t){var i=t.placement;if(t.kind===s&&("static"===i||"prototype"===i)){var a="static"===i?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var s=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],s=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),s.push.apply(s,t.finishers)}),this),!t)return{elements:r,finishers:s};var a=this.decorateConstructor(r,t);return s.push.apply(s,a.finishers),a.finishers=s,a},addElementPlacement:function(e,t,r){var s=t[e.placement];if(!r&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var r=[],s=[],i=e.decorators,a=i.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[a])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:s,extras:r}},decorateConstructor:function(e,t){for(var r=[],s=t.length-1;s>=0;s--){var i=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[s])(i)||i);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var n=o+1;n<e.length;n++)if(e[o].key===e[n].key&&e[o].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:s,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var s=(0,t[r])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function n(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var s=r.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,s=new Array(t);r<t;r++)s[r]=e[r];return s}!function(e,t,r,s){var i=o();if(s)for(var a=0;a<s.length;a++)i=s[a](i);var h=t((function(e){i.initializeInstanceElements(e,u.elements)}),r),u=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},s=0;s<e.length;s++){var i,a=e[s];if("method"===a.kind&&(i=t.find(r)))if(d(a.descriptor)||d(i.descriptor)){if(c(a)||c(i))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");i.descriptor=a.descriptor}else{if(c(a)){if(c(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");i.decorators=a.decorators}l(a,i)}else t.push(a)}return t}(h.d.map(n)),e);i.initializeClassElements(h.F,u.elements),i.runClassFinishers(h.F,u.finishers)}([(0,i.M)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.C)()],key:"header",value:void 0},{kind:"field",decorators:[(0,a.C)({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"get",static:!0,key:"styles",value:function(){return s.iv`
      :host {
        background: var(
          --ha-card-background,
          var(--card-background-color, white)
        );
        border-radius: var(--ha-card-border-radius, 4px);
        box-shadow: var(
          --ha-card-box-shadow,
          0px 2px 1px -1px rgba(0, 0, 0, 0.2),
          0px 1px 1px 0px rgba(0, 0, 0, 0.14),
          0px 1px 3px 0px rgba(0, 0, 0, 0.12)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: var(--ha-card-border-width, 1px);
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: 12px 16px 16px;
        display: block;
        margin-block-start: 0px;
        margin-block-end: 0px;
        font-weight: normal;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid var(--divider-color, #e8e8e8);
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return s.dy`
      ${this.header?s.dy`<h1 class="card-header">${this.header}</h1>`:s.dy``}
      <slot></slot>
    `}}]}}),s.oi)},41499:(e,t,r)=>{r.d(t,{A:()=>s,F:()=>i});const s="battery",i="timestamp"},26765:(e,t,r)=>{r.d(t,{Ys:()=>o,g7:()=>n,D9:()=>l});var s=r(47181);const i=()=>Promise.all([r.e(68200),r.e(30879),r.e(29907),r.e(34831),r.e(1281)]).then(r.bind(r,1281)),a=(e,t,r)=>new Promise((a=>{const o=t.cancel,n=t.confirm;(0,s.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:i,dialogParams:{...t,...r,cancel:()=>{a(!(null==r||!r.prompt)&&null),o&&o()},confirm:e=>{a(null==r||!r.prompt||e),n&&n(e)}}})})),o=(e,t)=>a(e,t),n=(e,t)=>a(e,t,{confirmation:!0}),l=(e,t)=>a(e,t,{prompt:!0})},27849:(e,t,r)=>{r(39841);var s=r(50856);r(28426);class i extends(customElements.get("app-header-layout")){static get template(){return s.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",i)},54845:(e,t,r)=>{r.d(t,{P:()=>s});const s=async()=>{"function"!=typeof ResizeObserver&&(window.ResizeObserver=(await r.e(88800).then(r.bind(r,88800))).default)}},70379:(e,t,r)=>{r.r(t);r(25230),r(53268),r(12730);var s=r(7599),i=r(26767),a=r(5701),o=r(349),n=r(22311),l=r(40095),c=(r(48932),r(13997),r(69371)),d=(r(27849),r(11654)),h=r(47181);function u(){u=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(s){t.forEach((function(t){var i=t.placement;if(t.kind===s&&("static"===i||"prototype"===i)){var a="static"===i?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var s=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],s=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!f(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),s.push.apply(s,t.finishers)}),this),!t)return{elements:r,finishers:s};var a=this.decorateConstructor(r,t);return s.push.apply(s,a.finishers),a.finishers=s,a},addElementPlacement:function(e,t,r){var s=t[e.placement];if(!r&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var r=[],s=[],i=e.decorators,a=i.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[a])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:s,extras:r}},decorateConstructor:function(e,t){for(var r=[],s=t.length-1;s>=0;s--){var i=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[s])(i)||i);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var n=o+1;n<e.length;n++)if(e[o].key===e[n].key&&e[o].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:s,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var s=(0,t[r])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var s=r.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,s=new Array(t);r<t;r++)s[r]=e[r];return s}!function(e,t,r,s){var i=u();if(s)for(var a=0;a<s.length;a++)i=s[a](i);var o=t((function(e){i.initializeInstanceElements(e,n.elements)}),r),n=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},s=0;s<e.length;s++){var i,a=e[s];if("method"===a.kind&&(i=t.find(r)))if(y(a.descriptor)||y(i.descriptor)){if(f(a)||f(i))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");i.descriptor=a.descriptor}else{if(f(a)){if(f(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");i.decorators=a.decorators}m(a,i)}else t.push(a)}return t}(o.d.map(p)),e);i.initializeClassElements(o.F,n.elements),i.runClassFinishers(o.F,n.finishers)}([(0,i.M)("ha-panel-media-browser")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.C)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.m)("mediaBrowseEntityId",!0)],key:"_entityId",value:()=>c.N8},{kind:"method",key:"render",value:function(){const e=this._entityId?this.hass.states[this._entityId]:void 0,t=this._entityId===c.N8?`${this.hass.localize("ui.components.media-browser.web-browser")}`:null!=e&&e.attributes.friendly_name?`${null==e?void 0:e.attributes.friendly_name}`:void 0;return s.dy`
      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title class="heading">
              <div>
                ${this.hass.localize("ui.components.media-browser.media-player-browser")}
              </div>
              <div class="secondary-text">${t||""}</div>
            </div>
            <mwc-button @click=${this._showSelectMediaPlayerDialog}>
              ${this.hass.localize("ui.components.media-browser.choose_player")}
            </mwc-button>
          </app-toolbar>
        </app-header>
        <div class="content">
          <ha-media-player-browse
            .hass=${this.hass}
            .entityId=${this._entityId}
            @media-picked=${this._mediaPicked}
          ></ha-media-player-browse>
        </div>
      </ha-app-layout>
    `}},{kind:"method",key:"_showSelectMediaPlayerDialog",value:function(){var e,t;e=this,t={mediaSources:this._mediaPlayerEntities,sourceSelectedCallback:e=>{this._entityId=e}},(0,h.B)(e,"show-dialog",{dialogTag:"hui-dialog-select-media-player",dialogImport:()=>Promise.all([r.e(29907),r.e(71662)]).then(r.bind(r,71662)),dialogParams:t})}},{kind:"method",key:"_mediaPicked",value:async function(e){const t=e.detail.item;if(this._entityId===c.N8){const e=await this.hass.callWS({type:"media_source/resolve_media",media_content_id:t.media_content_id});return s=this,i={sourceUrl:e.url,sourceType:e.mime_type,title:t.title},void(0,h.B)(s,"show-dialog",{dialogTag:"hui-dialog-web-browser-play-media",dialogImport:()=>Promise.all([r.e(29907),r.e(319),r.e(73132)]).then(r.bind(r,3212)),dialogParams:i})}var s,i;this.hass.callService("media_player","play_media",{entity_id:this._entityId,media_content_id:t.media_content_id,media_content_type:t.media_content_type})}},{kind:"get",key:"_mediaPlayerEntities",value:function(){return Object.values(this.hass.states).filter((e=>!("media_player"!==(0,n.N)(e)||!(0,l.e)(e,c.pu))))}},{kind:"get",static:!0,key:"styles",value:function(){return[d.Qx,s.iv`
        :host {
          --mdc-theme-primary: var(--app-header-text-color);
        }
        ha-media-player-browse {
          height: calc(100vh - var(--header-height));
        }
        :host([narrow]) app-toolbar mwc-button {
          width: 65px;
        }
        .heading {
          overflow: hidden;
          white-space: nowrap;
          margin-top: 4px;
        }
        .heading .secondary-text {
          font-size: 14px;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      `]}}]}}),s.oi)}}]);
//# sourceMappingURL=255aed7b.js.map