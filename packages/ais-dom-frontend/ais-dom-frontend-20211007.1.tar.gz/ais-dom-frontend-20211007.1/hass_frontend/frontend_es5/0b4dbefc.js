"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9897],{73826:function(e,t,r){r.d(t,{f:function(){return w}});var n=r(5701);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function o(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){return a=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},a(e,t)}function s(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=k(e);if(t){var i=k(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return c(this,r)}}function c(e,t){if(t&&("object"===i(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return l(e)}function l(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function u(e,t,r,n){var i=f();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(y(o.descriptor)||y(i.descriptor)){if(h(o)||h(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(h(o)){if(h(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}p(o,i)}else t.push(o)}return t}(a.d.map(d)),e);return i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}function f(){f=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function d(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!==i(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==i(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===i(t)?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function g(e,t,r){return g="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=k(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}},g(e,t,r||e)}function k(e){return k=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},k(e)}var w=function(e){var t=u(null,(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&a(e,t)}(n,t);var r=s(n);function n(){var t;o(this,n);for(var i=arguments.length,a=new Array(i),s=0;s<i;s++)a[s]=arguments[s];return t=r.call.apply(r,[this].concat(a)),e(l(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){g(k(r.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if(g(k(r.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){var e=this.__unsubs.pop();e instanceof Promise?e.then((function(e){return e()})):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){g(k(r.prototype),"updated",this).call(this,e),e.has("hass")&&this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&(this.__unsubs=this.hassSubscribe())}}]}}),e);return t}},9897:function(e,t,r){r.r(t),r.d(t,{HuiEnergyUsageGraphCard:function(){return L}});var n,i,o,a,s,c=r(27088),l=r(70390),u=r(3700),f=r(4535),d=r(59699),p=r(7599),h=r(26767),y=r(5701),m=r(17717),v=r(228),b=r(14516),g=r(15838),k=r(20030),w=r(89525),_=r(49684),E=r(91741),P=r(18457),S=(r(32833),r(22098),r(55424)),O=r(58763),C=r(73826);function j(e){return j="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},j(e)}function x(e,t){return J(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,i,o=[],a=!0,s=!1;try{for(r=r.call(e);!(a=(n=r.next()).done)&&(o.push(n.value),!t||o.length!==t);a=!0);}catch(c){s=!0,i=c}finally{try{a||null==r.return||r.return()}finally{if(s)throw i}}return o}(e,t)||G(e,t)||N()}function D(e,t,r,n,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void r(l)}s.done?t(c):Promise.resolve(c).then(n,i)}function A(e,t){var r="undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(!r){if(Array.isArray(e)||(r=G(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var n=0,i=function(){};return{s:i,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(e){throw e},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,s=!1;return{s:function(){r=r.call(e)},n:function(){var e=r.next();return a=e.done,e},e:function(e){s=!0,o=e},f:function(){try{a||null==r.return||r.return()}finally{if(s)throw o}}}}function T(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function z(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function R(e,t){return R=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},R(e,t)}function F(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=V(e);if(t){var i=V(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return I(this,r)}}function I(e,t){if(t&&("object"===j(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return M(e)}function M(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function V(e){return V=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},V(e)}function Z(){Z=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!W(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,J(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||G(t)||N()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=K(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:H(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=H(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function B(e){var t,r=K(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function U(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function W(e){return e.decorators&&e.decorators.length}function $(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function H(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function K(e){var t=function(e,t){if("object"!==j(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==j(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===j(t)?t:String(t)}function N(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function G(e,t){if(e){if("string"==typeof e)return q(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?q(e,t):void 0}}function q(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function J(e){if(Array.isArray(e))return e}var L=function(e,t,r,n){var i=Z();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if($(o.descriptor)||$(i.descriptor)){if(W(o)||W(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(W(o)){if(W(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}U(o,i)}else t.push(o)}return t}(a.d.map(B)),e);return i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,h.M)("hui-energy-usage-graph-card")],(function(e,t){var r,h,C=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&R(e,t)}(n,t);var r=F(n);function n(){var t;z(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(M(t)),t}return n}(t);return{F:C,d:[{kind:"field",decorators:[(0,y.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,m.S)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,m.S)()],key:"_chartData",value:function(){return{datasets:[]}}},{kind:"field",decorators:[(0,m.S)()],key:"_start",value:function(){return(0,c.Z)()}},{kind:"field",decorators:[(0,m.S)()],key:"_end",value:function(){return(0,l.Z)()}},{kind:"method",key:"hassSubscribe",value:function(){var e,t=this;return[(0,S.UB)(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((function(e){return t._getStatistics(e)}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?(0,p.dy)(i||(i=T(["\n      <ha-card>\n        ",'\n        <div\n          class="content ','"\n        >\n          <ha-chart-base\n            .data=',"\n            .options=",'\n            chart-type="bar"\n          ></ha-chart-base>\n          ',"\n        </div>\n      </ha-card>\n    "])),this._config.title?(0,p.dy)(o||(o=T(['<h1 class="card-header">',"</h1>"])),this._config.title):"",(0,v.$)({"has-header":!!this._config.title}),this._chartData,this._createOptions(this._start,this._end,this.hass.locale),this._chartData.datasets.some((function(e){return e.data.length}))?"":(0,p.dy)(a||(a=T(['<div class="no-data">\n                ',"\n              </div>"])),(0,u.Z)(this._start)?"There is no data to show. It can take up to 2 hours for new data to arrive after you configure your energy dashboard.":"There is no data for this period.")):(0,p.dy)(n||(n=T([""])))}},{kind:"field",key:"_createOptions",value:function(){return(0,b.Z)((function(e,t,r){var n=(0,f.Z)(t,e);return{parsing:!1,animation:!1,scales:{x:{type:"time",suggestedMin:e.getTime(),suggestedMax:t.getTime(),adapters:{date:{locale:r}},ticks:{maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:function(e){return e.tick&&e.tick.major?{weight:"bold"}:{}}},time:{tooltipFormat:n>35?"monthyear":n>7?"date":n>2?"weekday":n>0?"datetime":"hour",minUnit:n>35?"month":n>2?"day":"hour"},offset:!0},y:{stacked:!0,type:"linear",title:{display:!0,text:"kWh"},ticks:{beginAtZero:!0,callback:function(e){return(0,P.u)(Math.abs(e),r)}}}},plugins:{tooltip:{mode:"x",intersect:!0,position:"nearest",filter:function(e){return"0"!==e.formattedValue},callbacks:{title:function(e){if(n>0)return e[0].label;var t=new Date(e[0].parsed.x);return"".concat((0,_.mr)(t,r)," - ").concat((0,_.mr)((0,d.Z)(t,1),r))},label:function(e){return"".concat(e.dataset.label,": ").concat((0,P.u)(Math.abs(e.parsed.y),r)," kWh")},footer:function(e){var t,n=0,i=0,o=A(e);try{for(o.s();!(t=o.n()).done;){var a=t.value,s=a.dataset.data[a.dataIndex].y;s>0?n+=s:i+=Math.abs(s)}}catch(c){o.e(c)}finally{o.f()}return[n?"Total consumed: ".concat((0,P.u)(n,r)," kWh"):"",i?"Total returned: ".concat((0,P.u)(i,r)," kWh"):""].filter(Boolean)}}},filler:{propagate:!1},legend:{display:!1,labels:{usePointStyle:!0}}},hover:{mode:"nearest"},elements:{bar:{borderWidth:1.5,borderRadius:4},point:{hitRadius:5}},locale:(0,P.H)(r)}}))}},{kind:"method",key:"_getStatistics",value:(r=regeneratorRuntime.mark((function e(t){var r,n,i,o,a,s,c,u,d,p,h,y,m,v,b,_,P,S,C,j,D,T,z,R,F,I,M,V,Z,B,U,W,$,H,K,N,G,q,J,L=this;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:r=[],n={},i=A(t.prefs.energy_sources),e.prev=3,i.s();case 5:if((o=i.n()).done){e.next=21;break}if("solar"!==(a=o.value).type){e.next=10;break}return n.solar?n.solar.push(a.stat_energy_from):n.solar=[a.stat_energy_from],e.abrupt("continue",19);case 10:if("battery"!==a.type){e.next=13;break}return n.to_battery?(n.to_battery.push(a.stat_energy_to),n.from_battery.push(a.stat_energy_from)):(n.to_battery=[a.stat_energy_to],n.from_battery=[a.stat_energy_from]),e.abrupt("continue",19);case 13:if("grid"===a.type){e.next=15;break}return e.abrupt("continue",19);case 15:s=A(a.flow_from);try{for(s.s();!(c=s.n()).done;)u=c.value,n.from_grid?n.from_grid.push(u.stat_energy_from):n.from_grid=[u.stat_energy_from]}catch(Q){s.e(Q)}finally{s.f()}d=A(a.flow_to);try{for(d.s();!(p=d.n()).done;)h=p.value,n.to_grid?n.to_grid.push(h.stat_energy_to):n.to_grid=[h.stat_energy_to]}catch(Q){d.e(Q)}finally{d.f()}case 19:e.next=5;break;case 21:e.next=26;break;case 23:e.prev=23,e.t0=e.catch(3),i.e(e.t0);case 26:return e.prev=26,i.f(),e.finish(26);case 29:if(y=(0,f.Z)(t.end||new Date,t.start),this._start=t.start,this._end=t.end||(0,l.Z)(),m={},v={},b=getComputedStyle(this),_={to_grid:b.getPropertyValue("--energy-grid-return-color").trim(),to_battery:b.getPropertyValue("--energy-battery-in-color").trim(),from_grid:b.getPropertyValue("--energy-grid-consumption-color").trim(),used_grid:b.getPropertyValue("--energy-grid-consumption-color").trim(),used_solar:b.getPropertyValue("--energy-solar-color").trim(),used_battery:b.getPropertyValue("--energy-battery-out-color").trim()},P={used_grid:"Combined from grid",used_solar:"Consumed solar",used_battery:"Consumed battery"},S=b.getPropertyValue("--card-background-color").trim(),Object.entries(n).forEach((function(e){var r=x(e,2),n=r[0],i=r[1],o=["solar","to_grid","from_grid","to_battery","from_battery"].includes(n),a=!["solar","from_battery"].includes(n),s={},c={};i.forEach((function(e){var r=y>35?(0,O.Kk)(t.stats[e]):y>2?(0,O.VU)(t.stats[e]):t.stats[e];if(r){var n,i={};r.forEach((function(e){if(null!==e.sum)if(void 0!==n){var t=e.sum-n;o&&(s[e.start]=e.start in s?s[e.start]+t:t),a&&!(e.start in i)&&(i[e.start]=t),n=e.sum}else n=e.sum})),c[e]=i}})),o&&(v[n]=s),a&&(m[n]=c)})),C={},j={},(v.to_grid||v.to_battery)&&v.solar){for(D={},T=0,z=Object.keys(v.solar);T<z.length;T++)I=z[T],D[I]=(v.solar[I]||0)-((null===(R=v.to_grid)||void 0===R?void 0:R[I])||0)-((null===(F=v.to_battery)||void 0===F?void 0:F[I])||0),D[I]<0&&(v.to_battery&&(C[I]=-1*D[I],C[I]>((null===(M=v.from_grid)||void 0===M?void 0:M[I])||0)&&(j[I]=Math.min(0,C[I]-((null===(V=v.from_grid)||void 0===V?void 0:V[I])||0)),C[I]=null===(Z=v.from_grid)||void 0===Z?void 0:Z[I])),D[I]=0);m.used_solar={used_solar:D}}if(v.from_battery)if(v.to_grid){for(B={},U=0,W=Object.keys(v.from_battery);U<W.length;U++)$=W[U],B[$]=(v.from_battery[$]||0)-(j[$]||0);m.used_battery={used_battery:B}}else m.used_battery={used_battery:v.from_battery};if(m.from_grid&&v.to_battery){for(H={},K=function(){for(var e=G[N],t=0,r=void 0,n=0,i=Object.entries(m.from_grid);n<i.length;n++){var o=x(i[n],2),a=o[0];if(o[1][e]&&(r=a,t++),t>1)break}if(1===t)m.from_grid[r][e]-=C[e]||0;else{var s=0;Object.values(m.from_grid).forEach((function(t){s+=t[e]||0,delete t[e]})),H[e]=s-(C[e]||0)}},N=0,G=Object.keys(C);N<G.length;N++)K();m.used_grid={used_grid:H}}q=[],Object.values(m).forEach((function(e){Object.values(e).forEach((function(e){q=q.concat(Object.keys(e))}))})),J=Array.from(new Set(q)),Object.entries(m).forEach((function(e){var t=x(e,2),n=t[0],i=t[1];Object.entries(i).forEach((function(e,t){var i=x(e,2),o=i[0],a=i[1],s=[],c=L.hass.states[o],l=t>0?(0,g.CO)((0,g.p3)((0,w.W)((0,g.Rw)((0,g.wK)(_[n])),t))):_[n];s.push({label:n in P?P[n]:c?(0,E.C)(c):o,order:"used_solar"===n?0:"to_battery"===n?Object.keys(m).length:t+1,borderColor:l,backgroundColor:(0,k.o)(l,S,50),stack:"stack",data:[]});var u,f=A(J);try{for(f.s();!(u=f.n()).done;){var d=u.value,p=a[d]||0,h=new Date(d);s[0].data.push({x:h.getTime(),y:p&&["to_grid","to_battery"].includes(n)?-1*p:p})}}catch(Q){f.e(Q)}finally{f.f()}Array.prototype.push.apply(r,s)}))})),this._chartData={datasets:r};case 49:case"end":return e.stop()}}),e,this,[[3,23,26,29]])})),h=function(){var e=this,t=arguments;return new Promise((function(n,i){var o=r.apply(e,t);function a(e){D(o,n,i,a,s,"next",e)}function s(e){D(o,n,i,a,s,"throw",e)}a(void 0)}))},function(e){return h.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,p.iv)(s||(s=T(["\n      ha-card {\n        height: 100%;\n      }\n      .card-header {\n        padding-bottom: 0;\n      }\n      .content {\n        padding: 16px;\n      }\n      .has-header {\n        padding-top: 0;\n      }\n      .no-data {\n        position: absolute;\n        height: 100%;\n        top: 0;\n        left: 0;\n        right: 0;\n        display: flex;\n        justify-content: center;\n        align-items: center;\n        padding: 20%;\n        margin-left: 32px;\n        box-sizing: border-box;\n      }\n    "])))}}]}}),(0,C.f)(p.oi))}}]);