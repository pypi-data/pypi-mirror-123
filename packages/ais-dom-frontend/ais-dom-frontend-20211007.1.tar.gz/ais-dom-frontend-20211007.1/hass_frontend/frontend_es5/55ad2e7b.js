"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[16938],{73826:function(e,t,r){r.d(t,{f:function(){return w}});var n=r(5701);function a(e){return a="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},a(e)}function o(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function i(e,t){return i=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},i(e,t)}function l(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=g(e);if(t){var a=g(this).constructor;r=Reflect.construct(n,arguments,a)}else r=n.apply(this,arguments);return s(this,r)}}function s(e,t){if(t&&("object"===a(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return c(e)}function c(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function d(e,t,r,n){var a=u();if(n)for(var o=0;o<n.length;o++)a=n[o](a);var i=t((function(e){a.initializeInstanceElements(e,l.elements)}),r),l=a.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var a,o=e[n];if("method"===o.kind&&(a=t.find(r)))if(m(o.descriptor)||m(a.descriptor)){if(h(o)||h(a))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");a.descriptor=o.descriptor}else{if(h(o)){if(h(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");a.decorators=o.decorators}p(o,a)}else t.push(o)}return t}(i.d.map(f)),e);return a.initializeClassElements(i.F,l.elements),a.runClassFinishers(i.F,l.finishers)}function u(){u=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var a=t.placement;if(t.kind===n&&("static"===a||"prototype"===a)){var o="static"===a?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,a);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],a=e.decorators,o=a.length-1;o>=0;o--){var i=t[e.placement];i.splice(i.indexOf(e.key),1);var l=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,a[o])(l)||l);e=s.element,this.addElementPlacement(e,t),s.finisher&&n.push(s.finisher);var c=s.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var a=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(a)||a);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var i=0;i<e.length-1;i++)for(var l=i+1;l<e.length;l++)if(e[i].key===e[l].key&&e[i].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[i].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=b(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function f(e){var t,r=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function b(e){var t=function(e,t){if("object"!==a(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==a(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===a(t)?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function v(e,t,r){return v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(n){var a=Object.getOwnPropertyDescriptor(n,t);return a.get?a.get.call(r):a.value}},v(e,t,r||e)}function g(e){return g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},g(e)}var w=function(e){var t=d(null,(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&i(e,t)}(n,t);var r=l(n);function n(){var t;o(this,n);for(var a=arguments.length,i=new Array(a),l=0;l<a;l++)i[l]=arguments[l];return t=r.call.apply(r,[this].concat(i)),e(c(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){v(g(r.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if(v(g(r.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){var e=this.__unsubs.pop();e instanceof Promise?e.then((function(e){return e()})):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){v(g(r.prototype),"updated",this).call(this,e),e.has("hass")&&this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&(this.__unsubs=this.hassSubscribe())}}]}}),e);return t}},16938:function(e,t,r){r.r(t),r.d(t,{HuiEnergySourcesTableCard:function(){return oe}});var n,a,o,i,l,s,c,d,u,f,p,h,m,y,b,_,v,g,w,k,E,C,P,S,O,j,D,A=r(40521),T=r(7599),x=r(26767),z=r(5701),R=r(17717),F=r(47501),K=r(15838),W=r(89525),V=r(91741),I=r(18457),B=(r(5372),r(22098),r(55424)),M=r(58763),U=r(73826);function $(e){return $="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},$(e)}function G(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function N(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function H(e,t){return H=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},H(e,t)}function J(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=Q(e);if(t){var a=Q(this).constructor;r=Reflect.construct(n,arguments,a)}else r=n.apply(this,arguments);return L(this,r)}}function L(e,t){if(t&&("object"===$(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return q(e)}function q(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function Q(e){return Q=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},Q(e)}function X(){X=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var a=t.placement;if(t.kind===n&&("static"===a||"prototype"===a)){var o="static"===a?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!ee(e))return r.push(e);var t=this.decorateElement(e,a);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],a=e.decorators,o=a.length-1;o>=0;o--){var i=t[e.placement];i.splice(i.indexOf(e.key),1);var l=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,a[o])(l)||l);e=s.element,this.addElementPlacement(e,t),s.finisher&&n.push(s.finisher);var c=s.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var a=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(a)||a);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var i=0;i<e.length-1;i++)for(var l=i+1;l<e.length;l++)if(e[i].key===e[l].key&&e[i].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[i].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return ae(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?ae(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=ne(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:re(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=re(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function Y(e){var t,r=ne(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function Z(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function ee(e){return e.decorators&&e.decorators.length}function te(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function re(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function ne(e){var t=function(e,t){if("object"!==$(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==$(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===$(t)?t:String(t)}function ae(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var oe=function(e,t,r,n){var a=X();if(n)for(var o=0;o<n.length;o++)a=n[o](a);var i=t((function(e){a.initializeInstanceElements(e,l.elements)}),r),l=a.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var a,o=e[n];if("method"===o.kind&&(a=t.find(r)))if(te(o.descriptor)||te(a.descriptor)){if(ee(o)||ee(a))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");a.descriptor=o.descriptor}else{if(ee(o)){if(ee(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");a.decorators=o.decorators}Z(o,a)}else t.push(o)}return t}(i.d.map(Y)),e);return a.initializeClassElements(i.F,l.elements),a.runClassFinishers(i.F,l.finishers)}([(0,x.M)("hui-energy-sources-table-card")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&H(e,t)}(n,t);var r=J(n);function n(){var t;N(this,n);for(var a=arguments.length,o=new Array(a),i=0;i<a;i++)o[i]=arguments[i];return t=r.call.apply(r,[this].concat(o)),e(q(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,z.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,R.S)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,R.S)()],key:"_data",value:void 0},{kind:"method",key:"hassSubscribe",value:function(){var e,t=this;return[(0,B.UB)(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((function(e){t._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){var e,t,r,D,A,x,z,R=this;if(!this.hass||!this._config)return(0,T.dy)(n||(n=G([""])));if(!this._data)return(0,T.dy)(a||(a=G(["Loading..."])));var U=0,$=0,N=0,H=0,J=0,L=0,q=(0,B.Jj)(this._data.prefs),Q=getComputedStyle(this),X=Q.getPropertyValue("--energy-solar-color").trim(),Y=Q.getPropertyValue("--energy-battery-out-color").trim(),Z=Q.getPropertyValue("--energy-battery-in-color").trim(),ee=Q.getPropertyValue("--energy-grid-return-color").trim(),te=Q.getPropertyValue("--energy-grid-consumption-color").trim(),re=Q.getPropertyValue("--energy-gas-color").trim(),ne=(null===(e=q.grid)||void 0===e?void 0:e[0].flow_from.some((function(e){return e.stat_cost||e.entity_energy_price||e.number_energy_price})))||(null===(t=q.grid)||void 0===t?void 0:t[0].flow_to.some((function(e){return e.stat_compensation||e.entity_energy_price||e.number_energy_price})))||(null===(r=q.gas)||void 0===r?void 0:r.some((function(e){return e.stat_cost||e.entity_energy_price||e.number_energy_price}))),ae=(0,B.vE)(this.hass,this._data.prefs)||"";return(0,T.dy)(o||(o=G([" <ha-card>\n      ",'\n      <div class="mdc-data-table">\n        <div class="mdc-data-table__table-container">\n          <table class="mdc-data-table__table" aria-label="Energy sources">\n            <thead>\n              <tr class="mdc-data-table__header-row">\n                <th class="mdc-data-table__header-cell"></th>\n                <th\n                  class="mdc-data-table__header-cell"\n                  role="columnheader"\n                  scope="col"\n                >\n                  Source\n                </th>\n                <th\n                  class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"\n                  role="columnheader"\n                  scope="col"\n                >\n                  Energy\n                </th>\n                ','\n              </tr>\n            </thead>\n            <tbody class="mdc-data-table__content">\n              ',"\n              ","\n              ","\n              ","\n              ","\n              ","\n              ","\n              ","\n              ","\n            </tbody>\n          </table>\n        </div>\n      </div>\n    </ha-card>"])),this._config.title?(0,T.dy)(i||(i=G(['<h1 class="card-header">',"</h1>"])),this._config.title):"",ne?(0,T.dy)(l||(l=G([' <th\n                      class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"\n                      role="columnheader"\n                      scope="col"\n                    >\n                      Cost\n                    </th>']))):"",null===(D=q.solar)||void 0===D?void 0:D.map((function(e,t){var r=R.hass.states[e.stat_energy_from],n=(0,M.Kj)(R._data.stats[e.stat_energy_from])||0;N+=n;var a=t>0?(0,K.CO)((0,K.p3)((0,W.W)((0,K.Rw)((0,K.wK)(X)),t))):X;return(0,T.dy)(s||(s=G(['<tr class="mdc-data-table__row">\n                  <td class="mdc-data-table__cell cell-bullet">\n                    <div\n                      class="bullet"\n                      style=','\n                    ></div>\n                  </td>\n                  <th class="mdc-data-table__cell" scope="row">\n                    ','\n                  </th>\n                  <td\n                    class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                  >\n                    '," kWh\n                  </td>\n                  ","\n                </tr>"])),(0,F.V)({borderColor:a,backgroundColor:a+"7F"}),r?(0,V.C)(r):e.stat_energy_from,(0,I.u)(n,R.hass.locale),ne?(0,T.dy)(c||(c=G(['<td class="mdc-data-table__cell"></td>']))):"")})),q.solar?(0,T.dy)(d||(d=G(['<tr class="mdc-data-table__row total">\n                    <td class="mdc-data-table__cell"></td>\n                    <th class="mdc-data-table__cell" scope="row">\n                      Solar total\n                    </th>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      '," kWh\n                    </td>\n                    ","\n                  </tr>"])),(0,I.u)(N,this.hass.locale),ne?(0,T.dy)(u||(u=G(['<td class="mdc-data-table__cell"></td>']))):""):"",null===(A=q.battery)||void 0===A?void 0:A.map((function(e,t){var r=R.hass.states[e.stat_energy_from],n=R.hass.states[e.stat_energy_to],a=(0,M.Kj)(R._data.stats[e.stat_energy_from])||0,o=(0,M.Kj)(R._data.stats[e.stat_energy_to])||0;H+=a-o;var i=t>0?(0,K.CO)((0,K.p3)((0,W.W)((0,K.Rw)((0,K.wK)(Y)),t))):Y,l=t>0?(0,K.CO)((0,K.p3)((0,W.W)((0,K.Rw)((0,K.wK)(Z)),t))):Z;return(0,T.dy)(f||(f=G(['<tr class="mdc-data-table__row">\n                    <td class="mdc-data-table__cell cell-bullet">\n                      <div\n                        class="bullet"\n                        style=','\n                      ></div>\n                    </td>\n                    <th class="mdc-data-table__cell" scope="row">\n                      ','\n                    </th>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      '," kWh\n                    </td>\n                    ",'\n                  </tr>\n                  <tr class="mdc-data-table__row">\n                    <td class="mdc-data-table__cell cell-bullet">\n                      <div\n                        class="bullet"\n                        style=','\n                      ></div>\n                    </td>\n                    <th class="mdc-data-table__cell" scope="row">\n                      ','\n                    </th>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      '," kWh\n                    </td>\n                    ","\n                  </tr>"])),(0,F.V)({borderColor:i,backgroundColor:i+"7F"}),r?(0,V.C)(r):e.stat_energy_from,(0,I.u)(a,R.hass.locale),ne?(0,T.dy)(p||(p=G(['<td class="mdc-data-table__cell"></td>']))):"",(0,F.V)({borderColor:l,backgroundColor:l+"7F"}),n?(0,V.C)(n):e.stat_energy_from,(0,I.u)(-1*o,R.hass.locale),ne?(0,T.dy)(h||(h=G(['<td class="mdc-data-table__cell"></td>']))):"")})),q.battery?(0,T.dy)(m||(m=G(['<tr class="mdc-data-table__row total">\n                    <td class="mdc-data-table__cell"></td>\n                    <th class="mdc-data-table__cell" scope="row">\n                      Battery total\n                    </th>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      '," kWh\n                    </td>\n                    ","\n                  </tr>"])),(0,I.u)(H,this.hass.locale),ne?(0,T.dy)(y||(y=G(['<td class="mdc-data-table__cell"></td>']))):""):"",null===(x=q.grid)||void 0===x?void 0:x.map((function(e){return(0,T.dy)(b||(b=G(["","\n                ",""])),e.flow_from.map((function(e,t){var r=R.hass.states[e.stat_energy_from],n=(0,M.Kj)(R._data.stats[e.stat_energy_from])||0;U+=n;var a=e.stat_cost||R._data.info.cost_sensors[e.stat_energy_from],o=a?(0,M.Kj)(R._data.stats[a])||0:null;null!==o&&($+=o);var i=t>0?(0,K.CO)((0,K.p3)((0,W.W)((0,K.Rw)((0,K.wK)(te)),t))):te;return(0,T.dy)(_||(_=G(['<tr class="mdc-data-table__row">\n                    <td class="mdc-data-table__cell cell-bullet">\n                      <div\n                        class="bullet"\n                        style=','\n                      ></div>\n                    </td>\n                    <th class="mdc-data-table__cell" scope="row">\n                      ','\n                    </th>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      '," kWh\n                    </td>\n                    ","\n                  </tr>"])),(0,F.V)({borderColor:i,backgroundColor:i+"7F"}),r?(0,V.C)(r):e.stat_energy_from,(0,I.u)(n,R.hass.locale),ne?(0,T.dy)(v||(v=G([' <td\n                          class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                        >\n                          ',"\n                        </td>"])),null!==o?(0,I.u)(o,R.hass.locale,{style:"currency",currency:R.hass.config.currency}):""):"")})),e.flow_to.map((function(e,t){var r=R.hass.states[e.stat_energy_to],n=-1*((0,M.Kj)(R._data.stats[e.stat_energy_to])||0);U+=n;var a=e.stat_compensation||R._data.info.cost_sensors[e.stat_energy_to],o=a?-1*((0,M.Kj)(R._data.stats[a])||0):null;null!==o&&($+=o);var i=t>0?(0,K.CO)((0,K.p3)((0,W.W)((0,K.Rw)((0,K.wK)(ee)),t))):ee;return(0,T.dy)(g||(g=G(['<tr class="mdc-data-table__row">\n                    <td class="mdc-data-table__cell cell-bullet">\n                      <div\n                        class="bullet"\n                        style=','\n                      ></div>\n                    </td>\n                    <th class="mdc-data-table__cell" scope="row">\n                      ','\n                    </th>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      '," kWh\n                    </td>\n                    ","\n                  </tr>"])),(0,F.V)({borderColor:i,backgroundColor:i+"7F"}),r?(0,V.C)(r):e.stat_energy_to,(0,I.u)(n,R.hass.locale),ne?(0,T.dy)(w||(w=G([' <td\n                          class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                        >\n                          ',"\n                        </td>"])),null!==o?(0,I.u)(o,R.hass.locale,{style:"currency",currency:R.hass.config.currency}):""):"")})))})),q.grid?(0,T.dy)(k||(k=G([' <tr class="mdc-data-table__row total">\n                    <td class="mdc-data-table__cell"></td>\n                    <th class="mdc-data-table__cell" scope="row">Grid total</th>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      '," kWh\n                    </td>\n                    ","\n                  </tr>"])),(0,I.u)(U,this.hass.locale),ne?(0,T.dy)(E||(E=G(['<td\n                          class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                        >\n                          ',"\n                        </td>"])),(0,I.u)($,this.hass.locale,{style:"currency",currency:this.hass.config.currency})):""):"",null===(z=q.gas)||void 0===z?void 0:z.map((function(e,t){var r=R.hass.states[e.stat_energy_from],n=(0,M.Kj)(R._data.stats[e.stat_energy_from])||0;J+=n;var a=e.stat_cost||R._data.info.cost_sensors[e.stat_energy_from],o=a?(0,M.Kj)(R._data.stats[a])||0:null;null!==o&&(L+=o);var i=t>0?(0,K.CO)((0,K.p3)((0,W.W)((0,K.Rw)((0,K.wK)(re)),t))):re;return(0,T.dy)(C||(C=G(['<tr class="mdc-data-table__row">\n                  <td class="mdc-data-table__cell cell-bullet">\n                    <div\n                      class="bullet"\n                      style=','\n                    ></div>\n                  </td>\n                  <th class="mdc-data-table__cell" scope="row">\n                    ','\n                  </th>\n                  <td\n                    class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                  >\n                    '," ","\n                  </td>\n                  ","\n                </tr>"])),(0,F.V)({borderColor:i,backgroundColor:i+"7F"}),r?(0,V.C)(r):e.stat_energy_from,(0,I.u)(n,R.hass.locale),ae,ne?(0,T.dy)(P||(P=G(['<td\n                        class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                      >\n                        ',"\n                      </td>"])),null!==o?(0,I.u)(o,R.hass.locale,{style:"currency",currency:R.hass.config.currency}):""):"")})),q.gas?(0,T.dy)(S||(S=G(['<tr class="mdc-data-table__row total">\n                    <td class="mdc-data-table__cell"></td>\n                    <th class="mdc-data-table__cell" scope="row">Gas total</th>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      '," ","\n                    </td>\n                    ","\n                  </tr>"])),(0,I.u)(J,this.hass.locale),ae,ne?(0,T.dy)(O||(O=G(['<td\n                          class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                        >\n                          ',"\n                        </td>"])),(0,I.u)(L,this.hass.locale,{style:"currency",currency:this.hass.config.currency})):""):"",L&&$?(0,T.dy)(j||(j=G(['<tr class="mdc-data-table__row total">\n                    <td class="mdc-data-table__cell"></td>\n                    <th class="mdc-data-table__cell" scope="row">\n                      Total costs\n                    </th>\n                    <td class="mdc-data-table__cell"></td>\n                    <td\n                      class="mdc-data-table__cell mdc-data-table__cell--numeric"\n                    >\n                      ',"\n                    </td>\n                  </tr>"])),(0,I.u)(L+$,this.hass.locale,{style:"currency",currency:this.hass.config.currency})):"")}},{kind:"get",static:!0,key:"styles",value:function(){return(0,T.iv)(D||(D=G(["\n      ","\n      .mdc-data-table {\n        width: 100%;\n        border: 0;\n      }\n      .mdc-data-table__header-cell,\n      .mdc-data-table__cell {\n        color: var(--primary-text-color);\n        border-bottom-color: var(--divider-color);\n      }\n      .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {\n        background-color: rgba(var(--rgb-primary-text-color), 0.04);\n      }\n      .total {\n        --mdc-typography-body2-font-weight: 500;\n      }\n      .total .mdc-data-table__cell {\n        border-top: 1px solid var(--divider-color);\n      }\n      ha-card {\n        height: 100%;\n      }\n      .card-header {\n        padding-bottom: 0;\n      }\n      .content {\n        padding: 16px;\n      }\n      .has-header {\n        padding-top: 0;\n      }\n      .cell-bullet {\n        width: 32px;\n        padding-right: 0;\n      }\n      .bullet {\n        border-width: 1px;\n        border-style: solid;\n        border-radius: 4px;\n        height: 16px;\n        width: 32px;\n      }\n    "])),(0,T.$m)(A))}}]}}),(0,U.f)(T.oi))}}]);