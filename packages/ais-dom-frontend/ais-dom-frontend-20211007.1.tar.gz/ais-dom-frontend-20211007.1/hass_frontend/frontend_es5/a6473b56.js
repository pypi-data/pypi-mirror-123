"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[29311],{7323:function(e,t,n){n.d(t,{p:function(){return o}});var o=function(e,t){return e&&e.config.components.includes(t)}},83270:function(e,t,n){n.d(t,{LI:function(){return o},AV:function(){return i},Mc:function(){return r},dn:function(){return a},H9:function(){return c},De:function(){return s},Wz:function(){return l},LV:function(){return u},QD:function(){return d},A$:function(){return f},tW:function(){return p},n8:function(){return h}});var o=function(e){return e.callWS({type:"cloud/status"})},i=function(e,t){return e.callWS({type:"cloud/cloudhook/create",webhook_id:t})},r=function(e,t){return e.callWS({type:"cloud/cloudhook/delete",webhook_id:t})},a=function(e){return e.callWS({type:"cloud/remote/connect"})},c=function(e){return e.callWS({type:"cloud/remote/disconnect"})},s=function(e){return e.callWS({type:"cloud/subscription"})},l=function(e,t){return e.callWS({type:"cloud/thingtalk/convert",query:t})},u=function(e,t){return e.callWS(Object.assign({type:"cloud/update_prefs"},t))},d=function(e,t,n){return e.callWS(Object.assign({type:"cloud/google_assistant/entities/update",entity_id:t},n))},f=function(e){return e.callApi("POST","cloud/google_actions/sync")},p=function(e,t,n){return e.callWS(Object.assign({type:"cloud/alexa/entities/update",entity_id:t},n))},h=function(e){return e.callWS({type:"cloud/tts/info"})}},29311:function(e,t,n){n.r(t),n.d(t,{configSections:function(){return M},aisConfigSections:function(){return k}});n(53973),n(89194);var o=n(26767),i=n(5701),r=n(17717),a=n(7323),c=n(59708),s=n(83270),l=(n(15291),n(18199));function u(e){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},u(e)}function d(e,t,n,o,i,r,a){try{var c=e[r](a),s=c.value}catch(l){return void n(l)}c.done?t(s):Promise.resolve(s).then(o,i)}function f(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function p(e,t){return p=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},p(e,t)}function h(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=P(e);if(t){var i=P(this).constructor;n=Reflect.construct(o,arguments,i)}else n=o.apply(this,arguments);return m(this,n)}}function m(e,t){if(t&&("object"===u(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return g(e)}function g(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function y(){y=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(o){t.forEach((function(t){var i=t.placement;if(t.kind===o&&("static"===i||"prototype"===i)){var r="static"===i?e:n;this.defineClassElement(r,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var o=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===o?void 0:o.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],o=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!b(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),o.push.apply(o,t.finishers)}),this),!t)return{elements:n,finishers:o};var r=this.decorateConstructor(n,t);return o.push.apply(o,r.finishers),r.finishers=o,r},addElementPlacement:function(e,t,n){var o=t[e.placement];if(!n&&-1!==o.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");o.push(e.key)},decorateElement:function(e,t){for(var n=[],o=[],i=e.decorators,r=i.length-1;r>=0;r--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[r])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&o.push(s.finisher);var l=s.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);n.push.apply(n,l)}}return{element:e,finishers:o,extras:n}},decorateConstructor:function(e,t){for(var n=[],o=t.length-1;o>=0;o--){var i=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[o])(i)||i);if(void 0!==r.finisher&&n.push(r.finisher),void 0!==r.elements){e=r.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=A(e.key),o=String(e.placement);if("static"!==o&&"prototype"!==o&&"own"!==o)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+o+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:n,placement:o,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:H(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=H(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var o=(0,t[n])(e);if(void 0!==o){if("function"!=typeof o)throw new TypeError("Finishers must return a constructor.");e=o}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function C(e){var t,n=A(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var o={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(o.decorators=e.decorators),"field"===e.kind&&(o.initializer=e.value),o}function v(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function b(e){return e.decorators&&e.decorators.length}function V(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function H(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function A(e){var t=function(e,t){if("object"!==u(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var o=n.call(e,t||"default");if("object"!==u(o))return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===u(t)?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,o=new Array(t);n<t;n++)o[n]=e[n];return o}function w(e,t,n){return w="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var o=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=P(e)););return e}(e,t);if(o){var i=Object.getOwnPropertyDescriptor(o,t);return i.get?i.get.call(n):i.value}},w(e,t,n||e)}function P(e){return P=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},P(e)}var M={integrations:[{component:"integrations",path:"/config/integrations",translationKey:"ui.panel.config.integrations.caption",iconPath:"M20.5,11H19V7C19,5.89 18.1,5 17,5H13V3.5A2.5,2.5 0 0,0 10.5,1A2.5,2.5 0 0,0 8,3.5V5H4A2,2 0 0,0 2,7V10.8H3.5C5,10.8 6.2,12 6.2,13.5C6.2,15 5,16.2 3.5,16.2H2V20A2,2 0 0,0 4,22H7.8V20.5C7.8,19 9,17.8 10.5,17.8C12,17.8 13.2,19 13.2,20.5V22H17A2,2 0 0,0 19,20V16H20.5A2.5,2.5 0 0,0 23,13.5A2.5,2.5 0 0,0 20.5,11Z",core:!0},{component:"devices",path:"/config/devices",translationKey:"ui.panel.config.devices.caption",iconPath:"M3 6H21V4H3C1.9 4 1 4.9 1 6V18C1 19.1 1.9 20 3 20H7V18H3V6M13 12H9V13.78C8.39 14.33 8 15.11 8 16C8 16.89 8.39 17.67 9 18.22V20H13V18.22C13.61 17.67 14 16.88 14 16S13.61 14.33 13 13.78V12M11 17.5C10.17 17.5 9.5 16.83 9.5 16S10.17 14.5 11 14.5 12.5 15.17 12.5 16 11.83 17.5 11 17.5M22 8H16C15.5 8 15 8.5 15 9V19C15 19.5 15.5 20 16 20H22C22.5 20 23 19.5 23 19V9C23 8.5 22.5 8 22 8M21 18H17V10H21V18Z",core:!0},{component:"entities",path:"/config/entities",translationKey:"ui.panel.config.entities.caption",iconPath:"M11,13.5V21.5H3V13.5H11M12,2L17.5,11H6.5L12,2M17.5,13C20,13 22,15 22,17.5C22,20 20,22 17.5,22C15,22 13,20 13,17.5C13,15 15,13 17.5,13Z",core:!0},{component:"areas",path:"/config/areas",translationKey:"ui.panel.config.areas.caption",iconPath:"M12.5 7C12.5 5.89 13.39 5 14.5 5H18C19.1 5 20 5.9 20 7V9.16C18.84 9.57 18 10.67 18 11.97V14H12.5V7M6 11.96V14H11.5V7C11.5 5.89 10.61 5 9.5 5H6C4.9 5 4 5.9 4 7V9.15C5.16 9.56 6 10.67 6 11.96M20.66 10.03C19.68 10.19 19 11.12 19 12.12V15H5V12C5 10.9 4.11 10 3 10S1 10.9 1 12V17C1 18.1 1.9 19 3 19V21H5V19H19V21H21V19C22.1 19 23 18.1 23 17V12C23 10.79 21.91 9.82 20.66 10.03Z",core:!0}],automation:[{component:"blueprint",path:"/config/blueprint",translationKey:"ui.panel.config.blueprint.caption",iconPath:"M2.53,19.65L3.87,20.21V11.18L1.44,17.04C1.03,18.06 1.5,19.23 2.53,19.65M22.03,15.95L17.07,4C16.76,3.23 16.03,2.77 15.26,2.75C15,2.75 14.73,2.79 14.47,2.9L7.1,5.95C6.35,6.26 5.89,7 5.87,7.75C5.86,8 5.91,8.29 6,8.55L11,20.5C11.29,21.28 12.03,21.74 12.81,21.75C13.07,21.75 13.33,21.7 13.58,21.6L20.94,18.55C21.96,18.13 22.45,16.96 22.03,15.95M7.88,8.75A1,1 0 0,1 6.88,7.75A1,1 0 0,1 7.88,6.75C8.43,6.75 8.88,7.2 8.88,7.75C8.88,8.3 8.43,8.75 7.88,8.75M5.88,19.75A2,2 0 0,0 7.88,21.75H9.33L5.88,13.41V19.75Z"},{component:"automation",path:"/config/automation",translationKey:"ui.panel.config.automation.caption",iconPath:"M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2M7.5,13A2.5,2.5 0 0,0 5,15.5A2.5,2.5 0 0,0 7.5,18A2.5,2.5 0 0,0 10,15.5A2.5,2.5 0 0,0 7.5,13M16.5,13A2.5,2.5 0 0,0 14,15.5A2.5,2.5 0 0,0 16.5,18A2.5,2.5 0 0,0 19,15.5A2.5,2.5 0 0,0 16.5,13Z"},{component:"scene",path:"/config/scene",translationKey:"ui.panel.config.scene.caption",iconPath:"M17.5,12A1.5,1.5 0 0,1 16,10.5A1.5,1.5 0 0,1 17.5,9A1.5,1.5 0 0,1 19,10.5A1.5,1.5 0 0,1 17.5,12M14.5,8A1.5,1.5 0 0,1 13,6.5A1.5,1.5 0 0,1 14.5,5A1.5,1.5 0 0,1 16,6.5A1.5,1.5 0 0,1 14.5,8M9.5,8A1.5,1.5 0 0,1 8,6.5A1.5,1.5 0 0,1 9.5,5A1.5,1.5 0 0,1 11,6.5A1.5,1.5 0 0,1 9.5,8M6.5,12A1.5,1.5 0 0,1 5,10.5A1.5,1.5 0 0,1 6.5,9A1.5,1.5 0 0,1 8,10.5A1.5,1.5 0 0,1 6.5,12M12,3A9,9 0 0,0 3,12A9,9 0 0,0 12,21A1.5,1.5 0 0,0 13.5,19.5C13.5,19.11 13.35,18.76 13.11,18.5C12.88,18.23 12.73,17.88 12.73,17.5A1.5,1.5 0 0,1 14.23,16H16A5,5 0 0,0 21,11C21,6.58 16.97,3 12,3Z"},{component:"script",path:"/config/script",translationKey:"ui.panel.config.script.caption",iconPath:"M17.8,20C17.4,21.2 16.3,22 15,22H5C3.3,22 2,20.7 2,19V18H5L14.2,18C14.6,19.2 15.7,20 17,20H17.8M19,2C20.7,2 22,3.3 22,5V6H20V5C20,4.4 19.6,4 19,4C18.4,4 18,4.4 18,5V18H17C16.4,18 16,17.6 16,17V16H5V5C5,3.3 6.3,2 8,2H19M8,6V8H15V6H8M8,10V12H14V10H8Z"}],helpers:[{component:"helpers",path:"/config/helpers",translationKey:"ui.panel.config.helpers.caption",iconPath:"M21.71 20.29L20.29 21.71A1 1 0 0 1 18.88 21.71L7 9.85A3.81 3.81 0 0 1 6 10A4 4 0 0 1 2.22 4.7L4.76 7.24L5.29 6.71L6.71 5.29L7.24 4.76L4.7 2.22A4 4 0 0 1 10 6A3.81 3.81 0 0 1 9.85 7L21.71 18.88A1 1 0 0 1 21.71 20.29M2.29 18.88A1 1 0 0 0 2.29 20.29L3.71 21.71A1 1 0 0 0 5.12 21.71L10.59 16.25L7.76 13.42M20 2L16 4V6L13.83 8.17L15.83 10.17L18 8H20L22 4Z",core:!0}],experiences:[{component:"tag",path:"/config/tags",translationKey:"ui.panel.config.tag.caption",iconPath:"M18,6H13A2,2 0 0,0 11,8V10.28C10.41,10.62 10,11.26 10,12A2,2 0 0,0 12,14C13.11,14 14,13.1 14,12C14,11.26 13.6,10.62 13,10.28V8H16V16H8V8H10V6H8L6,6V18H18M20,20H4V4H20M20,2H4A2,2 0 0,0 2,4V20A2,2 0 0,0 4,22H20C21.11,22 22,21.1 22,20V4C22,2.89 21.11,2 20,2Z"},{component:"energy",path:"/config/energy",translationKey:"ui.panel.config.energy.caption",iconPath:"M11 15H6L13 1V9H18L11 23V15Z"}],lovelace:[{component:"lovelace",path:"/config/lovelace/dashboards",translationKey:"ui.panel.config.lovelace.caption",iconPath:"M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z"}],persons:[{component:"person",path:"/config/person",translationKey:"ui.panel.config.person.caption",iconPath:"M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"},{component:"zone",path:"/config/zone",translationKey:"ui.panel.config.zone.caption",iconPath:"M12,2C15.31,2 18,4.66 18,7.95C18,12.41 12,19 12,19C12,19 6,12.41 6,7.95C6,4.66 8.69,2 12,2M12,6A2,2 0 0,0 10,8A2,2 0 0,0 12,10A2,2 0 0,0 14,8A2,2 0 0,0 12,6M20,19C20,21.21 16.42,23 12,23C7.58,23 4,21.21 4,19C4,17.71 5.22,16.56 7.11,15.83L7.75,16.74C6.67,17.19 6,17.81 6,18.5C6,19.88 8.69,21 12,21C15.31,21 18,19.88 18,18.5C18,17.81 17.33,17.19 16.25,16.74L16.89,15.83C18.78,16.56 20,17.71 20,19Z"},{component:"users",path:"/config/users",translationKey:"ui.panel.config.users.caption",iconPath:"M22,4H14V7H10V4H2A2,2 0 0,0 0,6V20A2,2 0 0,0 2,22H22A2,2 0 0,0 24,20V6A2,2 0 0,0 22,4M8,9A2,2 0 0,1 10,11A2,2 0 0,1 8,13A2,2 0 0,1 6,11A2,2 0 0,1 8,9M12,17H4V16C4,14.67 6.67,14 8,14C9.33,14 12,14.67 12,16V17M20,18H14V16H20V18M20,14H14V12H20V14M20,10H14V8H20V10M13,6H11V2H13V6Z",core:!0,advancedOnly:!0}],general:[{component:"core",path:"/config/core",translationKey:"ui.panel.config.core.caption",iconPath:"M21.8,13H20V21H13V17.67L15.79,14.88L16.5,15C17.66,15 18.6,14.06 18.6,12.9C18.6,11.74 17.66,10.8 16.5,10.8A2.1,2.1 0 0,0 14.4,12.9L14.5,13.61L13,15.13V9.65C13.66,9.29 14.1,8.6 14.1,7.8A2.1,2.1 0 0,0 12,5.7A2.1,2.1 0 0,0 9.9,7.8C9.9,8.6 10.34,9.29 11,9.65V15.13L9.5,13.61L9.6,12.9A2.1,2.1 0 0,0 7.5,10.8A2.1,2.1 0 0,0 5.4,12.9A2.1,2.1 0 0,0 7.5,15L8.21,14.88L11,17.67V21H4V13H2.25C1.83,13 1.42,13 1.42,12.79C1.43,12.57 1.85,12.15 2.28,11.72L11,3C11.33,2.67 11.67,2.33 12,2.33C12.33,2.33 12.67,2.67 13,3L17,7V6H19V9L21.78,11.78C22.18,12.18 22.59,12.59 22.6,12.8C22.6,13 22.2,13 21.8,13M7.5,12A0.9,0.9 0 0,1 8.4,12.9A0.9,0.9 0 0,1 7.5,13.8A0.9,0.9 0 0,1 6.6,12.9A0.9,0.9 0 0,1 7.5,12M16.5,12C17,12 17.4,12.4 17.4,12.9C17.4,13.4 17,13.8 16.5,13.8A0.9,0.9 0 0,1 15.6,12.9A0.9,0.9 0 0,1 16.5,12M12,6.9C12.5,6.9 12.9,7.3 12.9,7.8C12.9,8.3 12.5,8.7 12,8.7C11.5,8.7 11.1,8.3 11.1,7.8C11.1,7.3 11.5,6.9 12,6.9Z",core:!0},{component:"server_control",path:"/config/server_control",translationKey:"ui.panel.config.server_control.caption",iconPath:"M4,1H20A1,1 0 0,1 21,2V6A1,1 0 0,1 20,7H4A1,1 0 0,1 3,6V2A1,1 0 0,1 4,1M4,9H20A1,1 0 0,1 21,10V14A1,1 0 0,1 20,15H4A1,1 0 0,1 3,14V10A1,1 0 0,1 4,9M4,17H20A1,1 0 0,1 21,18V22A1,1 0 0,1 20,23H4A1,1 0 0,1 3,22V18A1,1 0 0,1 4,17M9,5H10V3H9V5M9,13H10V11H9V13M9,21H10V19H9V21M5,3V5H7V3H5M5,11V13H7V11H5M5,19V21H7V19H5Z",core:!0},{component:"logs",path:"/config/logs",translationKey:"ui.panel.config.logs.caption",iconPath:"M18 7C16.9 7 16 7.9 16 9V15C16 16.1 16.9 17 18 17H20C21.1 17 22 16.1 22 15V11H20V15H18V9H22V7H18M2 7V17H8V15H4V7H2M11 7C9.9 7 9 7.9 9 9V15C9 16.1 9.9 17 11 17H13C14.1 17 15 16.1 15 15V9C15 7.9 14.1 7 13 7H11M11 9H13V15H11V9Z",core:!0},{component:"info",path:"/config/info",translationKey:"ui.panel.config.info.caption",iconPath:"M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z",core:!0}],advanced:[{component:"customize",path:"/config/customize",translationKey:"ui.panel.config.customize.caption",iconPath:"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z",core:!0,advancedOnly:!0}]},k={integrations:[{component:"ais_dom",path:"/config/ais_dom",translationKey:"ui.panel.config.ais_dom.caption",iconPath:"M10 20V18H3C1.9 18 1 17.1 1 16V4C1 2.89 1.89 2 3 2H21C22.1 2 23 2.89 23 4V8H21V4H3V16H12V22H8V20H10M18.5 15C17.12 15 16 16.12 16 17.5S17.12 20 18.5 20 21 18.88 21 17.5 19.88 15 18.5 15M23 10V21C23 21.55 22.55 22 22 22H15C14.45 22 14 21.55 14 21V10C14 9.45 14.45 9 15 9H22C22.55 9 23 9.45 23 10M17 11.5C17 12.33 17.67 13 18.5 13S20 12.33 20 11.5 19.33 10 18.5 10 17 10.67 17 11.5M22 17.5C22 15.57 20.43 14 18.5 14S15 15.57 15 17.5 16.57 21 18.5 21 22 19.43 22 17.5Z",core:!0},{component:"ais_dom_devices",path:"/config/ais_dom_devices",translationKey:"ui.panel.config.ais_dom_devices.caption",iconPath:"M12,21L15.6,16.2C14.6,15.45 13.35,15 12,15C10.65,15 9.4,15.45 8.4,16.2L12,21M12,3C7.95,3 4.21,4.34 1.2,6.6L3,9C5.5,7.12 8.62,6 12,6C15.38,6 18.5,7.12 21,9L22.8,6.6C19.79,4.34 16.05,3 12,3M12,9C9.3,9 6.81,9.89 4.8,11.4L6.6,13.8C8.1,12.67 9.97,12 12,12C14.03,12 15.9,12.67 17.4,13.8L19.2,11.4C17.19,9.89 14.7,9 12,9Z",core:!0},{component:"ais_dom_zigbee",path:"/config/ais_dom_zigbee",translationKey:"ui.panel.config.ais_dom_zigbee.caption",iconPath:"M4.06,6.15C3.97,6.17 3.88,6.22 3.8,6.28C2.66,7.9 2,9.87 2,12A10,10 0 0,0 12,22C15,22 17.68,20.68 19.5,18.6L17,18.85C14.25,19.15 11.45,19.19 8.66,18.96C7.95,18.94 7.24,18.76 6.59,18.45C5.73,18.06 5.15,17.23 5.07,16.29C5.06,16.13 5.12,16 5.23,15.87L7.42,13.6L15.03,5.7V5.6H10.84C8.57,5.64 6.31,5.82 4.06,6.15M20.17,17.5C20.26,17.47 20.35,17.44 20.43,17.39C21.42,15.83 22,14 22,12A10,10 0 0,0 12,2C9.22,2 6.7,3.13 4.89,4.97H5.17C8.28,4.57 11.43,4.47 14.56,4.65C15.5,4.64 16.45,4.82 17.33,5.17C18.25,5.53 18.89,6.38 19,7.37C19,7.53 18.93,7.7 18.82,7.82L9.71,17.19L9,17.95V18.06H13.14C15.5,18 17.84,17.81 20.17,17.5Z",core:!0},{component:"ais_dom_zwave",path:"/config/ais_dom_zwave",translationKey:"ui.panel.config.ais_dom_zwave.caption",iconPath:"M16.3,10.58C13.14,10.58 10.6,13.13 10.6,16.28C10.6,19.43 13.15,22 16.3,22C19.45,22 22,19.43 22,16.28C22,13.13 19.45,10.58 16.3,10.58M18,19.08H13.19L15.81,15H13.31L14.4,13.23H19.18L16.63,17.28H19.18L18,19.08M16.3,3.93V2C8.41,2 2,8.42 2,16.31H3.92C3.94,9.46 9.5,3.93 16.3,3.93M16.3,7.74V5.82C10.5,5.82 5.81,10.53 5.81,16.31H7.73C7.75,11.58 11.59,7.74 16.3,7.74",core:!0}]};!function(e,t,n,o){var i=y();if(o)for(var r=0;r<o.length;r++)i=o[r](i);var a=t((function(e){i.initializeInstanceElements(e,c.elements)}),n),c=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},o=0;o<e.length;o++){var i,r=e[o];if("method"===r.kind&&(i=t.find(n)))if(V(r.descriptor)||V(i.descriptor)){if(b(r)||b(i))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");i.descriptor=r.descriptor}else{if(b(r)){if(b(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");i.decorators=r.decorators}v(r,i)}else t.push(r)}return t}(a.d.map(C)),e);i.initializeClassElements(a.F,c.elements),i.runClassFinishers(a.F,c.finishers)}([(0,o.M)("ha-panel-config")],(function(e,t){var o,l,u=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&p(e,t)}(o,t);var n=h(o);function o(){var t;f(this,o);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=n.call.apply(n,[this].concat(r)),e(g(t)),t}return o}(t);return{F:u,d:[{kind:"field",decorators:[(0,i.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.C)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.C)()],key:"route",value:void 0},{kind:"field",key:"routerOptions",value:function(){return{defaultPage:"dashboard",routes:{areas:{tag:"ha-config-areas",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(196),n.e(95916),n.e(19870),n.e(55905),n.e(1359),n.e(7164),n.e(67065),n.e(12519),n.e(42150)]).then(n.bind(n,83567))}},automation:{tag:"ha-config-automation",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(88985),n.e(28055),n.e(54444),n.e(26561),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(35487),n.e(69505),n.e(32421),n.e(53268),n.e(32296),n.e(196),n.e(89841),n.e(77426),n.e(95916),n.e(46002),n.e(30486),n.e(22001),n.e(19870),n.e(11780),n.e(84511),n.e(27156),n.e(1359),n.e(67065),n.e(68331),n.e(68101),n.e(33902),n.e(47150),n.e(19475),n.e(90029)]).then(n.bind(n,4813))}},blueprint:{tag:"ha-config-blueprint",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(35487),n.e(32421),n.e(196),n.e(95916),n.e(19870),n.e(55905),n.e(1359),n.e(7164),n.e(67065),n.e(12519),n.e(47150),n.e(85011)]).then(n.bind(n,32958))}},tags:{tag:"ha-config-tags",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(196),n.e(95916),n.e(19870),n.e(1359),n.e(7164),n.e(67065),n.e(42952),n.e(12519),n.e(57389)]).then(n.bind(n,22130))}},cloud:{tag:"ha-config-cloud",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(32421),n.e(46002),n.e(39282),n.e(55905),n.e(60010),n.e(9381),n.e(72568),n.e(28878),n.e(78783)]).then(n.bind(n,95862))}},core:{tag:"ha-config-core",load:function(){return Promise.all([n.e(78161),n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(53268),n.e(48880),n.e(52266),n.e(55905),n.e(1359),n.e(54909),n.e(29389),n.e(36939),n.e(39220),n.e(81211)]).then(n.bind(n,81211))}},ais_dom:{tag:"ha-config-ais-dom-dashboard",load:function(){return Promise.all([n.e(53268),n.e(87087),n.e(55905),n.e(60010),n.e(51026),n.e(6366)]).then(n.bind(n,63081))}},ais_dom_config_update:{tag:"ha-config-ais-dom-config-update",load:function(){return Promise.all([n.e(78161),n.e(32421),n.e(53268),n.e(87087),n.e(91306),n.e(55905),n.e(60010),n.e(54909),n.e(51026),n.e(6366),n.e(45856)]).then(n.bind(n,52953))}},ais_dom_config_wifi:{tag:"ha-config-ais-dom-config-wifi",load:function(){return Promise.all([n.e(53268),n.e(87087),n.e(55905),n.e(60010),n.e(51026),n.e(6366),n.e(33137)]).then(n.bind(n,33137))}},ais_dom_config_display:{tag:"ha-config-ais-dom-config-display",load:function(){return Promise.all([n.e(53268),n.e(87087),n.e(55905),n.e(60010),n.e(51026),n.e(6366),n.e(56440)]).then(n.bind(n,56440))}},ais_dom_config_tts:{tag:"ha-config-ais-dom-config-tts",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(53268),n.e(87087),n.e(58902),n.e(55905),n.e(60010),n.e(51026),n.e(6366),n.e(9535)]).then(n.bind(n,9535))}},ais_dom_config_night:{tag:"ha-config-ais-dom-config-night",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(32421),n.e(53268),n.e(87087),n.e(41761),n.e(55905),n.e(60010),n.e(51026),n.e(6366),n.e(77141)]).then(n.bind(n,77141))}},ais_dom_config_remote:{tag:"ha-config-ais-dom-config-remote",load:function(){return Promise.all([n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(32421),n.e(53268),n.e(87087),n.e(55905),n.e(3143),n.e(60010),n.e(42952),n.e(9381),n.e(51026),n.e(10908),n.e(6366),n.e(31203),n.e(28878),n.e(6785)]).then(n.bind(n,96326))}},ais_dom_config_logs:{tag:"ha-config-ais-dom-config-logs",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(32421),n.e(53268),n.e(77426),n.e(87087),n.e(93843),n.e(55905),n.e(53822),n.e(60010),n.e(54909),n.e(46583),n.e(51026),n.e(6366),n.e(7579)]).then(n.bind(n,1065))}},ais_dom_config_usb:{tag:"ha-config-ais-dom-config-usb",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(32421),n.e(53268),n.e(87087),n.e(47402),n.e(55905),n.e(60010),n.e(51026),n.e(6366),n.e(66066)]).then(n.bind(n,66066))}},ais_dom_config_power:{tag:"ha-config-ais-dom-config-power",load:function(){return Promise.all([n.e(53268),n.e(87087),n.e(55905),n.e(60010),n.e(54909),n.e(51026),n.e(6366),n.e(91666)]).then(n.bind(n,28490))}},ais_dom_devices:{tag:"ha-config-ais-dom-devices",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(35487),n.e(32421),n.e(196),n.e(95916),n.e(30486),n.e(19870),n.e(84511),n.e(9681),n.e(55905),n.e(1359),n.e(3143),n.e(7164),n.e(60010),n.e(67065),n.e(42952),n.e(9381),n.e(12519),n.e(47150),n.e(10908),n.e(12844),n.e(23340),n.e(28562),n.e(36074),n.e(78793)]).then(n.bind(n,78793))}},ais_dom_zigbee:{tag:"ha-config-aiszigbee",load:function(){return Promise.all([n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(6126),n.e(55905),n.e(60010),n.e(89697)]).then(n.bind(n,32520))}},ais_dom_zwave:{tag:"ha-config-aiszwave",load:function(){return Promise.all([n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(41894),n.e(55905),n.e(60010),n.e(35317)]).then(n.bind(n,60553))}},ais_mqtt:{tag:"ais-mqtt-config-panel",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(53822),n.e(60010),n.e(58052),n.e(87402)]).then(n.bind(n,4628))}},devices:{tag:"ha-config-devices",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(35487),n.e(32421),n.e(196),n.e(30486),n.e(19870),n.e(84511),n.e(9681),n.e(55905),n.e(1359),n.e(3143),n.e(7164),n.e(60010),n.e(67065),n.e(42952),n.e(9381),n.e(12519),n.e(47150),n.e(10908),n.e(12844),n.e(23340),n.e(28562),n.e(36074),n.e(50734)]).then(n.bind(n,50734))}},server_control:{tag:"ha-config-server-control",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(53268),n.e(1359),n.e(54909),n.e(39220),n.e(44987)]).then(n.bind(n,77980))}},logs:{tag:"ha-config-logs",load:function(){return Promise.all([n.e(55905),n.e(1359),n.e(54909),n.e(94066),n.e(38207)]).then(n.bind(n,56795))}},info:{tag:"ha-config-info",load:function(){return Promise.all([n.e(54444),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(1359),n.e(18817)]).then(n.bind(n,74685))}},customize:{tag:"ha-config-customize",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(88985),n.e(28055),n.e(32296),n.e(5125),n.e(6421),n.e(55905),n.e(74535),n.e(1359),n.e(3143),n.e(94848)]).then(n.bind(n,9618))}},dashboard:{tag:"ha-config-dashboard",load:function(){return Promise.all([n.e(53268),n.e(51026),n.e(96216)]).then(n.bind(n,79578))}},entities:{tag:"ha-config-entities",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(32296),n.e(196),n.e(19870),n.e(7761),n.e(1359),n.e(7164),n.e(67065),n.e(12519),n.e(94009)]).then(n.bind(n,94009))}},energy:{tag:"ha-config-energy",load:function(){return Promise.all([n.e(1359),n.e(9381),n.e(55424),n.e(878),n.e(55207)]).then(n.bind(n,74313))}},integrations:{tag:"ha-config-integrations",load:function(){return Promise.all([n.e(78161),n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(95916),n.e(81480),n.e(76509),n.e(1359),n.e(7164),n.e(58052),n.e(47090)]).then(n.bind(n,47090))}},lovelace:{tag:"ha-config-lovelace",load:function(){return n.e(52730).then(n.bind(n,52730))}},person:{tag:"ha-config-person",load:function(){return Promise.all([n.e(95916),n.e(1359),n.e(92647)]).then(n.bind(n,77399))}},script:{tag:"ha-config-script",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(88985),n.e(28055),n.e(54444),n.e(26561),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(35487),n.e(69505),n.e(32421),n.e(53268),n.e(32296),n.e(196),n.e(89841),n.e(77426),n.e(95916),n.e(46002),n.e(30486),n.e(22001),n.e(19870),n.e(11780),n.e(84511),n.e(18639),n.e(1359),n.e(67065),n.e(68331),n.e(68101),n.e(33902),n.e(19475),n.e(46135)]).then(n.bind(n,29813))}},scene:{tag:"ha-config-scene",load:function(){return Promise.all([n.e(78161),n.e(68200),n.e(30879),n.e(88985),n.e(28055),n.e(54444),n.e(26561),n.e(87724),n.e(59799),n.e(196),n.e(95916),n.e(19870),n.e(69126),n.e(55905),n.e(74535),n.e(1359),n.e(3143),n.e(7164),n.e(67065),n.e(68101),n.e(77576),n.e(12519),n.e(35703),n.e(19475),n.e(1930)]).then(n.bind(n,38562))}},helpers:{tag:"ha-config-helpers",load:function(){return Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(196),n.e(95916),n.e(19870),n.e(13700),n.e(55905),n.e(1359),n.e(7164),n.e(67065),n.e(12519),n.e(18690)]).then(n.bind(n,18690))}},users:{tag:"ha-config-users",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(54444),n.e(26561),n.e(196),n.e(95916),n.e(19870),n.e(1359),n.e(7164),n.e(67065),n.e(12519),n.e(9914)]).then(n.bind(n,9914))}},zone:{tag:"ha-config-zone",load:function(){return Promise.all([n.e(78161),n.e(54444),n.e(95916),n.e(41603),n.e(55905),n.e(1359),n.e(29389),n.e(36939),n.e(39220),n.e(10873)]).then(n.bind(n,10873))}},zha:{tag:"zha-config-dashboard-router",load:function(){return n.e(86094).then(n.bind(n,86094))}},zwave:{tag:"zwave-config-router",load:function(){return n.e(88189).then(n.bind(n,88189))}},mqtt:{tag:"mqtt-config-panel",load:function(){return Promise.all([n.e(68200),n.e(30879),n.e(87724),n.e(62613),n.e(59799),n.e(6294),n.e(53822),n.e(60010),n.e(58052),n.e(31357)]).then(n.bind(n,42660))}},ozw:{tag:"ozw-config-router",load:function(){return n.e(37904).then(n.bind(n,37904))}},zwave_js:{tag:"zwave_js-config-router",load:function(){return n.e(17100).then(n.bind(n,17100))}}}}}},{kind:"field",decorators:[(0,r.S)()],key:"_wideSidebar",value:function(){return!1}},{kind:"field",decorators:[(0,r.S)()],key:"_wide",value:function(){return!1}},{kind:"field",decorators:[(0,r.S)()],key:"_cloudStatus",value:void 0},{kind:"field",key:"_listeners",value:function(){return[]}},{kind:"method",key:"connectedCallback",value:function(){var e=this;w(P(u.prototype),"connectedCallback",this).call(this),this._listeners.push((0,c.K)("(min-width: 1040px)",(function(t){e._wide=t}))),this._listeners.push((0,c.K)("(min-width: 1296px)",(function(t){e._wideSidebar=t})))}},{kind:"method",key:"disconnectedCallback",value:function(){for(w(P(u.prototype),"disconnectedCallback",this).call(this);this._listeners.length;)this._listeners.pop()()}},{kind:"method",key:"firstUpdated",value:function(e){var t=this;w(P(u.prototype),"firstUpdated",this).call(this,e),this.hass.loadBackendTranslation("title"),(0,a.p)(this.hass,"cloud")&&this._updateCloudStatus(),this.addEventListener("ha-refresh-cloud-status",(function(){return t._updateCloudStatus()})),this.style.setProperty("--app-header-background-color","var(--sidebar-background-color)"),this.style.setProperty("--app-header-text-color","var(--sidebar-text-color)"),this.style.setProperty("--app-header-border-bottom","1px solid var(--divider-color)")}},{kind:"method",key:"updatePageEl",value:function(e){var t,n,o="docked"===this.hass.dockedSidebar?this._wideSidebar:this._wide;"setProperties"in e?e.setProperties({route:this.routeTail,hass:this.hass,showAdvanced:Boolean(null===(t=this.hass.userData)||void 0===t?void 0:t.showAdvanced),isWide:o,narrow:this.narrow,cloudStatus:this._cloudStatus}):(e.route=this.routeTail,e.hass=this.hass,e.showAdvanced=Boolean(null===(n=this.hass.userData)||void 0===n?void 0:n.showAdvanced),e.isWide=o,e.narrow=this.narrow,e.cloudStatus=this._cloudStatus)}},{kind:"method",key:"_updateCloudStatus",value:(o=regeneratorRuntime.mark((function e(){var t=this;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,s.LI)(this.hass);case 2:this._cloudStatus=e.sent,("connecting"===this._cloudStatus.cloud||this._cloudStatus.logged_in&&this._cloudStatus.prefs.remote_enabled&&!this._cloudStatus.remote_connected)&&setTimeout((function(){return t._updateCloudStatus()}),5e3);case 4:case"end":return e.stop()}}),e,this)})),l=function(){var e=this,t=arguments;return new Promise((function(n,i){var r=o.apply(e,t);function a(e){d(r,n,i,a,c,"next",e)}function c(e){d(r,n,i,a,c,"throw",e)}a(void 0)}))},function(){return l.apply(this,arguments)})}]}}),l.n)}}]);