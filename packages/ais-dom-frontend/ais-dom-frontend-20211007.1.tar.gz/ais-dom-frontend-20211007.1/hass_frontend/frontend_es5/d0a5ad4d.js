"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[43047],{43047:function(e,t,n){n.r(t),n.d(t,{ExternalAuth:function(){return m},createExternalAuth:function(){return k}});var r=n(40788);function o(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var a=function(){function e(){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),i(this,"commands",{}),i(this,"cache",{}),i(this,"msgId",0)}var t,n,r;return t=e,(n=[{key:"attach",value:function(){var e,t=this;e=this,window.addEventListener("connection-status",(function(t){return e.fireMessage({type:"connection-status",payload:{event:t.detail}})})),function(e){window.addEventListener("haptic",(function(t){return e.fireMessage({type:"haptic",payload:{hapticType:t.detail}})}))}(this),window.externalBus=function(e){return t.receiveMessage(e)}}},{key:"sendMessage",value:function(e){var t=this,n=++this.msgId;return e.id=n,this.fireMessage(e),new Promise((function(e,r){t.commands[n]={resolve:e,reject:r}}))}},{key:"fireMessage",value:function(e){e.id||(e.id=++this.msgId),this._sendExternal(e)}},{key:"receiveMessage",value:function(e){var t=this.commands[e.id];t?"result"===e.type&&(e.success?t.resolve(e.result):t.reject(e.error)):console.warn("Received unknown msg ID",e.id)}},{key:"_sendExternal",value:function(e){window.externalApp?window.externalApp.externalBus(JSON.stringify(e)):window.webkit.messageHandlers.externalBus.postMessage(e)}}])&&o(t.prototype,n),r&&o(t,r),e}();function s(e){return s="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},s(e)}function u(e,t,n,r,o,i,a){try{var s=e[i](a),u=s.value}catch(c){return void n(c)}s.done?t(u):Promise.resolve(u).then(r,o)}function c(e){return function(){var t=this,n=arguments;return new Promise((function(r,o){var i=e.apply(t,n);function a(e){u(i,r,o,a,s,"next",e)}function s(e){u(i,r,o,a,s,"throw",e)}a(void 0)}))}}function l(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function f(e,t){return f=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},f(e,t)}function p(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=h(e);if(t){var o=h(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return w(this,n)}}function w(e,t){if(t&&("object"===s(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return d(e)}function d(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function h(e){return h=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},h(e)}function v(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var y="externalAuthSetToken",b="externalAuthRevokeToken";if(!window.externalApp&&!window.webkit)throw new Error("External auth requires either externalApp or webkit defined on Window object.");var m=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&f(e,t)}(s,e);var t,n,r,o,i,a=p(s);function s(e){var t;return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,s),v(d(t=a.call(this,{hassUrl:e,clientId:"",refresh_token:"",access_token:"",expires_in:0,expires:0})),"external",void 0),v(d(t),"_tokenCallbackPromise",void 0),t}return t=s,n=[{key:"refreshAccessToken",value:(i=c(regeneratorRuntime.mark((function e(t){var n,r;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!this._tokenCallbackPromise||t){e.next=10;break}return e.prev=1,e.next=4,this._tokenCallbackPromise;case 4:return e.abrupt("return");case 7:e.prev=7,e.t0=e.catch(1),this._tokenCallbackPromise=void 0;case 10:return n={callback:y},t&&(n.force=!0),this._tokenCallbackPromise=new Promise((function(e,t){window[y]=function(n,r){return n?e(r):t(r)}})),e.next=15,Promise.resolve();case 15:return window.externalApp?window.externalApp.getExternalAuth(JSON.stringify(n)):window.webkit.messageHandlers.getExternalAuth.postMessage(n),e.next=18,this._tokenCallbackPromise;case 18:r=e.sent,this.data.access_token=r.access_token,this.data.expires=1e3*r.expires_in+Date.now(),this._tokenCallbackPromise=void 0;case 22:case"end":return e.stop()}}),e,this,[[1,7]])}))),function(e){return i.apply(this,arguments)})},{key:"revoke",value:(o=c(regeneratorRuntime.mark((function e(){var t,n;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t={callback:b},n=new Promise((function(e,t){window[b]=function(n,r){return n?e(r):t(r)}})),e.next=4,Promise.resolve();case 4:return window.externalApp?window.externalApp.revokeExternalAuth(JSON.stringify(t)):window.webkit.messageHandlers.revokeExternalAuth.postMessage(t),e.next=7,n;case 7:case"end":return e.stop()}}),e)}))),function(){return o.apply(this,arguments)})}],n&&l(t.prototype,n),r&&l(t,r),s}(r.gx),k=function(e){var t=new m(e);return(window.externalApp&&window.externalApp.externalBus||window.webkit&&window.webkit.messageHandlers.externalBus)&&(t.external=new a,t.external.attach()),t}}}]);