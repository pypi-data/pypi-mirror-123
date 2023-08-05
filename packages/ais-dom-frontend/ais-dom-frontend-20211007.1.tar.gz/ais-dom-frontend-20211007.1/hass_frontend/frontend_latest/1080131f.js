/*! For license information please see 1080131f.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[46132],{35854:(e,t,a)=>{a.d(t,{G:()=>o,R:()=>c});a(65233);var r=a(21006),i=a(98235);const o={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},c=[r.V,i.x,o]},62132:(e,t,a)=>{a.d(t,{K:()=>n});a(65233);var r=a(35854),i=a(49075),o=a(84938);const c={_checkedChanged:function(){r.G._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){o.o._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},n=[i.B,r.R,c]},49075:(e,t,a)=>{a.d(t,{S:()=>c,B:()=>n});a(65233);var r=a(51644),i=a(26110),o=a(84938);const c={observers:["_focusedChanged(receivedFocusFromKeyboard)"],_focusedChanged:function(e){e&&this.ensureRipple(),this.hasRipple()&&(this._ripple.holdDown=e)},_createRipple:function(){var e=o.o._createRipple();return e.id="ink",e.setAttribute("center",""),e.classList.add("circle"),e}},n=[r.P,i.a,o.o,c]},84938:(e,t,a)=>{a.d(t,{o:()=>o});a(65233),a(60748);var r=a(51644),i=a(87156);const o={properties:{noink:{type:Boolean,observer:"_noinkChanged"},_rippleContainer:{type:Object}},_buttonStateChanged:function(){this.focused&&this.ensureRipple()},_downHandler:function(e){r.$._downHandler.call(this,e),this.pressed&&this.ensureRipple(e)},ensureRipple:function(e){if(!this.hasRipple()){this._ripple=this._createRipple(),this._ripple.noink=this.noink;var t=this._rippleContainer||this.root;if(t&&(0,i.vz)(t).appendChild(this._ripple),e){var a=(0,i.vz)(this._rippleContainer||this),r=(0,i.vz)(e).rootTarget;a.deepContains(r)&&this._ripple.uiDownAction(e)}}},getRipple:function(){return this.ensureRipple(),this._ripple},hasRipple:function(){return Boolean(this._ripple)},_createRipple:function(){return document.createElement("paper-ripple")},_noinkChanged:function(e){this.hasRipple()&&(this._ripple.noink=e)}}},32296:(e,t,a)=>{a(65233);var r=a(62132),i=a(49075),o=a(9672),c=a(50856),n=a(87529);const s=c.d`<style>
  :host {
    display: inline-block;
    white-space: nowrap;
    cursor: pointer;
    --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);
    /* -1px is a sentinel for the default and is replaced in \`attached\`. */
    --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);
    @apply --paper-font-common-base;
    line-height: 0;
    -webkit-tap-highlight-color: transparent;
  }

  :host([hidden]) {
    display: none !important;
  }

  :host(:focus) {
    outline: none;
  }

  .hidden {
    display: none;
  }

  #checkboxContainer {
    display: inline-block;
    position: relative;
    width: var(--calculated-paper-checkbox-size);
    height: var(--calculated-paper-checkbox-size);
    min-width: var(--calculated-paper-checkbox-size);
    margin: var(--paper-checkbox-margin, initial);
    vertical-align: var(--paper-checkbox-vertical-align, middle);
    background-color: var(--paper-checkbox-unchecked-background-color, transparent);
  }

  #ink {
    position: absolute;

    /* Center the ripple in the checkbox by negative offsetting it by
     * (inkWidth - rippleWidth) / 2 */
    top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    width: var(--calculated-paper-checkbox-ink-size);
    height: var(--calculated-paper-checkbox-ink-size);
    color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));
    opacity: 0.6;
    pointer-events: none;
  }

  #ink:dir(rtl) {
    right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: auto;
  }

  #ink[checked] {
    color: var(--paper-checkbox-checked-ink-color, var(--primary-color));
  }

  #checkbox {
    position: relative;
    box-sizing: border-box;
    height: 100%;
    border: solid 2px;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    border-radius: 2px;
    pointer-events: none;
    -webkit-transition: background-color 140ms, border-color 140ms;
    transition: background-color 140ms, border-color 140ms;

    -webkit-transition-duration: var(--paper-checkbox-animation-duration, 140ms);
    transition-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  /* checkbox checked animations */
  #checkbox.checked #checkmark {
    -webkit-animation: checkmark-expand 140ms ease-out forwards;
    animation: checkmark-expand 140ms ease-out forwards;

    -webkit-animation-duration: var(--paper-checkbox-animation-duration, 140ms);
    animation-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  @-webkit-keyframes checkmark-expand {
    0% {
      -webkit-transform: scale(0, 0) rotate(45deg);
    }
    100% {
      -webkit-transform: scale(1, 1) rotate(45deg);
    }
  }

  @keyframes checkmark-expand {
    0% {
      transform: scale(0, 0) rotate(45deg);
    }
    100% {
      transform: scale(1, 1) rotate(45deg);
    }
  }

  #checkbox.checked {
    background-color: var(--paper-checkbox-checked-color, var(--primary-color));
    border-color: var(--paper-checkbox-checked-color, var(--primary-color));
  }

  #checkmark {
    position: absolute;
    width: 36%;
    height: 70%;
    border-style: solid;
    border-top: none;
    border-left: none;
    border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-color: var(--paper-checkbox-checkmark-color, white);
    -webkit-transform-origin: 97% 86%;
    transform-origin: 97% 86%;
    box-sizing: content-box; /* protect against page-level box-sizing */
  }

  #checkmark:dir(rtl) {
    -webkit-transform-origin: 50% 14%;
    transform-origin: 50% 14%;
  }

  /* label */
  #checkboxLabel {
    position: relative;
    display: inline-block;
    vertical-align: middle;
    padding-left: var(--paper-checkbox-label-spacing, 8px);
    white-space: normal;
    line-height: normal;
    color: var(--paper-checkbox-label-color, var(--primary-text-color));
    @apply --paper-checkbox-label;
  }

  :host([checked]) #checkboxLabel {
    color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));
    @apply --paper-checkbox-label-checked;
  }

  #checkboxLabel:dir(rtl) {
    padding-right: var(--paper-checkbox-label-spacing, 8px);
    padding-left: 0;
  }

  #checkboxLabel[hidden] {
    display: none;
  }

  /* disabled state */

  :host([disabled]) #checkbox {
    opacity: 0.5;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
  }

  :host([disabled][checked]) #checkbox {
    background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled]) #checkboxLabel  {
    opacity: 0.65;
  }

  /* invalid state */
  #checkbox.invalid:not(.checked) {
    border-color: var(--paper-checkbox-error-color, var(--error-color));
  }
