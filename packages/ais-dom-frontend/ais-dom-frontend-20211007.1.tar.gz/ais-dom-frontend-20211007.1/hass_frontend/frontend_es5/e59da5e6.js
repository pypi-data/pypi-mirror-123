"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[75405],{25516:function(e,t,r){r.d(t,{i:function(){return n}});var n=function(e){return function(t){return{kind:"method",placement:"prototype",key:t.key,descriptor:{set:function(e){this["__".concat(String(t.key))]=e},get:function(){return this["__".concat(String(t.key))]},enumerable:!0,configurable:!0},finisher:function(r){var n=r.prototype.connectedCallback;r.prototype.connectedCallback=function(){if(n.call(this),this[t.key]){var r=this.renderRoot.querySelector(e);if(!r)return;r.scrollTop=this[t.key]}}}}}}},59110:function(e,t,r){var n,i,o,a,s,l,c=r(7599),u=r(26767),d=r(5701),f=r(14516),p=r(47181),h=r(87744);r(67065),r(3143),r(42952);function y(e){return y="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},y(e)}function m(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function v(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function b(e,t){return b=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},b(e,t)}function k(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=E(e);if(t){var i=E(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return w(this,r)}}function w(e,t){if(t&&("object"===y(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return g(e)}function g(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function E(e){return E=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},E(e)}function _(){_=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!S(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var u=0;u<c.length;u++)this.addElementPlacement(c[u],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return z(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=j(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:D(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=D(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function C(e){var t,r=j(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function P(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function S(e){return e.decorators&&e.decorators.length}function O(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function D(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function j(e){var t=function(e,t){if("object"!==y(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==y(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===y(t)?t:String(t)}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}!function(e,t,r,n){var i=_();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(O(o.descriptor)||O(i.descriptor)){if(S(o)||S(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(S(o)){if(S(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}P(o,i)}else t.push(o)}return t}(a.d.map(C)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,u.M)("hui-entity-picker-table")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&b(e,t)}(n,t);var r=k(n);function n(){var t;v(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(g(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,d.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.C)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,d.C)({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:function(){return!1}},{kind:"field",decorators:[(0,d.C)({type:Array})],key:"entities",value:void 0},{kind:"method",key:"render",value:function(){return(0,c.dy)(n||(n=m(["\n      <ha-data-table\n        selectable\n        .id=","\n        .columns=","\n        .data=","\n        .dir=","\n        .searchLabel=","\n        .noLabelFloat=","\n        .noDataText=","\n        @selection-changed=","\n      ></ha-data-table>\n    "])),"entity_id",this._columns(this.narrow),this.entities,(0,h.Zu)(this.hass),this.hass.localize("ui.panel.lovelace.unused_entities.search"),this.noLabelFloat,this.hass.localize("ui.panel.lovelace.unused_entities.no_data"),this._handleSelectionChanged)}},{kind:"field",key:"_columns",value:function(){var e=this;return(0,f.Z)((function(t){var r={icon:{title:"",type:"icon",template:function(t,r){return(0,c.dy)(i||(i=m(["\n          <state-badge\n            @click=","\n            .hass=","\n            .stateObj=","\n          ></state-badge>\n        "])),e._handleEntityClicked,e.hass,r.stateObj)}},name:{title:e.hass.localize("ui.panel.lovelace.unused_entities.entity"),sortable:!0,filterable:!0,grows:!0,direction:"asc",template:function(r,n){return(0,c.dy)(o||(o=m(["\n          <div @click=",' style="cursor: pointer;">\n            ',"\n            ","\n          </div>\n        "])),e._handleEntityClicked,r,t?(0,c.dy)(a||(a=m([' <div class="secondary">',"</div> "])),n.entity_id):"")}}};return r.entity_id={title:e.hass.localize("ui.panel.lovelace.unused_entities.entity_id"),sortable:!0,filterable:!0,width:"30%",hidden:t},r.domain={title:e.hass.localize("ui.panel.lovelace.unused_entities.domain"),sortable:!0,filterable:!0,width:"15%",hidden:t},r.last_changed={title:e.hass.localize("ui.panel.lovelace.unused_entities.last_changed"),type:"numeric",sortable:!0,width:"15%",hidden:t,template:function(t){return(0,c.dy)(s||(s=m(["\n        <ha-relative-time\n          .hass=","\n          .datetime=","\n          capitalize\n        ></ha-relative-time>\n      "])),e.hass,t)}},r}))}},{kind:"method",key:"_handleSelectionChanged",value:function(e){var t=e.detail.value;(0,p.B)(this,"selected-changed",{selectedEntities:t})}},{kind:"method",key:"_handleEntityClicked",value:function(e){var t=e.target.closest(".mdc-data-table__row").rowId;(0,p.B)(this,"hass-more-info",{entityId:t})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,c.iv)(l||(l=m(["\n      ha-data-table {\n        --data-table-border-width: 0;\n        height: 100%;\n      }\n    "])))}}]}}),c.oi)},47512:function(e,t,r){r.d(t,{f:function(){return o}});var n=r(47181),i=function(){return Promise.all([r.e(75009),r.e(35487),r.e(32421),r.e(77426),r.e(30486),r.e(84511),r.e(95213),r.e(70045),r.e(16729),r.e(72168),r.e(53918),r.e(24407),r.e(23481),r.e(53822),r.e(42952),r.e(9381),r.e(47150),r.e(10908),r.e(23340),r.e(57529),r.e(13542),r.e(96857)]).then(r.bind(r,9444))},o=function(e,t){(0,n.B)(e,"show-dialog",{dialogTag:"hui-dialog-suggest-card",dialogImport:i,dialogParams:t})}}}]);