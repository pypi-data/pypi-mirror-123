"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[94433],{94433:function(n,t,e){e.r(t);e(53918),e(21157),e(30879);var r,i=e(50856),o=e(28426);e(31206),e(4940);function u(n){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(n){return typeof n}:function(n){return n&&"function"==typeof Symbol&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},u(n)}function a(n,t){if(!(n instanceof t))throw new TypeError("Cannot call a class as a function")}function c(n,t){for(var e=0;e<t.length;e++){var r=t[e];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(n,r.key,r)}}function s(n,t){return s=Object.setPrototypeOf||function(n,t){return n.__proto__=t,n},s(n,t)}function f(n){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(n){return!1}}();return function(){var e,r=p(n);if(t){var i=p(this).constructor;e=Reflect.construct(r,arguments,i)}else e=r.apply(this,arguments);return l(this,e)}}function l(n,t){if(t&&("object"===u(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(n){if(void 0===n)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return n}(n)}function p(n){return p=Object.setPrototypeOf?Object.getPrototypeOf:function(n){return n.__proto__||Object.getPrototypeOf(n)},p(n)}var b=function(n){!function(n,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");n.prototype=Object.create(t&&t.prototype,{constructor:{value:n,writable:!0,configurable:!0}}),t&&s(n,t)}(l,n);var t,e,o,u=f(l);function l(){return a(this,l),u.apply(this,arguments)}return t=l,o=[{key:"template",get:function(){return(0,i.d)(r||(n=['\n      <style include="iron-flex"></style>\n      <style>\n        p {\n          margin: 8px 0;\n        }\n\n        a {\n          color: var(--primary-color);\n        }\n\n        p > img {\n          max-width: 100%;\n        }\n\n        p.center {\n          text-align: center;\n        }\n\n        p.error {\n          color: #c62828;\n        }\n\n        p.submit {\n          text-align: center;\n          height: 41px;\n        }\n\n        ha-circular-progress {\n          width: 14px;\n          height: 14px;\n          margin-right: 20px;\n        }\n\n        [hidden] {\n          display: none;\n        }\n      </style>\n\n      <div class="layout vertical">\n        <template is="dom-if" if="[[isConfigurable]]">\n          <ha-markdown\n            breaks\n            content="[[stateObj.attributes.description]]"\n          ></ha-markdown>\n\n          <p class="error" hidden$="[[!stateObj.attributes.errors]]">\n            [[stateObj.attributes.errors]]\n          </p>\n\n          <template is="dom-repeat" items="[[stateObj.attributes.fields]]">\n            <paper-input\n              label="[[item.name]]"\n              name="[[item.id]]"\n              type="[[item.type]]"\n              on-change="fieldChanged"\n            ></paper-input>\n          </template>\n\n          <p class="submit" hidden$="[[!stateObj.attributes.submit_caption]]">\n            <mwc-button\n              raised=""\n              disabled="[[isConfiguring]]"\n              on-click="submitClicked"\n            >\n              <ha-circular-progress\n                active="[[isConfiguring]]"\n                hidden="[[!isConfiguring]]"\n                alt="Configuring"\n              ></ha-circular-progress>\n              [[stateObj.attributes.submit_caption]]\n            </mwc-button>\n          </p>\n        </template>\n      </div>\n    '],t||(t=n.slice(0)),r=Object.freeze(Object.defineProperties(n,{raw:{value:Object.freeze(t)}}))));var n,t}},{key:"properties",get:function(){return{stateObj:{type:Object},action:{type:String,value:"display"},isConfigurable:{type:Boolean,computed:"computeIsConfigurable(stateObj)"},isConfiguring:{type:Boolean,value:!1},fieldInput:{type:Object,value:function(){return{}}}}}}],(e=[{key:"computeIsConfigurable",value:function(n){return"configure"===n.state}},{key:"fieldChanged",value:function(n){var t=n.target;this.fieldInput[t.name]=t.value}},{key:"submitClicked",value:function(){var n=this,t={configure_id:this.stateObj.attributes.configure_id,fields:this.fieldInput};this.isConfiguring=!0,this.hass.callService("configurator","configure",t).then((function(){n.isConfiguring=!1}),(function(){n.isConfiguring=!1}))}}])&&c(t.prototype,e),o&&c(t,o),l}(o.H3);customElements.define("more-info-configurator",b)}}]);