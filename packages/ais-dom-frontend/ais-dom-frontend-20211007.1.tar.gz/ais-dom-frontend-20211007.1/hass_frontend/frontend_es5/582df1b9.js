"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[53890],{53890:function(e,t,n){n.r(t),n.d(t,{HaAutomationTrace:function(){return oe}});var r,i,o,a,s,c,l,d,u,h,f,p,v,m,y,b,k,_,g=n(7599),w=n(26767),E=n(5701),x=n(17717),T=n(67352),I=n(228),S=n(86230),C=n(7323),P=n(44583),A=(n(54933),n(55422)),O=n(97389),j=n(26765),D=n(11654),L=n(29311),R=(n(71955),n(13126),n(89497),n(78940),n(10678),n(19476));function z(e){return z="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},z(e)}function N(e,t,n,r,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void n(l)}s.done?t(c):Promise.resolve(c).then(r,i)}function H(e){return function(){var t=this,n=arguments;return new Promise((function(r,i){var o=e.apply(t,n);function a(e){N(o,r,i,a,s,"next",e)}function s(e){N(o,r,i,a,s,"throw",e)}a(void 0)}))}}function M(e,t){return ne(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==n)return;var r,i,o=[],a=!0,s=!1;try{for(n=n.call(e);!(a=(r=n.next()).done)&&(o.push(r.value),!t||o.length!==t);a=!0);}catch(c){s=!0,i=c}finally{try{a||null==n.return||n.return()}finally{if(s)throw i}}return o}(e,t)||ee(e,t)||X()}function V(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function F(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function B(e,t){return B=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},B(e,t)}function U(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=ie(e);if(t){var i=ie(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return Z(this,n)}}function Z(e,t){if(t&&("object"===z(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return $(e)}function $(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function J(){J=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!Y(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,ne(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||ee(t)||X()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=K(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:G(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=G(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function Q(e){var t,n=K(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function W(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function Y(e){return e.decorators&&e.decorators.length}function q(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function G(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function K(e){var t=function(e,t){if("object"!==z(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==z(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===z(t)?t:String(t)}function X(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function ee(e,t){if(e){if("string"==typeof e)return te(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?te(e,t):void 0}}function te(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function ne(e){if(Array.isArray(e))return e}function re(e,t,n){return re="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=ie(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}},re(e,t,n||e)}function ie(e){return ie=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},ie(e)}var oe=function(e,t,n,r){var i=J();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),n),s=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(q(o.descriptor)||q(i.descriptor)){if(Y(o)||Y(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(Y(o)){if(Y(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}W(o,i)}else t.push(o)}return t}(a.d.map(Q)),e);return i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,w.M)("ha-automation-trace")],(function(e,t){var n,w,z=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&B(e,t)}(r,t);var n=U(r);function r(){var t;F(this,r);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=n.call.apply(n,[this].concat(o)),e($(t)),t}return r}(t);return{F:z,d:[{kind:"field",decorators:[(0,E.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,E.C)()],key:"automationId",value:void 0},{kind:"field",decorators:[(0,E.C)({attribute:!1})],key:"automations",value:void 0},{kind:"field",decorators:[(0,E.C)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,E.C)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,E.C)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,x.S)()],key:"_entityId",value:void 0},{kind:"field",decorators:[(0,x.S)()],key:"_traces",value:void 0},{kind:"field",decorators:[(0,x.S)()],key:"_runId",value:void 0},{kind:"field",decorators:[(0,x.S)()],key:"_selected",value:void 0},{kind:"field",decorators:[(0,x.S)()],key:"_trace",value:void 0},{kind:"field",decorators:[(0,x.S)()],key:"_logbookEntries",value:void 0},{kind:"field",decorators:[(0,x.S)()],key:"_view",value:function(){return"details"}},{kind:"field",decorators:[(0,T.I)("hat-script-graph")],key:"_graph",value:void 0},{kind:"method",key:"render",value:function(){var e,t=this,n=this._entityId?this.hass.states[this._entityId]:void 0,_=this._graph,w=null==_?void 0:_.trackedNodes,E=null==_?void 0:_.renderedNodes,x=(null==n?void 0:n.attributes.friendly_name)||this._entityId;var T=(0,g.dy)(r||(r=V(['\n      <mwc-icon-button label="Refresh" @click=',">\n        <ha-svg-icon .path=","></ha-svg-icon>\n      </mwc-icon-button>\n      <mwc-icon-button\n        .disabled=",'\n        label="Download Trace"\n        @click=',"\n      >\n        <ha-svg-icon .path=","></ha-svg-icon>\n      </mwc-icon-button>\n    "])),this._refreshTraces,"M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z",!this._trace,this._downloadTrace,"M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z");return(0,g.dy)(i||(i=V(["\n      ","\n      <hass-tabs-subpage\n        .hass=","\n        .narrow=","\n        .route=","\n        .tabs=","\n      >\n        ",'\n        <div class="toolbar">\n          ',"\n          ","\n          ","\n        </div>\n\n        ","\n      </hass-tabs-subpage>\n    "])),"",this.hass,this.narrow,this.route,L.configSections.automation,this.narrow?(0,g.dy)(o||(o=V(['<span slot="header">','</span>\n              <div slot="toolbar-icon">',"</div>"])),x,T):"",this.narrow?"":(0,g.dy)(a||(a=V(["<div>\n                ",'\n                <a\n                  class="linkButton"\n                  href="/config/automation/edit/','"\n                >\n                  <mwc-icon-button label="Edit Automation" tabindex="-1">\n                    <ha-svg-icon .path=',"></ha-svg-icon>\n                  </mwc-icon-button>\n                </a>\n              </div>"])),x,this.automationId,"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"),this._traces&&this._traces.length>0?(0,g.dy)(s||(s=V(["\n                <div>\n                  <mwc-icon-button\n                    .disabled=",'\n                    label="Older trace"\n                    @click=',"\n                  >\n                    <ha-svg-icon .path=","></ha-svg-icon>\n                  </mwc-icon-button>\n                  <select .value="," @change=",">\n                    ","\n                  </select>\n                  <mwc-icon-button\n                    .disabled=",'\n                    label="Newer trace"\n                    @click=',"\n                  >\n                    <ha-svg-icon .path=","></ha-svg-icon>\n                  </mwc-icon-button>\n                </div>\n              "])),this._traces[this._traces.length-1].run_id===this._runId,this._pickOlderTrace,"M1,12L5,16V13H17.17C17.58,14.17 18.69,15 20,15A3,3 0 0,0 23,12A3,3 0 0,0 20,9C18.69,9 17.58,9.83 17.17,11H5V8L1,12Z",this._runId,this._pickTrace,(0,S.r)(this._traces,(function(e){return e.run_id}),(function(e){return(0,g.dy)(c||(c=V(["<option value=",">\n                          ","\n                        </option>"])),e.run_id,(0,P.E8)(new Date(e.timestamp.start),t.hass.locale))})),this._traces[0].run_id===this._runId,this._pickNewerTrace,"M23,12L19,16V13H6.83C6.42,14.17 5.31,15 4,15A3,3 0 0,1 1,12A3,3 0 0,1 4,9C5.31,9 6.42,9.83 6.83,11H19V8L23,12Z"):"",this.narrow?"":(0,g.dy)(l||(l=V(["<div>","</div>"])),T),void 0===this._traces?(0,g.dy)(d||(d=V(['<div class="container">Loading…</div>']))):0===this._traces.length?(0,g.dy)(u||(u=V(['<div class="container">No traces found</div>']))):void 0===this._trace?"":(0,g.dy)(h||(h=V(['\n              <div class="main">\n                <div class="graph">\n                  <hat-script-graph\n                    .trace=',"\n                    .selected=","\n                    @graph-node-selected=",'\n                  ></hat-script-graph>\n                </div>\n\n                <div class="info">\n                  <div class="tabs top">\n                    ',"\n                    ","\n                  </div>\n                  ","\n                </div>\n              </div>\n            "])),this._trace,null===(e=this._selected)||void 0===e?void 0:e.path,this._pickNode,[["details","Step Details"],["timeline","Trace Timeline"],["logbook","Related logbook entries"],["config","Automation Config"]].map((function(e){var n=M(e,2),r=n[0],i=n[1];return(0,g.dy)(f||(f=V(['\n                        <button\n                          tabindex="0"\n                          .view=',"\n                          class=","\n                          @click=","\n                        >\n                          ","\n                        </button>\n                      "])),r,(0,I.$)({active:t._view===r}),t._showTab,i)})),this._trace.blueprint_inputs?(0,g.dy)(p||(p=V(['\n                          <button\n                            tabindex="0"\n                            .view=',"\n                            class=","\n                            @click=","\n                          >\n                            Blueprint Config\n                          </button>\n                        "])),"blueprint",(0,I.$)({active:"blueprint"===this._view}),this._showTab):"",void 0===this._selected||void 0===this._logbookEntries||void 0===w?"":"details"===this._view?(0,g.dy)(v||(v=V(["\n                        <ha-trace-path-details\n                          .hass=","\n                          .narrow=","\n                          .trace=","\n                          .selected=","\n                          .logbookEntries=","\n                          .trackedNodes=","\n                          .renderedNodes=","\n                        ></ha-trace-path-details>\n                      "])),this.hass,this.narrow,this._trace,this._selected,this._logbookEntries,w,E):"config"===this._view?(0,g.dy)(m||(m=V(["\n                        <ha-trace-config\n                          .hass=","\n                          .trace=","\n                        ></ha-trace-config>\n                      "])),this.hass,this._trace):"logbook"===this._view?(0,g.dy)(y||(y=V(["\n                        <ha-trace-logbook\n                          .hass=","\n                          .narrow=","\n                          .trace=","\n                          .logbookEntries=","\n                        ></ha-trace-logbook>\n                      "])),this.hass,this.narrow,this._trace,this._logbookEntries):"blueprint"===this._view?(0,g.dy)(b||(b=V(["\n                        <ha-trace-blueprint-config\n                          .hass=","\n                          .trace=","\n                        ></ha-trace-blueprint-config>\n                      "])),this.hass,this._trace):(0,g.dy)(k||(k=V(["\n                        <ha-trace-timeline\n                          .hass=","\n                          .trace=","\n                          .logbookEntries=","\n                          .selected=","\n                          @value-changed=","\n                        ></ha-trace-timeline>\n                      "])),this.hass,this._trace,this._logbookEntries,this._selected,this._timelinePathPicked)))}},{kind:"method",key:"firstUpdated",value:function(e){if(re(ie(z.prototype),"firstUpdated",this).call(this,e),this.automationId){var t=new URLSearchParams(location.search);this._loadTraces(t.get("run_id")||void 0)}}},{kind:"method",key:"updated",value:function(e){var t=this;if(re(ie(z.prototype),"updated",this).call(this,e),e.get("automationId")&&(this._traces=void 0,this._entityId=void 0,this._runId=void 0,this._trace=void 0,this._logbookEntries=void 0,this.automationId&&this._loadTraces()),e.has("_runId")&&this._runId&&(this._trace=void 0,this._logbookEntries=void 0,this._loadTrace()),e.has("automations")&&this.automationId&&!this._entityId){var n=this.automations.find((function(e){return e.attributes.id===t.automationId}));this._entityId=null==n?void 0:n.entity_id}}},{kind:"method",key:"_pickOlderTrace",value:function(){var e=this,t=this._traces.findIndex((function(t){return t.run_id===e._runId}));this._runId=this._traces[t+1].run_id,this._selected=void 0}},{kind:"method",key:"_pickNewerTrace",value:function(){var e=this,t=this._traces.findIndex((function(t){return t.run_id===e._runId}));this._runId=this._traces[t-1].run_id,this._selected=void 0}},{kind:"method",key:"_pickTrace",value:function(e){this._runId=e.target.value,this._selected=void 0}},{kind:"method",key:"_pickNode",value:function(e){this._selected=e.detail}},{kind:"method",key:"_refreshTraces",value:function(){this._loadTraces()}},{kind:"method",key:"_loadTraces",value:(w=H(regeneratorRuntime.mark((function e(t){var n,r=this;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,O.lj)(this.hass,"automation",this.automationId);case 2:if(this._traces=e.sent,this._traces.reverse(),t&&(this._runId=t),!this._runId||this._traces.some((function(e){return e.run_id===r._runId}))){e.next=11;break}return this._runId=void 0,this._selected=void 0,t&&((n=new URLSearchParams(location.search)).delete("run_id"),history.replaceState(null,"","".concat(location.pathname,"?").concat(n.toString()))),e.next=11,(0,j.Ys)(this,{text:"Chosen trace is no longer available"});case 11:!this._runId&&this._traces.length>0&&(this._runId=this._traces[0].run_id);case 12:case"end":return e.stop()}}),e,this)}))),function(e){return w.apply(this,arguments)})},{kind:"method",key:"_loadTrace",value:(n=H(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,O.mA)(this.hass,"automation",this.automationId,this._runId);case 2:if(t=e.sent,!(0,C.p)(this.hass,"logbook")){e.next=9;break}return e.next=6,(0,A.sS)(this.hass,t.timestamp.start,t.context.id);case 6:e.t0=e.sent,e.next=10;break;case 9:e.t0=[];case 10:this._logbookEntries=e.t0,this._trace=t;case 12:case"end":return e.stop()}}),e,this)}))),function(){return n.apply(this,arguments)})},{kind:"method",key:"_downloadTrace",value:function(){var e=document.createElement("a");e.download="trace ".concat(this._entityId," ").concat(this._trace.timestamp.start,".json"),e.href="data:application/json;charset=utf-8,".concat(encodeURI(JSON.stringify({trace:this._trace,logbookEntries:this._logbookEntries},void 0,2))),e.click()}},{kind:"method",key:"_importTrace",value:function(){var e=prompt("Enter downloaded trace");e&&(localStorage.devTrace=e,this._loadLocalTrace(e))}},{kind:"method",key:"_loadLocalStorageTrace",value:function(){localStorage.devTrace&&this._loadLocalTrace(localStorage.devTrace)}},{kind:"method",key:"_loadLocalTrace",value:function(e){var t=JSON.parse(e);this._trace=t.trace,this._logbookEntries=t.logbookEntries}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"method",key:"_timelinePathPicked",value:function(e){var t=e.detail.value,n=this._graph.trackedNodes;n[t]&&(this._selected=n[t])}},{kind:"get",static:!0,key:"styles",value:function(){return[D.Qx,R.b,(0,g.iv)(_||(_=V(["\n        .toolbar {\n          display: flex;\n          align-items: center;\n          justify-content: space-between;\n          font-size: 20px;\n          height: var(--header-height);\n          padding: 0 16px;\n          background-color: var(--primary-background-color);\n          font-weight: 400;\n          color: var(--app-header-text-color, white);\n          border-bottom: var(--app-header-border-bottom, none);\n          box-sizing: border-box;\n        }\n\n        .toolbar > * {\n          display: flex;\n          align-items: center;\n        }\n\n        :host([narrow]) .toolbar > * {\n          display: contents;\n        }\n\n        .main {\n          height: calc(100% - 56px);\n          display: flex;\n          background-color: var(--card-background-color);\n        }\n\n        :host([narrow]) .main {\n          height: auto;\n          flex-direction: column;\n        }\n\n        .container {\n          padding: 16px;\n        }\n\n        .graph {\n          border-right: 1px solid var(--divider-color);\n          overflow-x: auto;\n          max-width: 50%;\n          padding-bottom: 16px;\n        }\n        :host([narrow]) .graph {\n          max-width: 100%;\n          justify-content: center;\n          display: flex;\n        }\n\n        .info {\n          flex: 1;\n          background-color: var(--card-background-color);\n        }\n\n        .linkButton {\n          color: var(--primary-text-color);\n        }\n      "])))]}}]}}),g.oi)}}]);