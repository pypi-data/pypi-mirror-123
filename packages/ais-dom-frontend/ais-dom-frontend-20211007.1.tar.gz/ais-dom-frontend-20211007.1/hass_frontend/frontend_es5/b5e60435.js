/*! For license information please see b5e60435.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[61231],{25856:function(e,t,r){r(65233),r(65660);var n,i,a,o=r(26110),s=r(98235),l=r(9672),c=r(87156),d=r(50856);(0,l.k)({_template:(0,d.d)(n||(i=['\n    <style>\n      :host {\n        display: inline-block;\n        position: relative;\n        width: 400px;\n        border: 1px solid;\n        padding: 2px;\n        -moz-appearance: textarea;\n        -webkit-appearance: textarea;\n        overflow: hidden;\n      }\n\n      .mirror-text {\n        visibility: hidden;\n        word-wrap: break-word;\n        @apply --iron-autogrow-textarea;\n      }\n\n      .fit {\n        @apply --layout-fit;\n      }\n\n      textarea {\n        position: relative;\n        outline: none;\n        border: none;\n        resize: none;\n        background: inherit;\n        color: inherit;\n        /* see comments in template */\n        width: 100%;\n        height: 100%;\n        font-size: inherit;\n        font-family: inherit;\n        line-height: inherit;\n        text-align: inherit;\n        @apply --iron-autogrow-textarea;\n      }\n\n      textarea::-webkit-input-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea:-moz-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea::-moz-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea:-ms-input-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n    </style>\n\n    \x3c!-- the mirror sizes the input/textarea so it grows with typing --\x3e\n    \x3c!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML --\x3e\n    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>\n\n    \x3c!-- size the input/textarea with a div, because the textarea has intrinsic size in ff --\x3e\n    <div class="textarea-container fit">\n      <textarea id="textarea" name$="[[name]]" aria-label$="[[label]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" autocapitalize$="[[autocapitalize]]" inputmode$="[[inputmode]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" disabled$="[[disabled]]" rows$="[[rows]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]"></textarea>\n    </div>\n'],a||(a=i.slice(0)),n=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(a)}})))),is:"iron-autogrow-textarea",behaviors:[s.x,o.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},autocapitalize:{type:String,value:"none"},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&!navigator.userAgent.match(/OS 1[3456789]/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=s.x.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=(0,c.vz)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});r(2178),r(98121),r(65911);var u,p=r(21006),h=r(66668);(0,l.k)({_template:(0,d.d)(u||(u=function(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(['\n    <style>\n      :host {\n        display: block;\n      }\n\n      :host([hidden]) {\n        display: none !important;\n      }\n\n      label {\n        pointer-events: none;\n      }\n    </style>\n\n    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">\n\n      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>\n\n      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>\n\n      <template is="dom-if" if="[[errorMessage]]">\n        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>\n      </template>\n\n      <template is="dom-if" if="[[charCounter]]">\n        <paper-input-char-counter slot="add-on"></paper-input-char-counter>\n      </template>\n\n    </paper-input-container>\n']))),is:"paper-textarea",behaviors:[h.d0,p.V],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})},54091:function(e,t,r){r.r(t),r.d(t,{ReportProblemToAisWs:function(){return M},HuiDialogReportProblemToAis:function(){return B}});r(53918),r(62613),r(87724),r(53973),r(51095),r(25856);var n,i,a,o,s,l,c,d,u,p,h,f=r(7599),m=r(26767),y=r(5701),v=(r(31206),r(34821)),b=r(11654);function g(e){return g="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},g(e)}function w(e,t,r,n,i,a,o){try{var s=e[a](o),l=s.value}catch(c){return void r(c)}s.done?t(l):Promise.resolve(l).then(n,i)}function x(e){return function(){var t=this,r=arguments;return new Promise((function(n,i){var a=e.apply(t,r);function o(e){w(a,n,i,o,s,"next",e)}function s(e){w(a,n,i,o,s,"throw",e)}o(void 0)}))}}function _(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function k(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function E(e,t){return E=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},E(e,t)}function z(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=P(e);if(t){var i=P(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return A(this,r)}}function A(e,t){if(t&&("object"===g(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return $(e)}function $(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function P(e){return P=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},P(e)}function S(){S=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var a="static"===i?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!j(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var a=this.decorateConstructor(r,t);return n.push.apply(n,a.finishers),a.finishers=n,a},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,a=i.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return R(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?R(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=I(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:O(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=O(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function C(e){var t,r=I(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function D(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function j(e){return e.decorators&&e.decorators.length}function T(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function O(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function I(e){var t=function(e,t){if("object"!==g(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==g(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===g(t)?t:String(t)}function R(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var M=function(e,t,r,n){return e.callWS({type:"ais_cloud/report_ais_problem",problem_type:t,problem_desc:r,problem_data:n})},B=function(e,t,r,n){var i=S();if(n)for(var a=0;a<n.length;a++)i=n[a](i);var o=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},n=0;n<e.length;n++){var i,a=e[n];if("method"===a.kind&&(i=t.find(r)))if(T(a.descriptor)||T(i.descriptor)){if(j(a)||j(i))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");i.descriptor=a.descriptor}else{if(j(a)){if(j(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");i.decorators=a.decorators}D(a,i)}else t.push(a)}return t}(o.d.map(C)),e);return i.initializeClassElements(o.F,s.elements),i.runClassFinishers(o.F,s.finishers)}([(0,m.M)("hui-dialog-report-problem-to-ais")],(function(e,t){var r,m,g=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&E(e,t)}(n,t);var r=z(n);function n(){var t;k(this,n);for(var i=arguments.length,a=new Array(i),o=0;o<i;o++)a[o]=arguments[o];return t=r.call.apply(r,[this].concat(a)),e($(t)),t}return n}(t);return{F:g,d:[{kind:"field",decorators:[(0,y.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,y.C)({attribute:!1})],key:"_params",value:void 0},{kind:"field",decorators:[(0,y.C)()],key:"_loading",value:function(){return!1}},{kind:"field",decorators:[(0,y.C)()],key:"_problemDescription",value:function(){return""}},{kind:"field",decorators:[(0,y.C)()],key:"_aisAnswer",value:void 0},{kind:"field",key:"_aisMediaInfo",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._aisMediaInfo=this.hass.states["media_player.wbudowany_glosnik"],this._aisAnswer=void 0,this._problemDescription=""}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._aisAnswer=void 0,this._problemDescription=""}},{kind:"method",key:"render",value:function(){var e,t,r,h,m;return this._params?(0,f.dy)(i||(i=_([" <ha-dialog\n      open\n      hideActions\n      .heading=","\n      @closed=","\n    >\n      ","\n      ","\n    </ha-dialog>"])),(0,v.i)(this.hass,"Zgłoszenie problemu ze źródłem multimediów"),this.closeDialog,this._loading?(0,f.dy)(a||(a=_(["<ha-circular-progress active></ha-circular-progress>"]))):(0,f.dy)(o||(o=_([""]))),this._loading?(0,f.dy)(p||(p=_([" <p>\n            Wysyłam zgłoszenie do AIS\n          </p>"]))):(0,f.dy)(s||(s=_(["<p>\n                Problem z odtwarzaniem ",",\n                <b></b>",'</b>\n              <span class="aisUrl">\n                <br>z adresu URL <ha-icon icon="mdi:web"></ha-icon>:\n                <b></b>','</b>\n                </span\n              >\n              </p>\n              <div class="img404"><img src="','"/></div>\n              ',""])),null===(e=this._aisMediaInfo)||void 0===e?void 0:e.attributes.source,null===(t=this._aisMediaInfo)||void 0===t?void 0:t.attributes.media_title,null===(r=this._aisMediaInfo)||void 0===r?void 0:r.attributes.media_content_id,null===(h=this._aisMediaInfo)||void 0===h?void 0:h.attributes.media_stream_image,this._aisAnswer?(0,f.dy)(c||(c=_(['\n                      <div style="text-align: center;">\n                        ','\n                      </div>\n                      <div class="sendProblemToAisButton">\n                        <mwc-button raised @click=','>\n                          <ha-icon icon="hass:close-thick"></ha-icon>\n                          &nbsp; OK\n                        </mwc-button>\n                      </div>\n                    '])),this._aisAnswer.error?(0,f.dy)(d||(d=_(["\n                              <h2>\n                                Podczas przesyłania zgłoszenia wystąpił problem\n                              </h2>\n                              <p>\n                                ","\n                              </p>\n                              <p>\n                                Sprawdz połączenie z Internetem i spróbuj\n                                ponownie później.\n                              </p>\n                            "])),null===(m=this._aisAnswer)||void 0===m?void 0:m.message):(0,f.dy)(u||(u=_(["\n                              <h2>\n                                Przesłano zgłoszenie do AIS, o numerze:\n                                ","\n                              </h2>\n                              <p>\n                                ","\n                              </p>\n                            "])),this._aisAnswer.report_id,this._aisAnswer.message),this.closeDialog):(0,f.dy)(l||(l=_([' <p>\n                        Wyślij zgłoszenie do AI-Speaker. Postaramy się jak\n                        najszybciej naprawić ten problem.\n                      </p>\n                      <paper-textarea\n                        label="Dodatkowy opis dla AI-Speaker"\n                        placeholder="Tu możesz np. podać nowy adres zasobu, jeżeli go znasz."\n                        name="description"\n                        .value=',"\n                        @value-changed=",'\n                      ></paper-textarea>\n                      <div class="sendProblemToAisButton">\n                        <mwc-button\n                          raised\n                          @click=','\n                        >\n                          <ha-icon icon="hass:email-send"></ha-icon>\n                          &nbsp; Wyślij zgłoszenie do AI-Speaker\n                        </mwc-button>\n                      </div>'])),this._problemDescription,this._handleProblemDescriptionChange,this._handleReportProblemToAis))):(0,f.dy)(n||(n=_([""])))}},{kind:"method",key:"_reportProblemToAis",value:(m=x(regeneratorRuntime.mark((function e(){var t,r,n;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._loading=!0,t={message:"",email:"",report_id:0,error:!1},e.prev=2,e.next=5,M(this.hass,"media_source",this._problemDescription,(null===(r=this._aisMediaInfo)||void 0===r?void 0:r.attributes.media_title)+" "+(null===(n=this._aisMediaInfo)||void 0===n?void 0:n.attributes.media_content_id));case 5:t=e.sent,e.next=13;break;case 8:e.prev=8,e.t0=e.catch(2),t.message=e.t0.message,t.error=!0,this._loading=!1;case 13:return this._loading=!1,e.abrupt("return",t);case 15:case"end":return e.stop()}}),e,this,[[2,8]])}))),function(){return m.apply(this,arguments)})},{kind:"method",key:"_handleReportProblemToAis",value:(r=x(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this._reportProblemToAis();case 2:this._aisAnswer=e.sent;case 3:case"end":return e.stop()}}),e,this)}))),function(){return r.apply(this,arguments)})},{kind:"method",key:"_handleProblemDescriptionChange",value:function(e){this._problemDescription=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[b.yu,(0,f.iv)(h||(h=_(["\n        ha-dialog {\n          --dialog-content-padding: 0 24px 20px;\n        }\n        div.sendProblemToAisButton {\n          text-align: center;\n          margin: 10px;\n        }\n        div.img404 {\n          text-align: center;\n        }\n        img {\n          max-width: 500px;\n          max-height: 300px;\n          -webkit-filter: grayscale(100%);\n          filter: grayscale(100%);\n        }\n        span.aisUrl {\n          word-wrap: break-word;\n        }\n        ha-circular-progress {\n          --mdc-theme-primary: var(--primary-color);\n          display: flex;\n          justify-content: center;\n          margin-top: 40px;\n          margin-bottom: 20px;\n        }\n      "])))]}}]}}),f.oi)}}]);