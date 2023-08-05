/*! For license information please see 8a0a9972.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[87087],{39841:function(n,e,t){t(65233),t(65660);var i,o,r,a=t(9672),s=t(87156),l=t(50856),c=t(44181);(0,a.k)({_template:(0,l.d)(i||(o=['\n    <style>\n      :host {\n        display: block;\n        /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using `isolation: isolate`, but that\'s not well supported\n         * across browsers.\n         */\n        position: relative;\n        z-index: 0;\n      }\n\n      #wrapper ::slotted([slot=header]) {\n        @apply --layout-fixed-top;\n        z-index: 1;\n      }\n\n      #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) {\n        height: 100%;\n      }\n\n      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {\n        position: absolute;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) #wrapper #contentContainer {\n        @apply --layout-fit;\n        overflow-y: auto;\n        -webkit-overflow-scrolling: touch;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n        position: relative;\n      }\n\n      :host([fullbleed]) {\n        @apply --layout-vertical;\n        @apply --layout-fit;\n      }\n\n      :host([fullbleed]) #wrapper,\n      :host([fullbleed]) #wrapper #contentContainer {\n        @apply --layout-vertical;\n        @apply --layout-flex;\n      }\n\n      #contentContainer {\n        /* Create a stacking context here so that all children appear below the header. */\n        position: relative;\n        z-index: 0;\n      }\n\n      @media print {\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          overflow-y: visible;\n        }\n      }\n\n    </style>\n\n    <div id="wrapper" class="initializing">\n      <slot id="headerSlot" name="header"></slot>\n\n      <div id="contentContainer">\n        <slot></slot>\n      </div>\n    </div>\n'],r=['\n    <style>\n      :host {\n        display: block;\n        /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using \\`isolation: isolate\\`, but that\'s not well supported\n         * across browsers.\n         */\n        position: relative;\n        z-index: 0;\n      }\n\n      #wrapper ::slotted([slot=header]) {\n        @apply --layout-fixed-top;\n        z-index: 1;\n      }\n\n      #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) {\n        height: 100%;\n      }\n\n      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {\n        position: absolute;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) #wrapper #contentContainer {\n        @apply --layout-fit;\n        overflow-y: auto;\n        -webkit-overflow-scrolling: touch;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n        position: relative;\n      }\n\n      :host([fullbleed]) {\n        @apply --layout-vertical;\n        @apply --layout-fit;\n      }\n\n      :host([fullbleed]) #wrapper,\n      :host([fullbleed]) #wrapper #contentContainer {\n        @apply --layout-vertical;\n        @apply --layout-flex;\n      }\n\n      #contentContainer {\n        /* Create a stacking context here so that all children appear below the header. */\n        position: relative;\n        z-index: 0;\n      }\n\n      @media print {\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          overflow-y: visible;\n        }\n      }\n\n    </style>\n\n    <div id="wrapper" class="initializing">\n      <slot id="headerSlot" name="header"></slot>\n\n      <div id="contentContainer">\n        <slot></slot>\n      </div>\n    </div>\n'],r||(r=o.slice(0)),i=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(r)}})))),is:"app-header-layout",behaviors:[c.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,s.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var n=this.header;if(this.isAttached&&n){this.$.wrapper.classList.remove("initializing"),n.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var e=n.offsetHeight;this.hasScrollingRegion?(n.style.left="",n.style.right=""):requestAnimationFrame(function(){var e=this.getBoundingClientRect(),t=document.documentElement.clientWidth-e.right;n.style.left=e.left+"px",n.style.right=t+"px"}.bind(this));var t=this.$.contentContainer.style;n.fixed&&!n.condenses&&this.hasScrollingRegion?(t.marginTop=e+"px",t.paddingTop=""):(t.paddingTop=e+"px",t.marginTop="")}}})},63207:function(n,e,t){t(65660),t(15112);var i,o,r,a=t(9672),s=t(87156),l=t(50856),c=t(65233);(0,a.k)({_template:(0,l.d)(i||(o=["\n    <style>\n      :host {\n        @apply --layout-inline;\n        @apply --layout-center-center;\n        position: relative;\n\n        vertical-align: middle;\n\n        fill: var(--iron-icon-fill-color, currentcolor);\n        stroke: var(--iron-icon-stroke-color, none);\n\n        width: var(--iron-icon-width, 24px);\n        height: var(--iron-icon-height, 24px);\n        @apply --iron-icon;\n      }\n\n      :host([hidden]) {\n        display: none;\n      }\n    </style>\n"],r||(r=o.slice(0)),i=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(r)}})))),is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:c.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(n){var e=(n||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(n){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,s.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,s.vz)(this.root).appendChild(this._img))}})},15112:function(n,e,t){t.d(e,{P:function(){return r}});t(65233);var i=t(9672);function o(n,e){for(var t=0;t<e.length;t++){var i=e[t];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(n,i.key,i)}}var r=function(){function n(e){!function(n,e){if(!(n instanceof e))throw new TypeError("Cannot call a class as a function")}(this,n),n[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}var e,t,i;return e=n,(t=[{key:"value",get:function(){var e=this.type,t=this.key;if(e&&t)return n.types[e]&&n.types[e][t]},set:function(e){var t=this.type,i=this.key;t&&i&&(t=n.types[t]=n.types[t]||{},null==e?delete t[i]:t[i]=e)}},{key:"list",get:function(){if(this.type){var e=n.types[this.type];return e?Object.keys(e).map((function(n){return a[this.type][n]}),this):[]}}},{key:"byKey",value:function(n){return this.key=n,this.value}}])&&o(e.prototype,t),i&&o(e,i),n}();r[" "]=function(){},r.types={};var a=r.types;(0,i.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(n,e,t){var i=new r({type:n,key:e});return void 0!==t&&t!==i.value?i.value=t:this.value!==i.value&&(this.value=i.value),i},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(n){n&&(this.value=this)},byKey:function(n){return new r({type:this.type,key:n}).value}})},25782:function(n,e,t){t(65233),t(65660),t(70019),t(97968);var i,o,r,a=t(9672),s=t(50856),l=t(33760);(0,a.k)({_template:(0,s.d)(i||(o=['\n    <style include="paper-item-shared-styles"></style>\n    <style>\n      :host {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n        @apply --paper-font-subhead;\n\n        @apply --paper-item;\n        @apply --paper-icon-item;\n      }\n\n      .content-icon {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n\n        width: var(--paper-item-icon-width, 56px);\n        @apply --paper-item-icon;\n      }\n    </style>\n\n    <div id="contentIcon" class="content-icon">\n      <slot name="item-icon"></slot>\n    </div>\n    <slot></slot>\n'],r||(r=o.slice(0)),i=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(r)}})))),is:"paper-icon-item",behaviors:[l.U]})},21560:function(n,e,t){t.d(e,{ZH:function(){return p},MT:function(){return a},U2:function(){return l},RV:function(){return r},t8:function(){return c}});var i,o=function(){var n;return!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent)&&indexedDB.databases?new Promise((function(e){var t=function(){return indexedDB.databases().finally(e)};n=setInterval(t,100),t()})).finally((function(){return clearInterval(n)})):Promise.resolve()};function r(n){return new Promise((function(e,t){n.oncomplete=n.onsuccess=function(){return e(n.result)},n.onabort=n.onerror=function(){return t(n.error)}}))}function a(n,e){var t=o().then((function(){var t=indexedDB.open(n);return t.onupgradeneeded=function(){return t.result.createObjectStore(e)},r(t)}));return function(n,i){return t.then((function(t){return i(t.transaction(e,n).objectStore(e))}))}}function s(){return i||(i=a("keyval-store","keyval")),i}function l(n){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:s();return e("readonly",(function(e){return r(e.get(n))}))}function c(n,e){var t=arguments.length>2&&void 0!==arguments[2]?arguments[2]:s();return t("readwrite",(function(t){return t.put(e,n),r(t.transaction)}))}function p(){var n=arguments.length>0&&void 0!==arguments[0]?arguments[0]:s();return n("readwrite",(function(n){return n.clear(),r(n.transaction)}))}},228:function(n,e,t){t.d(e,{$:function(){return i.$}});var i=t(59685)}}]);