</style>

<div id="checkboxContainer">
  <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">
    <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>
  </div>
</div>

<div id="checkboxLabel"><slot></slot></div>`;s.setAttribute("strip-whitespace",""),(0,o.k)({_template:s,is:"paper-checkbox",behaviors:[r.K],hostAttributes:{role:"checkbox","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},attached:function(){(0,n.T8)(this,(function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-checkbox-ink-size").trim()){var e=this.getComputedStyleValue("--calculated-paper-checkbox-size").trim(),t="px",a=e.match(/[A-Za-z]+$/);null!==a&&(t=a[0]);var r=parseFloat(e),i=8/3*r;"px"===t&&(i=Math.floor(i))%2!=r%2&&i++,this.updateStyles({"--paper-checkbox-ink-size":i+t})}}))},_computeCheckboxClass:function(e,t){var a="";return e&&(a+="checked "),t&&(a+="invalid"),a},_computeCheckmarkClass:function(e){return e?"":"hidden"},_createRipple:function(){return this._rippleContainer=this.$.checkboxContainer,i.S._createRipple.call(this)}})},25782:(e,t,a)=>{a(65233),a(65660),a(70019),a(97968);var r=a(9672),i=a(50856),o=a(33760);(0,r.k)({_template:i.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[o.U]})},93217:(e,t,a)=>{a.d(t,{Ud:()=>h});const r=Symbol("Comlink.proxy"),i=Symbol("Comlink.endpoint"),o=Symbol("Comlink.releaseProxy"),c=Symbol("Comlink.thrown"),n=e=>"object"==typeof e&&null!==e||"function"==typeof e,s=new Map([["proxy",{canHandle:e=>n(e)&&e[r],serialize(e){const{port1:t,port2:a}=new MessageChannel;return l(e,t),[a,[a]]},deserialize:e=>(e.start(),h(e))}],["throw",{canHandle:e=>n(e)&&c in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function l(e,t=self){t.addEventListener("message",(function a(i){if(!i||!i.data)return;const{id:o,type:n,path:s}=Object.assign({path:[]},i.data),h=(i.data.argumentList||[]).map(m);let d;try{const t=s.slice(0,-1).reduce(((e,t)=>e[t]),e),a=s.reduce(((e,t)=>e[t]),e);switch(n){case"GET":d=a;break;case"SET":t[s.slice(-1)[0]]=m(i.data.value),d=!0;break;case"APPLY":d=a.apply(t,h);break;case"CONSTRUCT":d=function(e){return Object.assign(e,{[r]:!0})}(new a(...h));break;case"ENDPOINT":{const{port1:t,port2:a}=new MessageChannel;l(e,a),d=function(e,t){return b.set(e,t),e}(t,[t])}break;case"RELEASE":d=void 0;break;default:return}}catch(e){d={value:e,[c]:0}}Promise.resolve(d).catch((e=>({value:e,[c]:0}))).then((e=>{const[r,i]=v(e);t.postMessage(Object.assign(Object.assign({},r),{id:o}),i),"RELEASE"===n&&(t.removeEventListener("message",a),p(t))}))})),t.start&&t.start()}function p(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function h(e,t){return u(e,[],t)}function d(e){if(e)throw new Error("Proxy has been released and is not useable")}function u(e,t=[],a=function(){}){let r=!1;const c=new Proxy(a,{get(a,i){if(d(r),i===o)return()=>x(e,{type:"RELEASE",path:t.map((e=>e.toString()))}).then((()=>{p(e),r=!0}));if("then"===i){if(0===t.length)return{then:()=>c};const a=x(e,{type:"GET",path:t.map((e=>e.toString()))}).then(m);return a.then.bind(a)}return u(e,[...t,i])},set(a,i,o){d(r);const[c,n]=v(o);return x(e,{type:"SET",path:[...t,i].map((e=>e.toString())),value:c},n).then(m)},apply(a,o,c){d(r);const n=t[t.length-1];if(n===i)return x(e,{type:"ENDPOINT"}).then(m);if("bind"===n)return u(e,t.slice(0,-1));const[s,l]=k(c);return x(e,{type:"APPLY",path:t.map((e=>e.toString())),argumentList:s},l).then(m)},construct(a,i){d(r);const[o,c]=k(i);return x(e,{type:"CONSTRUCT",path:t.map((e=>e.toString())),argumentList:o},c).then(m)}});return c}function k(e){const t=e.map(v);return[t.map((e=>e[0])),(a=t.map((e=>e[1])),Array.prototype.concat.apply([],a))];var a}const b=new WeakMap;function v(e){for(const[t,a]of s)if(a.canHandle(e)){const[r,i]=a.serialize(e);return[{type:"HANDLER",name:t,value:r},i]}return[{type:"RAW",value:e},b.get(e)||[]]}function m(e){switch(e.type){case"HANDLER":return s.get(e.name).deserialize(e.value);case"RAW":return e.value}}function x(e,t,a){return new Promise((r=>{const i=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");e.addEventListener("message",(function t(a){a.data&&a.data.id&&a.data.id===i&&(e.removeEventListener("message",t),r(a.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:i},t),a)}))}},57835:(e,t,a)=>{a.d(t,{Xe:()=>r.Xe,pX:()=>r.pX,XM:()=>r.XM});var r=a(38941)}}]);
//# sourceMappingURL=1080131f.js.map