/*! For license information please see b90a8858.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[32296],{35854:function(e,n,a){a.d(n,{G:function(){return o},R:function(){return i}});a(65233);var c=a(21006),r=a(98235),o={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},i=[c.V,r.x,o]},62132:function(e,n,a){a.d(n,{K:function(){return t}});a(65233);var c=a(35854),r=a(49075),o=a(84938),i={_checkedChanged:function(){c.G._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){o.o._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},t=[r.B,c.R,i]},32296:function(e,n,a){a(65233);var c,r=a(62132),o=a(49075),i=a(9672),t=a(50856),l=a(87529);var p,h,d=(0,t.d)(c||(p=['<style>\n  :host {\n    display: inline-block;\n    white-space: nowrap;\n    cursor: pointer;\n    --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);\n    /* -1px is a sentinel for the default and is replaced in `attached`. */\n    --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);\n    @apply --paper-font-common-base;\n    line-height: 0;\n    -webkit-tap-highlight-color: transparent;\n  }\n\n  :host([hidden]) {\n    display: none !important;\n  }\n\n  :host(:focus) {\n    outline: none;\n  }\n\n  .hidden {\n    display: none;\n  }\n\n  #checkboxContainer {\n    display: inline-block;\n    position: relative;\n    width: var(--calculated-paper-checkbox-size);\n    height: var(--calculated-paper-checkbox-size);\n    min-width: var(--calculated-paper-checkbox-size);\n    margin: var(--paper-checkbox-margin, initial);\n    vertical-align: var(--paper-checkbox-vertical-align, middle);\n    background-color: var(--paper-checkbox-unchecked-background-color, transparent);\n  }\n\n  #ink {\n    position: absolute;\n\n    /* Center the ripple in the checkbox by negative offsetting it by\n     * (inkWidth - rippleWidth) / 2 */\n    top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n    left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n    width: var(--calculated-paper-checkbox-ink-size);\n    height: var(--calculated-paper-checkbox-ink-size);\n    color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));\n    opacity: 0.6;\n    pointer-events: none;\n  }\n\n  #ink:dir(rtl) {\n    right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n    left: auto;\n  }\n\n  #ink[checked] {\n    color: var(--paper-checkbox-checked-ink-color, var(--primary-color));\n  }\n\n  #checkbox {\n    position: relative;\n    box-sizing: border-box;\n    height: 100%;\n    border: solid 2px;\n    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n    border-radius: 2px;\n    pointer-events: none;\n    -webkit-transition: background-color 140ms, border-color 140ms;\n    transition: background-color 140ms, border-color 140ms;\n\n    -webkit-transition-duration: var(--paper-checkbox-animation-duration, 140ms);\n    transition-duration: var(--paper-checkbox-animation-duration, 140ms);\n  }\n\n  /* checkbox checked animations */\n  #checkbox.checked #checkmark {\n    -webkit-animation: checkmark-expand 140ms ease-out forwards;\n    animation: checkmark-expand 140ms ease-out forwards;\n\n    -webkit-animation-duration: var(--paper-checkbox-animation-duration, 140ms);\n    animation-duration: var(--paper-checkbox-animation-duration, 140ms);\n  }\n\n  @-webkit-keyframes checkmark-expand {\n    0% {\n      -webkit-transform: scale(0, 0) rotate(45deg);\n    }\n    100% {\n      -webkit-transform: scale(1, 1) rotate(45deg);\n    }\n  }\n\n  @keyframes checkmark-expand {\n    0% {\n      transform: scale(0, 0) rotate(45deg);\n    }\n    100% {\n      transform: scale(1, 1) rotate(45deg);\n    }\n  }\n\n  #checkbox.checked {\n    background-color: var(--paper-checkbox-checked-color, var(--primary-color));\n    border-color: var(--paper-checkbox-checked-color, var(--primary-color));\n  }\n\n  #checkmark {\n    position: absolute;\n    width: 36%;\n    height: 70%;\n    border-style: solid;\n    border-top: none;\n    border-left: none;\n    border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));\n    border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));\n    border-color: var(--paper-checkbox-checkmark-color, white);\n    -webkit-transform-origin: 97% 86%;\n    transform-origin: 97% 86%;\n    box-sizing: content-box; /* protect against page-level box-sizing */\n  }\n\n  #checkmark:dir(rtl) {\n    -webkit-transform-origin: 50% 14%;\n    transform-origin: 50% 14%;\n  }\n\n  /* label */\n  #checkboxLabel {\n    position: relative;\n    display: inline-block;\n    vertical-align: middle;\n    padding-left: var(--paper-checkbox-label-spacing, 8px);\n    white-space: normal;\n    line-height: normal;\n    color: var(--paper-checkbox-label-color, var(--primary-text-color));\n    @apply --paper-checkbox-label;\n  }\n\n  :host([checked]) #checkboxLabel {\n    color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));\n    @apply --paper-checkbox-label-checked;\n  }\n\n  #checkboxLabel:dir(rtl) {\n    padding-right: var(--paper-checkbox-label-spacing, 8px);\n    padding-left: 0;\n  }\n\n  #checkboxLabel[hidden] {\n    display: none;\n  }\n\n  /* disabled state */\n\n  :host([disabled]) #checkbox {\n    opacity: 0.5;\n    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n  }\n\n  :host([disabled][checked]) #checkbox {\n    background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n    opacity: 0.5;\n  }\n\n  :host([disabled]) #checkboxLabel  {\n    opacity: 0.65;\n  }\n\n  /* invalid state */\n  #checkbox.invalid:not(.checked) {\n    border-color: var(--paper-checkbox-error-color, var(--error-color));\n  }\n</style>\n\n<div id="checkboxContainer">\n  <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">\n    <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>\n  </div>\n</div>\n\n<div id="checkboxLabel"><slot></slot></div>'],(h=['<style>\n  :host {\n    display: inline-block;\n    white-space: nowrap;\n    cursor: pointer;\n    --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);\n    /* -1px is a sentinel for the default and is replaced in \\`attached\\`. */\n    --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);\n    @apply --paper-font-common-base;\n    line-height: 0;\n    -webkit-tap-highlight-color: transparent;\n  }\n\n  :host([hidden]) {\n    display: none !important;\n  }\n\n  :host(:focus) {\n    outline: none;\n  }\n\n  .hidden {\n    display: none;\n  }\n\n  #checkboxContainer {\n    display: inline-block;\n    position: relative;\n    width: var(--calculated-paper-checkbox-size);\n    height: var(--calculated-paper-checkbox-size);\n    min-width: var(--calculated-paper-checkbox-size);\n    margin: var(--paper-checkbox-margin, initial);\n    vertical-align: var(--paper-checkbox-vertical-align, middle);\n    background-color: var(--paper-checkbox-unchecked-background-color, transparent);\n  }\n\n  #ink {\n    position: absolute;\n\n    /* Center the ripple in the checkbox by negative offsetting it by\n     * (inkWidth - rippleWidth) / 2 */\n    top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n    left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n    width: var(--calculated-paper-checkbox-ink-size);\n    height: var(--calculated-paper-checkbox-ink-size);\n    color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));\n    opacity: 0.6;\n    pointer-events: none;\n  }\n\n  #ink:dir(rtl) {\n    right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);\n    left: auto;\n  }\n\n  #ink[checked] {\n    color: var(--paper-checkbox-checked-ink-color, var(--primary-color));\n  }\n\n  #checkbox {\n    position: relative;\n    box-sizing: border-box;\n    height: 100%;\n    border: solid 2px;\n    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n    border-radius: 2px;\n    pointer-events: none;\n    -webkit-transition: background-color 140ms, border-color 140ms;\n    transition: background-color 140ms, border-color 140ms;\n\n    -webkit-transition-duration: var(--paper-checkbox-animation-duration, 140ms);\n    transition-duration: var(--paper-checkbox-animation-duration, 140ms);\n  }\n\n  /* checkbox checked animations */\n  #checkbox.checked #checkmark {\n    -webkit-animation: checkmark-expand 140ms ease-out forwards;\n    animation: checkmark-expand 140ms ease-out forwards;\n\n    -webkit-animation-duration: var(--paper-checkbox-animation-duration, 140ms);\n    animation-duration: var(--paper-checkbox-animation-duration, 140ms);\n  }\n\n  @-webkit-keyframes checkmark-expand {\n    0% {\n      -webkit-transform: scale(0, 0) rotate(45deg);\n    }\n    100% {\n      -webkit-transform: scale(1, 1) rotate(45deg);\n    }\n  }\n\n  @keyframes checkmark-expand {\n    0% {\n      transform: scale(0, 0) rotate(45deg);\n    }\n    100% {\n      transform: scale(1, 1) rotate(45deg);\n    }\n  }\n\n  #checkbox.checked {\n    background-color: var(--paper-checkbox-checked-color, var(--primary-color));\n    border-color: var(--paper-checkbox-checked-color, var(--primary-color));\n  }\n\n  #checkmark {\n    position: absolute;\n    width: 36%;\n    height: 70%;\n    border-style: solid;\n    border-top: none;\n    border-left: none;\n    border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));\n    border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));\n    border-color: var(--paper-checkbox-checkmark-color, white);\n    -webkit-transform-origin: 97% 86%;\n    transform-origin: 97% 86%;\n    box-sizing: content-box; /* protect against page-level box-sizing */\n  }\n\n  #checkmark:dir(rtl) {\n    -webkit-transform-origin: 50% 14%;\n    transform-origin: 50% 14%;\n  }\n\n  /* label */\n  #checkboxLabel {\n    position: relative;\n    display: inline-block;\n    vertical-align: middle;\n    padding-left: var(--paper-checkbox-label-spacing, 8px);\n    white-space: normal;\n    line-height: normal;\n    color: var(--paper-checkbox-label-color, var(--primary-text-color));\n    @apply --paper-checkbox-label;\n  }\n\n  :host([checked]) #checkboxLabel {\n    color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));\n    @apply --paper-checkbox-label-checked;\n  }\n\n  #checkboxLabel:dir(rtl) {\n    padding-right: var(--paper-checkbox-label-spacing, 8px);\n    padding-left: 0;\n  }\n\n  #checkboxLabel[hidden] {\n    display: none;\n  }\n\n  /* disabled state */\n\n  :host([disabled]) #checkbox {\n    opacity: 0.5;\n    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n  }\n\n  :host([disabled][checked]) #checkbox {\n    background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));\n    opacity: 0.5;\n  }\n\n  :host([disabled]) #checkboxLabel  {\n    opacity: 0.65;\n  }\n\n  /* invalid state */\n  #checkbox.invalid:not(.checked) {\n    border-color: var(--paper-checkbox-error-color, var(--error-color));\n  }\n</style>\n\n<div id="checkboxContainer">\n  <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">\n    <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>\n  </div>\n</div>\n\n<div id="checkboxLabel"><slot></slot></div>'])||(h=p.slice(0)),c=Object.freeze(Object.defineProperties(p,{raw:{value:Object.freeze(h)}}))));d.setAttribute("strip-whitespace",""),(0,i.k)({_template:d,is:"paper-checkbox",behaviors:[r.K],hostAttributes:{role:"checkbox","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},attached:function(){(0,l.T8)(this,(function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-checkbox-ink-size").trim()){var e=this.getComputedStyleValue("--calculated-paper-checkbox-size").trim(),n="px",a=e.match(/[A-Za-z]+$/);null!==a&&(n=a[0]);var c=parseFloat(e),r=8/3*c;"px"===n&&(r=Math.floor(r))%2!=c%2&&r++,this.updateStyles({"--paper-checkbox-ink-size":r+n})}}))},_computeCheckboxClass:function(e,n){var a="";return e&&(a+="checked "),n&&(a+="invalid"),a},_computeCheckmarkClass:function(e){return e?"":"hidden"},_createRipple:function(){return this._rippleContainer=this.$.checkboxContainer,o.S._createRipple.call(this)}})}}]);