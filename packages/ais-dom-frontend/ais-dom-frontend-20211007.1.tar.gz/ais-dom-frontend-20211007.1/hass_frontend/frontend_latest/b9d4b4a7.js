/*! For license information please see b9d4b4a7.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[20005],{51654:(e,t,o)=>{o.d(t,{Z:()=>l,n:()=>s});o(65233);var i=o(75009),n=o(87156);const l={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(e,t){t&&(e?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(e){this.closingReason=this.closingReason||{},this.closingReason.confirmed=e},_onDialogClick:function(e){for(var t=(0,n.vz)(e).path,o=0,i=t.indexOf(this);o<i;o++){var l=t[o];if(l.hasAttribute&&(l.hasAttribute("dialog-dismiss")||l.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(l.hasAttribute("dialog-confirm")),this.close(),e.stopPropagation();break}}}},s=[i.$,l]},22626:(e,t,o)=>{o(65233),o(65660);var i=o(51654),n=o(9672),l=o(50856);(0,n.k)({_template:l.d`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(i.Z)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},50808:(e,t,o)=>{o(65233),o(65660),o(70019),o(54242);const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(i.content);var n=o(96540),l=o(51654),s=o(9672),a=o(50856);(0,s.k)({_template:a.d`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[l.n,n.t],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},28417:(e,t,o)=>{o(50808);var i=o(33367),n=o(93592),l=o(87156);const s={getTabbableNodes:function(e){const t=[];return this._collectTabbableNodes(e,t)?n.H._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!n.H._isVisible(e))return!1;const o=e,i=n.H._normalizedTabIndex(o);let s,a=i>0;i>=0&&t.push(o),s="content"===o.localName||"slot"===o.localName?(0,l.vz)(o).getDistributedNodes():(0,l.vz)(o.shadowRoot||o.root||o).children;for(let e=0;e<s.length;e++)a=this._collectTabbableNodes(s[e],t)||a;return a}},a=customElements.get("paper-dialog"),r={get _focusableNodes(){return s.getTabbableNodes(this)}};class d extends((0,i.P)([r],a)){}customElements.define("ha-paper-dialog",d)},20005:(e,t,o)=>{o.r(t);o(22626);var i=o(50856),n=o(28426),l=(o(28417),o(11052));o(36436);class s extends((0,l.I)(n.H3)){static get template(){return i.d`
    <style include="ha-style-dialog">
      pre {
        font-family: var(--code-font-family, monospace);
      }
    </style>
      <ha-paper-dialog id="pwaDialog" with-backdrop="" opened="{{_opened}}">
        <h2>OpenZwave internal logfile</h2>
        <paper-dialog-scrollable>
          <pre>[[_ozwLog]]</pre>
        <paper-dialog-scrollable>
      </ha-paper-dialog>
      `}static get properties(){return{hass:Object,_ozwLog:String,_dialogClosedCallback:Function,_opened:{type:Boolean,value:!1},_intervalId:String,_numLogLines:{type:Number}}}ready(){super.ready(),this.addEventListener("iron-overlay-closed",(e=>this._dialogClosed(e)))}showDialog({_ozwLog:e,hass:t,_tail:o,_numLogLines:i,dialogClosedCallback:n}){this.hass=t,this._ozwLog=e,this._opened=!0,this._dialogClosedCallback=n,this._numLogLines=i,setTimeout((()=>this.$.pwaDialog.center()),0),o&&this.setProperties({_intervalId:setInterval((()=>{this._refreshLog()}),1500)})}async _refreshLog(){const e=await this.hass.callApi("GET","zwave/ozwlog?lines="+this._numLogLines);this.setProperties({_ozwLog:e})}_dialogClosed(e){if("ZWAVE-LOG-DIALOG"===e.target.nodeName){clearInterval(this._intervalId),this._opened=!1;const e=!0;this._dialogClosedCallback({closedEvent:e}),this._dialogClosedCallback=null}}}customElements.define("zwave-log-dialog",s)},36436:(e,t,o)=>{o(21384);var i=o(11654);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML=`<dom-module id="ha-style-dialog">\n<template>\n  <style>\n    ${i.yu.cssText}\n  </style>\n</template>\n</dom-module>`,document.head.appendChild(n.content)}}]);
//# sourceMappingURL=b9d4b4a7.js.map