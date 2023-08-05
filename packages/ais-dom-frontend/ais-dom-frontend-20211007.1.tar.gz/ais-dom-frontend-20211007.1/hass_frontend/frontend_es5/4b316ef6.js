"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[81855],{55422:function(e,t,n){n.d(t,{jV:function(){return p},sS:function(){return m},rM:function(){return y},tf:function(){return w}});var r=n(49706),o=n(58831),i=n(29171),a=n(56007);function c(e,t){var n="undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(!n){if(Array.isArray(e)||(n=function(e,t){if(!e)return;if("string"==typeof e)return s(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return s(e,t)}(e))||t&&e&&"number"==typeof e.length){n&&(e=n);var r=0,o=function(){};return{s:o,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:o}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var i,a=!0,c=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return a=e.done,e},e:function(e){c=!0,i=e},f:function(){try{a||null==n.return||n.return()}finally{if(c)throw i}}}}function s(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function l(e,t,n,r,o,i,a){try{var c=e[i](a),s=c.value}catch(l){return void n(l)}c.done?t(s):Promise.resolve(s).then(r,o)}function u(e){return function(){var t=this,n=arguments;return new Promise((function(r,o){var i=e.apply(t,n);function a(e){l(i,r,o,a,c,"next",e)}function c(e){l(i,r,o,a,c,"throw",e)}a(void 0)}))}}var d,f="ui.components.logbook.messages",p=["proximity","sensor"],h={},m=32143==n.j?(d=u(regeneratorRuntime.mark((function e(t,n,r){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.t0=v,e.t1=t,e.next=4,g(t,n,void 0,void 0,void 0,r);case 4:return e.t2=e.sent,e.abrupt("return",(0,e.t0)(e.t1,e.t2));case 6:case"end":return e.stop()}}),e)}))),function(e,t,n){return d.apply(this,arguments)}):null,y=function(){var e=u(regeneratorRuntime.mark((function e(t,n,r,o,i){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.t0=v,e.t1=t,e.next=4,b(t,n,r,o,i);case 4:return e.t2=e.sent,e.abrupt("return",(0,e.t0)(e.t1,e.t2));case 6:case"end":return e.stop()}}),e)})));return function(t,n,r,o,i){return e.apply(this,arguments)}}(),v=function(e,t){var n,r=c(t);try{for(r.s();!(n=r.n()).done;){var i=n.value,a=e.states[i.entity_id];i.state&&a&&(i.message=k(e,i.state,a,(0,o.M)(i.entity_id)))}}catch(s){r.e(s)}finally{r.f()}return t},b=function(){var e=u(regeneratorRuntime.mark((function e(t,n,r,o,i){var a,c,s;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(a="*",o||(o=a),c="".concat(n).concat(r),h[c]||(h[c]={}),!(o in h[c])){e.next=6;break}return e.abrupt("return",h[c][o]);case 6:if(o===a||!h[c][a]){e.next=11;break}return e.next=9,h[c][a];case 9:return s=e.sent,e.abrupt("return",s.filter((function(e){return e.entity_id===o})));case 11:return h[c][o]=g(t,n,r,o!==a?o:void 0,i).then((function(e){return e.reverse()})),e.abrupt("return",h[c][o]);case 13:case"end":return e.stop()}}),e)})));return function(t,n,r,o,i){return e.apply(this,arguments)}}(),g=function(){var e=u(regeneratorRuntime.mark((function e(t,n,r,o,i,a){var c;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return c=new URLSearchParams,r&&c.append("end_time",r),o&&c.append("entity",o),i&&c.append("entity_matches_only",""),a&&c.append("context_id",a),e.abrupt("return",t.callApi("GET","logbook/".concat(n,"?").concat(c.toString())));case 6:case"end":return e.stop()}}),e)})));return function(t,n,r,o,i,a){return e.apply(this,arguments)}}(),w=function(e,t){h["".concat(e).concat(t)]={}},k=function(e,t,n,o){switch(o){case"device_tracker":case"person":return"not_home"===t?e.localize("".concat(f,".was_away")):"home"===t?e.localize("".concat(f,".was_at_home")):e.localize("".concat(f,".was_at_state"),"state",t);case"sun":return"above_horizon"===t?e.localize("".concat(f,".rose")):e.localize("".concat(f,".set"));case"binary_sensor":var c=t===r.uo,s=t===r.lC,l=n.attributes.device_class;switch(l){case"battery":if(c)return e.localize("".concat(f,".was_low"));if(s)return e.localize("".concat(f,".was_normal"));break;case"connectivity":if(c)return e.localize("".concat(f,".was_connected"));if(s)return e.localize("".concat(f,".was_disconnected"));break;case"door":case"garage_door":case"opening":case"window":if(c)return e.localize("".concat(f,".was_opened"));if(s)return e.localize("".concat(f,".was_closed"));break;case"lock":if(c)return e.localize("".concat(f,".was_unlocked"));if(s)return e.localize("".concat(f,".was_locked"));break;case"plug":if(c)return e.localize("".concat(f,".was_plugged_in"));if(s)return e.localize("".concat(f,".was_unplugged"));break;case"presence":if(c)return e.localize("".concat(f,".was_at_home"));if(s)return e.localize("".concat(f,".was_away"));break;case"safety":if(c)return e.localize("".concat(f,".was_unsafe"));if(s)return e.localize("".concat(f,".was_safe"));break;case"cold":case"gas":case"heat":case"moisture":case"motion":case"occupancy":case"power":case"problem":case"smoke":case"sound":case"vibration":if(c)return e.localize("".concat(f,".detected_device_class"),"device_class",l);if(s)return e.localize("".concat(f,".cleared_device_class"),"device_class",l)}break;case"cover":switch(t){case"open":return e.localize("".concat(f,".was_opened"));case"opening":return e.localize("".concat(f,".is_opening"));case"closing":return e.localize("".concat(f,".is_closing"));case"closed":return e.localize("".concat(f,".was_closed"))}break;case"lock":if("unlocked"===t)return e.localize("".concat(f,".was_unlocked"));if("locked"===t)return e.localize("".concat(f,".was_locked"))}return t===r.uo?e.localize("".concat(f,".turned_on")):t===r.lC?e.localize("".concat(f,".turned_off")):a.V_.includes(t)?e.localize("".concat(f,".became_unavailable")):e.localize("".concat(f,".changed_to_state"),"state",n?(0,i.D)(e.localize,n,e.locale,t):t)}},97740:function(e,t,n){var r,o,i,a,c,s,l,u,d,f,p,h=n(196),m=n(7599),y=n(26767),v=n(5701),b=n(84982),g=n(228),w=n(49706),k=n(12198),_=n(49684),x=n(25516),z=n(47181),E=n(58831),C=n(16023),P=n(87744),S=(n(3143),n(31206),n(42952),n(11654));function D(e){return D="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},D(e)}function A(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function T(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function j(e,t){return j=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},j(e,t)}function O(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=B(e);if(t){var o=B(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return I(this,n)}}function I(e,t){if(t&&("object"===D(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return R(e)}function R(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function B(e){return B=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},B(e)}function F(){F=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var i="static"===o?e:n;this.defineClassElement(i,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!$(e))return n.push(e);var t=this.decorateElement(e,o);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var i=this.decorateConstructor(n,t);return r.push.apply(r,i.finishers),i.finishers=r,i},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],o=e.decorators,i=o.length-1;i>=0;i--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,o[i])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&r.push(s.finisher);var l=s.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),i=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==i.finisher&&n.push(i.finisher),void 0!==i.elements){e=i.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return G(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?G(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=V(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var i={kind:t,key:n,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),i.initializer=e.initializer),i},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:U(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=U(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function M(e){var t,n=V(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function N(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function $(e){return e.decorators&&e.decorators.length}function L(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function U(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function V(e){var t=function(e,t){if("object"!==D(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==D(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===D(t)?t:String(t)}function G(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}!function(e,t,n,r){var o=F();if(r)for(var i=0;i<r.length;i++)o=r[i](o);var a=t((function(e){o.initializeInstanceElements(e,c.elements)}),n),c=o.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===i.key&&e.placement===i.placement},r=0;r<e.length;r++){var o,i=e[r];if("method"===i.kind&&(o=t.find(n)))if(L(i.descriptor)||L(o.descriptor)){if($(i)||$(o))throw new ReferenceError("Duplicated methods ("+i.key+") can't be decorated.");o.descriptor=i.descriptor}else{if($(i)){if($(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+i.key+").");o.decorators=i.decorators}N(i,o)}else t.push(i)}return t}(a.d.map(M)),e);o.initializeClassElements(a.F,c.elements),o.runClassFinishers(a.F,c.finishers)}([(0,y.M)("ha-logbook")],(function(e,t){var n=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&j(e,t)}(r,t);var n=O(r);function r(){var t;T(this,r);for(var o=arguments.length,i=new Array(o),a=0;a<o;a++)i[a]=arguments[a];return t=n.call.apply(n,[this].concat(i)),e(R(t)),t}return r}(t);return{F:n,d:[{kind:"field",decorators:[(0,v.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,v.C)({attribute:!1})],key:"userIdToName",value:function(){return{}}},{kind:"field",decorators:[(0,v.C)({attribute:!1})],key:"traceContexts",value:function(){return{}}},{kind:"field",decorators:[(0,v.C)({attribute:!1})],key:"entries",value:function(){return[]}},{kind:"field",decorators:[(0,v.C)({type:Boolean,attribute:"narrow"})],key:"narrow",value:function(){return!1}},{kind:"field",decorators:[(0,v.C)({attribute:"rtl",type:Boolean})],key:"_rtl",value:function(){return!1}},{kind:"field",decorators:[(0,v.C)({type:Boolean,attribute:"virtualize",reflect:!0})],key:"virtualize",value:function(){return!1}},{kind:"field",decorators:[(0,v.C)({type:Boolean,attribute:"no-icon"})],key:"noIcon",value:function(){return!1}},{kind:"field",decorators:[(0,v.C)({type:Boolean,attribute:"no-name"})],key:"noName",value:function(){return!1}},{kind:"field",decorators:[(0,v.C)({type:Boolean,attribute:"relative-time"})],key:"relativeTime",value:function(){return!1}},{kind:"field",decorators:[(0,x.i)(".container")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){var t=e.get("hass"),n=void 0===t||t.locale!==this.hass.locale;return e.has("entries")||e.has("traceContexts")||n}},{kind:"method",key:"updated",value:function(e){var t=e.get("hass");void 0!==t&&t.language===this.hass.language||(this._rtl=(0,P.HE)(this.hass))}},{kind:"method",key:"render",value:function(){var e,t=this;return null!==(e=this.entries)&&void 0!==e&&e.length?(0,m.dy)(o||(o=A(['\n      <div\n        class="container ha-scrollbar ','"\n        @scroll=',"\n      >\n        ","\n      </div>\n    "])),(0,g.$)({narrow:this.narrow,rtl:this._rtl,"no-name":this.noName,"no-icon":this.noIcon}),this._saveScrollPos,this.virtualize?(0,h.AR)({items:this.entries,layout:h.bW,renderItem:function(e,n){return t._renderLogbookItem(e,n)}}):this.entries.map((function(e,n){return t._renderLogbookItem(e,n)}))):(0,m.dy)(r||(r=A(['\n        <div class="container no-entries" .dir=',">\n          ","\n        </div>\n      "])),(0,P.$3)(this._rtl),this.hass.localize("ui.components.logbook.entries_not_found"))}},{kind:"method",key:"_renderLogbookItem",value:function(e,t){var n;if(void 0===t)return(0,m.dy)(i||(i=A([""])));var r=this.entries[t-1],o=e.entity_id?this.hass.states[e.entity_id]:void 0,p=e.context_user_id&&this.userIdToName[e.context_user_id],h=e.entity_id?(0,E.M)(e.entity_id):e.domain;return(0,m.dy)(a||(a=A(['\n      <div class="entry-container">\n        ','\n\n        <div class="entry ','">\n          <div class="icon-message">\n            ','\n            <div class="message-relative_time">\n              <div class="message">\n                ',"\n                ","\n                ",'\n              </div>\n              <div class="secondary">\n                <span\n                  >',"</span\n                >\n                -\n                <ha-relative-time\n                  .hass=","\n                  .datetime=","\n                  capitalize\n                ></ha-relative-time>\n                ","\n              </div>\n            </div>\n          </div>\n        </div>\n      </div>\n    "])),0===t||null!=e&&e.when&&null!=r&&r.when&&new Date(e.when).toDateString()!==new Date(r.when).toDateString()?(0,m.dy)(c||(c=A(['\n              <h4 class="date">\n                ',"\n              </h4>\n            "])),(0,k.p6)(new Date(e.when),this.hass.locale)):(0,m.dy)(s||(s=A([""]))),(0,g.$)({"no-entity":!e.entity_id}),this.noIcon?"":(0,m.dy)(l||(l=A(["\n                  <state-badge\n                    .hass=","\n                    .overrideIcon=","\n                    .overrideImage=","\n                  ></state-badge>\n                "])),this.hass,null!==(n=e.icon)&&void 0!==n?n:(0,C.K)(h,o,e.state),w.iY.has(h)?"":(null==o?void 0:o.attributes.entity_picture_local)||(null==o?void 0:o.attributes.entity_picture)),this.noName?"":(0,m.dy)(u||(u=A(['<a\n                      href="#"\n                      @click=',"\n                      .entityId=",'\n                      ><span class="name">',"</span></a\n                    >"])),this._entityClicked,e.entity_id,e.name),e.message,p?" ".concat(this.hass.localize("ui.components.logbook.by")," ").concat(p):e.context_event_type?"call_service"===e.context_event_type?" ".concat(this.hass.localize("ui.components.logbook.by_service"),"\n                  ").concat(e.context_domain,".").concat(e.context_service):e.context_entity_id===e.entity_id?" ".concat(this.hass.localize("ui.components.logbook.by"),"\n                  ").concat(e.context_name?e.context_name:e.context_event_type):(0,m.dy)(d||(d=A([" ",'\n                      <a\n                        href="#"\n                        @click=',"\n                        .entityId=",'\n                        class="name"\n                        >',"</a\n                      >"])),this.hass.localize("ui.components.logbook.by"),this._entityClicked,e.context_entity_id,e.context_entity_id_name):"",(0,_.Vu)(new Date(e.when),this.hass.locale),this.hass,e.when,"automation"===e.domain&&e.context_id in this.traceContexts?(0,m.dy)(f||(f=A(["\n                      -\n                      <a\n                        href=","\n                        >","</a\n                      >\n                    "])),"/config/automation/trace/".concat(this.traceContexts[e.context_id].item_id,"?run_id=").concat(this.traceContexts[e.context_id].run_id),this.hass.localize("ui.components.logbook.show_trace")):"")}},{kind:"method",decorators:[(0,b.h)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_entityClicked",value:function(e){var t=e.currentTarget.entityId;t&&(e.preventDefault(),e.stopPropagation(),(0,z.B)(this,"hass-more-info",{entityId:t}))}},{kind:"get",static:!0,key:"styles",value:function(){return[S.Qx,S.$c,(0,m.iv)(p||(p=A(["\n        :host([virtualize]) {\n          display: block;\n          height: 100%;\n        }\n\n        .rtl {\n          direction: ltr;\n        }\n\n        .entry-container {\n          width: 100%;\n        }\n\n        .entry {\n          display: flex;\n          width: 100%;\n          line-height: 2em;\n          padding: 8px 16px;\n          box-sizing: border-box;\n          border-top: 1px solid var(--divider-color);\n        }\n\n        .entry.no-entity,\n        .no-name .entry {\n          cursor: default;\n        }\n\n        .entry:hover {\n          background-color: rgba(var(--rgb-primary-text-color), 0.04);\n        }\n\n        .narrow:not(.no-icon) .time {\n          margin-left: 32px;\n        }\n\n        .message-relative_time {\n          display: flex;\n          flex-direction: column;\n        }\n\n        .secondary {\n          font-size: 12px;\n          line-height: 1.7;\n        }\n\n        .secondary a {\n          color: var(--secondary-text-color);\n        }\n\n        .date {\n          margin: 8px 0;\n          padding: 0 16px;\n        }\n\n        .narrow .date {\n          padding: 0 8px;\n        }\n\n        .rtl .date {\n          direction: rtl;\n        }\n\n        .icon-message {\n          display: flex;\n          align-items: center;\n        }\n\n        .no-entries {\n          text-align: center;\n          color: var(--secondary-text-color);\n        }\n\n        state-badge {\n          margin-right: 16px;\n          flex-shrink: 0;\n          color: var(--state-icon-color);\n        }\n\n        .message {\n          color: var(--primary-text-color);\n        }\n\n        .no-name .message:first-letter {\n          text-transform: capitalize;\n        }\n\n        a {\n          color: var(--primary-color);\n        }\n\n        .container {\n          max-height: var(--logbook-max-height);\n        }\n\n        :host([virtualize]) .container {\n          height: 100%;\n        }\n\n        .narrow .entry {\n          line-height: 1.5;\n          padding: 8px;\n        }\n\n        .narrow .icon-message state-badge {\n          margin-left: 0;\n        }\n      "])))]}}]}}),m.oi)}}]);